import cv2
import numpy as np
import imutils
import time

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

tr = 180
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
            return approx


def contour_recognition():
    # Create Window
    win = "Contour Detection"
    cv2.namedWindow(win)
    cv2.createTrackbar('Thresh:', win, tr, 255, updateThresh)
    cv2.createTrackbar('Epsilon:', win, int(e * 100), 100, updateE)

    while(cap.isOpened):
        ret, frame = cap.read()
        height, width, channels = frame.shape

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blur, tr, 255, cv2.THRESH_BINARY)[1]

        contour_frame = frame.copy()

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        outer_rectangle = detectRectangle(cnts)
        

        destination_pts = np.array([[0, 0], [399, 0], [399, 399], [0, 399]])
        h, status = cv2.findHomography(outer_rectangle, destination_pts)
        adjustedImg = cv2.warpPerspective(frame, h, (400, 400))

        adjustedGray = cv2.cvtColor(adjustedImg, cv2.COLOR_BGR2GRAY)
        adjustedThres = cv2.threshold(adjustedGray, tr, 255, cv2.THRESH_BINARY_INV)[1]

        innerCnts = cv2.findContours(adjustedThres.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        innerCnts = imutils.grab_contours(innerCnts)
        inner_rectangle = detectRectangle(innerCnts)

        h_inner, status_inner = cv2.findHomography(inner_rectangle, destination_pts)
        innerImg = cv2.warpPerspective(adjustedImg, h_inner, (400, 400))

        innerGray = cv2.cvtColor(innerImg, cv2.COLOR_BGR2GRAY)
        innerThres = cv2.threshold(innerGray, tr, 255, cv2.THRESH_BINARY)[1]

        featureCnts = cv2.findContours(innerThres.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        featureCnts = imutils.grab_contours(featureCnts)

        for c in featureCnts:
            cv2.drawContours(adjustedImg, [c], -1, (0, 255, 255), 2)  


        cv2.drawContours(contour_frame, [outer_rectangle], -1, (0, 255, 0), 2)
        cv2.drawContours(adjustedImg, [inner_rectangle], -1, (0, 0, 255), 2)

        cv2.imshow("Binary", thresh)
        cv2.imshow(win, contour_frame)
        cv2.imshow("Warped", adjustedImg)
        cv2.imshow("Warped_Inner", innerImg)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    # Release capture and close windows
    cap.release()
    cv2.destroyAllWindows()


contour_recognition()
