import cv2
import os
import cv2
import json
import shutil
import numpy as np
from google.cloud import storage
from keras import layers
from keras.utils import image_dataset_from_directory
from keras.applications import vgg16
from keras.layers import Dense, GlobalAveragePooling2D
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.losses import SparseCategoricalCrossentropy
from keras.models import Model, load_model
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import ImageDataGenerator

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'credentials.json'
# gcs = storage.Client()
# bucket = gcs.bucket("ispy-bucket")

# if not os.path.isdir("data"):
#     os.mkdir("data")
# blobs = bucket.list_blobs()
# data_exist = False
# for blob in blobs:
#     if "images" in blob.name:
#         data_exist = True
#         person = blob.name.split("/")[0]
#         if not os.path.isdir(f"data/{person}"):
#             os.mkdir(f"data/{person}")
#         num = blob.name.split("/")[-1]  
#         blob.download_to_filename(f"data/{person}/{num}")

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

train_generator = train_datagen.flow_from_directory(
    './data',
    target_size=(224,224),
    color_mode='rgb',
    batch_size=32,
    class_mode='categorical',
    shuffle=True
)

num_classes = len(train_generator.class_indices.values())
print(list(train_generator.class_indices.keys()))
# base_model = vgg16.VGG16(
#     include_top=False,
#     input_shape=(224, 224, 3)
# ) 

# x = base_model.output
# x = GlobalAveragePooling2D()(x)
# x = Dense(1024, activation='relu')(x)
# x = Dense(1024, activation='relu')(x)
# x = Dense(512, activation='relu')(x)
# x = Dense(num_classes, activation='softmax')(x)

# new_model = Model(inputs = base_model.input, outputs = x)
# layer_num = 0
# for layer in new_model.layers[:19]:
#     if layer_num > 19:
#         layer.trainable = True
#     else:   
#         layer.trainable = False
#     layer_num += 1

# new_model.compile(
#     optimizer='Adam',
#     loss='categorical_crossentropy',
#     metrics=['accuracy']
# )

# new_model.fit(
#     train_generator,
#     batch_size = 1,
#     verbose = 1,
#     epochs = 12
# )

# new_model.save("./model.h5")









# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# model = load_model('model.h5') 
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(grey, 1.15, 7)    
#     people = ["BARACK OBAMA", "DONALD TRUMP"]
    
#     if len(faces) != 0:
#         for x, y, w, h in faces:
#             face = frame[y: y + h, x: x + w]
#             resized = cv2.resize(face, (224, 224))
#             img = image.img_to_array(resized)
#             img = np.expand_dims(img, axis=0)
#             img = preprocess_input(img)
            
#             prediction = model.predict(img)
#             print(prediction)
#             num = prediction[0].argmax()
#             person = people[num]
#             person = " ".join(person.split("_"))
            
#             color = [4, 138, 202]
#             font = cv2.FONT_HERSHEY_PLAIN
#             stroke = 5
#             cv2.rectangle(frame, (x, y), (x + w, y + h), color, stroke)
#             cv2.putText(frame, person, (x,y-5), font, 3.5, color, stroke, cv2.LINE_AA)
    
#     cv2.imshow('Test', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
