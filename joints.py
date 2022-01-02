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
        self.CONNECTIONS_PARENT = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.CONNECTIONS_CHILD =  [0, 1, 2, 3, 0, 5, 6, 7, 0,  9, 10, 11,  0, 13, 14, 15,  0, 17, 18, 19]


        #store angles to annotate
        #[landmark label, conn1, conn2]
        self.ANGLES_SHOW   = [0, 0, 0, 1, 1, 1, 0,  0,  0,  0,  0,  0,  0,  0,  0]
        self.ANGLES_AT     = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19]
        self.ANGLES_PARENT = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19]
        self.ANGLES_CHILD  = [0, 1, 2, 4, 5, 6, 8,  9, 10, 12, 13, 14, 16, 17, 18]

        #coordinates, connections, and angels between connections
        self.landmarks = np.zeros((self.LANDMARK_COUNT, 3))
        self.coord = np.zeros((self.LANDMARK_COUNT, 3))
        self.conn = np.zeros((self.LANDMARK_COUNT, 3))
        self.angles = np.zeros((self.LANDMARK_COUNT, 3))

    def calc_coordinates(self, image, results):
        height, width = image.shape[:2]
        # print(image.shape)
        for idx, landmark in enumerate(results.multi_hand_landmarks[0].landmark):
            self.coord[idx] = [landmark.x, landmark.y, landmark.z]
        # print(results.multi_hand_landmarks[0].landmark)
        return self.coord

    def calc_connections(self, image, results):
        coords = self.calc_coordinates(image, results)
        # print(coords)
        for idx, (a, b) in enumerate(zip(self.CONNECTIONS_PARENT, self.CONNECTIONS_CHILD)):
            self.conn[idx] = coords[a] - coords[b]
        # print('conns:', self.conn)
        # for idx,landmarks in enumerate(self.coord):
        #     if idx == 0:
        #         continue
        #     self.conn[idx] = coords[idx] - coords[idx - 1]
        #
        # for connect in self.CONNNECTIONS_HAND:
        #     idx = connect[0]
        #     conn_to = connect[1]
        #     conn_from = connect[2]
        #     self.conn[idx] = coords[conn_to] - coords[conn_from]
        return self.conn

    def angle_between(self, conn1, conn2):
        unit_conn1 = conn1/np.linalg.norm(conn1)
        unit_conn2 = conn2/np.linalg.norm(conn2)
        # unit_conn1 = conn1 / np.linalg.norm(conn1[:2])
        # unit_conn2 = conn2 / np.linalg.norm(conn2[:2])
        # print(unit_conn1, unit_conn2)
        dot_product = np.dot(unit_conn1, unit_conn2)
        rad_angle = np.arccos(dot_product)
        deg_angle = rad_angle * 180/np.pi
        return deg_angle

    def label_angle(self, image, coord, conn1, conn2):
        angle = self.angle_between(conn1, conn2)
        # print(angle)
        image_width, image_height = image.shape[:2]
        x = math.floor(coord[0] * image_height)
        y = math.floor(coord[1] * image_width)

        #text params
        angle_text = str(math.floor(angle))
        font = cv2.FONT_HERSHEY_DUPLEX
        fontscale = 0.7
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

    def draw_angles(self, image, results):
        conn = self.calc_connections(image, results)
        for show, idx, a, b in zip(self.ANGLES_SHOW, self.ANGLES_AT, self.ANGLES_PARENT, self.ANGLES_CHILD):
            if show == 1:
                landmark = self.coord[idx]
                conn1 = self.conn[a]
                conn2 = self.conn[b]
                self.label_angle(image, landmark, conn1, conn2)

        #TEST
        # self.label_angle(image, self.coord[5], self.conn[5], self.conn[6])

        return image

    def get_coords(self):
        return self.coord

