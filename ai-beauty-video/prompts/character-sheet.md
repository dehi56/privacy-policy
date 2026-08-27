# キャラクターシート テンプレート

生成を始める前に埋めてください。**ここを飛ばすと必ず後で作り直しになります。**

---

## 基本設定

| 項目 | 内容 |
|---|---|
| 名前（架空） | |
| トリガーワード | `_______v1`（固有の造語。既存単語と被らせない） |
| 年齢感 | 20代前半 など |
| 身長・体型 | |
| 出身・設定 | |
| 性格・雰囲気 | 清楚 / クール / 元気 / ミステリアス |
| 想定プラットフォーム | Threads / Reels / TikTok |

## 外見の固定要素（毎回同じにする）

| 項目 | 内容 |
|---|---|
| 髪型 | 例: 鎖骨までのストレート、center part |
| 髪色 | 例: dark brown |
| 目 | 例: almond-shaped, dark brown eyes |
| 眉 | 例: straight, soft |
| 顔立ち | 例: oval face, high cheekbones, small nose |
| 肌 | 例: fair, natural texture with visible pores |
| 特徴 | 例: 左目の下にほくろ ← **1つ入れると一貫性の判定が楽になる** |

---

## 基準画像プロンプト（日本人ベース・雛形）

```
photorealistic portrait of a young Japanese woman, early 20s,
east asian features, slim oval face, soft jawline,
almond-shaped dark brown eyes with natural double eyelids,
small straight nose, gentle mouth,
long straight black hair to collarbone, center part,
light warm-toned skin with natural texture and visible pores,
natural minimal makeup, small mole under left eye,
neutral expression, looking at camera,
plain light gray background, soft diffused studio lighting,
shot on 85mm lens, f/2.0, shallow depth of field,
high quality, sharp focus on eyes
```

### ネガティブプロンプト
```
caucasian, western face, deep set eyes,
plastic skin, airbrushed, doll-like, cgi, 3d render, illustration, anime,
deformed hands, extra fingers, watermark, text, logo,
oversaturated, heavy makeup, celebrity, child, teenager
```

### アジア系の顔を出すコツ

SDXL系（Juggernaut XL X 含む）は**放っておくと欧米顔に戻る**。
`asian` の一語だけでは無国籍顔か韓国アイドル風に寄るため、
**国籍 + 具体的な骨格・目の形**をセットで指定し、
ネガティブで `caucasian, western face, deep set eyes` を押し返すこと。

| 出た結果 | 対処 |
|---|---|
| 韓国アイドル風に寄りすぎ | ネガティブに `korean idol, k-pop, heavy makeup` を追加 |
| 中華系に寄る | Positive に `Japanese, tokyo` を強調、`chinese` をネガティブへ |
| 幼く見えすぎる | `early 20s` → `mid 20s`、`mature features` を追加 |
| 目を一重にしたい | `natural double eyelids` → `monolid eyes` |
| 肌が白すぎる | `light warm-toned skin` → `warm beige skin tone` |

プロンプトで足りない場合は、アジア系特化のコミュニティモデル
（モデル検索欄で `asian` / `BRA` / `majic` などを検索）への切り替えを検討する。

---

## データセット用バリエーション指示（Qwen-Image-Edit）

基準画像を入力し、以下を順に指示して素材を集めます。

```
1.  keep the same face, turn the head 45 degrees to the left
2.  keep the same face, turn the head 45 degrees to the right
3.  keep the same face, profile view facing left
4.  keep the same face, slight smile showing teeth
5.  keep the same face, laughing naturally
6.  keep the same face, looking down softly
7.  keep the same face, camera angle slightly from above
8.  keep the same face, camera angle slightly from below
9.  keep the same face, change outfit to a white casual shirt
10. keep the same face, change outfit to a beige knit sweater
11. keep the same face, full body standing, casual outfit
12. keep the same face, sitting in a cafe, natural window light
```

---

## 記録欄（必ず残す）

| 項目 | 値 |
|---|---|
| ベースモデル | |
| Seed | |
| Steps / CFG | |
| 解像度 | |
| LoRAファイル名 | |
| 学習steps | |
| 推奨LoRA重み | |
