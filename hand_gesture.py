import cv2
import mediapipe as mp

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
                # Convert normalized coordinates to pixel coordinates
                h, w, _ = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                # Draw the landmark index as text
                cv2.putText(frame, str(idx), (cx + 5, cy + 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

            # Simple gesture classification (example: open vs closed)
            landmarks = hand_landmarks.landmark
            thumb_tip = landmarks[4].y
            index_tip = landmarks[8].y
            if abs(thumb_tip - index_tip) > 0.2:  # Adjust threshold
                gesture = "Open Hand"
            else:
                gesture = "Closed Fist"

    # Overlay gesture text
    cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return frame


def main():
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break

            frame = cv2.flip(frame, 1)
            frame = detect_hand_gesture(frame, hands, mp_hands)
            cv2.imshow("Hand Gesture Recognition (MediaPipe)", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        hands.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()