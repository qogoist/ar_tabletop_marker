import cv2
import numpy as np
import imutils

projMtx = []
mtx = []
dist = []


def calibrateCamera(camera):
    global mtx, dist, projMtx

    calib_image = cv2.imread("main/local/pattern_chessboard.png")
    cv2.namedWindow("Calibration", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(
        "Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow("Calibration", 1920, 0)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    patternsize = (9, 6)

    objp = np.zeros((patternsize[0] * patternsize[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:patternsize[0], 0:patternsize[1]].T.reshape(-1, 2)

    objpoints = []
    imgpoints = []

    cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    num = 20
    found = 0
    while(found < num):
        cv2.imshow("Calibration", calib_image)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_copy = frame.copy()

        foundCorners, corners = cv2.findChessboardCorners(
            frame, patternsize, None, None)

        if foundCorners:
            print("grid found")
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            cv2.drawChessboardCorners(
                frame_copy, patternsize, corners2, foundCorners)

            found += 1

        cv2.imshow("Img", frame_copy)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)

    ret, calibCorners = cv2.findChessboardCorners(
        calib_image, patternsize, None, None)
    cv2.drawChessboardCorners(calib_image, patternsize, calibCorners, ret)

    cv2.imwrite("CalibCorners.jpg", calib_image)

    projMtx, status = cv2.findHomography(corners2, calibCorners)

    h, w = calib_image.shape[:2]
    warp = cv2.warpPerspective(frame, projMtx, (1280, 720))

    cv2.imwrite("WarpTest.jpg", warp)

    return mtx, dist, projMtx


tr = 14
blur = 5


def updateThresh(val):
    global tr
    tr = val


def updateBlur(val):
    global blur
    if val % 2 == 1:
        blur = val
    else:
        blur = val + 1


def detectRectangle(cnts):
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        if len(approx) == 4:
            return approx, True

    return -1, False


def calibrateProjection(camera):
    global mtx, dist, projMtx

    black = np.zeros((720, 1280, 3), np.uint8)

    cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Create Window
    win = "Contour Detection"
    cv2.namedWindow(win)
    cv2.createTrackbar('Thresh:', win, tr, 255, updateThresh)
    cv2.createTrackbar('Blur:', win, blur, 50, updateBlur)

    cv2.namedWindow("Calibration", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(
        "Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow("Calibration", 1920, 0)

    print("Adjust threshold until the border matches the projected image")

    cornerPoints = []
    corner_pts = [[]]
    detected = False
    status = False

    while(cap.isOpened):
        cv2.imshow("Calibration", black)
        ret, frame = cap.read()
        height, width, channels = frame.shape

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurIm = cv2.GaussianBlur(gray, (blur, blur), 0)
        thresh = cv2.threshold(blurIm, tr, 255, cv2.THRESH_BINARY)[1]

        # cv2.imshow("Thres", thresh)

        contour_frame = frame.copy()

        if len(cornerPoints) == 0:
            black[:] = (0, 0, 0)
            cv2.rectangle(black, (0, 0), (20, 20,), (255, 255, 255), -1)
        if len(cornerPoints) == 1:
            black[:] = (0, 0, 0)
            cv2.rectangle(black, (1260, 0), (1280, 20,), (255, 255, 255), -1)
        if len(cornerPoints) == 2:
            black[:] = (0, 0, 0)
            cv2.rectangle(black, (0, 700), (20, 720), (255, 255, 255), -1)
        if len(cornerPoints) == 3:
            black[:] = (0, 0, 0)
            cv2.rectangle(black, (1260, 700), (1280, 720), (255, 255, 255), -1)
        if len(cornerPoints) > 3:
            black[:] = (0, 0, 0)
            cv2.circle(contour_frame, cornerPoints[0], 5, (255, 0, 0), -1)
            cv2.circle(contour_frame, cornerPoints[1], 5, (255, 0, 0), -1)
            cv2.circle(contour_frame, cornerPoints[2], 5, (255, 0, 0), -1)
            cv2.circle(contour_frame, cornerPoints[3], 5, (255, 0, 0), -1)
            detected = True

        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        rect = detectRectangle(cnts)

        xCenter = 0
        yCenter = 0
        for c in rect:
            M = cv2.moments(c)
            if M["m00"] != 0:
                xCenter = int(M["m10"] / M["m00"])
                yCenter = int(M["m01"] / M["m00"])
            cv2.drawContours(contour_frame, [c], -1, (0, 255, 0), 2)
            cv2.circle(contour_frame, (xCenter, yCenter), 5, (255, 0, 0), -1)

        cv2.imshow(win, contour_frame)

        if detected:
            destination_pts = np.array(
                [[10, 10], [1270, 10], [10, 710], [1270, 710]])
            projMtx, mask = cv2.findHomography(
                corner_pts, destination_pts)
            status = True
            # adjustedImg = cv2.warpPerspective(frame, projMtx, (1280, 720))
            # cv2.imshow("Adjusted", adjustedImg)

        if status:
            break

        key = cv2.waitKey(1)
        if key == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            return False, -1
        elif key == 13:
            if len(cornerPoints) < 4:
                cornerPoints.append((xCenter, yCenter))
                print((xCenter, yCenter))

            if len(cornerPoints) == 4:
                corner_pts = np.array([[cornerPoints[0][0], cornerPoints[0][1]],
                                       [cornerPoints[1][0], cornerPoints[1][1]],
                                       [cornerPoints[2][0], cornerPoints[2][1]],
                                       [cornerPoints[3][0], cornerPoints[3][1]]])

    # Release capture and close windows
    cap.release()
    cv2.destroyAllWindows()

    ######### UNCOMMENT TO SAVE DIFFERENT PROJECTION IMAGES  #############
    # cv2.imwrite("Testimage.jpg", adjustedImg)

    # h, w = frame.shape[:2]
    # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # dst = cv2.undistort(adjustedImg, mtx, dist, None, newcameramtx)

    # cv2.imwrite("Testimage2.jpg", dst)

    # x,y,w,h = roi
    # dst = dst[y:y+h, x:x+w]

    # cv2.imwrite("Testimage3.jpg", dst)

    return True, projMtx


# calibrateCamera()
calibrateProjection(0)
