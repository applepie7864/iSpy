import cv2
import numpy as np
from PIL import Image
import os

# path to database
path = 'dataset'

# define which recognizer algorithm we will use
model = cv2.face.LBPHFaceRecognizer_create()

# load the base classifier
faceCascade = cv2.CascadeClassifier('venv/lib/python3.11/site-packages/cv2/data/haarcascade_frontalface_default.xml')

def getData(dataset):   
    face_samples = []
    ids = []

    # make list of paths to all images in the dataset
    image_paths = []
    for person in os.listdir(dataset):
        person_directory = os.path.join(dataset, person)
        for img in os.listdir(person_directory):
            image_path = os.path.join(person_directory, img)
            image_paths.append(image_path)
    
    # edit images for training
    for image in image_paths:
        grayscale_img = Image.open(image).convert('L') # convert to grayscale
        numpy_img = np.array(grayscale_img, 'uint8') # convert to numpy array

        id = 0 # hardcoded for now, 0 corresponds to bill gates, change later ***
        faces = faceCascade.detectMultiScale(numpy_img) # detect faces

        # extract faces and corresponding label
        for (x, y, w, h) in faces:
            face_samples.append(numpy_img[y: y + h, x: x + w])
            ids.append(id)

    return face_samples, ids

# train the model on given dataset and save as a yml file
faces, ids = getData(path)
model.train(faces, np.array(ids))
model.save('./trainer.yml')

    

    

    
