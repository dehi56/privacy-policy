#!/usr/bin/env python3
"""Threadsへ本文を投稿し、そのスレッドにコメント欄(自己リプ)をぶら下げる。

posts.json のスケジュールを見て、いま実行すべき投稿があるときだけ送る。
スケジュールに無い時刻に起動された場合は何もせず正常終了する。

環境変数:
  THREADS_ACCESS_TOKEN  長期アクセストークン(必須)
  THREADS_USER_ID       ThreadsのユーザーID(必須)
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
REPLY_DELAY = 10


def api_post(path, params):
    """Threads Graph APIにPOSTし、JSONを返す。"""
    url = f"{API_BASE}/{path}"
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise RuntimeError(f"POST {path} failed ({e.code}): {detail}") from e


def publish_text(user_id, token, text, reply_to_id=None):
    """テキストを1件公開し、公開後のIDを返す。"""
    params = {
        "media_type": "TEXT",
        "text": text,
        "access_token": token,
    }
    if reply_to_id:
        params["reply_to_id"] = reply_to_id

    container = api_post(f"{user_id}/threads", params)
    creation_id = container["id"]
    print(f"  container created: {creation_id}")

    time.sleep(PUBLISH_DELAY)

    published = api_post(
        f"{user_id}/threads_publish",
        {"creation_id": creation_id, "access_token": token},
    )
    print(f"  published: {published['id']}")
    return published["id"]


def current_slot():
    """いまのJST時刻を、スケジュールの (日付, 時刻) キーに丸める。

    cronの起動は数分ずれることがあるので、直近のスロットに寄せる。
    一致するスロットが無ければ None。
    """
    override = os.environ.get("SLOT_OVERRIDE")
    if override:
        date_part, time_part = override.split("T")
        return date_part, time_part

    now = datetime.now(JST)
    slots = ["00:00", "10:00", "12:00", "15:00", "18:00", "21:00"]
    for slot in slots:
        hh, mm = (int(x) for x in slot.split(":"))
        target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
        # 起動が定刻の前後20分以内なら、そのスロットとみなす
        if abs((now - target).total_seconds()) <= 20 * 60:
            return now.strftime("%Y-%m-%d"), slot
    return None


def main():
    token = os.environ.get("THREADS_ACCESS_TOKEN")
    user_id = os.environ.get("THREADS_USER_ID")
    dry_run = os.environ.get("DRY_RUN") == "1"

    if not dry_run and (not token or not user_id):
        sys.exit("THREADS_ACCESS_TOKEN と THREADS_USER_ID を設定してください")

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

    parent_id = publish_text(user_id, token, post["body"])

    time.sleep(REPLY_DELAY)

    print("  コメント欄をリプライとして投稿します")
    publish_text(user_id, token, post["comment"], reply_to_id=parent_id)

    print(f"完了: No.{entry['post_id']}")


if __name__ == "__main__":
    main()
