![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Streamlit](https://img.shields.io/badge/streamlit-%E2%AC%9B-orange)
![dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen)
![GitHub Stars](https://img.shields.io/github/stars/ymmtshch/TimeLapseCamera?style=social)
![Last Commit](https://img.shields.io/github/last-commit/ymmtshch/TimeLapseCamera)
![GitHub Issues](https://img.shields.io/github/issues/ymmtshch/TimeLapseCamera)
![GitHub Forks](https://img.shields.io/github/forks/ymmtshch/TimeLapseCamera?style=social)

# 📷 タイムラプスカメラアプリとGIF作成アプリ

このアプリは、StreamlitとOpenCVを使用してタイムラプス撮影を行い、キャプチャ画像からGIFアニメーションを作成できるツールです。
カメラを指定して一定間隔で画像を保存し、GIFとしてダウンロードすることができます。(`main.py`)
通信状態が不安定であったり、スタンドアローンで使用したい場合は `main2.py` をpythonローカル環境で使用してみてね。StreamlitのようなUIで使用できるデスクトップアプリも作成したので、要望あれば配布します。

## 📄 概要

主な機能：
- USBカメラを選択してタイムラプス撮影を開始
- サイドバーで撮影間隔（秒）や撮影時間（分）を指定可能
- ユーザー指定のフォルダに画像を保存
- 撮影した画像をGIFアニメーションに変換し、ローカルに保存またはダウンロード
- 撮影中のプレビュー表示

---

## 🚀 アプリの使用方法

### 1. サイドバーで設定を入力
- **カメラの選択**: 接続しているUSBカメラの番号を指定します（例: 0, 1）。
- **ファイル名のプレフィックス**: 保存する画像やGIFの名前を指定します（例: `timelapse`）。
- **撮影間隔**: キャプチャする間隔を1～60秒で指定します。
- **撮影時間**: 全体の撮影時間を1～90分で指定します。

### 2. タイムラプス撮影を開始
- 「Start Capture」をクリックすると、設定に基づいて撮影が開始されます。
- 撮影中は、ライブカメラプレビューが表示されます。
- 撮影を終了したい場合は「Stop Capture」をクリックします。

### 3. GIFアニメーションを作成
- 撮影終了後、「Create GIF from Images」ボタンをクリックしてGIFを生成します。
- 作成されたGIFはダウンロードフォルダに保存されます。
- GIFが成功すると「Download GIF」ボタンでダウンロードが可能です。

---

## 💻 ローカルでの実行方法（仮想環境を使用）
ローカルでの開発環境を汚染しないよう、仮想環境を使用することを推奨します。仮想環境を使うと、必要なライブラリをプロジェクトごとに分離して管理でき、異なるプロジェクトでのバージョン競合を回避できます。

### 1. 仮想環境を作成する
`main.py`を保存するフォルダに移動して、以下のコマンドを実行します。これにより、新しい仮想環境が作成されます。
```bash
python -m venv venv
```

### 2. 仮想環境を有効化する
仮想環境を有効にするには、以下のコマンドを実行します。

#### Windowsの場合:
```bash
venv\Scripts\activate
```
仮想環境が有効になると、コマンドラインの先頭に'(venv)'と表示されます。

### 3. 必要なライブラリをインストールする
仮想環境内で以下のコマンドを実行し、必要なライブラリをインストールします。
```bash
pip install -r requirements.txt
```

### 4. アプリを起動する
仮想環境を有効にした状態で、以下のコマンドを実行してアプリを起動します。
```bash
streamlit run main.py
```
上で実行できない場合は
```bash
python -m streamlit run main.py
```
コマンドプロンプトに表示されるURLをクリックするか、ブラウザにコピーして貼り付けると、アプリを利用できます。

### 5. アプリを終了する
サーバーを終了する場合は、'Ctrl+Cキー'を押下してください
※streamlitコマンドを実行すると、ポート番号8501でWebサーバが起動します。 ブラウザを終了してもサーバは停止しません。

### 6. 仮想環境の終了
作業が完了したら、仮想環境を終了するために以下のコマンドを実行します。
```bash
deactivate
```

## 🛠️ 主な関数の説明
#### `recv(frame)`
WebRTCのビデオフレームを受信し、一定の間隔で画像を保存する処理を行います。
#### `make_archive()`
保存された画像をzip形式でアーカイブする関数です。
#### `generate_gif()`
キャプチャされた画像からGIFアニメーションを作成するための関数です。

## 📦 ファイル構成
- キャプチャ間隔は1秒から3600秒までの間で設定可能です。
- GIF作成時の画像サイズは、最初のキャプチャ画像に基づいて調整されます。
- すべてのキャプチャ画像は、実行ディレクトリのtimelapse_images/フォルダに保存されます。

## 🌟 注意事項
- 保存される画像はスクリプト実行フォルダ内の指定フォルダに格納されます。
- 撮影中にエラーが発生した場合は、カメラ設定やフォルダの書き込み権限を確認してください。
- GIF作成時にはフォルダ内の画像を昇順に並べます。ファイル名形式に基づいて処理されるため、他のファイルが混ざらないよう注意してください。

## 📜 ライセンス
このプロジェクトのライセンスはMITライセンスです、詳細は`LICENSE.txt`をご覧ください。
