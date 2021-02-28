import cv2
import numpy as np
import imutils

def calibrate():
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

  objp = np.zeros((6*9,3), np.float32)
  objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

  objpoints = []
  imgpoints = []

  cap = cv2.VideoCapture(1)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

  num = 10
  found = 0
  while(found < num):
      ret, frame = cap.read()
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      frame_copy = frame.copy()

      foundCorners, corners = cv2.findChessboardCorners(gray, (9,6), None, None)

      if foundCorners:
        print("grid found")
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        frame_copy = cv2.drawChessboardCorners(frame, (9, 6), corners2, foundCorners)

        found += 1

      cv2.imshow("Img", frame_copy)
      
      if cv2.waitKey(1) == ord('q'):
          break

  cap.release()
  cv2.destroyAllWindows()

  ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

  return mtx, dist