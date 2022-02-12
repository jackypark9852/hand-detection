# "10 32 43 90 90 90 90 12 09 38 45 32 58 39 20 48 ..."
import joints
import numpy as np
import serial

class AngleSerial:
    def __init__(self, port = 'com3', baudrate = 115200):
        self.port = port
        self.baudrate = baudrate
        # self.arduinoData = serial.Serial(port, baudrate, writeTimeout=3.0)

    def _angles_to_string(self, angles):
        ret = '<'
        for angle in angles:
            ret += str(int(angle))
            ret += ","
        # Remove extra space from the end of string
        ret = ret[:-1]
        ret += '>'
        return ret

    def send_angles(self, angles):
        angles_string = self._angles_to_string(angles)
        # self.arduinoData.write(angles_string.encode())
        return angles_string