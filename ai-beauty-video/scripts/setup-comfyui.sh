#!/usr/bin/env bash
# ComfyUI + AI美女動画制作に必要なカスタムノードを一括セットアップする。
#
#   bash ai-beauty-video/scripts/setup-comfyui.sh [インストール先]
#
# 既定のインストール先: ~/ComfyUI
# モデル本体(weights)はダウンロードしない。ComfyUI起動後、
# Workflow > Browse Templates > Video > Wan 2.2 から取得するのが確実。

set -euo pipefail

TARGET="${1:-$HOME/ComfyUI}"
CUDA_INDEX="https://download.pytorch.org/whl/cu124"

info() { printf '\033[1;34m==>\033[0m %s\n' "$1"; }
warn() { printf '\033[1;33m[WARN]\033[0m %s\n' "$1"; }
die()  { printf '\033[1;31m[ERROR]\033[0m %s\n' "$1" >&2; exit 1; }

command -v git >/dev/null    || die "git が必要です"
command -v python3 >/dev/null || die "python3 が必要です"
command -v ffmpeg >/dev/null || warn "ffmpeg が未インストールです（書き出しに必要）"

if command -v nvidia-smi >/dev/null; then
  info "NVIDIA GPU 検出"
  nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
  warn "NVIDIA GPU が見つかりません。動画生成は非常に遅いか動作しません"
  warn "詳細は ai-beauty-video/docs/01-hardware.md を参照"
fi

# --- ComfyUI 本体 -----------------------------------------------------------
if [ -d "$TARGET/.git" ]; then
  info "既存の ComfyUI を更新: $TARGET"
  git -C "$TARGET" pull --ff-only
else
  info "ComfyUI を取得: $TARGET"
  git clone https://github.com/comfyanonymous/ComfyUI "$TARGET"
fi

# --- 仮想環境 ---------------------------------------------------------------
if [ ! -d "$TARGET/venv" ]; then
  info "仮想環境を作成"
  python3 -m venv "$TARGET/venv"
fi
# shellcheck disable=SC1091
source "$TARGET/venv/bin/activate"
python -m pip install --upgrade pip

# --- PyTorch ----------------------------------------------------------------
if python -c 'import torch' 2>/dev/null; then
  info "PyTorch はインストール済み: $(python -c 'import torch; print(torch.__version__)')"
else
  if command -v nvidia-smi >/dev/null; then
    info "PyTorch (CUDA) をインストール"
    pip install torch torchvision torchaudio --index-url "$CUDA_INDEX"
  else
    info "PyTorch (CPU/MPS) をインストール"
    pip install torch torchvision torchaudio
  fi
fi

info "ComfyUI の依存関係をインストール"
pip install -r "$TARGET/requirements.txt"

# --- カスタムノード ---------------------------------------------------------
NODES=(
  "https://github.com/ltdrdata/ComfyUI-Manager"                 # ノード管理（必須）
  "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite"     # 動画の読み書き・結合
  "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation"   # RIFEフレーム補間
  "https://github.com/ltdrdata/ComfyUI-Impact-Pack"             # FaceDetailer（顔崩れ対策）
  "https://github.com/cubiq/ComfyUI_IPAdapter_plus"             # IP-Adapter（顔の一貫性）
  "https://github.com/Fannovel16/comfyui_controlnet_aux"        # ControlNet前処理
  "https://github.com/city96/ComfyUI-GGUF"                      # GGUF量子化（低VRAM向け）
)

mkdir -p "$TARGET/custom_nodes"
for repo in "${NODES[@]}"; do
  name="$(basename "$repo")"
  dest="$TARGET/custom_nodes/$name"
  if [ -d "$dest/.git" ]; then
    info "更新: $name"
    git -C "$dest" pull --ff-only || warn "$name の更新に失敗（手動で確認してください）"
  else
    info "取得: $name"
    git clone --depth 1 "$repo" "$dest" || warn "$name の取得に失敗"
  fi
  if [ -f "$dest/requirements.txt" ]; then
    pip install -r "$dest/requirements.txt" || warn "$name の依存解決に失敗"
  fi
done

# --- モデル配置用ディレクトリ -----------------------------------------------
mkdir -p "$TARGET"/models/{diffusion_models,text_encoders,vae,loras,upscale_models,controlnet}

cat <<MSG

============================================================
 セットアップ完了: $TARGET
============================================================

起動:
  source $TARGET/venv/bin/activate
  python $TARGET/main.py
  # 別マシン(Mac等)のブラウザから使う場合:
  # python $TARGET/main.py --listen 0.0.0.0 --port 8188
  # VRAMが厳しい場合: --lowvram

次の手順:
  1. ブラウザで http://127.0.0.1:8188 を開く
  2. Workflow > Browse Templates > Video > Wan 2.2 Image to Video
  3. 不足モデルのダウンロードを促されるので指示に従う
  4. ai-beauty-video/docs/03-workflow.md の Step 1 へ

MSG
