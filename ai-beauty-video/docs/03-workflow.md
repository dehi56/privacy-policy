# 03. 制作ワークフロー

企画から投稿までの一本道。**最初の1本は品質を捨てて、とにかく最後まで通すこと。**

---

## Step 0. 環境構築

```bash
# ComfyUI 本体
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate

# PyTorch（CUDA版。バージョンは公式サイトで最新を確認）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt

# ComfyUI-Manager（これを入れると以降のノード導入がGUIで完結）
git clone https://github.com/ltdrdata/ComfyUI-Manager custom_nodes/ComfyUI-Manager

python main.py
# → http://127.0.0.1:8188
```

モデルの配置先:
```
ComfyUI/models/
├── diffusion_models/   Wan 2.2、FLUX の本体
├── text_encoders/      umt5_xxl（Wan用）、t5xxl / clip_l（FLUX用）
├── vae/                wan_2.1_vae 等
└── loras/              学習したキャラLoRA
```

起動後 `Workflow → Browse Templates → Video → Wan 2.2 Image to Video` を開けば、
必要なモデルのダウンロードリンクが表示されます。

---

## Step 1. キャラクター設計

いきなり生成せず、**先に文章で決める**。ここが曖昧だと後で全部やり直しになります。

- 年齢感 / 髪型・髪色 / 目の色・形 / 骨格・体型 / 肌の質感
- 服装の系統、雰囲気（清楚 / クール / 元気）
- 「誰にも似ていない」ことの確認（実在人物名をプロンプトに入れない）

テンプレート → [../prompts/character-sheet.md](../prompts/character-sheet.md)

---

## Step 2. 基準画像を作る

FLUX または Qwen-Image で正面バストアップを生成。**納得いくまでここで粘る。**

- 解像度 1024x1024、seedを必ず記録
- 数十枚出して1枚選ぶ。この1枚がキャラの「原本」になります
- 選んだら `assets/character/<name>/base.png` として保存し、生成パラメータをメモ

---

## Step 3. キャラLoRAを学習（同じ顔を保つ鍵）

1. **データセット作成（20〜40枚）**
   - Qwen-Image-Edit で基準画像から角度・表情・服装違いを生成するのが最も早い
   - 正面 / 斜め45° / 横顔 / 上下アングル / 笑顔 / 無表情 をバランスよく
2. **学習**（ai-toolkit または kohya_ss）
   - FLUX LoRA: rank 16〜32、学習率 1e-4、1500〜2500 steps が出発点
   - トリガーワードは固有の造語にする（例: `ayaka_v1`）
3. **検証**: 未学習のプロンプトで10枚生成し、同一人物に見えるか確認

詳細 → [04-character.md](04-character.md)

---

## Step 4. 動画の1枚目（キーフレーム）を量産

LoRAを効かせて、動画にしたいシーンの静止画を作ります。

- 縦型なら **832x1472**（9:16）付近が扱いやすい
- ControlNet（openpose / depth）でポーズを指定すると再現性が上がる
- 顔が崩れたら ComfyUI-Impact-Pack の FaceDetailer で顔だけ再生成

---

## Step 5. 画像 → 動画（i2v）

Wan 2.2 の Image-to-Video ワークフローに Step 4 の画像を入力。

### プロンプトの鉄則
**画像の中身を再説明しない。「どう動くか」だけ書く。**

```
❌ 悪い例: 長い黒髪の若い女性が白いワンピースを着てカフェに座っている
✅ 良い例: She slowly turns her head to the right and smiles softly,
           hair gently swaying, camera slowly pushes in
```
モデルはすでに画像を見ています。動きの記述にトークンを使ってください。

### パラメータの目安
| 項目 | 値 |
|---|---|
| 長さ | 5秒（81フレーム / 16fps）※まず短く |
| 解像度 | 720p（1280x720 または 720x1280） |
| steps | 20〜30 |
| CFG | 5.0〜7.0 |
| shift | 5.0（Wan系のデフォルト付近） |

モーション集 → [../prompts/video-motion.md](../prompts/video-motion.md)

### 破綻しやすいので避けるもの
- 手を大きく動かす（指が溶ける最大の原因）
- 全身の激しい移動・ダンス
- 5秒を超える長尺（1クリップ5秒 × 複数を編集で繋ぐ方が確実）

---

## Step 6. 仕上げ

```
生成動画（720p / 16fps）
   ↓ ① 顔補正        CodeFormer（fidelity 0.7前後、上げすぎると別人になる）
   ↓ ② アップスケール Real-ESRGAN or SeedVR2 → 1080p
   ↓ ③ フレーム補間   Practical-RIFE → 32fps or 60fps
   ↓ ④ 音楽・編集     FFmpeg / 動画編集ソフト
完成品
```

```bash
# 縦型9:16に書き出す例
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p output_vertical.mp4

# 複数クリップを連結
ffmpeg -f concat -safe 0 -i list.txt -c copy merged.mp4
```

---

## Step 7. 投稿

→ [05-publishing.md](05-publishing.md)（本リポジトリの Threads 自動投稿と連携できます）

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| CUDA out of memory | GGUF量子化モデルに変更 / 解像度を下げる / `--lowvram` で起動 |
| 顔が別人になる | LoRAの重みを 0.8〜1.0 に / FaceDetailerで顔だけ再生成 |
| 手・指が破綻 | 手を動かすモーションを避ける。バストアップ構図に寄せる |
| 動きがほぼ静止 | プロンプトに動詞を追加、CFGを上げる |
| 動きが激しすぎて崩壊 | プロンプトの動きを1つに絞る、CFGを下げる |
| 顔がちらつく | 生成後にCodeFormerを全フレームに適用 |
| とにかく遅い | まずLTX-Videoで当たりを探し、本番だけWanで回す |
