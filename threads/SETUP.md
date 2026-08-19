# Threads自動投稿のセットアップ

GitHub Actionsが1日6枠(10:00 / 12:00 / 15:00 / 18:00 / 21:00 / 00:00 JST)で起動し、
`posts.json` のスケジュールに予定がある枠だけ投稿します。本文を投稿したあと、
コメント欄を同じスレッドへの自己リプとしてぶら下げます。

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
   - **リダイレクトURI**: 自分で受け取れるURLなら何でもよい(後述の手動フローでは
     `https://localhost/` でも可)
   - **プライバシーポリシーURL**: このリポジトリのGitHub Pagesで公開しているURL
     (`https://dehi56.github.io/privacy-policy/`)
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

レスポンスの `access_token` と `user_id` を控える。

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

`id` と `username` が返れば成功です。この `id` が `THREADS_USER_ID` です。

---

## 4. GitHub Secretsに登録する

リポジトリの Settings → Secrets and variables → Actions → New repository secret

| Secret名 | 値 |
| --- | --- |
| `THREADS_ACCESS_TOKEN` | 3-3で取得した長期トークン |
| `THREADS_USER_ID` | 3-4で確認した `id` |

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

- **GitHub Actionsのcronは数分〜十数分遅れることがあります。** スクリプトは定刻の
  前後20分以内の起動を同じ枠として扱うので、多少の遅れは問題ありません。

- **投稿制限は24時間あたり250件**です。1日5本なので余裕があります。

- **スケジュールを変えたい**ときは `posts.json` の `schedule` を編集してください。
  `date` と `time` が一致する枠で `post_id` の投稿が送られます。

- **止めたい**ときは Actionsタブ → 「Threads 自動投稿」→ 右上の「...」→ Disable workflow。
