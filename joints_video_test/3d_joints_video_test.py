import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
import joints
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

# Image capture settings
cap = cv2.VideoCapture(0)
if cap.isOpened():
    # print('CAMERA OPENED')
    image_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    image_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cv2.namedWindow('frame')
    cap.set(cv2.CAP_PROP_FPS, 60)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
else:
    print('FAILED TO OPEN CAMERA')
    exit(1)

# Joints initialization
joints_hand = joints.joints()

# 3d figure setup
# fig = plt.figure(figsize=(8, 8))
# ax = fig.add_subplot(111, projection='3d')
# plt.ion()
# plt.show()

# Mediapipe drawing setup
circle_spec = mp_drawing.DrawingSpec(color=(0, 47, 255), thickness=5, circle_radius=8)
connection_spec = mp_drawing.DrawingSpec(color=(0, 217, 255), thickness=5, circle_radius=2)

# Fps tracker init
prev_frame_time = 0
new_frame_time = 0

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        scale_percent = 200  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)

        #
        # Resize image
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

        # Fps tracker start
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        fps = str(int(fps))
        prev_frame_time = new_frame_time
        cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)


        # BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # set flag
        # image.flags.writeable = False

        # Detections
        results = hands.process(image)

        # set flag to true
        # image.flags.writeable = True

        # RGB to BGR
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Detections
        # print(results)


        # Detection is successful
        if results.multi_hand_landmarks:
            # Label landmarks and connections
            for hand in results.multi_hand_landmarks:
                # print(hand)
                mp_drawing.draw_landmarks(frame,
                                          hand,
                                          mp_hands.HAND_CONNECTIONS,
                                          mp_drawing_styles.get_default_hand_landmarks_style(),
                                          mp_drawing_styles.get_default_hand_connections_style())
            # label angles
            frame = joints_hand.draw_angles(frame, results)

            # calc 3d results
            # plt.cla()
            #
            # x = joints_hand.coord[:,0]
            # y = joints_hand.coord[:,1]
            # z = joints_hand.coord[:,2]
            # ax.scatter(x, 1- y, z)  # plot the point (2,3,4) on the figure
            # for a, b in zip(joints_hand.CONNECTIONS_PARENT, joints_hand.CONNECTIONS_CHILD):
            #     arr = np.array([joints_hand.coord[a], joints_hand.coord[b]]).T
            #     ax.plot(arr[0], 1 - arr[1], arr[2], linewidth=3, color='black')

        # display image
        cv2.imshow('frame', frame)

        # display 3d scatter plot
        # ax.set_zlim3d(-0.25, 0.25)  # viewrange for z-axis should be [-4,4]
        # ax.set_ylim3d(0, 1)  # viewrange for y-axis should be [-2,2]
        # ax.set_xlim3d(0, 1)  # viewrange for x-axis should be [-2,2]
        # ax.set_xlabel('x-axis')
        # ax.set_ylabel('y-axis')
        # ax.set_zlabel('z-axis')
        # plt.pause(0.000001)  # Note this correction

        # termination
        if (cv2.waitKey(10) & 0xFF) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
