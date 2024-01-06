from PIL import Image
import numpy as np
import cv2
from keras.models import load_model
from keras.preprocessing import image

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = load_model('model.h5')
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        bw,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )

    if len(faces) > 0:
        for x, y, w, h in faces: 
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cropped = rgb[y: y + h, x: x + w]
            color = (0, 255, 0)
            stroke = 2
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, stroke)
            resized = cv2.resize(cropped, (224, 224))
            img = image.img_to_array(resized)
            img /= 255
            img = np.expand_dims(img, axis=0)
            prediction = model.predict(img)
            print(prediction)
            font = cv2.FONT_HERSHEY_SIMPLEX
            num = prediction[0].argmax()
            print(num)
            if num == 0:
                name = "Annie"
            elif num == 1:
                name = "Obama"
            color = (0, 255, 0)
            stroke = 2
            cv2.putText(frame, name, (x,y-5), font, 1, color, stroke, cv2.LINE_AA)

    cv2.imshow("iSpy", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"): 
        break      

cam.release()
cv2.destroyAllWindows()
