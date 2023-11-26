import os
import cv2
for file in os.listdir("test-images/elon-musk"):
    img = cv2.imread("test-images/elon-musk/" + file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faceCascade = cv2.CascadeClassifier('backend/haarcascade_frontalface_default.xml')
    faces = faceCascade.detectMultiScale(
        img,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    if len(faces) != 0:
        x = faces[0][0]
        y = faces[0][1]
        w = faces[0][2]
        h = faces[0][3]
        cropped = img[y: y + h, x: x + w]
        resized = cv2.resize(cropped, (224, 224))
        cv2.imwrite("test-images/elon-musk/" + file, resized)