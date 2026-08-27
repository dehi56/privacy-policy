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

## 基準画像プロンプト（雛形）

```
photorealistic portrait of a young woman, early 20s,
oval face, high cheekbones, small nose, almond-shaped dark brown eyes,
straight soft eyebrows, small mole under left eye,
dark brown straight hair to collarbone, center part,
fair skin with natural texture and visible pores,
neutral expression, looking at camera,
plain light gray background, soft diffused studio lighting,
shot on 85mm lens, f/2.0, shallow depth of field,
high quality, sharp focus on eyes
```

### ネガティブプロンプト
```
plastic skin, airbrushed, doll-like, cgi, 3d render, illustration, anime,
deformed hands, extra fingers, watermark, text, logo,
oversaturated, heavy makeup, celebrity, child, teenager
```

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
