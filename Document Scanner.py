import numpy as np
import cv2

# Beginning by accessing the webcam from the user

cam = cv2.VideoCapture(0)


# Making sure the webcam is being opened
# raises an exception otherwise

if not cam.isOpened():
    raise IOError("Webcam failed to open")


# infinite loop to continuously display the webcam until escape is pressed, which has an ASCII value of 27
# ret is a bool value returned by the read function, which is an indicator as to whether or not the frame was successfully captured
# if it was successfully captured, it is placed into the frame variable

while True:
    ret, frame = cam.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()