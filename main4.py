import streamlit as st
import cv2
import os
import time
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def extract_number_from_filename(filename):
    # ファイル名から最後の数字を抽出する関数
    import re
    match = re.search(r'_(\d+)-sec', filename)
    return int(match.group(1)) if match else float('inf')

def create_gif(input_folder, output_gif, duration=500):
    """
    指定したフォルダ内の画像を使ってGIFを生成する。
    """
    images = []
    size = (1920, 1080)  # 解像度を固定

    # ファイルを抽出し、名前に基づいてソート
    sorted_files = sorted(os.listdir(input_folder), key=extract_number_from_filename)

    for file_name in sorted_files:
        if file_name.lower().endswith(('png', 'jpg', 'jpeg', 'bmp')):
            file_path = os.path.join(input_folder, file_name)
            try:
                img = Image.open(file_path)
                img = img.convert("RGBA").resize(size, Image.LANCZOS)
                images.append(img)
            except OSError as e:
                print(f"破損または無効な画像: {file_name} - {e}")

    if images:
        images[0].save(
            output_gif,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=0,
            optimize=True,
            colors=256
        )
        print(f"GIFが作成されました: {output_gif}")
    else:
        print("有効な画像が見つかりませんでした。")

# Streamlit camera input
st.title("Time-Lapse Camera")
st.sidebar.header("Settings")

# Camera selection
camera_list = [0, 1, 2, 3]  # Add the number of USB cameras you want to select
camera_index = st.sidebar.selectbox("Select Camera", camera_list)

# User-defined file name
file_name_prefix = st.sidebar.text_input("Enter file name prefix (e.g., 'timelapse')", "timelapse")

# Camera settings
capture_interval = st.sidebar.slider("Capture Interval (seconds)", 1, 60, 10)
duration = st.sidebar.slider("Duration (minutes)", 1, 90, 5)

# Set Desktop directory for saving files
desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
output_folder = os.path.join(desktop_path, file_name_prefix)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Confirm write permission
if not os.access(output_folder, os.W_OK):
    st.error(f"Error: No write permission for directory {output_folder}.")
    st.stop()

# Initialize OpenCV webcam
cap = cv2.VideoCapture(camera_index)

# Check if the camera is opened correctly
if not cap.isOpened():
    st.error("Error: Could not access the camera.")
    st.stop()

# Button to start capturing
start_button = st.button("Start Capture")
stop_button = st.button("Stop Capture")

if start_button:
    st.write("Capturing images...")

    # Warm up the camera
    for _ in range(10):
        cap.read()
    
    # Start time-lapse capture
    start_time = time.time()
    next_capture_time = start_time

    while time.time() - start_time < duration * 60:
        current_time = time.time()
        ret, frame = cap.read()
        if not ret or frame is None:
            st.error("Error: Failed to capture valid frame.")
            continue

        # Show the live camera feed
        st.image(frame, channels="BGR")

        # Capture image at specified intervals
        if current_time >= next_capture_time:
            elapsed_time = int(current_time - start_time)  # Calculate elapsed time in seconds
            file_name = f"{file_name_prefix}-{elapsed_time:03d}-sec.jpg"
            img_filename = os.path.join(output_folder, file_name)

            # Attempt to write the image
            success = cv2.imwrite(img_filename, frame)
            st.write(f"Trying to save: {img_filename}")  # Log file path
            if success:
                st.write(f"Captured {img_filename}")
            else:
                st.error(f"Error: Failed to write image to {img_filename}.")
                st.write(f"Output folder: {output_folder}")
                st.write(f"Frame type: {type(frame)} | Frame shape: {frame.shape if frame is not None else 'None'}")

            next_capture_time += capture_interval

        if stop_button:
            st.write("Capture stopped.")
            break

    cap.release()

    # GIF生成処理を呼び出し
    st.write("Generating GIF animation...")
    output_gif = os.path.join(output_folder, "output_animation.gif")
    create_gif(output_folder, output_gif, duration=500)
    st.write(f"GIF animation created: {output_gif}")

elif stop_button:
    st.write("Capture not started yet.")

st.write("Time-lapse capture complete.")
