"""
This script is recommended for use when main.py is difficult to work with.
This version focuses on reducing module dependencies and ensuring that the capture functionality runs smoothly.
Select camera_list = [0] to use the inner camera supplied with the PC, or camera_list = [1] to use the USB camera.
Improvements from main2.py:
(1) To reduce the time lag at the start of shooting, camera warm-up, more efficient time measurement and frame acquisition were implemented.
(ii) Folder names were changed to those based on the file name prefix set by the user.
(iii) The data storage destination was changed to the user's desktop.
"""

import streamlit as st
import cv2
import os
import time

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

# Create a folder on the Desktop named after the file name prefix
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_folder = os.path.join(desktop_path, file_name_prefix)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize OpenCV webcam
cap = cv2.VideoCapture(camera_index)

# Check if the camera is opened correctly
if not cap.isOpened():
    st.error("Error: Could not access the camera.")

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
        if not ret:
            st.error("Error: Failed to capture image.")
            break

        # Show the live camera feed
        st.image(frame, channels="BGR")

        # Capture image at specified intervals
        if current_time >= next_capture_time:
            elapsed_time = int(current_time - start_time)  # Calculate elapsed time in seconds
            file_name = f"{file_name_prefix}-{elapsed_time:03d}-sec.jpg"
            img_filename = os.path.join(output_folder, file_name)
            cv2.imwrite(img_filename, frame)
            st.write(f"Captured {img_filename}")
            next_capture_time += capture_interval

        if stop_button:
            st.write("Capture stopped.")
            break

    cap.release()

elif stop_button:
    st.write("Capture not started yet.")

st.write("Time-lapse capture complete.")