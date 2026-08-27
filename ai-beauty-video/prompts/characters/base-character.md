# 基準キャラクター（確定）

このプロジェクトの主人公。**すべての生成物はこの1枚を起点とする。**

| 項目 | 値 |
|---|---|
| 名前 | （未定） |
| トリガーワード | （未定 / LoRA学習時に確定） |
| 確定日 | 2026-08-27 |
| 再現テスト | ✅ 済（シード指定で同一の顔を再現できることを確認） |
| 基準画像 | `assets/character/base.png` |

---

## 生成設定（この一式で再現される）

| 項目 | 値 |
|---|---|
| ツール | Draw Things（macOS / M4 MacBook Air 24GB） |
| モデル | **Juggernaut XL X**（Stable Diffusion XL Base） |
| **シード** | **1926734438** |
| シードモード | サイズ類似（Scale Alike） |
| ステップ数 | 16 |
| テキストガイダンス（CFG） | 5.0 |
| サンプラー | DPM++ 2M AYS |
| CLIPスキップ | 2 |
| シフト | 1.00 |
| 強度 | 100%（テキストから画像へ） |
| サイズ | 1024 × 1024 |
| LoRA / コントロール | 無効 |

> ⚠️ **再現時の注意**
> - シード欄の `-1` は「ランダム」の意味。数字を直接入力すること
> - **「生成時に新しいシードを使用」のチェックを外す。** 入っていると手入力したシードが上書きされる
> - モデル・サンプラー・ステップ数・CFG・サイズのいずれかを変えると別の顔になる

---

## プロンプト

**Positive:**
```
photorealistic portrait of a Japanese woman in her mid 20s,
adult woman, mature facial features, defined jawline,
short bob haircut with blunt bangs, dark brown hair,
almond-shaped dark brown eyes, natural double eyelids,
light warm-toned skin with natural texture and visible pores,
natural matte skin, minimal makeup,
wearing a white cotton blouse,
calm expression, looking at camera,
plain light gray background, soft diffused studio lighting,
85mm lens, f/2.0, sharp focus on eyes, high quality
```

**Negative:**
```
child, teenager, underage, childlike face, oversized eyes, chibi proportions,
nude, topless, bare shoulders,
korean idol, k-pop, v-line jaw, aegyo sal, glossy skin,
caucasian, western face, deep set eyes,
plastic skin, airbrushed, doll-like, cgi, 3d render, illustration, anime,
deformed hands, extra fingers, watermark, text, logo
```

---

## 外見の固定要素

| 項目 | 内容 |
|---|---|
| 年齢感 | 20代半ば |
| 髪型 | 顎ラインのボブ、ぱっつん前髪（blunt bangs） |
| 髪色 | ダークブラウン |
| 目 | アーモンド型・ダークブラウン・自然な二重 |
| 顔立ち | 輪郭がはっきりした顎。成人らしい骨格 |
| 肌 | ライトウォームトーン、マットな質感 |
| 服（基準） | 白のコットンブラウス |
| 識別用の特徴 | **未設定** → 次工程で `small mole under left eye` を追加 |

---

## この顔を選んだ理由

- **年齢感が明確に成人**。顎のラインと目元の作りが大人の顔になっている
- **着衣で鎖骨まわりが安定**。破綻の起点になりやすい部位が隠れている
- **データセットの原本に適した4条件が揃っている**
  正面 / 均一な光 / プレーン背景 / 手が写っていない
- K-POP風にも欧米風にも寄りすぎず、日本人として自然な範囲

## 既知の課題

- 髪の左側の毛先がわずかに溶けている
  → データセットに入れる際は再生成するか、他アングルで補う
- 識別用の特徴が未設定

---

## 次工程

- [ ] ほくろ追加版の作成（シード固定のまま `small mole under left eye` を追加）
- [ ] 名前・トリガーワードの決定
- [ ] データセット作成（20〜40枚）
- [ ] LoRA学習（3070 Ti機 or クラウド）
- [ ] i2vで動画化
