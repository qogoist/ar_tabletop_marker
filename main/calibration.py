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
  cv2.setWindowProperty("Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
  cv2.moveWindow("Calibration", 1920, 0)

  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

  objp = np.zeros((6*9,3), np.float32)
  objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

  objpoints = []
  imgpoints = []

  cap = cv2.VideoCapture(camera)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

  num = 20
  found = 0
  while(found < num):
      cv2.imshow("Calibration", calib_image)
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

  ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

  return mtx, dist

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

def calibrateProjection(camera):
  global mtx, dist, projMtx

  white = np.zeros((1280, 720, 3), np.uint8)
  white[:] = (255, 255, 255)

  cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

  # Create Window
  win = "Contour Detection"
  cv2.namedWindow(win)
  cv2.createTrackbar('Thresh:', win, tr, 255, updateThresh)
  cv2.createTrackbar('Epsilon:', win, int(e * 100), 100, updateE)

  cv2.namedWindow("Calibration", cv2.WND_PROP_FULLSCREEN)
  cv2.setWindowProperty("Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
  cv2.moveWindow("Calibration", 1920, 0)

  print("Adjust threshold until the border matches the projected image")

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

    cv2.imshow(win, contour_frame)
    
    outer_rectangle, detected = detectRectangle(cnts)

    if detected:
        destination_pts = np.array([[1279, 0], [0, 0], [0, 719], [1279, 719]])
        projMtx, status = cv2.findHomography(outer_rectangle, destination_pts)
        adjustedImg = cv2.warpPerspective(frame, projMtx, (1280, 720))
        # cv2.imshow(win, adjustedImg)


    key = cv2.waitKey(1)
    if key == ord("q"):
        break

  # Release capture and close windows
  cap.release()
  cv2.destroyAllWindows()


  ######### UNCOMMENT TO SAVE DIFFERENT PROJECTION IMAGES  #############
  cv2.imwrite("Testimage.jpg", adjustedImg)

  # h, w = frame.shape[:2]
  # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
  # dst = cv2.undistort(adjustedImg, mtx, dist, None, newcameramtx)

  # cv2.imwrite("Testimage2.jpg", dst)

  # x,y,w,h = roi
  # dst = dst[y:y+h, x:x+w]
  
  # cv2.imwrite("Testimage3.jpg", dst)

  return projMtx

# calibrateCamera()
# calibrateProjection()