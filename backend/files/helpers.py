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

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'credentials.json'
gcs = storage.Client()
bucket = gcs.bucket("ispy-bucket")

# generate frame by frame from camera
def gen_frames():
    """
        :type n/a
        :rtype: n/a
    """
    cam = cv2.VideoCapture(0)
    blob = bucket.blob("model.h5")
    blob.download_to_filename("model.h5")
    blob = bucket.get_blob("metadata.json")
    downloaded_json = json.loads(blob.download_as_text(encoding="utf-8"))
    people = downloaded_json["people"]
    model = load_model('model.h5') 
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    while True:
        ret, frame = cam.read() 
        frame = recognize_faces(frame, people, model, face_cascade)
        if ret:
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

# recognizes faces and draws on frame
def recognize_faces(frame, people, model, face_cascade):
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey, 1.15, 7)    
    
    if len(faces) != 0:
        for x, y, w, h in faces:
            face = frame[y: y + h, x: x + w]
            resized = cv2.resize(face, (224, 224))
            img = image.img_to_array(resized)
            img /= 255
            img = np.expand_dims(img, axis=0)
            
            prediction = model.predict(img)
            print(prediction)
            num = prediction[0].argmax()
            person = people[num]
            person = " ".join(person.split("_"))
            
            color = [4, 138, 202]
            font = cv2.FONT_HERSHEY_PLAIN
            stroke = 5
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, stroke)
            cv2.putText(frame, person, (x,y-5), font, 3.5, color, stroke, cv2.LINE_AA)
    frame = cv2.flip(frame, 1)
    return frame

# detect face and resize and image
def preprocess(file):
    """
        :type file_path: str
        :rtype: List[List[List[int]]] (numpy array)
                None, if face not found
    """
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(file)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey, 1.15, 7)

    if len(faces) != 1:
        return None
    
    x, y, w, h = faces[0]
    face = img[y: y + h, x: x + w]
    resized = cv2.resize(face, (224, 224))
    return resized

# determine if user exists
def user_exists(fname, lname):
    """
        :type fname: str
              lname: str
        :rtype: bool
    """
    blob = bucket.get_blob("metadata.json")
    downloaded_json = json.loads(blob.download_as_text(encoding="utf-8"))
    person_name = f"{fname.upper()}_{lname.upper()}"
    if person_name in downloaded_json["people"]:
        return True
    else:
        return False

# determines how many people are currently in the bucket
def get_num_people():
    """
        :type n/a
        :rtype: int
    """
    blob = bucket.get_blob("metadata.json")
    downloaded_json = json.loads(blob.download_as_text(encoding="utf-8"))
    num_people = downloaded_json["num_people"]
    return num_people

# edits people and num_people key values in metadata.json
def edit_metadata(people):
    """
        :type people: List[str]
        :rtype: n/a
    """
    num_people = len(people)
    blob = bucket.get_blob("metadata.json")
    downloaded_json = json.loads(blob.download_as_text(encoding="utf-8"))
    downloaded_json["num_people"] = num_people
    downloaded_json["people"] = people
    with open("edit_metadata.json", "w") as f:
        json.dump(downloaded_json, f, indent=4)
    blob = bucket.blob("metadata.json")
    blob.upload_from_filename("edit_metadata.json")
    os.remove("edit_metadata.json")

# edits values found in metadata of a specific user
def edit_user_field(fname, lname, option, value):
    """
        :type fname: str
              lname: str
              option: one of "location", "occupation", "email", "num_images"
              value: str, int
        :rtype: n/a
    """
    file = f"{fname.upper()}_{lname.upper()}/metadata.json"
    blob = bucket.get_blob(file)
    downloaded_json = json.loads(blob.download_as_text(encoding="utf-8"))
    downloaded_json[option] = value
    with open("edit_user_field.json", "w") as f:
        json.dump(downloaded_json, f, indent=4)
    blob = bucket.blob(file)
    blob.upload_from_filename("edit_user_field.json")
    os.remove("edit_user_field.json")

# train custom face recognition model on dataset
def train():
    """
        :type n/a
        :rtype: List[str]
    """
    if not os.path.isdir("data"):
        os.mkdir("data")
    blobs = bucket.list_blobs()
    for blob in blobs:
        if "images" in blob.name:
            person = blob.name.split("/")[0]
            if not os.path.isdir(f"data/{person}"):
                os.mkdir(f"data/{person}")
            num = blob.name.split("/")[-1]  
            blob.download_to_filename(f"data/{person}/{num}")
        
    train_set = image_dataset_from_directory(
        "./data",
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(224, 224),
        batch_size=32
    )
    val_set = image_dataset_from_directory(
        "./data",
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(224, 224),
        batch_size=32
    )
    class_names = train_set.class_names
    num_classes = len(class_names)
    normalization = layers.Rescaling(1./255)
    train_set = train_set.map(lambda x, y: (normalization(x), y))
    val_set = val_set.map(lambda x, y: (normalization(x), y))
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
    new_model.compile(
        optimizer="Adam",
        loss=SparseCategoricalCrossentropy(),
        metrics=["accuracy"]
    ) 
    early_stop = EarlyStopping(monitor='val_loss', patience=3)
    checkpoint = ModelCheckpoint("model.h5", monitor="accuracy", save_best_only=True)
    new_model.fit(
        train_set,
        batch_size = 32,
        epochs = 10,
        callbacks=[early_stop, checkpoint],
        validation_data=val_set,
        shuffle=True
    )
    shutil.rmtree("./data")
    return class_names

# uploads a file to gcs bucket at a specific file path
def upload_file(source, destination):
    """
        :type source: str
              destination: str
        :rtype: n/a
    """
    blob = bucket.blob(destination)
    blob.upload_from_filename(source)

# downloads a file from gcs bucket to local directory 
def get_file(source, destination):
    """
        :type source: str
              destination: str
        :rtype: n/a
    """
    blob = bucket.blob(source)
    blob.download_to_filename(destination)
   
# deletes folder in gcs for a specified person
def delete_person_folder(fname, lname):
    """
        :type fname: str
              lname: str
        :rtype: n/a
    """
    blobs = bucket.list_blobs(prefix=f'{fname}_{lname}')
    for blob in blobs:
        blob.delete()
        
# determines how many images for a person
def get_num_images(fname, lname):
    """
        :type fname: str
              lname: str
        :rtype: int
    """
    file = f"{fname.upper()}_{lname.upper()}/metadata.json"
    blob = bucket.get_blob(file)
    downloaded_json = json.loads(blob.download_as_text(encoding="utf-8"))
    num = downloaded_json["num_images"]
    return num

# get all users in database and their corresponding metadata
def get_all_users():
    """
        :type n/a
        :rtype: Dict
    """
    blob = bucket.get_blob("metadata.json")
    downloaded_json = json.loads(blob.download_as_text(encoding="utf-8"))
    people = downloaded_json["people"]
    data = []
    for person in people:
        name = " ".join(person.split("_"))
        blob2 = bucket.get_blob(f"{person}/metadata.json")
        downloaded_json2 = json.loads(blob2.download_as_text(encoding="utf-8"))
        data.append(downloaded_json2) 
    return data