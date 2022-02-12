import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
import joints
import time
import ang_serial

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

# Open camera
cap = cv2.VideoCapture(0)

# print('CAMERA OPENED')
if cap.isOpened():
    image_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    image_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cv2.namedWindow('frame')
    cap.set(cv2.CAP_PROP_FPS, 60)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
else:
    print('FAILED TO OPEN CAMERA')
    exit(1)

# Joints Initialization
joints_hand = joints.joints()

# 3d figure initialization
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
plt.ion()
plt.show()

# Mediapipe drawing setup
circle_spec = mp_drawing.DrawingSpec(color=(0, 47, 255), thickness=5, circle_radius=8)
connection_spec = mp_drawing.DrawingSpec(color=(0, 217, 255), thickness=5, circle_radius=2)

# Fps tracker init
prev_frame_time = 0
new_frame_time = 0

# Display mode
calib_flag = False

# Initialize serial communication
angle_serial = ang_serial.AngleSerial(port='COM3', baudrate=115200)

def drawScatter(ax, coord):
    x = coord[:, 0]
    y = coord[:, 1]
    z = coord[:, 2]
    ax.scatter(x, 1 - y, z)  # plot the point (2,3,4) on the figure


def drawVector(ax, start, end, width, color):
    vector = np.array([start, end]).T
    ax.plot(vector[0], 1 - vector[1], vector[2], linewidth=width, color=color, scalex=False, scaley=False)


def setUp3dDisplay(ax, xmin, xmax, ymin, ymax, zmin, zmax):
    ax.set_zlim3d(zmin, zmax)  # viewrange for z-axis should be [-4,4]
    ax.set_ylim3d(ymin, ymax)  # viewrange for y-axis should be [-2,2]
    ax.set_xlim3d(xmin, xmax)  # viewrange for x-axis should be [-2,2]
    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.set_zlabel('z-axis')


def labelInstructions(img):
    img_h, img_w, _ = img.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    text_color = (100, 255, 0)
    text_thickness = 3
    line_spacing = 20
    text = "Press 'q' to quit\nPress 'c' to calibrate"
    (txt_w, txt_h), _ = cv2.getTextSize(text, font, font_scale, text_thickness)

    for i, line in enumerate(text.split('\n')):
        y = img_h - txt_h - (i * (txt_h + line_spacing))
        cv2.putText(img, line, (7, y), font, font_scale, text_color, text_thickness, cv2.LINE_AA)

    return img


with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Resize image
        scale_percent = 200  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        frame = cv2.resize(frame, dim=(width, height), interpolation=cv2.INTER_AREA)

        # Fps tracker start
        new_frame_time = time.time()
        fps = str(int(1 / (new_frame_time - prev_frame_time)))
        prev_frame_time = new_frame_time
        cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

        # Label instructions
        frame = labelInstructions(frame)

        # BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detections
        results = hands.process(image)

        # Detection is successful
        if results.multi_hand_landmarks:
            #Label detection results on live video feed
            landmarks_style = mp_drawing_styles.get_default_hand_landmarks_style() # Labeling Style
            connections_style = mp_drawing_styles.get_default_hand_connections_style()

            for hand in results.multi_hand_landmarks: # Label landmarks
                mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS, landmarks_style, connections_style)

            frame = joints_hand.draw_angles(frame, results, True) # label angles


            # Display detection result in 3D
            plt.cla() # Clear 3D screen
            setUp3dDisplay(ax, 0, 1, 0, 1, -0.25, 0.25)
            drawScatter(ax, joints_hand.coord) # Draw joint nodes

            for a, b in zip(joints_hand.CONNECTIONS_PARENT, joints_hand.CONNECTIONS_CHILD): # Draw connections between joints
                drawVector(ax, joints_hand.coord[a], joints_hand.coord[b], 3, 'black')

            norm_at = joints_hand.NORMAL_AT # Draw normal vectors
            for idx, normal in enumerate(joints_hand.normal):
                drawVector(ax, joints_hand.coord[norm_at[idx]], joints_hand.coord[norm_at[idx]] + normal * 7, 3, 'red')

            # Send serial data
            ang_serial.send_angles(joints_hand.get_angles())

        # Display annotated image
        cv2.imshow('frame', frame)

        # For 3d display to refresh
        plt.pause(0.00000001)

        # Termination
        pressed_key = cv2.waitKey(10) & 0xFF
        if pressed_key == ord('q'):
            break
        elif pressed_key == ord('c'):
            joints_hand.calibrate()

cap.release()
cv2.destroyAllWindows()
