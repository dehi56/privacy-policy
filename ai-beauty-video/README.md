# AI美女動画制作

AI生成のオリジナル人物（バーチャルモデル）による短尺動画を、ローカル環境で継続的に量産・投稿するためのプロジェクト。

- 出力想定: 5〜10秒 / 720p〜1080p / 縦型 9:16（Threads・Reels・TikTok・Shorts）
- 方針: **実在人物に似せない完全オリジナルキャラクター**をLoRAで固定し、同一人物の動画を安定して量産する
- 実行環境: **M4 MacBook Air 24GB**（キャラ設計・画像生成・編集） + **RTX 3070 Ti 8GB**（動画量産・後処理）。クラウドGPUはLoRA学習時のみ

---

## 1. 結論だけ先に

| 質問 | 答え |
|---|---|
| MacとWindows、どっち？ | **Windows + NVIDIA GPU（VRAM 16GB以上、できれば24GB）**。動画生成は事実上CUDA一択 |
| ツールはGitHubにある？ | **ある。ほぼ全部オープンソース**。中心は ComfyUI + Wan 2.2。詳細は [docs/02-tools.md](docs/02-tools.md) |
| Macは無理？ | **お試しなら十分いける。Draw Things（無料アプリ）でWan 2.2が動く。**詰まるのは量産フェーズ。買うかどうかはそこで判断すればOK |

詳細な比較 → [docs/01-hardware.md](docs/01-hardware.md)

---

## 2. ディレクトリ構成

```
ai-beauty-video/
├── README.md              このファイル（プロジェクト全体像）
├── docs/
│   ├── 01-hardware.md     Mac vs Windows / 推奨マシン構成
│   ├── 02-tools.md        GitHubツールカタログ（全リンク付き）
│   ├── 03-workflow.md     制作パイプライン（企画→生成→仕上げ→投稿）
│   ├── 04-character.md    キャラクター一貫性（同じ顔を保つ方法）
│   ├── 05-publishing.md   投稿・運用（本リポジトリのThreads自動投稿と連携）
│   └── 06-guidelines.md   法務・倫理・プラットフォーム規約 ← 必読
├── prompts/
│   ├── character-sheet.md キャラ設定＋画像生成プロンプト雛形
│   └── video-motion.md    i2v用モーションプロンプト集
├── scripts/
│   ├── check-env.py       GPU/VRAM/PyTorch環境チェック
│   └── setup-comfyui.sh   ComfyUI + カスタムノード一括セットアップ
└── assets/                生成物置き場（gitignore対象）
```

---

## 3. 制作パイプライン（概要）

```
[1] キャラ設計      キャラシート作成 → 顔・体型・雰囲気を文章で固定
        ↓
[2] 基準画像生成    FLUX / Qwen-Image で正面顔を生成（ここが一番大事）
        ↓
[3] LoRA学習        20〜40枚のデータセットを作り、キャラLoRAを学習
        ↓          （※これで「毎回同じ顔」が実現する）
[4] 静止画量産      LoRA + ポーズ/背景指定で動画の1枚目を作る
        ↓
[5] 動画化 (i2v)    Wan 2.2 で画像→動画（5秒/クリップ）
        ↓
[6] 仕上げ          顔補正 → アップスケール → フレーム補間 → 音楽
        ↓
[7] 投稿            縦型書き出し → Threads/Reels等へ（AI生成である旨を明記）
```

各ステップの具体的な手順・設定値 → [docs/03-workflow.md](docs/03-workflow.md)

---

## 4. スタート手順

### Macでお試しする場合（最短30分・無料）

1. Mac App Store で **Draw Things** を入れる
2. モデル一覧から **Wan 2.2 5B** をダウンロード
3. 手持ちの画像を1枚読み込んで Image-to-Video
4. プロンプトは1行だけ: `The camera slowly pushes in toward her face, she blinks slowly and smiles softly`

→ 詳細は [docs/01-hardware.md](docs/01-hardware.md#macだけで完結させたい場合--draw-things)

### NVIDIA GPU機でセットアップする場合

```bash
# 1. 環境チェック（GPU / VRAM / PyTorch）
python ai-beauty-video/scripts/check-env.py

# 2. ComfyUI と必要ノードのセットアップ
bash ai-beauty-video/scripts/setup-comfyui.sh

# 3. ComfyUI 起動後、公式 Wan 2.2 テンプレートを開く
#    Workflow → Browse Templates → Video → Wan 2.2 Image to Video
```

---

## 5. 進め方の推奨（最初の2週間）

| 日程 | やること | ゴール |
|---|---|---|
| Day 1-2 | 環境構築（Mac: Draw Things / GPU機: ComfyUI + Wan 2.2 5B） | とにかく5秒動画を1本出す |
| Day 3-5 | キャラ設計 + 基準画像 | 「この子でいく」という1枚を決める |
| Day 6-8 | データセット作成 + LoRA学習 | 同じ顔が10枚連続で出る |
| Day 9-11 | i2vのプロンプト詰め | 破綻しないモーションの型を3つ持つ |
| Day 12-14 | 仕上げ〜投稿まで通す | 完成品を1本公開する |

**最初からLoRA学習に行かないこと。** まず1本、雑でいいので最後まで通すのが最短。

---

## 6. 必ず守るルール

- 実在人物の顔・名前・特徴を模倣しない（フェイススワップ系ツールは本プロジェクトでは使わない）
- 未成年に見える人物を生成しない
- 各プラットフォームの成人向けコンテンツ規約を遵守する
- 投稿時に「AI生成」であることを明示する

詳細 → [docs/06-guidelines.md](docs/06-guidelines.md)
