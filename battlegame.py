import cv2
import mediapipe as mp
import pyautogui
import math
import webbrowser

url = "https://poki.com/en/g/12-minibattles"
webbrowser.open(url)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

key_A_pressed = False
key_L_pressed = False

DISTANCE_THRESHOLD = 0.05
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            distance = calculate_distance(thumb_tip, index_tip)

            if idx == 0:
                if distance < DISTANCE_THRESHOLD:
                    if not key_A_pressed:
                        pyautogui.keyDown('a')
                        key_A_pressed = True
                else:
                    if key_A_pressed:
                        pyautogui.keyUp('a')
                        key_A_pressed = False

            elif idx == 1:
                if distance < DISTANCE_THRESHOLD:
                    if not key_L_pressed:
                        pyautogui.keyDown('l')
                        key_L_pressed = True
                else:
                    if key_L_pressed:
                        pyautogui.keyUp('l')
                        key_L_pressed = False
                        
    frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
    window_name = 'Game Control'
    cv2.imshow('Game Control', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break
cap.release()
cv2.destroyAllWindows()
hands.close()