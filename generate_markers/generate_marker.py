import numpy as np
import cv2
import sys

ARUCO_DICT = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)

def generate_marker(id):
  print("[INFO] generating ArUCo tag with ID '{}'".format(id))

  tag = np.zeros((300, 300, 1), dtype="uint8")
  cv2.aruco.drawMarker(ARUCO_DICT, id, 300, tag, 1)

  cv2.imwrite("tag_" + str(id) + ".jpg", tag)


for i in range(0, 10):
  generate_marker(i)
  i += 1