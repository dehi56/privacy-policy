# 澪（mio_dt1）— LoRA学習用データセット

目標 **30〜40枚**。この工程が LoRA の品質を決める。地味だが最重要。

---

## 1. 生成方法：2つのやり方

### 方法A：シード固定 + プロンプト微変更（基本）

シードを **`1926734438`** に固定したまま、下の各プロンプトで生成する。

> ⚠️ **「シード固定＝同じ顔」ではない。**
> シードはノイズの初期値でしかなく、テキスト条件が変われば結果全体が動く。
> 実際、ベース確定後に1行追加しただけで別人になった（[base-character.md](base-character.md) 参照）。
> 方法Aで顔が離れたカットは、迷わず方法Bに切り替えること。

- 「生成時に新しいシードを使用」の**チェックを外す**
- バッチサイズ 1、回数 1（シード固定なのでバッチを増やしても同じ絵が出るだけ）

### 方法B：img2img（顔が離れてきた時の補正）

方法Aで別人になってしまうカットは、こちらで作る。

1. 左パネルの強度を **「画像から画像へ」** に切り替え
2. 基準画像 `base.png` をキャンバスにドラッグ
3. **強度 35〜50%** に設定（低いほど元画像に忠実）
4. 変えたい要素だけをプロンプトに書いて生成

横顔や大きく角度が変わるカットは、方法Bの方が安定する。

---

## 2. 歩留まりの現実

**採用できるのは生成した半分程度。** 60〜80枚生成して30〜40枚残す想定で進める。
M4 Air で1枚約2分なので、**合計2〜3時間**。夜間に分割して回すこと
（ファンレスなので連続20〜30分でサーマルスロットリングに入る）。

---

## 3. 共通プロンプト

すべてのカットで、この**前半部分は固定**する。ここを変えると別人になる。

```
photorealistic portrait of a Japanese woman in her mid 20s,
adult woman, mature facial features, defined jawline,
short bob haircut with blunt bangs, dark brown hair,
almond-shaped dark brown eyes, natural double eyelids,
light warm-toned skin with natural texture and visible pores,
natural matte skin, minimal makeup,
```

**Negative（全カット共通・固定）:**
```
child, teenager, underage, childlike face, oversized eyes, chibi proportions,
nude, topless, bare shoulders,
korean idol, k-pop, v-line jaw, aegyo sal, glossy skin,
caucasian, western face, deep set eyes,
plastic skin, airbrushed, doll-like, cgi, 3d render, illustration, anime,
deformed hands, extra fingers, watermark, text, logo
```

**共通の末尾:**
```
85mm lens, f/2.0, sharp focus on eyes, high quality
```

以下の各行を、共通プロンプトと末尾の**あいだ**に挟む。

---

## 4. カット一覧（40枚）

### A. 正面顔（8枚）— 最重要。ここは枚数を確保する

```
01  calm neutral expression, looking straight at camera, plain light gray background, soft diffused studio lighting
02  soft closed-mouth smile, looking at camera, plain light gray background, soft diffused studio lighting
03  bright natural smile showing teeth, looking at camera, plain light gray background, soft diffused studio lighting
04  looking down softly, eyes lowered, plain light gray background, soft diffused studio lighting
05  slightly surprised expression, eyes wide, plain light gray background, soft diffused studio lighting
06  calm expression, plain white background, bright even lighting
07  gentle smile, warm window light from the left, plain beige background
08  neutral expression, soft rim lighting, dark gray background
```

### B. 斜め45度（8枚）

```
09  head turned 45 degrees to the left, calm expression, plain light gray background, soft studio lighting
10  head turned 45 degrees to the left, soft smile, plain light gray background, soft studio lighting
11  head turned 45 degrees to the right, calm expression, plain light gray background, soft studio lighting
12  head turned 45 degrees to the right, soft smile, plain light gray background, soft studio lighting
13  three-quarter view facing left, looking at camera, plain white background, bright lighting
14  three-quarter view facing right, looking at camera, plain white background, bright lighting
15  three-quarter view, looking away from camera, plain light gray background, soft lighting
16  three-quarter view, chin slightly lifted, plain light gray background, soft lighting
```

### C. 横顔（4枚）— 方法Bを推奨

```
17  full profile view facing left, calm expression, plain light gray background, soft studio lighting
18  full profile view facing right, calm expression, plain light gray background, soft studio lighting
19  profile view facing left, slight smile, plain white background, bright lighting
20  near-profile view, eyes closed, plain light gray background, soft lighting
```

### D. 上下アングル（4枚）

```
21  camera angle slightly from above, looking up at camera, plain light gray background, soft lighting
22  camera angle slightly from below, calm expression, plain light gray background, soft lighting
23  high angle shot, soft smile, plain white background, bright lighting
24  eye level, chin tilted down, plain light gray background, soft lighting
```

### E. バストアップ・服装違い（8枚）

```
25  upper body, wearing a white cotton blouse, plain light gray background, soft studio lighting
26  upper body, wearing a beige knit sweater, plain light gray background, soft studio lighting
27  upper body, wearing a navy blazer over a white shirt, plain white background, bright lighting
28  upper body, wearing a black turtleneck, plain dark gray background, soft rim lighting
29  upper body, wearing a light blue denim shirt, plain white background, natural daylight
30  upper body, wearing a gray hoodie, plain light gray background, soft lighting
31  upper body, wearing a white t-shirt, outdoor park background, natural sunlight
32  upper body, wearing a beige trench coat, city street background, overcast daylight
```

### F. 全身・環境違い（8枚）

```
33  full body standing, wearing a white blouse and beige trousers, plain light gray studio background
34  full body standing, wearing a navy dress, plain white studio background
35  full body standing, casual outfit, hands at her sides, outdoor park, natural sunlight
36  full body walking, wearing a beige trench coat, city sidewalk, overcast daylight
37  sitting on a chair, wearing a knit sweater, cafe interior, warm window light
38  sitting by a window, wearing a white shirt, indoor natural light
39  standing near a window, wearing a light dress, soft backlight
40  full body standing, wearing a black coat, evening city street, ambient street lighting
```

> ⚠️ **手が写るカットは最小限にする。** 指の破綻はデータセット汚染の最大要因。
> 全身カットで手が崩れたら、そのカットは容赦なく捨てる（`hands at her sides` 指定でも崩れることがある）。

---

## 5. 採用基準（ここが本番）

生成したら、1枚ずつこの4項目で判定する。**1つでも×なら捨てる。**

- [ ] **同一人物に見えるか** ← 最重要。輪郭・目の間隔・前髪の分かれ方で判定する
- [ ] 顔が潰れていない・ぼやけていない
- [ ] 手・指・耳・首が破綻していない
- [ ] 髪の生え際・毛先が溶けていない

**迷ったら捨てる。** 微妙な1枚を入れるより、30枚で確実な方が良いLoRAになる。

### バランス確認

背景・服装が偏ると、そこまで学習されてしまう。最終的に：

| 項目 | 目安 |
|---|---|
| プレーン背景 | 60〜70% |
| 環境あり背景 | 30〜40% |
| 同じ服 | 全体の3割以下に抑える |
| 正面顔 | 最低6枚は確保 |

---

## 6. ファイル名とキャプション

### ファイル名
```
mio_001.png, mio_002.png, ...
```

### キャプション（各画像に同名の .txt）

**シンプルに保つこと。** 顔の特徴を細かく書くと、その表現がトリガーワードから剥がれる。

```
mio_001.txt →  mio_dt1, a woman, front view, neutral expression, white blouse, plain background
mio_017.txt →  mio_dt1, a woman, profile view, plain background
mio_035.txt →  mio_dt1, a woman, full body, outdoor park, casual outfit
```

書くのは**「変わる要素」だけ**。髪型・目の色・顔立ちは書かない（それを覚えさせたいので、
言葉で説明してしまうとトリガーワードに紐づかなくなる）。

---

## 7. 完成後

`datasets/mio_dt1/` にまとめて、3070 Ti 機かクラウドへ転送 → LoRA学習へ。
学習設定は [../../docs/04-character.md](../../docs/04-character.md) を参照。

## 進捗

- [ ] A. 正面顔 8枚
- [ ] B. 斜め45度 8枚
- [ ] C. 横顔 4枚
- [ ] D. 上下アングル 4枚
- [ ] E. バストアップ 8枚
- [ ] F. 全身 8枚
- [ ] 採用基準で選別（30〜40枚に確定）
- [ ] キャプション作成
