import cv2
import numpy as np
import imutils



white = np.zeros((720, 1280, 3), np.uint8)
white[:] = (0, 255, 255)

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


cv2.namedWindow("Calibration", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.moveWindow("Calibration", 3440, 0)

cv2.fillConvexPoly(white, np.array([[[0,0], [1280, 0], [1280, 720], [0, 720]]], dtype="int32"), (0,0,0))

cv2.imshow("Calibration", white)

cv2.waitKey()
