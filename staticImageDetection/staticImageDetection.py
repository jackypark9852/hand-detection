import mediapipe as mp
import numpy as np
import cv2

image = cv2.imread("hand.jpg")
iamge = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#mp utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

#Detect hand
processed_image = image
with mp_hands.Hands(
    static_image_mode= True,
    max_num_hands= 2,
    min_detection_confidence= 0.7,
) as hand:
    results = hand.process(image)

    if not results.multi_hand_landmarks:
        print("Failed to detect hand")
        exit()
    else:
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(processed_image, landmarks, mp_hands.HAND_CONNECTIONS)


#End script
cv2.imshow("hand", processed_image)
while True:
    if cv2.waitKey(10) & 0xFF is ord('q'):
        break

exit(0)
