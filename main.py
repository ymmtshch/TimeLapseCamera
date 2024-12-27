"""
This script is recommended for use if you want to create a GIF animation after the capture by adding it to the main3.py process.
Selecting camera_list = [0] uses the internal camera supplied with the PC, selecting camera_list = [1] uses the USB camera.
Changes since main3.py.
(i) After taking a time-lapse video, a GIF animation is automatically generated using the images in the specified folder.
"""

import streamlit as st
import cv2
import os
import time
from PIL import Image, ImageFile
import re

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Function to extract the number from a filename for sorting
def extract_number_from_filename(filename):
    match = re.search(r'_(\d+)-sec', filename)
    return int(match.group(1)) if match else float('inf')

# Function to create GIF animation
def create_gif(input_folder, output_gif, duration=500):
    images = []
    size = (1920, 1080)  # Fixed resolution

    sorted_files = sorted(os.listdir(input_folder), key=extract_number_from_filename)

    for file_name in sorted_files:
        if file_name.lower().endswith(('png', 'jpg', 'jpeg', 'bmp')):
            file_path = os.path.join(input_folder, file_name)
            try:
                img = Image.open(file_path)
                img.load()
                img = img.convert("RGBA")
                img = img.resize(size, Image.LANCZOS)
                images.append(img)
            except OSError as e:
                st.warning(f"Invalid or corrupted image skipped: {file_name}")

    if not images:
        st.error("No valid images found in the folder.")
        return None

    images[0].save(
        output_gif,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,
        optimize=True,
        colors=256
    )
    return output_gif

# Streamlit camera input
st.title("Time-Lapse Camera and GIF Creator")
st.sidebar.header("Settings")

# Camera selection
camera_list = [0, 1]  # Add the number of USB cameras you want to select
camera_index = st.sidebar.selectbox("Select Camera", camera_list)

# User-defined file name (used for both folder and file naming)
file_name_prefix = st.sidebar.text_input("Enter file name prefix (e.g., 'timelapse')", "timelapse")

# Camera settings
capture_interval = st.sidebar.slider("Capture Interval (seconds)", 1, 60, 10)
duration = st.sidebar.slider("Duration (minutes)", 1, 90, 5)

# Set output directory relative to the script's location
output_folder = os.path.join(os.getcwd(), file_name_prefix)
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
            file_name = f"{file_name_prefix}-{elapsed_time:04d}-sec.jpg"  # 4桁にゼロパディング
            img_filename = os.path.join(output_folder, file_name)

            # Attempt to write the image
            success = cv2.imwrite(img_filename, frame)
            st.write(f"Trying to save: {img_filename}")  # Log file path
            if success:
                st.write(f"Captured {img_filename}")
            else:
                st.error(f"Error: Failed to write image to {img_filename}.")

            next_capture_time += capture_interval

        if stop_button:
            st.write("Capture stopped.")
            break

    cap.release()

elif stop_button:
    st.write("Capture not started yet.")

# GIF creation
gif_button = st.button("Create GIF from Images")
if gif_button:
    # Set the download folder path for the GIF
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    gif_output_path = os.path.join(download_folder, f"{file_name_prefix}.gif")
    
    gif_result = create_gif(output_folder, gif_output_path, duration=500)
    if gif_result:
        st.success(f"GIF created successfully: {gif_result}")
        with open(gif_result, "rb") as gif_file:
            st.download_button(
                label="Download GIF",
                data=gif_file,
                file_name=f"{file_name_prefix}.gif",
                mime="image/gif"
            )
