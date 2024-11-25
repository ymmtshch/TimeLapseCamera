import os
import cv2
import time
import numpy as np
from datetime import datetime
import streamlit as st

# タイムラプス保存ディレクトリ
SAVE_DIR = "timelapse_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Streamlitアプリ
st.title("タイムラプスカメラアプリ")
st.sidebar.header("設定")

# ユーザー設定
capture_interval = st.sidebar.number_input("撮影間隔 (秒)", min_value=1, max_value=3600, value=5, step=1)
video_duration = st.sidebar.number_input("タイムラプスの長さ (秒)", min_value=1, max_value=3600, value=10, step=1)
fps = st.sidebar.number_input("タイムラプスFPS", min_value=1, max_value=60, value=10, step=1)

# Webカメラの初期化
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    st.error("カメラが接続されていません。Logicool C270が正しく接続されていることを確認してください。")
else:
    st.success("カメラが正常に動作しています。")

# 撮影の開始
if st.button("撮影開始"):
    st.write("タイムラプス撮影を開始します...")
    st.info(f"撮影間隔: {capture_interval}秒, 撮影時間: {video_duration}秒")
    
    image_count = 0
    start_time = time.time()
    captured_images = []

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # 指定の撮影間隔で画像をキャプチャ
        if elapsed_time > image_count * capture_interval:
            ret, frame = camera.read()
            if ret:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(SAVE_DIR, f"frame_{timestamp}.jpg")
                cv2.imwrite(filename, frame)
                captured_images.append(filename)
                st.write(f"画像を保存しました: {filename}")
                image_count += 1
            else:
                st.error("画像の取得に失敗しました。")

        # 撮影時間を超えたら終了
        if elapsed_time > video_duration:
            st.success("撮影が完了しました。タイムラプスを生成中...")
            break

    # カメラ解放
    camera.release()

    # タイムラプス動画を生成
    if captured_images:
        output_video = os.path.join(SAVE_DIR, "timelapse.mp4")
        height, width, _ = cv2.imread(captured_images[0]).shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

        for image_file in captured_images:
            frame = cv2.imread(image_file)
            video.write(frame)

        video.release()
        st.success(f"タイムラプス動画を生成しました: {output_video}")
        st.video(output_video)
    else:
        st.error("画像が1枚も保存されませんでした。")

# カメラ解放 (アプリ終了時)
st.sidebar.button("終了", on_click=camera.release)
