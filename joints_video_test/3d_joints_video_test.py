import mediapipe as mp
import cv2
import joints
import matplotlib.pyplot as plt
import time
import numpy as np
import uuid
import os

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)

#3d figure setup
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
plt.ion()

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # set flag
        image.flags.writeable = False

        # Detections
        results = hands.process(image)

        # set flag to true
        image.flags.writeable = True

        # RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Detections
        # print(results)

        # Test
        image_height, image_width = image.shape[:2]

        circle_spec = mp_drawing.DrawingSpec(color=(0, 47, 255), thickness=5, circle_radius=8)

        connection_spec = mp_drawing.DrawingSpec(color=(0, 217, 255), thickness=5, circle_radius=2)

        #detection is successful
        if results.multi_hand_landmarks:
            #label landmarks and connections
            for num, hand in enumerate(results.multi_hand_landmarks):
                print(hand)
                mp_drawing.draw_landmarks(image,
                                          hand,
                                          mp_hands.HAND_CONNECTIONS,
                                          mp_drawing_styles.get_default_hand_landmarks_style(),
                                          mp_drawing_styles.get_default_hand_connections_style())
            #label angles
            joints_hand = joints.joints()
            image = joints_hand.drawAngles(image, results)

            # calc 3d results
            plt.cla()

            x = joints_hand.coord[:,0]
            y = joints_hand.coord[:,1]
            z = joints_hand.coord[:,2]
            ax.scatter(x, 1- y, z)  # plot the point (2,3,4) on the figure

        #display image
        cv2.imshow('frame', image)

        #display 3d scatter plot
        ax.set_zlim3d(-0.1, 0.1)  # viewrange for z-axis should be [-4,4]
        ax.set_ylim3d(0, 1)  # viewrange for y-axis should be [-2,2]
        ax.set_xlim3d(0, 1)  # viewrange for x-axis should be [-2,2]
        ax.set_xlabel('x-axis')
        ax.set_ylabel('y-axis')
        ax.set_zlabel('z-axis')
        plt.show()
        plt.pause(0.00001)  # Note this correction

        #termination
        if (cv2.waitKey(10) & 0xFF) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()