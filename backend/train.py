import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet import preprocess_input


# function to train the model
def train():
    imgs = ImageDataGenerator(preprocessing_function=preprocess_input)
    dataset = imgs.flow_from_directory('./db/imgs', target_size=(224,224), color_mode='rgb', batch_size=32, class_mode='categorical', shuffle=True)
    
    """
        :type: N/A
        :rtype: N/A
    """
    # get images
    # https://www.codemag.com/Article/2205081/Implementing-Face-Recognition-Using-Deep-Learning-and-Support-Vector-Machines
    # save temp_demo_recognizer.hdf5 to db
    return

if __name__ == '__main__':
    train()