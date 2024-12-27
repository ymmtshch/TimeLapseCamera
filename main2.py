# デスクトップローカルでのタイムラプスカメラ撮影スクリプト
import cv2
import os
import time

# カメラ設定
camera_list = [0, 1, 2, 3]  # 使用可能なカメラのインデックスをリストアップ
print("使用するカメラを選択してください:")
for i, cam in enumerate(camera_list):
    print(f"{i}: Camera {cam}")
camera_index = int(input("カメラ番号を入力: "))

if camera_index not in camera_list:
    print("無効なカメラ番号です。終了します。")
    exit()

# ユーザー定義のファイル名プレフィックス
file_name_prefix = input("ファイル名プレフィックスを入力してください (例: 'timelapse'): ")
if not file_name_prefix:
    file_name_prefix = "timelapse"

# 撮影間隔と撮影時間を設定
capture_interval = int(input("撮影間隔を秒単位で入力してください (例: 10): "))
duration = int(input("撮影時間を分単位で入力してください (例: 5): "))

# デスクトップ上にフォルダを作成
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_folder = os.path.join(desktop_path, file_name_prefix)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# OpenCVでカメラを初期化
cap = cv2.VideoCapture(camera_index)

# カメラが正しくオープンできたか確認
if not cap.isOpened():
    print("エラー: カメラにアクセスできませんでした。")
    exit()

print("カメラ準備中...")

# カメラをウォームアップ
for _ in range(10):
    cap.read()

print("撮影を開始します...")

# タイムラプス撮影を開始
start_time = time.time()
next_capture_time = start_time

try:
    while time.time() - start_time < duration * 60:
        current_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print("エラー: 画像を取得できませんでした。")
            break

        # 指定された間隔で画像をキャプチャ
        if current_time >= next_capture_time:
            elapsed_time = int(current_time - start_time)  # 経過時間を秒単位で計算
            file_name = f"{file_name_prefix}-{elapsed_time:04d}-sec.jpg"
            img_filename = os.path.join(output_folder, file_name)
            cv2.imwrite(img_filename, frame)
            print(f"画像を保存しました: {img_filename}")
            next_capture_time += capture_interval

except KeyboardInterrupt:
    print("撮影を中断しました。")

finally:
    cap.release()
    print("撮影を終了しました。")