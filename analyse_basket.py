import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

def analyse_match(video_path):

    # Charger YOLOv8 (modèle pré-entraîné)
    model = YOLO("yolov8n.pt")

    # Tracker DeepSORT
    tracker = DeepSort(max_age=30)

    cap = cv2.VideoCapture(video_path)

    shots_positions = []
    events = []

    frame_id = 0
    last_ball_y = None
    shot_detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_id += 1
        h, w = frame.shape[:2]

        # Détection YOLO
        results = model(frame, verbose=False)[0]

        detections = []
        ball_pos = None

        for box in results.boxes:
            cls = int(box.cls[0])
            x1, y1, x2, y2 = box.xyxy[0]

            # Classe 0 = personne (joueur)
            if cls == 0:
                detections.append(([x1, y1, x2 - x1, y2 - y1], 0.9, "player"))

            # Classe 32 = ballon (selon COCO)
            if cls == 32:
                ball_pos = ((x1 + x2) / 2, (y1 + y2) / 2)

        # Tracking joueurs
        tracker.update_tracks(detections, frame=frame)

        # Détection tir simple (ballon monte puis descend)
        if ball_pos:
            if last_ball_y is not None:
                if ball_pos[1] < last_ball_y:  # ballon monte
                    shot_detected = True
                if shot_detected and ball_pos[1] > last_ball_y:  # ballon redescend
                    events.append({
                        "time": frame_id / 25,
                        "type": "shot_attempt",
                        "player": 0
                    })
                    shots_positions.append({
                        "x": ball_pos[0] / w,
                        "y": ball_pos[1] / h
                    })
                    shot_detected = False

            last_ball_y = ball_pos[1]

    cap.release()

    # Stats simples
    stats = {
        "shots": len(shots_positions),
        "passes": 0,
        "steals": 0,
        "possession": 50,
        "shots_positions": shots_positions,
        "events": events
    }

    return stats
