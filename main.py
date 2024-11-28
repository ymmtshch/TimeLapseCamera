import av
import cv2
import os
import time
from datetime import datetime
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

# タイムラプス保存用ディレクトリ
SAVE_DIR = "timelapse_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# WebRTC用のビデオプロセッサ
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.capture_interval = 5  # 撮影間隔（秒）
        self.last_captured_time = time.time()  # 最後にキャプチャした時間

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # 撮影間隔ごとに画像を保存
        current_time = time.time()
        if current_time - self.last_captured_time >= self.capture_interval:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(SAVE_DIR, f"frame_{timestamp}.jpg")
            cv2.imwrite(filename, img)
            self.last_captured_time = current_time

        # 表示用の映像を返す
        return av.VideoFrame.from_ndarray(img, format="bgr24")


# Streamlitアプリ
st.title("タイムラプスカメラアプリ（クラウド対応）")
st.sidebar.header("設定")

# 撮影間隔の設定
capture_interval = st.sidebar.number_input("撮影間隔（秒）", min_value=1, max_value=3600, value=5)

# WebRTCストリームの設定（STUNサーバーを設定）#追加
rtc_configuration = {
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},  # Google STUNサーバー
        {"urls": ["stun:stun1.l.google.com:19302"]}, # 追加のGoogle STUNサーバー
        {"urls": ["stun:stun2.l.google.com:19302"]}  # 追加のGoogle STUNサーバー
    ]
}

# WebRTCストリームの開始
ctx = webrtc_streamer(
    key="timelapse",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
)

# VideoProcessorに撮影間隔を適用
if ctx and ctx.video_processor:
    ctx.video_processor.capture_interval = capture_interval

# 保存した画像をダウンロード可能にする
if st.button("保存した画像をダウンロード"):
    zip_filename = "timelapse_images.zip"
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    import shutil
    shutil.make_archive("timelapse_images", "zip", SAVE_DIR)
    with open(f"{zip_filename}", "rb") as file:
        btn = st.download_button(
            label="タイムラプス画像をダウンロード",
            data=file,
            file_name=zip_filename,
            mime="application/zip"
        )
