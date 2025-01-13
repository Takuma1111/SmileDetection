# 笑顔検出アプリ
このアプリはカメラを使用してリアルタイムで笑顔を検出し、笑顔の度合いを測定します。
また、笑顔度が設定された閾値を超えた場合に自動的に写真を撮影し、保存する機能も実装しております。

# 特徴
- リアルタイムで笑顔を検出
- 笑顔の度合いを計算し、画面に表示
- 笑顔度が閾値を超えると自動で写真を撮影して保存。
- 撮影間隔を設定して連続撮影を防止。

# 使用方法
1. このリポジトリをクローンまたはダウンロードします
```shell
git clone git@github.com:Takuma1111/SmileDetection.git
cd SmileDetection
```

2. 必要なPythonパッケージをインストールします
```shell
pip install mediapipe opencv-python numpy
```

3. スクリプトを実行します
```shell
python3 smile_detection.py
```

4. 笑顔が検出されるとcaptured_smilesフォルダに写真が自動的に保存されます
5. ESCキーを押すとプログラムを終了します

# Pythonパッケージ
- opencv-python
  - 映像取得とリアルタイム表示するために使用
- mediapipe
  - 顔特徴点の検出するために使用（[参考](https://yoppa.org/mit-design4-22/14113.html)） 
- numpy
  - 数値計算するために使用
 
# 備考
- スクリプト内の以下の行で笑顔度の閾値を調整できます
  - 笑顔度（smile_ratio）がこの値を超えると写真を撮影します
  - 値を大きくすると笑顔判定が厳密になり、小さくすると少しの笑顔でも検出されやすくなります
```python
SMILE_THRESHOLD = 0.3  # 笑顔度の閾値
```
- 写真撮影間隔は下記の行で調整できます
  - 連続撮影を防ぐための間隔を以下の行で設定できます 
```python
CAPTURE_INTERVAL = 2  # 写真撮影間隔（秒）
```
