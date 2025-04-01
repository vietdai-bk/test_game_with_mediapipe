import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

with mp_hands.Hands(min_detection_confidence=0.5, max_num_hands=2, min_tracking_confidence=0.5) as hands:

    while True:
        ret, frame = cap.read()
        frame.flags.writeable = False
        if not ret:
            break
        results = hands.process(frame)
        frame.flags.writeable = True
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i, landmark in enumerate(hand_landmarks.landmark):
                    h, w, _ = frame.shape
                    x, y = int(landmark.x * w), int(landmark.y * h) ## Tọa độ từng đốt ngón tay
                    cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                mp_draw.draw_landmarks(frame, hand_landmarks)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()