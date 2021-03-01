import cv2
import numpy as np
import imutils

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

objpoints = []
imgpoints = []

cap = cv2.VideoCapture(0)
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

h, w = frame.shape[:2]
newmtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newmtx,(w,h),5)
dst = cv2.remap(frame,mapx,mapy,cv2.INTER_LINEAR)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]

cv2.imshow("Normal", frame)
cv2.imshow("Undistorted", dst)

cv2.waitKey()

mean_error = 0
for i in range(0, len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

print("total error: ", mean_error/len(objpoints))

# fs = cv2.FileStorage('calibration.yml', cv2.FILE_STORAGE_WRITE)
# fs.write('camera_matrix', mtx)
# fs.write('dist_coeff', dist)
# fs.release()