import cv2
import numpy as np
import img2pdf
from PIL import Image

def capture_screenshot(cam):
    """
    Capture a screenshot from the webcam.
    """
    ret, frame = cam.read()
    if not ret:
        raise ValueError("Failed to capture screenshot from webcam")
    return frame

def find_contours(img):
    """
    Find contours in the image.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (7, 7), 1.41)
    edges = cv2.Canny(gray_blur, 100, 200)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_birds_eye_view(img, contours):
    """
    Generate bird's eye view of the image.
    """
    perimeter = cv2.arcLength(contours[0], True)
    epsilon = 0.02 * perimeter
    approx_corners = cv2.approxPolyDP(contours[0], epsilon, True)

    pts1 = np.float32([approx_corners[0], approx_corners[3], approx_corners[1], approx_corners[2]])
    pts2 = np.float32([[0, 0], [850, 0], [0, 1100], [850, 1100]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_print = cv2.warpPerspective(img, matrix, (850, 1100))

    return img_print

def save_as_pdf(img, file_count):
    """
    Save the image as a PDF.
    """
    img_stored = 'D:/Users/romeo/Finished-Images/imageToPNG.{}.png'.format(file_count)
    cv2.imwrite(img_stored, img)

    with Image.open(img_stored) as opened_img:
        bytes_pdf = img2pdf.convert(opened_img.filename)

    save_to = 'D:/Users/romeo/Converted-PDFS/imageToPDF.{}.pdf'.format(file_count)
    with open(save_to, "wb") as file_pointer:
        file_pointer.write(bytes_pdf)

def main():
    file_count = 0
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cam.isOpened():
        raise IOError("Webcam failed to open")

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                raise ValueError("Failed to capture screenshot from webcam")

            cv2.imshow('Original video', frame)

            key = cv2.waitKey(1)
            if key == 27:  # Press ESC to exit
                break 
            elif key == 32:  # Press SPACE to capture screenshot
                cv2.imshow('Captured Screenshot', frame)  # Show captured screenshot
                screenshot = frame.copy()  # Make a copy of the frame
                contours = find_contours(screenshot)

                # Display contours
                contour_img = np.zeros_like(screenshot)
                cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
                cv2.imshow('Contours', contour_img)

                birds_eye_view = get_birds_eye_view(screenshot, contours)

                # Display bird's eye view
                cv2.imshow("Bird's Eye View", birds_eye_view)
  
                save_as_pdf(birds_eye_view, file_count)  # Pass file_count as an argument
                file_count += 1  # Increment file_count after each screenshot

    finally:
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
