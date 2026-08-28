#!/usr/bin/env python3
"""Threadsへ本文を投稿し、そのスレッドにコメント欄(自己リプ)をぶら下げる。

posts.json のスケジュールを見て、いま実行すべき投稿があるときだけ送る。
スケジュールに無い時刻に起動された場合は何もせず正常終了する。

環境変数:
  THREADS_ACCESS_TOKEN  長期アクセストークン(必須)
  DRY_RUN               "1" なら送信せず内容だけ表示
  SLOT_OVERRIDE         "2026-08-20T10:00" 形式。指定時刻の投稿を強制実行(手動テスト用)
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

API_BASE = "https://graph.threads.net/v1.0"
JST = timezone(timedelta(hours=9))
POSTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts.json")

# コンテナ作成から公開までMetaが推奨する待機時間(秒)
PUBLISH_DELAY = 30
# 親スレッド公開からリプライを付けるまでの待機時間(秒)
# 10秒では公開直後にリプライを作ろうとして500が返ることがあったため延ばした
REPLY_DELAY = 30
# cron起動が定刻よりどれだけ遅れても同じスロットとみなすか(分)
# GitHub Actionsのcronは混雑時に1時間前後遅れるうえ、起動自体が破棄されることもある。
# 30分おきの起動と組み合わせて、1スロットにつき3回の機会を確保する。
# 隣り合うスロットの最短間隔(2時間)より短くして、別スロットに寄らないようにする。
SLOT_WINDOW_MINUTES = 90
# 二重投稿チェックで遡る投稿数。1日6本なので4日分をカバーする
RECENT_POSTS_LIMIT = 25
# 送信の試行回数(初回 + 再試行)
POST_ATTEMPTS = 4
# 再試行の待ち時間(秒)。試行ごとにこの値ずつ延ばす
RETRY_BACKOFF_SECONDS = 15


def api_post(path, params):
    """Threads Graph APIにPOSTし、JSONを返す。

    Meta側が500を返すことが実際にある(本文の公開直後にリプライを作ろうとして発生)。
    サーバー側の一時的な失敗と接続断は、間隔を空けて数回やり直す。
    リクエスト内容が悪い4xxは、やり直しても同じなので即座に諦める。
    """
    url = f"{API_BASE}/{path}"
    data = urllib.parse.urlencode(params).encode()
    last = None
    for attempt in range(1, POST_ATTEMPTS + 1):
        req = urllib.request.Request(url, data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                return json.loads(res.read().decode())
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")
            last = RuntimeError(f"POST {path} failed ({e.code}): {detail}")
            if e.code < 500:
                raise last from e
        except urllib.error.URLError as e:
            last = RuntimeError(f"POST {path} failed (接続エラー): {e.reason}")
        if attempt < POST_ATTEMPTS:
            wait = RETRY_BACKOFF_SECONDS * attempt
            print(f"  一時エラー。{wait}秒後に再試行します ({attempt}/{POST_ATTEMPTS}): {last}")
            time.sleep(wait)
    raise last


def api_get(path, params):
    """Threads Graph APIにGETし、JSONを返す。"""
    url = f"{API_BASE}/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as res:
            return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise RuntimeError(f"GET {path} failed ({e.code}): {detail}") from e


def find_posted(token, texts):
    """与えたテキストが直近の投稿に既にあるかを調べ、あればそのIDを返す。

    起動回数を増やしている都合上、ひとつのスロットを複数の起動が拾いうるので、
    送る前にここで弾く。本文とコメント欄を別々に見るのは、本文だけ通って
    コメント欄が失敗した状態から再開できるようにするため。

    APIの照合自体に失敗した場合は例外を送出し、送信前に中断する。
    重複投稿より、1回見送って次の起動に任せる方が安全なため。
    """
    res = api_get("me/threads", {
        "fields": "id,text",
        "limit": RECENT_POSTS_LIMIT,
        "access_token": token,
    })
    seen = {}
    for item in res.get("data", []):
        text = item.get("text")
        if text:
            seen.setdefault("".join(text.split()), item.get("id"))
    return [seen.get("".join(t.split())) for t in texts]


def publish_text(token, text, reply_to_id=None):
    """テキストを1件公開し、公開後のIDを返す。

    エンドポイントには数値のユーザーIDではなく "me" を使う。
    数値IDを指定すると、正しいIDであっても
    「Object with ID ... does not exist」で拒否される。
    """
    params = {
        "media_type": "TEXT",
        "text": text,
        "access_token": token,
    }
    if reply_to_id:
        params["reply_to_id"] = reply_to_id

    container = api_post("me/threads", params)
    creation_id = container["id"]
    print(f"  container created: {creation_id}")

    time.sleep(PUBLISH_DELAY)

    published = api_post(
        "me/threads_publish",
        {"creation_id": creation_id, "access_token": token},
    )
    print(f"  published: {published['id']}")
    return published["id"]


def current_slot():
    """いまのJST時刻を、スケジュールの (日付, 時刻) キーに丸める。

    GitHub Actionsのcronは混雑時に1時間近く遅れることがあるため、
    「定刻を過ぎていて、まだ SLOT_WINDOW_MINUTES 以内」の直近スロットを採用する
    (未来のスロットには寄せない)。一致するスロットが無ければ None。
    """
    override = os.environ.get("SLOT_OVERRIDE")
    if override:
        date_part, time_part = override.split("T")
        return date_part, time_part

    now = datetime.now(JST)
    slots = ["00:00", "10:00", "12:00", "15:00", "18:00", "21:00"]
    best = None
    for slot in slots:
        hh, mm = (int(x) for x in slot.split(":"))
        target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
        elapsed = (now - target).total_seconds()
        if 0 <= elapsed <= SLOT_WINDOW_MINUTES * 60:
            if best is None or elapsed < best[0]:
                best = (elapsed, slot)
    if best is None:
        return None
    return now.strftime("%Y-%m-%d"), best[1]


def main():
    token = os.environ.get("THREADS_ACCESS_TOKEN")
    dry_run = os.environ.get("DRY_RUN") == "1"

    if not dry_run and not token:
        sys.exit("THREADS_ACCESS_TOKEN を設定してください")

    slot = current_slot()
    if slot is None:
        print(f"{datetime.now(JST):%Y-%m-%d %H:%M} JST — 該当スロットなし。終了します。")
        return

    date, time_str = slot
    with open(POSTS_FILE, encoding="utf-8") as f:
        data = json.load(f)

    entry = next(
        (e for e in data["schedule"] if e["date"] == date and e["time"] == time_str),
        None,
    )
    if entry is None:
        print(f"{date} {time_str} JST — この枠に投稿予定はありません。終了します。")
        return

    post = data["posts"][str(entry["post_id"])]
    print(f"{date} {time_str} JST — No.{entry['post_id']} ({post['type']}) を投稿します")
    print(f"  本文: {post['body'][:40]}…")

    if dry_run:
        print("\n--- DRY RUN (送信していません) ---")
        print(f"[本文 {len(post['body'])}字]\n{post['body']}\n")
        print(f"[コメント欄 {len(post['comment'])}字]\n{post['comment']}")
        return

    parent_id, comment_id = find_posted(token, [post["body"], post["comment"]])

    if parent_id and comment_id:
        print(f"  No.{entry['post_id']} は投稿済みです。二重投稿を避けて終了します。")
        return

    if parent_id:
        # 前回の起動で本文だけ通り、コメント欄が失敗した状態。続きから再開する。
        print("  本文は投稿済みです。コメント欄だけ投稿します。")
    else:
        parent_id = publish_text(token, post["body"])
        time.sleep(REPLY_DELAY)

    print("  コメント欄をリプライとして投稿します")
    publish_text(token, post["comment"], reply_to_id=parent_id)

    print(f"完了: No.{entry['post_id']}")


if __name__ == "__main__":
    main()
