import cv2
import numpy as np
from PIL import Image
import os

# path to database
dataset = 'dataset'

# define which recognizer algorithm we will use
model = cv2.face.LBPHFaceRecognizer_create()

# load the base classifier
faceCascade = cv2.CascadeClassifier('venv/lib/python3.11/site-packages/cv2/data/haarcascade_frontalface_default.xml')

def getData(path):
    # make list of paths to all images in the dataset
    image_paths = []
    for person in os.listdir(dataset):
        person_directory = os.path.join(dataset, person)
        for img in os.listdir(person_directory):
            image_path = os.path.join(person_directory, img)
            image_paths.append(image_path)

    

    
