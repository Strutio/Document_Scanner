import numpy as np
import cv2

# Beginning by accessing the webcam from the user

cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)


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

# realized that there's no point in saving more than one screenshot, just utilizing the one last taken by user instead

    elif c == 32:
        screenshot = "file_screenshot_0.png" #.format(count)
        cv2.imwrite(screenshot, frame)
        count += 1

    cv2.imshow('Original video', frame)

cam.release()
cv2.destroyAllWindows()

################################ OPENING THE SCREENSHOT THAT THE USER HAS TAKEN ################################

# opening the latest screenshot the user has taken

# using matplotlib as a way to visualize the edges that are going to be detected

# moving on to detecting  edges in the image

# first attempt at canny algorithm

# beginning by adding grayscale to the webcam
# using gaussian blur to remove extra noise and detail, makes it easier to find the edges

img = cv2.imread("file_screenshot_0.png")

img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img2 = cv2.GaussianBlur(img2, (7, 7), 1.41)

edges = cv2.Canny(img2, 100, 200)

cv2.imshow("Original image", edges)

# smoothening the image to help find edges

# felt that smoothening the image caused borders to be more skewed, decided to comment it out for the time being

#kernel = np.ones((15, 15),np.float32)/225
#edges = cv2.filter2D(edges, -1, kernel)

#### END OF SMOOTHENING ####

#### CONTOUR FUNCTION ####

# look at these params documentation further

# first param is source image, second is contour retrieval mode, third is contour approximation method

contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# now drawing the contours

# first param is source image, second is the contours created before, third is the index of contours, to draw all use -1, last is color, thickness, etc

cv2.drawContours(img2, contours, -1, (0,255,0), 3)

cv2.imshow("Contoured image", img2)  
cv2.waitKey(0)