import os
import cv2
import numpy as np
from keras import layers
from keras.utils import image_dataset_from_directory
from keras.applications import vgg16
from keras.layers import Dense, GlobalAveragePooling2D
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.losses import SparseCategoricalCrossentropy
from keras.models import Model

# face detection crop
for root, dirs, files in os.walk("./data"):
    for file in files:
        file_path = os.path.join(root, file)
        print(file_path)
        
        if not "jpg" in file_path and not "png" in file_path:
            os.remove(file_path)
            continue
        
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        img = cv2.imread(file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.15, 7)
        
        if len(faces) != 1:
            os.remove(file_path)
            continue
        
        for (x, y, w, h) in faces:
            face = img[y: y + h, x: x + w]
            resize = cv2.resize(face, (224, 224))
            cv2.imwrite(file_path, resize)
            break

# define datasets
train = image_dataset_from_directory(
    "./data",
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(224, 224),
    batch_size=32
)

val = image_dataset_from_directory(
    "./data",
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(224, 224),
    batch_size=32
)

class_names = train.class_names
num_classes = len(class_names)
print(class_names)

# data augmentation
normalization = layers.Rescaling(1./255)
train = train.map(lambda x, y: (normalization(x), y))
val = val.map(lambda x, y: (normalization(x), y))
      
# build the model
base_model = vgg16.VGG16(
    include_top=False,
    input_shape=(224, 224, 3)
) 

for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dense(1024, activation='relu')(x)
x = Dense(512, activation='relu')(x)
x = Dense(num_classes, activation='softmax')(x)

new_model = Model(inputs=base_model.input, outputs=x)
for (i, layer) in enumerate(new_model.layers):
    print(str(i) + ": " + layer.__class__.__name__ + ", " + str(layer.trainable))

new_model.compile(
    optimizer="Adam",
    loss=SparseCategoricalCrossentropy(),
    metrics=["accuracy"]
) 

early_stop = EarlyStopping(monitor='val_loss', patience=3)
checkpoint = ModelCheckpoint("model.h5", monitor="accuracy", save_best_only=True)

new_model.fit(
    train,
    batch_size = 32,
    epochs = 10,
    callbacks=[early_stop, checkpoint],
    validation_data=val,
    shuffle=True
) 

        
    
        