# 01. Mac vs Windows — どっちを買うべきか

## 結論

**Windows + NVIDIA GPU を買ってください。** 動画生成に限れば、これはほぼ議論の余地がありません。

理由は一つ、**CUDA**です。オープンソースの動画生成モデル（Wan、HunyuanVideo、CogVideoX、Mochi など）は
NVIDIA CUDA前提で書かれており、Apple Silicon（MPSバックエンド）は「動けばラッキー」の扱いです。

---

## 1. 実際の差

| 項目 | Windows + RTX | Mac (Apple Silicon) |
|---|---|---|
| 画像生成（SD/FLUX） | 速い | 動く。実用範囲だが1.5〜3倍遅い |
| **動画生成（Wan等）** | **本命。全モデル対応** | **未対応モデルが多い。動いても激遅** |
| LoRA学習 | 快適（kohya_ss / ai-toolkit） | 実質厳しい |
| VRAM | GPUに固定（8〜32GB） | ユニファイドメモリで大容量を確保しやすい |
| 拡張性 | GPU換装で延命可能 | 買い替えのみ |
| 静音性・電力 | うるさい・高消費電力 | 静か・省電力 |
| 動画編集・投稿運用 | 普通 | 快適 |

ベンチ的には、32GBに収まるモデルで **RTX 5090 は Apple Silicon の2〜3倍高速**、
拡散モデル全般でも **MPSは30〜50%遅い**うえに新しいアーキテクチャに未対応、という報告が一般的です。

---

## 2. 推奨構成（予算別）

### A. 最小構成 — 「とりあえず始める」
- GPU: **RTX 4060 Ti 16GB** / RTX 5060 Ti 16GB
- RAM: 32GB / SSD: 1TB NVMe
- できること: Wan 2.2 **TI2V-5B** で 720p 5秒。GGUF量子化を使えば14Bも一応動く
- 生成時間の目安: 5秒クリップで 5〜15分

> VRAM 8GBでもGGUF量子化モデルで「試す」ことは可能ですが、待ち時間で心が折れます。**16GBが実質的な下限**です。

### B. 推奨構成 — 「量産したい」★おすすめ
- GPU: **RTX 4090 / 5090（24〜32GB VRAM）**
- RAM: 64GB / SSD: 2TB NVMe
- できること: Wan 2.2 **A14B**（高品質モデル）、LoRA学習も快適
- 生成時間の目安: 720p 5秒クリップが **9分以内**（4090 / 5Bなら数分）

### C. ハイエンド — 「事業としてやる」
- GPU: RTX 6000 Ada / A6000（48GB）
- 14Bモデルを量子化なしで720p生成できる。単体消費者向けGPUでは到達できない領域

### D. 買わない選択 — クラウドGPU
- RunPod / Vast.ai / Thunder Compute などで RTX 4090 が **時間 $0.3〜0.5 程度**
- 「月に数本しか作らない」なら圧倒的にこちらが安い
- 検証してから本体を買う、という順序を強く推奨

---

## 3. すでにMacを持っている場合

**買い替える必要はありません。2台構成が最適解です。**

```
Mac（メイン作業）                 Windows機 / クラウドGPU（生成専用）
├─ 企画・キャラ設定               ├─ ComfyUI をサーバーとして起動
├─ 画像の選定・レタッチ     ←→   ├─ Wan 2.2 で動画生成
├─ 動画編集（Final Cut / Premiere）└─ LoRA学習
└─ 投稿・分析・運用
```

ComfyUIは `--listen` オプションでLAN内の他マシンからブラウザ操作できます。
Windows機は物理的に別室に置いて、MacのブラウザからComfyUIを叩く、という運用が現実的で快適です。

```bash
# Windows機（生成マシン）側で起動
python main.py --listen 0.0.0.0 --port 8188
# → Mac側のブラウザで http://<WindowsのIP>:8188
```

### Macだけで完結させたい場合 — Draw Things

**お試しならこれが最短です。** ターミナル操作もPython環境構築も不要。

- **Draw Things**（Mac App Store・無料）https://drawthings.ai/
- Wan 2.2 5B の t2v / i2v に対応（Wan 2.1 / HunyuanVideo / SkyReels / SVD も選べる）
- Apple Silicon 最適化済みで、**Mac上ではComfyUIより約40%高速**という比較結果
- 720pまで対応

| 項目 | 要件 |
|---|---|
| チップ | M2以降推奨（M1でも画像生成は可、動画は厳しい） |
| メモリ | 16GBが下限 / 24GB以上で快適 / 48GBならBF16で高品質 |

**手順**: アプリを入れる → モデル一覧から Wan 2.2 5B をダウンロード → 画像を読み込んで Image-to-Video → モーションプロンプトを1行入れて生成。

### MacでComfyUIを使う場合

MPS（Metal）でGPUアクセラレーションは効きます。LTX-Video なら M4 Pro で 768×512・97フレームが**3分半程度**。

ただし現状の制約:
- `torch.compile` 非対応（高速化の恩恵が受けられない）
- FP8モデルは回避策が必要
- Wan 2.2 / LTX 2.3 は Mac ネイティブの Metal 最適化が未完了
- LoRA学習は実質困難

**お試しは Draw Things、本格化するなら ComfyUI**、という順番が素直です。

### 実機プロファイル: M4 MacBook Air / 24GB

このプロジェクトの想定実行環境。ファンレス・メモリ帯域120GB/s級のため、
「画像は実用、動画は試作まで」という切り分けになる。

| 工程 | 実力 | 判断 |
|---|---|---|
| キャラ設計・基準画像（FLUX） | ✅ 実用 | 24GBならGGUF量子化で余裕をもって回せる |
| キーフレーム量産（SDXL/FLUX） | ✅ 実用 | SDXL 1024px で数十秒/枚 |
| 動画化（Wan 2.2 5B） | ⚠️ 動くが遅い | 試作はOK、量産は非現実的 |
| LoRA学習 | ❌ 非現実的 | クラウドへ |

**速度の目安**: Draw Things は M4 Pro/24GB で FLUX 1024×1024・20ステップが約50秒。
AirのM4はGPUコア数もメモリ帯域もProの半分以下なので、**その1.5〜2.5倍**を見ておく。
SDXLなら25〜40秒級で、こちらは十分軽快。

**16GBとの差**: 16GBではFLUXがQ4量子化でギリギリ（Q4_KS + 量子化T5が定番）。
24GBあれば余裕をもって回せる。この1点で作業効率がかなり変わる。

**ファンレス対策**（重要）:
- Airは **20〜30分の連続生成でサーマルスロットリング**に入る
- 電源に繋ぐ（バッテリー駆動は最初から性能が抑えられる）
- スタンドで底面を浮かせる
- **クラムシェル運用は避ける**（熱がこもる）
- 「夜間に10本バッチ」はこのマシンには向かない。数本ずつ休ませながら回す

**推奨設定（Draw Things）**:
| 用途 | 設定 |
|---|---|
| 動作確認の1枚目 | SDXL / 1024×1024 / 20 steps |
| 基準画像・キーフレーム | FLUX.1 dev GGUF（Q4_KSで確認 → 余裕があればQ6_K） |
| 動画の初回テスト | Wan 2.2 5B / **480p / 2〜3秒** / 20 steps |
| 動画の常用 | 480〜720p / 5秒（1本あたり数十分は見ておく） |

720p 5秒を最初から狙わないこと。まず480p・2秒で「出る」ことを確認する。

### この構成での役割分担

```
M4 Air（手元）                      クラウドGPU（必要な時だけ）
├─ キャラ設計・基準画像 ★最重要      ├─ LoRA学習（1回 $2〜3程度）
├─ データセット作り                  └─ 動画の量産（1本 $0.1未満）
├─ キーフレーム生成
└─ 編集・投稿・分析
```

動画の一貫性は**入力画像の顔で決まる**（→ [04-character.md](04-character.md)）。
つまり最重要工程は画像側にあり、そこはM4 Airで完結する。
動画化は最後の変換処理にすぎないので、そこだけクラウドに投げるのが合理的。

### Macの限界がどこに来るか

Macで詰まるのは品質ではなく**量産フェーズ**です。「試す・キャラを固める・画像を作る」までは十分実用的で、
1日10本回そうとした時点で待ち時間が効いてきます。**そこまで来てからGPUかクラウドを考えれば十分**で、
最初からWindows機を買う必要はありません。

---

## 4. OS別の注意点

### Windows
- **WSL2ではなくネイティブWindowsで動かす**方が、ComfyUIは情報量が多く安定
- NVIDIAドライバは Studio Driver 系が安定
- Python は 3.11 か 3.12（3.13は一部ライブラリが未対応なことがある）
- 電源ユニットに余裕を（RTX 5090なら1000W以上）

### Linux（第3の選択肢）
- 実は最速。同じGPUでWindowsより数%〜十数%速いことが多い
- CLI運用・自動化・複数GPUに強い
- 「動画編集はMac、生成はUbuntu機」が上級者の定番構成

---

## 5. 判断フローチャート

```
動画生成を本気でやる？
├─ YES → NVIDIA GPU必須
│         ├─ 予算20万〜  → RTX 4090/5090 の自作 or BTO（★推奨）
│         ├─ 予算10万〜  → RTX 4060 Ti 16GB / 5060 Ti 16GB
│         └─ 予算出せない → クラウドGPU（RunPod / Vast.ai）
└─ まず画像だけ試す → 手持ちのMacでOK（Draw Things / ComfyUI）
```

---

## 参考

- [Wan 2.2 ComfyUI: How to Generate AI Videos (2026) — Thunder Compute](https://www.thundercompute.com/blog/wan-2-2-comfyui-ai-video-model)
- [RTX 5090 vs Mac Studio M4 Max for AI — 2026 Compared](https://www.compute-market.com/blog/rtx-5090-vs-mac-studio-m4-max-local-ai-2026)
- [Deploy Wan 2.1/2.2: GPU Requirements and ComfyUI Setup — Spheron](https://www.spheron.network/blog/deploy-wan-2-1-ai-video-generation-gpu-setup/)
- [ComfyUI 動画生成ガイド【2026年版】— PERSC JOURNAL](https://journal.persc.jp/comfyui-video-guide/)
- [Video Generation Basics — Draw Things WIKI](https://wiki.drawthings.ai/wiki/Video_Generation_Basics)
- [Draw Things on Mac 2026: Tutorial + 40% Faster than ComfyUI](https://www.heyuan110.com/posts/ai/2026-02-15-draw-things-ultimate-guide/)
- [LTX-Video on ComfyUI: local AI video on Apple Silicon](https://stridenote.net/ltx-video-comfyui-apple-silicon/)
- [Working Apple Silicon / macOS workaround for ComfyUI FP8 MPS — ComfyUI Discussion #13273](https://github.com/Comfy-Org/ComfyUI/discussions/13273)
