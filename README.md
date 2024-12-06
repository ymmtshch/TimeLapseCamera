![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Streamlit](https://img.shields.io/badge/streamlit-%E2%AC%9B-orange)
![dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen)
![WebRTC](https://img.shields.io/badge/WebRTC-enabled-brightgreen)
![GitHub Stars](https://img.shields.io/github/stars/ymmtshch/TimeLapseCamera?style=social)
![Last Commit](https://img.shields.io/github/last-commit/ymmtshch/TimeLapseCamera)
![GitHub Issues](https://img.shields.io/github/issues/ymmtshch/TimeLapseCamera)
![GitHub Forks](https://img.shields.io/github/forks/ymmtshch/TimeLapseCamera?style=social)

# 📷 タイムラプスカメラアプリ

このアプリは、WebRTCとStreamlitを使用してタイムラプス動画の作成を行うインタラクティブなツールです。
一定の間隔で画像をキャプチャし、保存した画像をzip形式またはGIFアニメーションとしてダウンロードできます。

## 📄 概要

本アプリケーションの主な機能：
- WebRTCを用いたリアルタイムビデオストリーム
- ユーザーが指定した撮影間隔での自動キャプチャ
- ~~画像のプレフィックス設定機能（名前を自由に設定可能）~~　名前は`name_●●-sec`で、●●に経過時間が入るよ
- 保存した画像のzip形式での一括ダウンロード
- 撮影した画像をGIFアニメーションに変換してダウンロード

---

## 🚀 アプリの使用方法

### 1. 撮影間隔の設定
サイドバーから撮影間隔（秒単位）を設定し、画像ファイル名のプレフィックスも入力してください。

### 2. WebRTCストリームの開始
アプリケーションの中心にあるボタンを押してWebRTCストリームを開始します。

### 3. 画像の保存とダウンロード
キャプチャされた画像は自動的に保存されます。ストリーム終了後、以下のダウンロードオプションを利用できます：
- **zip形式でダウンロード**: すべての画像をまとめて一括ダウンロード。
- **GIFアニメーションでダウンロード**: すべてのキャプチャ画像をGIFに変換し、アニメーションとしてダウンロード。

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
※`Failed building wheel for av`の場合は、下記も試してみてください。
#### Windowsの場合:
```bash
pip install av
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
- キャプチャ間隔は1秒から3600秒までの間で設定可能です。
- GIF作成時の画像サイズは、最初のキャプチャ画像に基づいて調整されます。
- すべてのキャプチャ画像は、実行ディレクトリのtimelapse_images/フォルダに保存されます。
- ファイル名の`name_●●-sec.jpg`を一括で変更したい場合は、ローカルに落とした後に`PowerShell`を使う方法があります。
#### ファイル名を自力で変更する方法
1. 名前を変更するファイルが格納されたフォルダを開く。
2. Shiftキーを押しながら右クリック→「PowerShellウィンドウをここで開く」を選択する。
3. コードをコピーし、PowerShellウィンドウ上にて右クリックでペーストする。
4. Enterキーを押してコードを実行する。
```bash
Get-ChildItem -Filter "name_*-sec.jpg" | 
ForEach-Object {
    $newName = $_.Name -replace "^name_", "SampleName_"
    Rename-Item $_.FullName $newName
}
```
※"SampleName_"を変更したい名前に代えて使用してください。

## 📜 ライセンス
このプロジェクトのライセンスはMITライセンスです、詳細は`LICENSE.txt`をご覧ください。
