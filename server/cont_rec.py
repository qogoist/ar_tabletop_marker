import cv2
import numpy as np
import imutils
import time

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

tr = 100
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

    # for c in cnts:
    #     m = cv2.moments(c)
    #     cX = 0
    #     cY = 0

    #     if m["m10"] != 0.0:
    #         cX = int(m["m10"] / m["m00"])
    #         cY = int(m["m01"] / m["m00"])

    #     peri = cv2.arcLength(c, True)
    #     approx = cv2.approxPolyDP(c, e * peri, True)

    #     shape = ""

    #     if len(approx) == 4:
    #         shape = "rectangle"

    #         cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
    #         cv2.putText(frame, shape, (cX - 20, cY - 20),
    #                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


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

        cv2.imshow("Binary", thresh)

        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        outer_rectangle = detectRectangle(cnts)
        
        contour_frame = frame.copy()

        cv2.drawContours(contour_frame, [outer_rectangle], -1, (0, 255, 0), 2)
        cv2.imshow(win, contour_frame)

        destination_pts = np.array([[0, 0], [399, 0], [399, 399], [0, 399]])
        h, status = cv2.findHomography(outer_rectangle, destination_pts)
        im_out = cv2.warpPerspective(frame, h, (400, 400))

        cv2.imshow("Warped", im_out)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    # Release capture and close windows
    cap.release()
    cv2.destroyAllWindows()


contour_recognition()
