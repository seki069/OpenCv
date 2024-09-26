import cv2
import mediapipe as mp
import time
import math

# 第1のROI（Region of Interest：関心領域）の座標とサイズ
roi1_x = 100
roi1_y = 100
roi1_width = 400
roi1_height = 400

# 第2のROIの座標とサイズ
roi2_x = 800
roi2_y = 100
roi2_width = 400
roi2_height = 400

# 手指の4つの関節から手指の伸び具合を判断する
def get_angleError(point_4, point_3, point_2, point_1):
    try:
        point_4_cx, point_4_cy = int(point_4.x * w), int(point_4.y * h)
        point_3_cx, point_3_cy = int(point_3.x * w), int(point_3.y * h)
        point_2_cx, point_2_cy = int(point_2.x * w), int(point_2.y * h)
        point_1_cx, point_1_cy = int(point_1.x * w), int(point_1.y * h)

        angle_1 = math.degrees(math.atan((point_3_cx - point_4_cx) / (point_3_cy - point_4_cy)))
        angle_2 = math.degrees(math.atan((point_1_cx - point_2_cx) / (point_1_cy - point_2_cy)))
        angle_error = abs(angle_1 - angle_2)
        if angle_error < 12:
            isStraight = 1
        else:
            isStraight = 0
    except:
        angle_error = 1000
        isStraight = 0

    return angle_error, isStraight


# 5本の手指の伸び具合に基づいて手のジェスチャーを識別する
def getGesture(isStraight_list):
    if isStraight_list[0] == 0 and isStraight_list[1] == 1 and isStraight_list[2] == 0 and isStraight_list[3] == 0 and isStraight_list[4] == 0:
        gesture = "1"
    elif isStraight_list[0] == 0 and isStraight_list[1] == 1 and isStraight_list[2] == 1 and isStraight_list[3] == 0 and isStraight_list[4] == 0:
        gesture = "2"
    elif isStraight_list[0] == 0 and isStraight_list[1] == 0 and isStraight_list[2] == 1 and isStraight_list[3] == 1 and isStraight_list[4] == 1:
        gesture = "3"
    elif isStraight_list[0] == 0 and isStraight_list[1] == 1 and isStraight_list[2] == 1 and isStraight_list[3] == 1 and isStraight_list[4] == 1:
        gesture = "4"
    elif isStraight_list[0] == 1 and isStraight_list[1] == 1 and isStraight_list[2] == 1 and isStraight_list[3] == 1 and isStraight_list[4] == 1:
        gesture = "5"
    else:
        gesture = "None"

    return gesture

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)

mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        # 拇指のジェスチャーを判断
        isStraight_list = []
        point_4 = handLms.landmark[4]
        point_3 = handLms.landmark[3]
        point_2 = handLms.landmark[2]
        point_1 = handLms.landmark[1]
        angle_error_1, isStraight_1 = get_angleError(point_4, point_3, point_2, point_1)
        print("isStraight_1:", isStraight_1)
        isStraight_list.append(isStraight_1)

        # 食指のジェスチャーを判断
        point_4 = handLms.landmark[8]
        point_3 = handLms.landmark[7]
        point_2 = handLms.landmark[6]
        point_1 = handLms.landmark[5]
        angle_error_2, isStraight_2 = get_angleError(point_4, point_3, point_2, point_1)
        print("isStraight_2:", isStraight_2)
        isStraight_list.append(isStraight_2)

        # 中指のジェスチャーを判断
        point_4 = handLms.landmark[12]
        point_3 = handLms.landmark[11]
        point_2 = handLms.landmark[10]
        point_1 = handLms.landmark[9]
        angle_error_3, isStraight_3 = get_angleError(point_4, point_3, point_2, point_1)
        print("isStraight_3:", isStraight_3)
        isStraight_list.append(isStraight_3)

        # 人差し指のジェスチャーを判断
        point_4 = handLms.landmark[16]
        point_3 = handLms.landmark[15]
        point_2 = handLms.landmark[14]
        point_1 = handLms.landmark[13]
        angle_error_4, isStraight_4 = get_angleError(point_4, point_3, point_2, point_1)
        print("isStraight_4:", isStraight_4)
        isStraight_list.append(isStraight_4)

        # 小指のジェスチャーを判断
        point_4 = handLms.landmark[20]
        point_3 = handLms.landmark[19]
        point_2 = handLms.landmark[18]
        point_1 = handLms.landmark[17]
        angle_error_5, isStraight_5 = get_angleError(point_4, point_3, point_2, point_1)
        print("isStraight_5:", isStraight_5)
        isStraight_list.append(isStraight_5)

        # 5本の手指の伸び具合に基づいてジェスチャーを判断
        gesture = getGesture(isStraight_list)
        print("gesture:", gesture)

        cv2.putText(img, gesture, (10, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
