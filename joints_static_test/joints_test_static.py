import joints
import mediapipe as mp
import cv2

image = cv2.imread("joints_test_hand_back.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#mp utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

#Detect hand
hand = mp_hands.Hands(
    static_image_mode= True,
    max_num_hands= 2,
    min_detection_confidence= 0.7)

results = hand.process(image)
image_joint = joints.joints()
# coords = image_joint.calcCoordinates(image, results)

#display result
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
processed_image = image.copy()
for landmarks in results.multi_hand_landmarks:
    mp_drawing.draw_landmarks(processed_image, landmarks, mp_hands.HAND_CONNECTIONS)

# for item in coords:
#     cv2.drawMarker(processed_image, (item[0], item[1]), (0, 0, 255), markerType=cv2.MARKER_CROSS,
#                    markerSize=40, thickness=2, line_type=cv2.LINE_AA)
# cv2.drawMarker(processed_image, (362, 299), (255, 0, 255), markerType=cv2.MARKER_CROSS,
#                markerSize=40, thickness=2, line_type=cv2.LINE_AA)

processed_image = image_joint.drawAngles(processed_image, results)
cv2.imshow('test', processed_image)
# print(image_joint.angleBetween([0,1,0], [1, 0, 0]))
# cv2.imshow('original', image)
while True:
    if cv2.waitKey(10) & 0xFF is ord('q'):
        cv2.destroyAllWindows()
        exit(11)

exit(1)