import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

tr = 100

def updateThresh(val):
    global tr
    tr = val

# Create Window
win = "Contour Detection"
cv2.namedWindow(win)
cv2.createTrackbar('Thresh:', win, tr, 255, updateThresh)

while(cap.isOpened):
    ret, frame = cap.read()
    height, width, channels = frame.shape

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, tr, 255, cv2.THRESH_BINARY_INV)[1]

    cv2.imshow("Binary", thresh)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

    cv2.imshow(win, frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Release capture and close windows
cap.release()
cv2.destroyAllWindows()