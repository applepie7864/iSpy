import numpy as np
import cv2

# load the base classifier
faceCascade = cv2.CascadeClassifier('venv/lib/python3.11/site-packages/cv2/data/haarcascade_frontalface_default.xml')

# set video source to default webcam
cam = cv2.VideoCapture(0)
cam.set(3, 1280) # set width
cam.set(4, 720) # set height

while True:
    ret, frame = cam.read() # extracting a camera frame

    # detect objects based on supplied cascade and save as an array of faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        frame,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )

    # draw a rectangle around each detected face from the frame
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
        cv2.imshow('iSpy', frame) # display
    
    # press 'ESC' to quit
    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

# clean up
cam.release()
cv2.destroyAllWindows()
