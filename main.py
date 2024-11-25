import os
import cv2
import av
import time
from datetime import datetime
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
from av import VideoFrame

# タイムラプス保存用ディレクトリ
SAVE_DIR = "timelapse_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# WebRTC用のビデオプロセッサ
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.capture_interval = 5  # デフォルトの撮影間隔
        self.last_captured_time = time.time()  # 最後にキャプチャした時間

    def recv(self, frame):
        # フレームを取得
        img = frame.to_ndarray(format="bgr24")

        # タイムラプス画像の保存処理
        current_time = time.time()
        if current_time - self.last_captured_time >= self.capture_interval:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(SAVE_DIR, f"frame_{timestamp}.jpg")
            cv2.imwrite(filename, img)
            self.last_captured_time = current_time

        # 表示用の映像を返す（そのまま）
        return VideoFrame.from_ndarray(img, format="bgr24")

# Streamlitアプリ
st.title("タイムラプスカメラアプリ")
st.sidebar.header("設定")

# ユーザー設定
capture_interval = st.sidebar.number_input("撮影間隔 (秒)", min_value=1, max_value=3600, value=5, step=1)

# 利用可能なカメラデバイスを表示
import cv2
def get_video_devices():
    index = 0
    devices = []
    while True:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            devices.append(index)
            cap.release()
        else:
            break
        index += 1
    return devices

# 利用可能なカメラデバイスのリストを取得
devices = get_video_devices()

# カメラが接続されているか確認
if len(devices) == 0:
    st.error("カメラが接続されていません。")
else:
    # 使用するカメラデバイスのインデックスを選択
    device_index = st.sidebar.selectbox("使用するカメラを選択", devices, index=0)
    st.sidebar.write(f"選択されたカメラ: {device_index}")

    # WebRTCストリームの設定
    media_stream_constraints = {
        "video": {"device": device_index, "width": 640, "height": 480},
        "audio": False
    }

    # WebRTCストリーム開始
    ctx = webrtc_streamer(
        key="example",
        video_processor_factory=VideoProcessor,
        media_stream_constraints=media_stream_constraints,
        mode=WebRtcMode.SENDRECV,
    )

    # WebRTC ストリームが開始されているか確認
    if ctx and ctx.state.playing:
        st.success("カメラが正常に接続され、映像が表示されています。")
    else:
        st.error("カメラが接続されていないか、アクセスできません。カメラの設定を確認してください。")

    # VideoProcessorに撮影間隔を反映
    if ctx and ctx.video_processor:
        ctx.video_processor.capture_interval = capture_interval

    # タイムラプス動画の生成ボタン
    if st.button("タイムラプス動画を生成"):
        st.info("タイムラプス動画を生成中...")

        # 保存された画像から動画を生成
        images = sorted(
            [img for img in os.listdir(SAVE_DIR) if img.endswith(".jpg")]
        )
        if not images:
            st.error("保存された画像がありません。")
        else:
            # 動画生成処理
            first_image = cv2.imread(os.path.join(SAVE_DIR, images[0]))
            height, width, _ = first_image.shape
            output_video = os.path.join(SAVE_DIR, "timelapse.mp4")
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video = cv2.VideoWriter(output_video, fourcc, 10, (width, height))

            for image_file in images:
                frame = cv2.imread(os.path.join(SAVE_DIR, image_file))
                video.write(frame)
            video.release()

            st.success(f"タイムラプス動画を生成しました: {output_video}")

            # 動画を表示
            st.video(output_video)

            # ダウンロードボタンを作成
            with open(output_video, "rb") as file:
                btn = st.download_button(
                    label="タイムラプス動画をダウンロード",
                    data=file,
                    file_name="timelapse.mp4",
                    mime="video/mp4",
                )

    # 画像をダウンロードできるようにする
    st.subheader("保存されたタイムラプス画像")
    image_files = sorted(
        [img for img in os.listdir(SAVE_DIR) if img.endswith(".jpg")]
    )

    if image_files:
        for image_file in image_files:
            image_path = os.path.join(SAVE_DIR, image_file)
            with open(image_path, "rb") as img_file:
                st.download_button(
                    label=f"{image_file} をダウンロード",
                    data=img_file,
                    file_name=image_file,
                    mime="image/jpeg",
                )
    else:
        st.warning("タイムラプス画像が保存されていません。")
