import numpy as np
import cv2
import os

# create dict for people in database + id / edit later for efficiency
people = {}
with open('./pairs.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split(': ')
        people[int(key)] = value

# define which recognizer algorithm we will use and the trained model we are using
model = cv2.face.LBPHFaceRecognizer_create()
model.read('./trainer.yml')

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
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )

    # draw a rectangle around each detected face from the frame
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
        id, confidence = model.predict(gray[y: y + h, x: x + w])
        print(id)
        print(people[id])
        print(confidence)
        if (confidence < 35): # define a threshold, 0 is a perfect match
            id = people[id]
        else:
            id = "unknown"

        # display detected name
        cv2.putText(frame, 
                    str(id), 
                    (x + 5, y - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1, 
                    (0, 255, 0), 
                    2
                   )
        
    cv2.imshow('iSpy', frame) # display frame
    
    # press 'ESC' to quit
    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

# clean up
cam.release()
cv2.destroyAllWindows()
