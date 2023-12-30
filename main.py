import pyautogui
import mediapipe as mp
import cv2, math, random

# Get the current position of the mouse
current_x, current_y = pyautogui.position()

# Move the mouse to a new position
# new_x, new_y = 400, 400


cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

top_left = (20,20)
bottom_right = (220,220)


def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = cv2.flip(imgRGB, 1)
    results = hands.process(imgRGB)

    img = cv2.resize(img, (0,0), fx=1, fy=1)
    img = cv2.flip(img, 1)

    if results.multi_hand_landmarks:
        for handLM in results.multi_hand_landmarks:
            index_fingure = None
            middle_fingure = None
            thump_fingure = None
            for id,lm in enumerate(handLM.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 4:
                    thump_fingure = (cx,cy)
                    cv2.circle(center=(cx,cy), img=img, color=(0,0,255), radius=20, thickness=-1)
                if id == 8:
                    index_fingure = (cx,cy)
                    cv2.circle(center=(cx,cy), img=img, color=(0,0,255), radius=20, thickness=-1)
                    pyautogui.moveTo(index_fingure[0]*4, index_fingure[1]*4,0.1)
                if id==12:
                    middle_fingure = (cx,cy)
                    cv2.circle(center=(cx,cy), img=img, color=(0,0,255), radius=20, thickness=-1)
                if thump_fingure and middle_fingure:
                    res2 = calculate_distance(thump_fingure[0],thump_fingure[1],middle_fingure[0],middle_fingure[1])
                    if res2<60:
                        pyautogui.click()
                        
            mp_draw.draw_landmarks(img, handLM, mp_hands.HAND_CONNECTIONS)
            
    

    cv2.imshow("frame", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break