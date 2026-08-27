# 基準キャラクター（確定）

このプロジェクトの主人公。**すべての生成物はこの1枚を起点とする。**

| 項目 | 値 |
|---|---|
| 名前 | **澪（みお）** |
| トリガーワード | **`mio_dt1`** |
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
| 識別用の特徴 | **なし**（ほくろは不採用。下記参照）。判定は髪型＋輪郭で行う |

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

## 検証：ほくろ追加は不採用

シードを固定したまま Positive に `small mole under left eye,` を1行追加して再生成した結果：

- **ほくろは出なかった。** SDXL は小さな局所的特徴を CFG 5 程度では無視しやすい
- **顔が別人になった。** 顎が丸くなり、目が顔に対して大きくなって年齢感が下がった

### 学び：シードを固定しても、プロンプトを変えると顔は変わる

シードは「ノイズの初期値」でしかなく、そこに掛かるテキスト条件が変われば結果全体が動く。
**「シード固定＝同じ顔」ではない。** 同じ顔を再現したいなら、
プロンプトも1文字残らず同じにする必要がある。

データセット作成でも同じことが起きる。角度や服装を変えたカットは、
シードが同じでも顔が寄っていかないことがある。その場合は
img2img（強度35〜50%）に切り替えて、基準画像から作ること。

### 識別用の特徴について

ほくろは目視判定の補助でしかなく、必須ではない。
**一貫性を担保するのは LoRA 本体**であって、プロンプト上の小さな特徴ではない。
澪は髪型（ボブ＋ぱっつん前髪）と輪郭で十分に判定できるため、
顔を作り直してまで特徴を足す価値はないと判断した。

どうしても入れたい場合は Draw Things の強調構文
`(small mole under left eye:1.4)` で効きを強められるが、顔が再び変わるリスクがある。

## 次工程

- [x] ~~ほくろ追加版の作成~~ → **不採用**（下記の検証結果を参照）
- [x] 名前・トリガーワードの決定（澪 / `mio_dt1`）
- [ ] データセット作成（20〜40枚）
- [ ] LoRA学習（3070 Ti機 or クラウド）
- [ ] i2vで動画化
