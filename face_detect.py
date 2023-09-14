import numpy as np
import cv2

# set video source to default webcam
cam = cv2.VideoCapture(0)
cam.set(3, 1280) # set width
cam.set(4, 720) # set height

while True:
    ret, frame = cam.read() # extracting a camera frame
    cv2.imshow('frame', frame) # displaying the frame
    
    # press 'ESC' to quit
    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

# clean up
cam.release()
cv2.destroyAllWindows()
