import cv2
import numpy as np
import imutils

def calibrate():
  calib_image = cv2.imread("main/local/pattern_chessboard.png")
  win = "Calibration"
  cv2.namedWindow(win, cv2.WINDOW_NORMAL)
  
  print("Showing calibration pattern, please adjust it so it is visible on the projector.")

  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

  objp = np.zeros((6*9,3), np.float32)
  objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

  objpoints = []
  imgpoints = []

  cap = cv2.VideoCapture(1)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

  num = 10
  found = 0
  while(found < num):
      cv2.imshow(win, calib_image)
      ret, frame = cap.read()
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      frame_copy = frame.copy()

      foundCorners, corners = cv2.findChessboardCorners(gray, (9,6), None, None)

      if foundCorners:
        print("grid found")
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        cv2.drawChessboardCorners(frame_copy, (9, 6), corners2, foundCorners)

        found += 1

      cv2.imshow("Img", frame_copy)
      
      if cv2.waitKey(1) == ord('q'):
          break
  
  cap.release()
  cv2.destroyAllWindows()

  #Edge Detection
  thresh = cv2.threshold(gray, 180, )

  ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

  ret, dest_points = cv2.findChessboardCorners(calib_image, (9,6), None, None)
  calib_image_gray = cv2.cvtColor(calib_image, cv2.COLOR_BGR2GRAY)
  dest_points2 = cv2.cornerSubPix(calib_image_gray, dest_points, (11,11), (-1,-1), criteria)
  cv2.drawChessboardCorners(calib_image, (9,6), dest_points2, ret)

  projMtx, status = cv2.findHomography(corners2, dest_points2)

  height, width, channels = frame.shape

  testImg = cv2.warpPerspective(frame_copy, projMtx, (10*width, 10*height))

  # cv2.namedWindow(, cv2.WINDOW_NORMAL)
  # cv2.imshow(win, testImg)
  cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
  cv2.imwrite("TestImage.jpg", testImg)
  cv2.imshow("Test", testImg)
  cv2.waitKey()

  cv2.destroyAllWindows()

  return mtx, dist

calibrate()