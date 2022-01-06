import numpy as np
import mediapipe as mp
import cv2
import math
from enum import IntEnum, auto

class ConnLabel(IntEnum):
    def _generate_next_value_(self, _start, count, _last_values):
        """Generate consecutive automatic numbers starting from zero."""
        return count
    THUMB_CB = auto()
    THUMB_MCB = auto()
    THUMB_PPB = auto()
    THUMB_DPB = auto()
    INDEX_FINGER_CB = auto()
    INDEX_FINGER_MCB = auto()
    INDEX_FINGER_PPB = auto()
    INDEX_FINGER_DPB = auto()
    MIDDLE_FINGER_CB = auto()
    MIDDLE_FINGER_MCB = auto()
    MIDDLE_FINGER_PPB = auto()
    MIDDLE_FINGER_DPB = auto()
    RING_FINGER_CB = auto()
    RING_FINGER_MCB = auto()
    RING_FINGER_PPB = auto()
    RING_FINGER_DPB = auto()
    PINKY_FINGER_CB = auto()
    PINKY_FINGER_MCB = auto()
    PINKY_FINGER_PPB = auto()
    PINKY_FINGER_DPB = auto()
    PALM_NORMAL = auto()

class joints:
    def __init__(self):
        # Constants
        self.LANDMARK_COUNT = 21
        self.CONNECTION_COUNT = 21
        self.COORD_DIM = 3
        self.PLACE_HOLDER = 0

        # Store connection instructions
        # last for palm_normal
        self.CONNECTIONS_PARENT = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, self.PLACE_HOLDER]
        self.CONNECTIONS_CHILD =  [0, 1, 2, 3, 0, 5, 6, 7, 0,  9, 10, 11,  0, 13, 14, 15,  0, 17, 18, 19, self.PLACE_HOLDER]

        # Store angles to annotate
        # [landmark label, conn1, conn2]
        self.ANGLES_SHOW_FLAG = [0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0,  0, 1]
        self.ANGLES_SHOW_AT   = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19, 5]
        self.ANGLES_CONN1     = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19, ConnLabel.PALM_NORMAL]
        self.ANGLES_CONN2     = [0, 1, 2, 4, 5, 6, 8,  9, 10, 12, 13, 14, 16, 17, 18, 5]

        # Coordinates, connections, and angels between connections
        self.landmarks = np.zeros((self.LANDMARK_COUNT, 3))
        self.coord = np.zeros((self.LANDMARK_COUNT, 3))
        self.conn = np.zeros((self.CONNECTION_COUNT, 3))
        self.angles = np.zeros((self.LANDMARK_COUNT, 3))


        # Image
        self.image = np.zeros((480, 480, 3), np.uint8)

    def _calc_coordinates(self, results):
        for idx, landmark in enumerate(results.multi_hand_landmarks[0].landmark):
            self.coord[idx] = [landmark.x, landmark.y, landmark.z]
        return self.coord

    def _calc_connections(self, results):
        coords = self._calc_coordinates(results)
        for idx, (a, b) in enumerate(zip(self.CONNECTIONS_PARENT, self.CONNECTIONS_CHILD)):
            self.conn[idx] = coords[a] - coords[b]

        self.conn[ConnLabel.PALM_NORMAL] = np.cross(
            self.conn[ConnLabel.PINKY_FINGER_CB], self.conn[ConnLabel.INDEX_FINGER_CB])
        print(self.conn[ConnLabel.PALM_NORMAL])
        return self.conn

    def _angle_between(self, conn1, conn2):
        unit_conn1 = conn1/np.linalg.norm(conn1)
        unit_conn2 = conn2/np.linalg.norm(conn2)
        dot_product = np.dot(unit_conn1, unit_conn2)

        rad_angle = np.arccos(dot_product)
        deg_angle = rad_angle * 180/np.pi

        return deg_angle

    def _label_angle(self, coord, conn1, conn2):
        MAX_ANGLE = 180
        angle = self._angle_between(conn1, conn2)
        angle = min(MAX_ANGLE, angle)
        image_width, image_height = self.image.shape[:2]
        x = math.floor(coord[0] * image_height)
        y = math.floor(coord[1] * image_width)

        # Text params
        angle_text = str(math.floor(angle))
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.7
        text_color = (0, 0, 0)
        text_thickness = 1

        # Rect params
        (w, h), _ = cv2.getTextSize(angle_text, cv2.FONT_HERSHEY_DUPLEX, font_scale, text_thickness)
        rect_color = (255, 255, 255)
        rect_border_color = (0, 0, 0)

        # Labelling
        image = cv2.rectangle(self.image, (x, y - h), (x + w, y), rect_color, -1)
        image = cv2.rectangle(self.image, (x, y - h), (x + w, y), rect_border_color, 1)
        image = cv2.putText(self.image, angle_text, (x, y), font, font_scale, text_color, text_thickness)

        return self.image

    def draw_angles(self, image, results):
        self.image = image

        conn = self._calc_connections(results)
        for show, idx, a, b in zip(self.ANGLES_SHOW_FLAG, self.ANGLES_SHOW_AT, self.ANGLES_CONN1, self.ANGLES_CONN2):
            if show == 1:
                landmark = self.coord[idx]
                conn1 = self.conn[a]
                conn2 = self.conn[b]
                print(conn1, conn2)
                self._label_angle(landmark, conn1, conn2)

        return image

    def get_coords(self):
        return self.coord

