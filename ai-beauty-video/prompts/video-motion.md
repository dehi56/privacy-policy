# i2v モーションプロンプト集

## 鉄則

**画像の中身を説明しない。「どう動くか」だけを書く。**
モデルは入力画像をすでに見ています。トークンは全部モーションに使ってください。

```
❌ A young woman with long black hair in a white dress sitting in a cafe, she smiles
✅ She slowly turns her head to the right and smiles softly, camera slowly pushes in
```

もう一つの鉄則: **動きは1クリップにつき1つ**。欲張ると必ず破綻します。

---

## 破綻しにくいモーション（推奨）

### 顔・視線
```
She slowly turns her head to the right, then looks back at the camera
She blinks slowly and smiles softly
Her gaze shifts from the side to the camera, subtle smile appears
She tilts her head slightly, expression softening
She looks down, then slowly raises her eyes to the camera
```

### 髪・服（自然な動きが出やすく、AI感が消える）
```
A gentle breeze moves her hair softly, she narrows her eyes slightly
Her hair sways as she turns slowly
The fabric of her dress flutters gently in the wind
```

### カメラワーク（被写体を動かさないので最も安全）
```
The camera slowly pushes in toward her face, she remains still
The camera slowly orbits around her from left to right
Slow dolly out revealing more of the scene, subject stays centered
Slight handheld camera shake, cinematic feel
```

### 環境（背景が動くと被写体が静止していても生きた画になる）
```
She stands still while people walk past in the blurred background
Soft sunlight flickers across her face through moving leaves
Rain falls in the background, she remains still, looking at the camera
Neon lights shift color on her face at night
```

---

## 破綻しやすいモーション（避ける）

| モーション | 症状 |
|---|---|
| 手を大きく動かす | 指が溶ける・6本になる（最頻出） |
| 歩く・走る | 脚が入れ替わる、体が浮く |
| ダンス | 全身が崩壊する |
| 物を持つ・触る | 物体が変形・消失する |
| 髪をかき上げる | 手と髪が融合する |
| 振り向き（180度） | 別人の顔になる |

どうしても手を映したい場合は、**手を画面外に置く構図**にするか、
バストアップに寄せてフレームから手を外してください。

---

## クリップ構成の型（5秒×3本 = 15秒）

```
[Clip 1 / 0-5s]  掴み: 顔のアップ + カメラプッシュイン
                 The camera slowly pushes in, she looks up at the camera and smiles

[Clip 2 / 5-10s] 展開: バストアップ + 環境の動き
                 A gentle breeze moves her hair, she looks off to the side

[Clip 3 / 10-15s] 締め: 引き + 余韻
                 Slow dolly out, she turns away slowly, soft sunlight
```

冒頭1秒で顔が見えないクリップは、視聴維持率が明確に落ちます。**必ず顔から始めること。**

---

## ネガティブプロンプト（Wan系）

```
static, still image, no motion, blurry, distorted face, deformed hands,
extra fingers, morphing, flickering, jittery motion, watermark, text,
oversaturated, low quality, duplicate person
```

---

## パラメータ早見表

| 症状 | 対処 |
|---|---|
| ほとんど動かない | プロンプトに具体的な動詞を追加 / CFGを 6.0〜7.0 に上げる |
| 動きすぎて崩壊 | 動きの記述を1つに減らす / CFGを 4.0〜5.0 に下げる |
| 顔が途中で変わる | クリップを短く（3秒） / 入力画像の顔を大きく |
| 全体がちらつく | steps を 30 に増やす / 生成後にCodeFormerを全フレーム適用 |
