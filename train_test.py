from google.cloud import storage
import os
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image
from keras.applications import vgg16
from keras.layers import BatchNormalization
from keras.layers import Dense, Dropout
from keras.models import Model
from keras.callbacks import EarlyStopping, ModelCheckpoint
import shutil

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'credentials.json'
gcs = storage.Client()
bucket = gcs.bucket("ispy-bucket")

if not os.path.isdir("data_dir"):
    os.mkdir("data_dir")
blobs = bucket.list_blobs()
for blob in blobs:
    if "images" in blob.name:
        person = blob.name.split("/")[0]
        if not os.path.isdir(f"data_dir/{person}"):
            os.mkdir(f"data_dir/{person}")
        num = blob.name.split("/")[-1]
        blob.download_to_filename(f"data_dir/{person}/{num}")

facecascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

id = 0
labels = {}

for root, dirs, files in os.walk("./data_dir"):
    for file in files:
        img_path = os.path.join(root, file)
        label = img_path.split("/")[-2]
        if not label in labels:
            labels[id] = label
            id += 1
            
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        norm_img = np.zeros((gray_img.shape[0], gray_img.shape[1]))
        img = cv2.normalize(gray_img, norm_img, 0, 255, cv2.NORM_MINMAX)
        img_array = np.array(img, "uint8")
        
        faces = facecascade.detectMultiScale(img, scaleFactor=1.15, minNeighbors=10)
        if len(faces) != 1:
            os.remove(img_path)
            continue

        for (x, y, w, h) in faces:
            dimensions = (224, 224)
            roi = img_array[y: y + h, x: x + w]
            resized_img = cv2.resize(roi, dimensions)
            img_array = np.array(resized_img, "uint8")
            
            os.remove(img_path)
            face_img = Image.fromarray(img_array)
            face_img.save(img_path)
            break

datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    fill_mode='nearest',
    brightness_range=[0.8, 1.2],
    validation_split=0.2
)

train_generator = datagen.flow_from_directory(
    './data_dir',
    target_size=(224,224),
    color_mode='rgb',
    batch_size=25,
    class_mode='categorical',
    shuffle=True,
    subset="training"
)
print(train_generator.class_indices.keys())

validation_generator = datagen.flow_from_directory(
    './data_dir',
    subset='validation'
)

base_model = vgg16.VGG16(
    include_top=False,
    pooling='max',
    input_shape=(224, 224, 3)
)

new_layer1 = Dense(256, activation="relu")(base_model.output)
new_layer2 = Dropout(rate=0.5)(new_layer1)
new_layer3 = Dense(128, activation="relu")(new_layer2)
new_layer4 = Dropout(rate=0.5)(new_layer3)
new_layer5 = BatchNormalization()(new_layer4)
new_layer6 = Dense(2, activation="softmax")(new_layer5)

model = Model(base_model.input, new_layer6)
for i in range(len(base_model.layers)):
    model.layers[i].trainable = False
    
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

early_stop = EarlyStopping(monitor='val_loss', patience=3)
checkpoint = ModelCheckpoint("model.h5", monitor="accuracy", save_best_only=True)

model.fit(
    train_generator,
    verbose = 1,
    epochs = 20,
    callbacks=[early_stop, checkpoint],
    validation_data=validation_generator
)

# shutil.rmtree("./data_dir")