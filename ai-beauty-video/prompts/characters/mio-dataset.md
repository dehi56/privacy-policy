# 澪（mio_dt1）— LoRA学習用データセット

目標 **30〜40枚**。この工程が LoRA の品質を決める。地味だが最重要。

---

## 1. 生成方法（2026-08-27 検証済み）

### 検証の結論

同一の顔を保ったまま角度・表情を変える方法を3つ試し、**すべて失敗した。**

| 方法 | 結果 |
|---|---|
| t2i + シード固定 | ❌ プロンプトを1語変えると別人になる |
| img2img（強度45〜55%） | ❌ キャンバスの出力が次の入力になり、反復で崩壊する |
| IP Adapter Plus Face | ❌ 重み70%で別人 / 85%で構図・表情まで全ロック。使える帯がない |

原因は道具側の限界。この用途に必要な **InstantID / IP-Adapter FaceID** が
Draw Things に存在しない（2026-08 時点、SDXL Base 向けの一覧に無し）。

### 採用する方法：t2i 大量生成 + 選別

**base.png の顔を厳密に再現することは諦める。**
プロンプトで角度・光・服を振って大量に生成し、顔が似ているものを選別する。
identity は LoRA が30枚から収束させる。これが標準的なLoRAデータセットの作り方。

| 項目 | 値 |
|---|---|
| モード | テキストから画像へ |
| コントロール | IP Adapter Plus Face / **重み 50%**（顔の引きを残しつつプロンプトを効かせる帯） |
| ムードボード | `base.png` |
| ステップ数 | 16 / サンプラー DPM++ 2M AYS / CFG 5.0 |
| シード | ランダム |
| バッチサイズ 4 × 回数 2 | 1プロンプトあたり8枚・約16分 |

**「澪」は base.png ではなく、選んだ30枚の平均になる。** 顔は多少変わるが実用上問題ない。

### img2img を使う場合の必須ルール

角度の大きいカットで img2img を使うなら、**生成のたびに `base.png` を読み込み直すこと。**
img2img はキャンバスの内容を入力にするため、生成結果がそのまま次の入力になり、
反復するたびに絵が崩壊する（テクスチャ化 → 線画化）。

### 将来の選択肢：3070 Ti 機 + ComfyUI + InstantID

厳密に顔を固定したいなら、Windows機で ComfyUI + InstantID を組むのが本来の構成。
base.png の顔を保ったまま角度も表情も変えられる。
→ [../../docs/01-hardware.md](../../docs/01-hardware.md) のメモリ16GB対策を先に実施すること。

## 2. 歩留まりの現実

**採用できるのは生成した半分以下。** 60〜80枚生成して30枚残す想定。
M4 Air で1枚約2分（8枚バッチで約16分）なので、**合計2〜3時間**。
ファンレスなので連続20〜30分でサーマルスロットリングに入る。分割して回すこと。

**1セット（8枚）ごとに歩留まりを確認する。** 似ている顔が3枚以上出れば順調。
1枚以下ならコントロールの重みを調整する。

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

## 4-B. 角度カットは別プロンプトを使う（2026-08-27 検証済み）

正面用のプロンプトに `head turned 45 degrees` を足しても**角度は一切効かない。**
正面を誘導する語が強すぎて押し負けるため。

| 押し負けの原因 | 影響 |
|---|---|
| `portrait` | 正面のバストショットを強く示唆する |
| `sharp focus on eyes` | 両目が見える構図＝正面 |
| `almond-shaped eyes, natural double eyelids` | 目の描写＝正面 |

### 解決した4つの修正

1. **角度を先頭に置き、強調構文で重み付け**（先頭のトークンほど強く効く）
2. `portrait` → `photo` に変更
3. `sharp focus on eyes` と目の描写を**削除**
4. `looking away from camera` / `only one eye visible` を追加

`only one eye visible` は横顔を出すときの決定打。

### 横顔（検証済み・確実に出る）

```
(strict side profile view:1.5), photorealistic photo of a Japanese woman in her mid 20s,
her face turned 90 degrees to the left, only one eye visible,
adult woman, mature facial features, softly rounded face,
short bob haircut with blunt bangs, dark brown hair,
light warm-toned skin with natural texture, natural matte skin, minimal makeup,
plain light gray background, soft diffused studio lighting,
85mm lens, f/2.0, high quality
```

### 斜め45度

```
(three-quarter view from the side:1.4), photorealistic photo of a Japanese woman in her mid 20s,
her head turned to the side, looking away from camera,
adult woman, mature facial features, softly rounded face,
short bob haircut with blunt bangs, dark brown hair,
light warm-toned skin with natural texture, natural matte skin, minimal makeup,
plain light gray background, soft diffused studio lighting,
85mm lens, f/2.0, high quality
```

### 検証結果まとめ

| カテゴリ | 状況 |
|---|---|
| 正面 | ✅ IP Adapter 50%（顔が最も安定する） |
| 服違い・バストアップ | ✅ 正面用プロンプト・IP Adapter OFF |
| 全身 | ✅ 正面用プロンプト・手の破綻なし |
| 横顔 | ✅ 上の角度用プロンプト |
| 斜め45度 | ✅ 上の角度用プロンプト |

**輪郭が細くなる場合**は `defined jawline` を `softly rounded face` に置き換える。
`mature facial features` だけで成人らしさは保たれる。

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
