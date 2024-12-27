"""
This script is recommended for use when main.py is difficult to work with.
This version focuses on reducing module dependencies and ensuring that the capture functionality runs smoothly.
Select camera_list = [0] to use the inner camera supplied with the PC, or camera_list = [1] to use the USB camera.
"""

import streamlit as st
import cv2
import os
import time

# Create the timelapse_images folder if it doesn't exist
if not os.path.exists("timelapse_images"):
    os.makedirs("timelapse_images")

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

    # Start time-lapse capture
    start_time = time.time()
    frame_count = 0

    while time.time() - start_time < duration * 60:
        ret, frame = cap.read()
        if not ret:
            st.error("Error: Failed to capture image.")
            break

        # Show the live camera feed
        st.image(frame, channels="BGR")

        # Capture image at specified intervals
        if frame_count % capture_interval == 0:
            elapsed_time = int(time.time() - start_time)  # Calculate elapsed time in seconds
            file_name = f"{file_name_prefix}-{elapsed_time:03d}-sec.jpg"
            img_filename = os.path.join("timelapse_images", file_name)
            cv2.imwrite(img_filename, frame)
            st.write(f"Captured {img_filename}")

        frame_count += 1
        time.sleep(1)  # Simulate frame rate

        if stop_button:
            st.write("Capture stopped.")
            break

    cap.release()

elif stop_button:
    st.write("Capture not started yet.")

st.write("Time-lapse capture complete.")
