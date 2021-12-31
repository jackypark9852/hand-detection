import numpy as np
import mediapipe as mp
import cv2
import math

class joints:
    def __init__(self):
        #constants
        self.LANDMARK_COUNT = 21
        self.COORD_DIM = 3

        #Store connection instructions
        self.CONNNECTIONS_HAND = np.zeros((self.LANDMARK_COUNT, self.COORD_DIM), dtype = np.int32)
        for idx, conn in enumerate(self.CONNNECTIONS_HAND):
            conn = [idx, idx, idx - 1]
        self.CONNNECTIONS_HAND[5] = [5, 5, 0]
        self.CONNNECTIONS_HAND[9] = [9, 9, 0]
        self.CONNNECTIONS_HAND[13] = [13, 13, 0]
        self.CONNNECTIONS_HAND[17] = [17, 17, 0]

        #store angles to annotate
        #[landmark label, conn1, conn2]
        self.ANGLES_HAND = np.zeros((21, 3), dtype = np.int32)
        self.ANGLES_HAND = [[1, 1, 2],
                       [2, 2, 3],
                       [3, 3, 4],
                       [5, 5, 6],
                       [6, 6, 7],
                       [7, 7, 8],
                       [9, 9, 10],
                       [10, 10, 11],
                       [11, 11, 12],
                       [13, 13, 14],
                       [14, 14, 15],
                       [15, 15, 16],
                       [17, 17, 18],
                       [18, 18, 19],
                       [19, 19, 20],
        ]

        #coordinates, connections, and angels between connections
        self.coord = np.zeros((self.LANDMARK_COUNT, 3))
        self.conn = np.zeros((self.LANDMARK_COUNT, 3))
        self.angles = np.zeros((self.LANDMARK_COUNT, 3))

    def calcCoordinates(self, image, results):
        height, width = image.shape[:2]
        # print(image.shape)
        for idx, landmark in enumerate(results.multi_hand_landmarks[0].landmark):
            self.coord[idx] = np.multiply([landmark.x, landmark.y, landmark.z], [width, height, 500])
        # print(results.multi_hand_landmarks[0].landmark)
        return self.coord

    def calcConnections(self, image, results):
        coords = self.calcCoordinates(image, results)
        print(coords)
        for idx,landmarks in enumerate(self.coord):
            if idx == 0:
                continue
            self.conn[idx] = coords[idx] - coords[idx - 1]

        for connect in self.CONNNECTIONS_HAND:
            idx = connect[0]
            conn_to = connect[1]
            conn_from = connect[2]
            self.conn[idx] = coords[conn_to] - coords[conn_from]
        return self.conn

    def angleBetween(self, conn1, conn2):
        unit_conn1  = conn1/np.linalg.norm(conn1)
        unit_conn2  = conn2/np.linalg.norm(conn2)
        # print(unit_conn1, unit_conn2)
        dot_product = np.dot(unit_conn1, unit_conn2)
        rad_angle = np.arccos(dot_product)
        deg_angle = rad_angle * 180/np.pi
        return deg_angle

    def labelAngle(self, image, coord, conn1, conn2):
        angle = self.angleBetween(conn1, conn2)

        x = math.floor(coord[0])
        y = math.floor(coord[1])

        #text params
        angle_text = str(math.floor(angle))
        font = cv2.FONT_HERSHEY_DUPLEX
        fontscale = 0.6
        text_color = (0, 0, 0)
        text_thickness = 1

        #rect params
        (w, h), _ = cv2.getTextSize(angle_text, cv2.FONT_HERSHEY_DUPLEX, fontscale, text_thickness)
        rect_color = (255, 255, 255)
        rect_border_color = (0, 0, 0)

        #labelling
        image = cv2.rectangle(image, (x, y - h), (x +  w, y), rect_color, -1)
        image = cv2.rectangle(image, (x, y - h), (x +  w, y), rect_border_color, 1)
        image = cv2.putText(image, angle_text, (x, y), font, fontscale, text_color, text_thickness)

    def drawAngles(self, image, results):
        conn = self.calcConnections(image, results)
        print(conn)
        for item in self.ANGLES_HAND:
            landmark = self.coord[item[0]]
            conn1 = self.conn[item[1]]
            conn2 = self.conn[item[2]]
            self.labelAngle(image, landmark, conn1, conn2)

        #TEST
        # self.labelAngle(image, self.coord[5], self.conn[5], self.conn[6])

        return image
