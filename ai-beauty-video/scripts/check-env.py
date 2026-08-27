#!/usr/bin/env python3
"""AI動画生成の実行環境チェック。

    python ai-beauty-video/scripts/check-env.py

GPU / VRAM / PyTorch を確認し、このマシンで現実的に回せるモデルを提案する。
"""

import platform
import shutil
import subprocess
import sys

OK, WARN, NG = "[OK]  ", "[WARN]", "[NG]  "


def line(mark: str, msg: str) -> None:
    print(f"{mark} {msg}")


def check_system() -> str:
    print("\n=== システム ===")
    os_name = platform.system()
    line(OK, f"OS: {os_name} {platform.release()} ({platform.machine()})")
    line(OK, f"Python: {sys.version.split()[0]}")

    major, minor = sys.version_info[:2]
    if (major, minor) < (3, 10):
        line(NG, "Python 3.10 以上が必要です（推奨 3.11 / 3.12）")
    elif (major, minor) > (3, 12):
        line(WARN, "3.13以降は一部ライブラリが未対応の場合があります（推奨 3.11 / 3.12）")
    return os_name


def check_gpu(os_name: str) -> float:
    """利用可能なVRAM(GB)を返す。判定不能なら 0.0。"""
    print("\n=== GPU ===")

    if shutil.which("nvidia-smi"):
        try:
            out = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,driver_version",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=15, check=True,
            ).stdout.strip()
        except (subprocess.SubprocessError, OSError) as e:
            line(WARN, f"nvidia-smi の実行に失敗: {e}")
            return 0.0

        vram_max = 0.0
        for row in out.splitlines():
            name, mem, driver = (c.strip() for c in row.split(","))
            vram = float(mem) / 1024
            vram_max = max(vram_max, vram)
            line(OK, f"NVIDIA {name} / VRAM {vram:.1f}GB / Driver {driver}")
        return vram_max

    if os_name == "Darwin" and platform.machine() == "arm64":
        line(WARN, "Apple Silicon 検出 — 画像生成は可能ですが、動画生成は未対応モデルが多く低速です")
        line(WARN, "  → 動画生成は Windows/Linux + NVIDIA GPU かクラウドGPUを推奨（docs/01-hardware.md）")
        return 0.0

    line(NG, "NVIDIA GPU が見つかりません。ローカルでの動画生成は困難です")
    line(NG, "  → クラウドGPU（RunPod / Vast.ai）を検討してください")
    return 0.0


def check_torch() -> None:
    print("\n=== PyTorch ===")
    try:
        import torch
    except ImportError:
        line(WARN, "PyTorch 未インストール")
        line(WARN, "  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124")
        return

    line(OK, f"torch {torch.__version__}")
    if torch.cuda.is_available():
        line(OK, f"CUDA 利用可能 (device={torch.cuda.get_device_name(0)}, cuda={torch.version.cuda})")
    elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        line(WARN, "MPS (Apple Silicon) 利用可能 — 画像生成のみ実用的")
    else:
        line(NG, "GPUバックエンドが利用できません（CPU実行は非現実的な速度になります）")


def check_tools() -> None:
    print("\n=== 外部ツール ===")
    for cmd, note in (("git", "必須"), ("ffmpeg", "必須（書き出し・連結・音声）")):
        if shutil.which(cmd):
            line(OK, f"{cmd} 検出")
        else:
            line(NG, f"{cmd} が見つかりません（{note}）")


def recommend(vram: float) -> None:
    print("\n=== このマシンで回せるモデル ===")
    if vram >= 40:
        line(OK, "Wan 2.2 A14B を量子化なしで720p生成可能。LoRA学習も余裕")
    elif vram >= 24:
        line(OK, "Wan 2.2 A14B（本命）/ HunyuanVideo / LoRA学習すべて快適")
    elif vram >= 16:
        line(OK, "Wan 2.2 TI2V-5B で720p 5秒が実用範囲。14BはGGUF量子化で")
        line(WARN, "  LoRA学習は解像度を落とせば可能")
    elif vram >= 12:
        line(WARN, "LTX-Video / Wan 2.1 / AnimateDiff 中心。GGUF量子化を前提に")
    elif vram >= 8:
        line(WARN, "LTX-Video + GGUF量子化なら動作。待ち時間は長い")
        line(WARN, "  → ComfyUI-GGUF: https://github.com/city96/ComfyUI-GGUF")
    else:
        line(NG, "ローカルでの動画生成は非推奨。クラウドGPUを使ってください")
    print("\n詳細 → ai-beauty-video/docs/01-hardware.md\n")


def main() -> int:
    print("=" * 56)
    print(" AI美女動画制作 — 環境チェック")
    print("=" * 56)
    os_name = check_system()
    vram = check_gpu(os_name)
    check_torch()
    check_tools()
    recommend(vram)
    return 0


if __name__ == "__main__":
    sys.exit(main())
