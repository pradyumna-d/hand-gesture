import cv2
import numpy as np
import mediapipe as mp
import gestures
import base64
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
import asyncio

app = FastAPI()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

def detect_hand_gesture(frame, hands, mp_hands):
    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    gesture = "No Hand Detected"
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Draw landmark indices
            for idx, landmark in enumerate(hand_landmarks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.putText(frame, str(idx), (cx + 5, cy + 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

            # Simple gesture classification
            landmarks = hand_landmarks.landmark
            gesture = gestures.get_gesture(landmarks)

    # Overlay gesture text
    cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return frame

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive frame data from browser (expecting base64-encoded JPEG)
            data = await websocket.receive_text()
            try:
                # Decode base64 frame
                img_data = base64.b64decode(data.split(",")[1] if "," in data else data)
                np_arr = np.frombuffer(img_data, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                if frame is None:
                    continue

                # Process frame for gesture detection
                frame = cv2.flip(frame, 1)  # Flip horizontally for mirror effect (corrected from 2 to 1)
                processed_frame = detect_hand_gesture(frame, hands, mp_hands)

                # Encode processed frame back to base64 JPEG
                _, buffer = cv2.imencode(".jpg", processed_frame)
                encoded_frame = base64.b64encode(buffer).decode("utf-8")
                await websocket.send_text(f"data:image/jpeg;base64,{encoded_frame}")
            except Exception as e:
                print(f"Error processing frame: {e}")
                continue
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        await websocket.close()

async def shutdown():
    hands.close()

@app.on_event("shutdown")
async def on_shutdown():
    await shutdown()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7069)