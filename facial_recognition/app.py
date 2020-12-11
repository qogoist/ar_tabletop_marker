import numpy as np
import cv2

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

face_cascade = cv2.CascadeClassifier("facial_recognition\haarcascades\haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("facial_recognition\haarcascades\haarcascade_eye.xml")

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    height, width, channels = frame.shape

    # Mirror image ... cuz webcam
    mir = cv2.flip(frame, 1)

    # Convert ot grayscale
    gray = cv2.cvtColor(mir, cv2.COLOR_BGR2GRAY)

    # Try to detect faces and eyes
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        mir = cv2.rectangle(mir,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = mir[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    # Add some text to the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(mir,'MEMES',(0,height), font, 4,(255,255,255),2,cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow("Webcam", mir)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord("s"):
        cv2.imwrite("snapshot.png",mir)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()