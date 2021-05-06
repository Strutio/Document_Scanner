import numpy as np
import cv2

# Beginning by accessing the webcam from the user

cam = cv2.VideoCapture(0)


# Making sure the webcam is being opened
# raises an exception otherwise

if not cam.isOpened():
    raise IOError("Webcam failed to open")

#todo 
  # access the screenshot the user creates, subsequently named file_screenshot_count or whatever

# infinite loop to continuously display the webcam until escape is pressed, which has an ASCII value of 27
# ret is a bool value returned by the read function, which is an indicator as to whether or not the frame was successfully captured
# if it was successfully captured, it is placed into the frame variable
# user presses enter to take a screenshot of their webcam which will be used to then be scanned into a pdf

count = 0

while True:

    ret, frame = cam.read()
    frame = cv2.resize(frame, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_AREA)
 ##   cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

# using curly brackets as placeholders to be paired with format(), ensuring no screenshots get overwritten during the process

    elif c == 32:
        screenshot = "file_screenshot_{}.png".format(count)
        cv2.imwrite(screenshot, frameGray)
      
        count += 1

cap.release()
cv2.destroyAllWindows()

# moving on to detecting  edges in the image

# beginning by adding grayscale to the webcam
# using gaussian blur to remove extra noise and detail, makes it easier to find the edges

frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
frame = cv2.GaussianBlur(frame, (7, 7), 1.41)

    # smoothening the image to help find edges  

kernel = np.ones((15,15),np.float32)/225
smooth = cv2.filter2D(frame, -1, kernel)

  #  threshold = cv2.adaptiveThreshold(smooth, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN.C, cv2.THRESH_BINARY,11,2)

# displaying the current webcam feed to the monitor

cv2.imshow('Original video', frame)    
   # cv2.imshow('Original video', smooth)



