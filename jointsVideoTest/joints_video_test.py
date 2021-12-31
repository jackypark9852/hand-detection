import mediapipe as mp
import numpy as np
import cv2

image = cv2.imread("../joints_static_test/joints_static_test_hand.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#mp utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

#Detect hand
processed_image = image
hand = mp_hands.Hands(
    static_image_mode= True,
    max_num_hands= 2,
    min_detection_confidence= 0.7)

results = hand.process(image)

if not results.multi_hand_landmarks:
    print("Failed to detect hand")
    exit(0)
else:
    for landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(processed_image, landmarks, mp_hands.HAND_CONNECTIONS)

#store coordinates in np arr
coor = np.zeros((21,3))
for idx, landmark in enumerate(results.multi_hand_landmarks[0].landmark):
    coor[idx][0] = landmark.x
    coor[idx][1] = landmark.y
    coor[idx][2] = landmark.z
print(coor)

#End script
# cv2.imshow("hand", processed_image)
while True:
    if cv2.waitKey(10) & 0xFF is ord('q'):
        break

exit(0)
