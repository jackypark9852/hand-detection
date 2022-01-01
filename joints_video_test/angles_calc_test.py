import joints
import numpy as np
import cv2
jnts = joints.joints()
coord0 = np.array([ 6.16427362e-01,  9.30325329e-01, -6.40707398e-08])
coord5 = np.array([ 6.24458671e-01,  6.20993435e-01, -6.35541091e-03])
coord6 = np.array([ 5.90875566e-01,  5.70845187e-01,  1.08246170e-02])

conn4 = coord5 - coord0
conn5 = coord6 - coord5

angle = jnts.angleBetween(conn5, conn4)
print(angle)