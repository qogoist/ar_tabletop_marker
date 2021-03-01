import cv2
import numpy as np
import imutils
import time
import cv2.aruco as aruco

def detect(camera, cameraMtx, distCoeff, projMtx):
    print("STARTING MARKER DETECTION:")

    cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    white = np.zeros((720, 1280, 3), np.uint8)
    white[:] = (255, 255, 255)

    cv2.namedWindow("Calibration", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow("Calibration", 1920, 0)

    while(True):
        # white[:] = (255, 255, 255)
        cv2.imshow("Calibration", white)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_copy = frame.copy()
        warped = cv2.warpPerspective(frame_copy, projMtx, (frame.shape[1], frame.shape[0]))

        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        arucoParameters = aruco.DetectorParameters_create()
        
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParameters)
        
        if ids is not None:
            for i in range(0, len(ids)):
                rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(corners[i], 0.02, cameraMtx, distCoeff)
                (rvec-tvec).any()
                aruco.drawAxis(frame, cameraMtx, distCoeff, rvec, tvec, 0.01)
                
                # Transform Marker and draw on transformed image.
                rect = cv2.perspectiveTransform(corners[i], projMtx)
                cv2.polylines(white, np.int32(rect), True, (0,255,0), 2)
                cv2.fillPoly(white, np.int32(rect), (0,0,0))

            # frame = aruco.drawDetectedMarkers(frame, corners, ids) # Draw marker on original frame

        # cv2.imshow("Display", frame)
        cv2.imshow("Display2", warped)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()