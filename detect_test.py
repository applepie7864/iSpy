import cv2
import numpy as np
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'credentials.json'
gcs = storage.Client()
bucket = gcs.bucket("ispy-bucket")

def preprocess(file_path):
    """
        :type file_path: str
        :rtype: List[List[List[int]]] (numpy array)
                None, if face not found
    """
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(file_path)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey, 1.15, 7)

    if len(faces) == 0:
        exit()

    count = 0
    for x, y, w, h in faces: 
        face = img[y: y + h, x: x + w]
        resized = cv2.resize(face, (224, 224))
        cv2.imwrite("face.jpg", resized)

preprocess("413.jpg")
from keras.preprocessing import image

blob = bucket.blob("model.h5")
blob.download_to_filename("model.h5")

from keras.models import load_model
model = load_model('model.h5')

face = cv2.imread("face.jpg")
face = image.img_to_array(face)
face /= 255
face = np.expand_dims(face, axis=0)

preds = model.predict(face)
print(preds)