# 02. GitHubツールカタログ

> 質問「美女を作るツールはGitHubにあるの？」への答え → **ほぼ全部あります。しかも無料・オープンソースです。**
> 有料SaaS（Kling / Runway / Hailuo など）を使わなくても、この構成でひと通り完結します。

---

## 0. 最小構成（これだけ入れれば動く）

| 役割 | ツール | リンク |
|---|---|---|
| 実行基盤 | **ComfyUI** | https://github.com/comfyanonymous/ComfyUI |
| ノード管理 | **ComfyUI-Manager** | https://github.com/ltdrdata/ComfyUI-Manager |
| 動画生成 | **Wan 2.2** | https://github.com/Wan-Video/Wan2.2 |
| 画像生成 | **FLUX.1 dev** | https://github.com/black-forest-labs/flux |
| 顔補正 | **CodeFormer** | https://github.com/sczhou/CodeFormer |
| アップスケール | **Real-ESRGAN** | https://github.com/xinntao/Real-ESRGAN |

以下は用途別の詳細カタログ。

---

## 1. 実行環境（UI / 基盤）

| ツール | 特徴 | リンク |
|---|---|---|
| **ComfyUI** ★本命 | ノードベース。動画生成は事実上これ一択。公式にWan 2.2テンプレート同梱 | https://github.com/comfyanonymous/ComfyUI |
| ComfyUI-Manager | カスタムノードをGUIから導入。最初に必ず入れる | https://github.com/ltdrdata/ComfyUI-Manager |
| Stable Diffusion WebUI (A1111) | 老舗。UIは直感的だが動画は弱い | https://github.com/AUTOMATIC1111/stable-diffusion-webui |
| SD WebUI Forge | A1111の高速フォーク。低VRAMに強い | https://github.com/lllyasviel/stable-diffusion-webui-forge |
| Fooocus | 設定を隠した簡単UI。静止画のお試し用 | https://github.com/lllyasviel/Fooocus |
| InvokeAI | 商用利用を意識した統合環境 | https://github.com/invoke-ai/InvokeAI |
| SwarmUI | ComfyUIをバックエンドに使う扱いやすいUI | https://github.com/mcmonkeyprojects/SwarmUI |

---

## 2. 動画生成モデル（本丸）

| モデル | 強み | VRAM目安 | リンク |
|---|---|---|---|
| **Wan 2.2** ★第一候補 | t2v / i2v / 動画編集を1モデルで。Apache-2.0で**商用可**。質感とカメラ制御が強い | 5B: 16GB〜 / A14B: 24GB〜 | https://github.com/Wan-Video/Wan2.2 |
| Wan 2.1 | 一世代前。情報とLoRA資産が多い | 12GB〜 | https://github.com/Wan-Video/Wan2.1 |
| **HunyuanVideo** | **人物描写が特に得意**。美女系と相性◎ | 24GB〜 | https://github.com/Tencent-Hunyuan/HunyuanVideo |
| **LTX-Video** | とにかく速い。**試作・当たり探し用** | 8GB〜 | https://github.com/Lightricks/LTX-Video |
| CogVideoX | 安定した品質。研究用途で情報が豊富 | 12GB〜 | https://github.com/THUDM/CogVideo |
| Mochi 1 | モーションの自然さに定評 | 24GB〜 | https://github.com/genmoai/models |
| AnimateDiff | 既存のSD1.5/SDXL資産をそのまま動かせる | 8GB〜 | https://github.com/guoyww/AnimateDiff |
| FramePack | 低VRAMで長尺を生成する手法 | 6GB〜 | https://github.com/lllyasviel/FramePack |

### 実務的な二段構え（これが効く）
```
LTX-Video で10〜20パターンを高速生成 → 方向性を決定
        ↓
Wan 2.2 / HunyuanVideo で本番品質に仕上げる
```
いきなり重いモデルで回すと、1パターン試すのに何十分もかかって検証が進みません。

---

## 3. 画像生成モデル（動画の1枚目を作る）

| モデル | 特徴 | リンク |
|---|---|---|
| **FLUX.1 dev** ★ | 現行の写実系の定番。手・肌の破綻が少ない | https://github.com/black-forest-labs/flux |
| **Qwen-Image / Qwen-Image-Edit** | 編集能力が高く、**同一人物のデータセット作りに最適** | https://github.com/QwenLM/Qwen-Image |
| Stable Diffusion 3.5 | 汎用。LoRA資産が豊富 | https://github.com/Stability-AI/sd3.5 |
| SDXL | 枯れていて安定。LoRAとControlNetが最も充実 | https://github.com/Stability-AI/generative-models |

モデル本体（weights）は基本 **Hugging Face** から取得します（GitHubはコード側）。

---

## 4. キャラクター一貫性（同じ顔を保つ）★最重要

| ツール | 用途 | リンク |
|---|---|---|
| **kohya_ss** | LoRA学習の定番GUI | https://github.com/bmaltais/kohya_ss |
| **ai-toolkit** | FLUX/Wan系のLoRA学習ならこちら | https://github.com/ostris/ai-toolkit |
| **IP-Adapter** | 参照画像を渡して顔を寄せる（学習不要） | https://github.com/tencent-ailab/IP-Adapter |
| **InstantID** | 顔ランドマークで構造的に固定。LoRAと併用可 | https://github.com/instantX-research/InstantID |
| **PuLID** | 高忠実度の顔ID保持 | https://github.com/ToTheBeginning/PuLID |
| **ControlNet** | ポーズ・構図の制御 | https://github.com/lllyasviel/ControlNet |

詳しい使い分け → [04-character.md](04-character.md)

> ⚠️ **フェイススワップ系（Roop / FaceFusion / Deep-Live-Cam 等）は本プロジェクトでは使いません。**
> 実在人物の顔を移植する用途が中心で、肖像権・名誉毀損・プラットフォーム規約すべてに抵触するリスクがあります。
> オリジナル顔をLoRAで固定する方が、品質・法務の両面で優れています。

---

## 5. 仕上げ（後処理）

| ツール | 用途 | リンク |
|---|---|---|
| **Real-ESRGAN** | 画像・動画のアップスケール | https://github.com/xinntao/Real-ESRGAN |
| **CodeFormer** | 顔の復元・補正（動画のちらつき対策に有効） | https://github.com/sczhou/CodeFormer |
| GFPGAN | 顔復元（軽量） | https://github.com/TencentARC/GFPGAN |
| **Practical-RIFE** | フレーム補間（16fps → 32/60fpsで滑らかに） | https://github.com/hzwer/Practical-RIFE |
| SeedVR2 | 動画特化の高品質アップスケーラ | https://github.com/IceClear/SeedVR2 |
| Video2X | 動画アップスケールの統合ツール | https://github.com/k4yt3x/video2x |
| FFmpeg | 連結・トリム・音声合成・エンコード（必須） | https://github.com/FFmpeg/FFmpeg |

---

## 6. 音声・リップシンク（喋らせる場合）

| ツール | 用途 | リンク |
|---|---|---|
| **LivePortrait** | 表情・頭部モーションの転写。品質が高い | https://github.com/KwaiVGI/LivePortrait |
| SadTalker | 静止画＋音声から喋る動画 | https://github.com/OpenTalker/SadTalker |
| **Style-Bert-VITS2** | 日本語音声合成。感情表現が豊か | https://github.com/litagin02/Style-Bert-VITS2 |
| RVC | 音声変換 | https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI |

---

## 7. ComfyUI カスタムノード（入れておくと捗る）

| ノード | 用途 | リンク |
|---|---|---|
| ComfyUI-VideoHelperSuite | 動画の読み書き・結合 | https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite |
| ComfyUI-Frame-Interpolation | RIFE等をノード化 | https://github.com/Fannovel16/ComfyUI-Frame-Interpolation |
| ComfyUI_IPAdapter_plus | IP-Adapter統合 | https://github.com/cubiq/ComfyUI_IPAdapter_plus |
| comfyui_controlnet_aux | ControlNet前処理 | https://github.com/Fannovel16/comfyui_controlnet_aux |
| ComfyUI-Impact-Pack | 顔の自動検出＋部分再生成（顔崩れ対策の定番） | https://github.com/ltdrdata/ComfyUI-Impact-Pack |
| ComfyUI-GGUF | GGUF量子化モデル対応（低VRAMの救世主） | https://github.com/city96/ComfyUI-GGUF |

---

## 8. ライセンスの注意

商用利用（広告収益・PR案件）を考えるなら、**モデルごとのライセンス確認は必須**です。

| モデル | ライセンス | 商用 |
|---|---|---|
| Wan 2.2 | Apache-2.0 | ✅ 可 |
| FLUX.1 dev | Non-Commercial License | ⚠️ 不可（商用は FLUX.1 pro / schnell(Apache-2.0) を検討） |
| SDXL / SD3.5 | Stability AI License | ⚠️ 条件付き |
| HunyuanVideo | Tencent Community License | ⚠️ 要確認 |

Civitai等で配布されているLoRAにも個別のライセンスがあります。「商用可」と明記されたものだけを使ってください。

---

## 参考

- [Open Source Video Generation Models (2026 Landscape Guide) — LTX](https://ltx.io/blog/open-source-video-generation-models-guide)
- [Wan2.2 ComfyUI 公式ワークフロー例](https://docs.comfy.org/tutorials/video/wan/wan2_2)
- [Best Open Source AI Video Generation Models in 2026 — Pixazo](https://www.pixazo.ai/blog/best-open-source-ai-video-generation-models)
