import os
import time
from datetime import datetime
import cv2
from PIL import Image
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av  # avライブラリのインポート（StreamlitでWebRTCのフレームを処理するために必要）

# タイムラプス保存用ディレクトリ
SAVE_DIR = "timelapse_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# WebRTC用のビデオプロセッサ
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.capture_interval = 5  # 撮影間隔（秒）
        self.last_captured_time = None  # 最初はNoneにして0秒時点で保存
        self.start_time = time.time()  # 撮影開始時刻

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        current_time = time.time()  # 現在の時刻

        # 最初の撮影（0秒）または間隔経過で撮影
        if self.last_captured_time is None or current_time - self.last_captured_time >= self.capture_interval:
            # 撮影時点の経過時間を取得
            elapsed_time = int(current_time - self.start_time)

            # 最初の撮影時に負の時間を回避（0秒固定）
            if self.last_captured_time is None:
                elapsed_time = 0

            name = st.session_state.get('name', 'name')  # プレフィックス取得
            filename = os.path.join(SAVE_DIR, f"{name}_{elapsed_time}-sec.jpg")
            cv2.imwrite(filename, img)  # 画像保存

            # 最後にキャプチャした時間を更新
            self.last_captured_time = current_time

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Streamlitアプリ
st.title("タイムラプスカメラアプリ（クラウド対応）")
st.sidebar.header("設定")

# 撮影間隔の設定
capture_interval = st.sidebar.number_input("撮影間隔（秒）", min_value=1, max_value=3600, value=5)

# ユーザーが画像のプレフィックスを設定できるように、サイドバーに追加
name = st.sidebar.text_input("画像のプレフィックスを設定", "name")
st.session_state['name'] = name  # プレフィックスをセッションに保存

# WebRTCストリームの設定（STUNサーバーを設定）
rtc_configuration = {
    "iceServers": [
        {"urls": ["stun:stun1.l.google.com:19302"]},  # 代わりのGoogle STUNサーバー
        {"urls": ["stun:stun2.l.google.com:19302"]},  # 別のGoogle STUNサーバー
        {"urls": ["stun:stun3.l.google.com:19302"]},  # 追加のSTUNサーバー
    ]
}

# WebRTCストリームの開始
ctx = webrtc_streamer(
    key="timelapse",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={
        "video": {"width": 1920, "height": 1080},
        "audio": False
    },
)

# VideoProcessorに撮影間隔を適用
if ctx and ctx.video_processor:
    ctx.video_processor.capture_interval = capture_interval

# 保存した画像をダウンロード可能にする
if st.button("保存した画像zipをダウンロード"):
    zip_filename = "timelapse_images.zip"
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    import shutil
    shutil.make_archive("timelapse_images", "zip", SAVE_DIR)
    with open(f"{zip_filename}", "rb") as file:
        btn = st.download_button(
            label="タイムラプス画像zipをダウンロード",
            data=file,
            file_name=zip_filename,
            mime="application/zip"
        )

# GIFアニメーションを作成してダウンロードする機能
if st.button("GIFアニメーションを作成してダウンロード"):
    image_files = [os.path.join(SAVE_DIR, f) for f in os.listdir(SAVE_DIR) if f.endswith(".jpg")]
    images = []
    
    # 最初の画像のサイズを基準にする
    base_img = Image.open(image_files[0])
    base_size = base_img.size  # 基準となるサイズを取得
    
    for image_file in sorted(image_files):  # 画像を名前順にソート
        img = Image.open(image_file)
        
        # すべての画像を基準サイズにリサイズ
        img_resized = img.resize(base_size)
        images.append(img_resized)

    gif_filename = "timelapse_animation.gif"
    images[0].save(gif_filename, save_all=True, append_images=images[1:], loop=0, duration=500)
    
    with open(gif_filename, "rb") as gif_file:
        st.download_button(
            label="GIFアニメーションをダウンロード",
            data=gif_file,
            file_name=gif_filename,
            mime="image/gif"
        )
