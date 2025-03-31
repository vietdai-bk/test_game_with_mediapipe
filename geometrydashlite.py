import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def is_hand_open(landmarks):
    finger_tips = [8, 12, 16, 20]
    open_count = 0
    for tip in finger_tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            open_count += 1
    return open_count >= 3

time.sleep(3)

last_jump_time = 0
jump_cooldown = 0.1

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    current_time = time.time()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            if is_hand_open(hand_landmarks.landmark) and (current_time - last_jump_time >= jump_cooldown):
                pyautogui.press('space')
                cv2.putText(frame, "Jump", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                last_jump_time = current_time
            else:
                cv2.putText(frame, "Ready", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    else:
        cv2.putText(frame, "No Hand - Ready", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Geometry Dash Controller', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
