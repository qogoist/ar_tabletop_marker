import cv2
import numpy as np
import imutils
import time

white = np.zeros((1920, 1080, 3), np.uint8)
white[:] = (255, 255, 255)

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

tr = 14
e = 0.04


def updateThresh(val):
    global tr
    tr = val


def updateE(val):
    global e
    e = val * 0.01


def detectRectangle(cnts):
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, e * peri, True)

        if len(approx) == 4:
            return approx, True
    
    return -1, False


def contour_recognition():
    # Create Window
    win = "Contour Detection"
    cv2.namedWindow(win)
    cv2.createTrackbar('Thresh:', win, tr, 255, updateThresh)
    cv2.createTrackbar('Epsilon:', win, int(e * 100), 100, updateE)

    cv2.namedWindow("Calibration", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow("Calibration", 1920, 0)

    while(cap.isOpened):

        cv2.imshow("Calibration", white)
        ret, frame = cap.read()
        height, width, channels = frame.shape

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blur, tr, 255, cv2.THRESH_BINARY)[1]

        cv2.imshow(win, thresh)

        contour_frame = frame.copy()

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            cv2.drawContours(contour_frame, [c], -1, (0,255,0), 2)

        cv2.imshow("Contours", contour_frame)
        
        outer_rectangle, detected = detectRectangle(cnts)

        if detected:
            destination_pts = np.array([[0, 0], [0, 1079], [1919, 1079], [1919, 0]])
            h, status = cv2.findHomography(outer_rectangle, destination_pts)
            adjustedImg = cv2.warpPerspective(frame, h, (1920, 1080))
            cv2.imshow("Adjusted", adjustedImg)
  

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    # Release capture and close windows
    cap.release()
    cv2.destroyAllWindows()

    print(outer_rectangle)

contour_recognition()
