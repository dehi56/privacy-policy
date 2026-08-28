# Threads自動投稿のセットアップ

1日6枠(10:00 / 12:00 / 15:00 / 18:00 / 21:00 / 00:00 JST)に、`posts.json` の
スケジュールで指定した投稿を送ります。`posts.json` の `body` と `comment` を
**1つの投稿にまとめて**出します(間に空行が入ります)。

GitHub Actions自体は30分おきに起動し、そのとき投稿すべき枠があるかを
スクリプトが判定します(理由は後述の「運用メモ」)。

必要な作業はアクセストークンの取得とSecrets登録だけです。

---

## 1. 投稿内容の数字を実際の値に置き換える

**投稿を始める前に必ずやってください。**

`posts.json` の各 `comment` に入っている数字のうち、事実として確認できているのは
スクール120万・借金200万・クレカ2回ブラック・AI歴2ヶ月の4つだけです。
それ以外(残高164万、月3万、note1980円×9本、サブスク8400円、延滞61日、ツール300個、
表示回数300→1800 など)は文章の型を成立させるために置いた仮の値です。

自分の実体験として発信する以上、仮の値のままでは事実と違う内容を発信することになります。
実際の数字に置き換えるか、該当する実績がない文はその一文ごと削ってください。
各コメントは210〜245字あるので、1文削っても文章は成立します。

---

## 2. Meta開発者アプリを作る

1. https://developers.facebook.com/ で開発者登録する
2. 「アプリを作成」→ ユースケースで **Threads API** を選ぶ
3. アプリ設定の「Threads API」で以下を登録する
   - **リダイレクトURI**: `https://dehi56.github.io/privacy-policy/`

     Threads APIは `localhost` を受け付けません。入力しても
     「フォームを保存できません」で弾かれます。実在するHTTPSのURLが必要なので、
     このリポジトリのGitHub Pagesを使います(リポジトリの Settings → Pages で
     Source を「Deploy from a branch」、Branch を `main` / `(root)` にして有効化)。

     入力後は一度URLをクリックして確定させてから保存してください。入力しただけだと
     保存に失敗することがあります。
   - **プライバシーポリシーURL**: 同じく `https://dehi56.github.io/privacy-policy/`
4. 「アプリロール」→「ロール」で、自分のThreadsアカウントを **Threadsテスター** として追加する
5. Threadsアプリ側(スマホ)で 設定 → アカウント → ウェブサイトの権限 → 招待 から承認する

テスターとして自分のアカウントを追加すれば、本番向けのアプリ審査を通さなくても
自分のアカウントへは投稿できます。

---

## 3. アクセストークンを取る

### 3-1. 認可コードを受け取る

ブラウザで以下のURLを開き、許可する。`{APP_ID}` と `{REDIRECT_URI}` は自分のものに差し替える。

```
https://threads.net/oauth/authorize
  ?client_id={APP_ID}
  &redirect_uri={REDIRECT_URI}
  &scope=threads_basic,threads_content_publish
  &response_type=code
```

リダイレクト先URLの `?code=` の後ろが認可コードです(末尾の `#_` は取り除く)。

### 3-2. 短期トークンに交換する

```bash
curl -X POST https://graph.threads.net/oauth/access_token \
  -d client_id={APP_ID} \
  -d client_secret={APP_SECRET} \
  -d grant_type=authorization_code \
  -d redirect_uri={REDIRECT_URI} \
  -d code={CODE}
```

レスポンスの `access_token` を控える(この時点ではまだ短期トークンです)。

### 3-3. 長期トークン(60日)に交換する

```bash
curl "https://graph.threads.net/access_token\
?grant_type=th_exchange_token\
&client_secret={APP_SECRET}\
&access_token={SHORT_LIVED_TOKEN}"
```

返ってきた `access_token` が長期トークンです。

> Metaの仕様は変わることがあります。うまくいかない場合は
> https://developers.facebook.com/docs/threads で現在の手順を確認してください。

### 3-4. 動作確認

```bash
curl "https://graph.threads.net/v1.0/me?fields=id,username&access_token={LONG_LIVED_TOKEN}"
```

`id` と `username` が返れば成功です。

> **投稿エンドポイントには数値のユーザーIDではなく `me` を使ってください。**
> ここで返ってくる正しい `id` を指定しても、投稿(POST)だけは
> 「Object with ID ... does not exist」で拒否されます。読み取りは通るので
> 紛らわしいですが、`me/threads` と `me/threads_publish` を使えば通ります。

投稿まで通るか確認するには、実際に1件送ってみるのが確実です。

```bash
# コンテナを作る
curl -X POST "https://graph.threads.net/v1.0/me/threads" \
  --data-urlencode "media_type=TEXT" \
  --data-urlencode "text=接続テストです" \
  --data-urlencode "access_token={LONG_LIVED_TOKEN}"

# 30秒ほど待ってから、返ってきた id で公開する
curl -X POST "https://graph.threads.net/v1.0/me/threads_publish" \
  --data-urlencode "creation_id={上で返ってきたid}" \
  --data-urlencode "access_token={LONG_LIVED_TOKEN}"
```

---

## 4. GitHub Secretsに登録する

リポジトリの Settings → Secrets and variables → Actions → New repository secret

| Secret名 | 値 |
| --- | --- |
| `THREADS_ACCESS_TOKEN` | 3-3で取得した長期トークン |

トークンは絶対にコードに直接書かないでください。Secretsに入れればログにも出ません。

---

## 5. テストしてから本番を待つ

Actionsタブ → 「Threads 自動投稿」→ Run workflow

- **dry_run にチェックを入れたまま** 実行すると、送信せず内容だけログに出ます
- `slot` に `2026-08-20T10:00` のように入れると、その枠の投稿内容を確認できます
- 実際に1本だけ投稿して確かめたい場合は、dry_run のチェックを外して実行してください

問題なければ何もしなくて構いません。スケジュール通りに自動で走ります。

---

## 運用メモ

- **トークンの期限は60日**です。切れる前に更新してください。

  ```bash
  curl "https://graph.threads.net/refresh_access_token\
  ?grant_type=th_refresh_token\
  &access_token={LONG_LIVED_TOKEN}"
  ```

  更新したトークンでSecretsを上書きします。

- **GitHub Actionsのスケジュール実行は、遅れるだけでなく起動そのものが消えます。**
  実測では1時間以上の遅延が常態で、6回の予定のうち5回が実行されなかった日もあります。
  そのため枠ちょうどに1回だけ起動するのではなく、**30分おきに起動**して、
  「定刻を過ぎて90分以内」の枠を拾う方式にしています。1枠につき3回の機会があるので、
  2回落ちても投稿されます。予定の無い時刻に起動した場合は何もせず終了します。

- **同じ枠を複数の起動が拾っても二重投稿にはなりません。** 送信前に直近25件の投稿を
  取得し、同じ本文が既にあれば送信を見送ります。この照合に失敗した場合は
  送信せずエラー終了します(重複させるよりは1回見送る方が安全なため)。

- **Actionsの実行履歴には「該当スロットなし」で終わる緑のログが大量に並びます。**
  これは正常です。30分おきに起動して、ほとんどの回は何もせず終わるためです。
  実際に投稿された回はログに `published:` が出ます。

- **コメント欄を自己リプとしてぶら下げる構成は使えませんでした。** リプライの作成が
  `{"code":1,"message":"An unknown error occurred"}` で失敗し続けたためです
  (5時間・3回の実行・2つの親投稿にわたり計9回。本文の投稿は同じトークンで通るので、
  リプライ固有の問題)。コメント欄が落ちると内容の核心が届かないので、
  1つの投稿にまとめる方式に切り替えました。全30本が最長276字で、上限500字に収まります。

  Metaのリプライ作成が直ったら、`post_to_threads.py` の
  `COMBINE_BODY_AND_COMMENT` を `False` に戻せば元のスレッド構成に復帰します。

- **投稿制限は24時間あたり250件**です。1日6本なので余裕があります。

- **スケジュールを変えたい**ときは `posts.json` の `schedule` を編集してください。
  `date` と `time` が一致する枠で `post_id` の投稿が送られます。
  **スケジュールを使い切ると何も投稿されなくなります**(エラーにはならず、
  「この枠に投稿予定はありません」と出て終わるだけです)。日付を切らさないよう
  追記してください。

- **止めたい**ときは Actionsタブ → 「Threads 自動投稿」→ 右上の「...」→ Disable workflow。
