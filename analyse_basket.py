import random
import cv2

def analyse_match(video_path):
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

    cap.release()

    shots = random.randint(20, 40)
    passes = random.randint(80, 150)
    steals = random.randint(5, 15)
    possession = random.randint(40, 60)

    shots_positions = [
        {"x": random.random(), "y": random.random()}
        for _ in range(shots)
    ]

    events = []
    for _ in range(10):
        events.append({
            "time": random.randint(0, 2400),
            "type": random.choice(["shot_made", "shot_missed", "steal", "assist"]),
            "player": random.randint(1, 12)
        })

    return {
        "shots": shots,
        "passes": passes,
        "steals": steals,
        "possession": possession,
        "shots_positions": shots_positions,
        "events": events
    }
