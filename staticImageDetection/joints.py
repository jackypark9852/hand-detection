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
        self.CONN = np.zeros((self.LANDMARK_COUNT, self.COORD_DIM), dtype= np.int32)
        for idx, conn in enumerate(self.CONN):
            conn = [idx, idx, idx - 1]
        self.CONN[5] = [5, 5, 0]
        self.CONN[9] = [9, 9, 0]
        self.CONN[13] = [13, 13, 0]
        self.CONN[17] = [17, 17, 0]

        #coordinates, connections, and angels between connections
        self.coord = np.zeros((self.LANDMARK_COUNT, 3), dtype = np.int32)
        self.conn = np.zeros((self.LANDMARK_COUNT, 3))
        self.angles = np.zeros((self.LANDMARK_COUNT, 3))

    def calcCoordinates(self, image, results):
        height, width = image.shape[:2]
        # print(image.shape)
        for idx, landmark in enumerate(results.multi_hand_landmarks[0].landmark):
            self.coord[idx] = np.multiply([landmark.x, landmark.y, landmark.z], [width, height, 1])
        # print(results.multi_hand_landmarks[0].landmark)
        return self.coord

    def calcConnections(self, image, results):
        coords = self.calcCoordinates(image, results)

        for idx,landmarks in enumerate(self.coord):
            if idx == 0:
                continue
            self.conn[idx] = coords[idx] - coords[idx - 1]

        for connect in self.CONN:
            idx = connect[0]
            conn_to = connect[1]
            conn_from = connect[2]
            self.conn[idx] = coords[conn_to] - coords[conn_from]
        return self.conn

    # def drawAngles(self, image, results):
