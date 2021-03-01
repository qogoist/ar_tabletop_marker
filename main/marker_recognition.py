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
    cv2.setWindowProperty(
        "Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow("Calibration", 1920, 0)

    while(True):
        # white[:] = (255, 255, 255)
        cv2.imshow("Calibration", white)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_copy = frame.copy()
        warped = cv2.warpPerspective(
            frame_copy, projMtx, (frame.shape[1], frame.shape[0]))

        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        arucoParameters = aruco.DetectorParameters_create()

        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, aruco_dict, parameters=arucoParameters)
        centers = []

        if ids is not None:
            for i in range(0, len(ids)):
                rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(
                    corners[i], 0.02, cameraMtx, distCoeff)
                (rvec-tvec).any()

                aruco.drawAxis(frame, cameraMtx, distCoeff, rvec, tvec, 0.01)

                # Transform Marker and draw on transformed image.
                rect = cv2.perspectiveTransform(corners[i], projMtx)
                cv2.polylines(warped, np.int32(rect), True, (0, 255, 0), 2)
                cv2.fillPoly(warped, np.int32(rect), (0, 0, 0))

                sx = 0
                sy = 0
                for c in corners[i][0]:
                    sx += c[0]
                    sy += c[1]

                cx = sx / 4
                cy = sy / 4
                center = {
                    "id": i,
                    "point": (int(cx), int(cy))
                }
                centers.append(center)

            for i in range(0, len(centers)):
                indexes = [i for i, x in enumerate(
                    centers) if x["id"] == centers[i]["id"]]

                if len(indexes) != 2:
                    continue

                point = [0, 0]
                for j in indexes:
                    point[0] += centers[j]["point"][0]
                    point[1] += centers[j]["point"][1]

                point = [int(point[0] / 2), int(point[1] / 2)]
                tempP = np.array([[point]], dtype="float32")
                warpPoint = cv2.transform(tempP, projMtx)
                warpTuple = (warpPoint[0][0][0], warpPoint[0][0][1])

                cv2.circle(warped, warpTuple, 40, (0, 255, 0), 2)
                cv2.circle(white, warpTuple, 40, (0, 255, 0), 2)
                cv2.circle(frame, (point[0], point[1]), 40, (0, 255, 0), 2)

                # frame = aruco.drawDetectedMarkers(frame, corners, ids) # Draw marker on original frame

                # cv2.imshow("Display", frame)
        cv2.imshow("Display2", warped)
        cv2.imshow("Display3", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
