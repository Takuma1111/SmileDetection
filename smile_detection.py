# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import numpy as np
import time
import os

# Mediapipe初期化
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

# 保存ディレクトリを作成
output_dir = "captured_smiles"
os.makedirs(output_dir, exist_ok=True)

# 笑顔度を計算する関数
def calculate_smile_ratio(landmarks, img_width, img_height):
    left_mouth = landmarks[61]  # 左口角
    right_mouth = landmarks[291]  # 右口角
    upper_lip = landmarks[13]  # 上唇
    lower_lip = landmarks[14]  # 下唇

    left_mouth = np.array([left_mouth.x * img_width, left_mouth.y * img_height])
    right_mouth = np.array([right_mouth.x * img_width, right_mouth.y * img_height])
    upper_lip = np.array([upper_lip.x * img_width, upper_lip.y * img_height])
    lower_lip = np.array([lower_lip.x * img_width, lower_lip.y * img_height])

    mouth_width = np.linalg.norm(right_mouth - left_mouth)
    mouth_height = np.linalg.norm(upper_lip - lower_lip)

    smile_ratio = mouth_height / mouth_width
    return smile_ratio

# カメラ起動
cap = cv2.VideoCapture(0)

# 笑顔の閾値と連続撮影防止のタイマー
SMILE_THRESHOLD = 0.2  # 笑顔度の閾値
last_captured_time = 0  # 最後に写真を撮影した時間
CAPTURE_INTERVAL = 2  # 写真撮影間隔（秒）

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    img_height, img_width, _ = frame.shape

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            smile_ratio = calculate_smile_ratio(face_landmarks.landmark, img_width, img_height)

            # 笑顔度を画面に表示
            cv2.putText(
                frame,
                f"Smile Ratio: {smile_ratio:.2f}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0) if smile_ratio > SMILE_THRESHOLD else (0, 0, 255),
                2
            )

            # 笑顔度が閾値を超えた場合に写真を撮影
            if smile_ratio > SMILE_THRESHOLD:
                current_time = time.time()
                if current_time - last_captured_time > CAPTURE_INTERVAL:
                    # 写真を保存
                    timestamp = int(current_time)
                    filename = os.path.join(output_dir, f"smile_{timestamp}.jpg")
                    cv2.imwrite(filename, frame)
                    print(f"Photo saved: {filename}")
                    last_captured_time = current_time

            # 顔特徴点の描画
            mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_LIPS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
            )

    cv2.imshow('Smile Detection', frame)

    if cv2.waitKey(1) == 27:  # ESCキーで終了
        break

cap.release()
cv2.destroyAllWindows()
