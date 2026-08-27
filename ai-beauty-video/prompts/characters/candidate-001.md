# 候補001（不採用）

> **不採用。** 欧米顔だったため方向転換した。確定キャラは
> [base-character.md](base-character.md) を参照。
> 初回生成のベースラインとして記録のみ残す。

![candidate-001](../../assets/character/candidate-001.png)
> 画像は `assets/` 配下（gitignore対象）。手元で保管すること。

## 生成環境

| 項目 | 値 |
|---|---|
| ツール | Draw Things（macOS） |
| マシン | M4 MacBook Air / 24GB |
| 生成時間 | 約2分 |

## 設定（この一式で再現される）

| 項目 | 値 |
|---|---|
| モデル | **Juggernaut XL X**（Stable Diffusion XL Base） |
| **シード** | **1656102627** |
| シードモード | サイズ類似（Scale Alike） |
| ステップ数 | 16 |
| テキストガイダンス（CFG） | 5.0 |
| サンプラー | DPM++ 2M AYS |
| CLIPスキップ | 2 |
| シフト | 1.00 |
| 強度 | 100%（テキストから画像へ） |
| サイズ | 1024 × 1024 |
| LoRA | 無効 |
| コントロール | 無効 |

> ⚠️ シードが同じでも、**モデル・サンプラー・ステップ数・CFG・サイズのいずれかを変えると別の顔になる。**
> 再現するときは上の表を丸ごと合わせること。

## プロンプト

**Positive:**
```
photorealistic portrait of a young woman, early 20s, oval face,
almond-shaped dark brown eyes, dark brown straight hair to collarbone,
fair skin with natural texture, neutral expression, looking at camera,
plain light gray background, soft diffused studio lighting,
85mm lens, f/2.0, sharp focus on eyes, high quality
```

**Negative:**
```
plastic skin, airbrushed, doll-like, cgi, 3d render, illustration, anime,
deformed hands, extra fingers, watermark, text, logo, celebrity, child
```

## 評価

**良い点**
- 肌に毛穴の質感が残っており、いわゆる「AIっぽいツルツル」になっていない
  （ネガティブの `plastic skin, airbrushed` が効いている）
- 顔のパーツバランスが自然。破綻なし
- 背景がプレーングレーで、後のデータセット作成に適している

**課題**
- 髪型がプロンプト（`straight hair to collarbone`）と一致せず、まとめ髪になった
  → 髪型を固定したい場合は指定を強める必要がある
- 識別用の特徴（ほくろ等）が未設定
  → 顔を確定させたら `small mole under left eye` を追加した版を作る

## ステータス

- [x] 生成・設定記録
- [ ] バッチ4枚で比較
- [ ] キャラ確定
- [ ] 特徴（ほくろ）追加版の作成
- [ ] データセット作成（20〜40枚）
- [ ] LoRA学習
