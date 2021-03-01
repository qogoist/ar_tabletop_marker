import cv2
import numpy as np
import imutils
import time
import cv2.aruco as aruco

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    arucoParameters = aruco.DetectorParameters_create()
    
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParameters)
    
    centers = []

    if ids is not None:
        for i in range(0, len(ids)):
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

        for i in range (0, len(centers)):
            indexes = [i for i,x in enumerate(centers) if x["id"] == centers[i]["id"]]

            if len(indexes) != 2:
                continue

            point = [0, 0]
            for j in indexes:
                point[0] += centers[j]["point"][0]
                point[1] += centers[j]["point"][1]

            point = (int(point[0] / 2), int(point[1] / 2))

            cv2.circle(frame, point, 40, (0, 255, 0), 2)


    cv2.imshow("Display", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()