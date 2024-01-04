from flask import Flask, request
import shutil
from google.cloud import storage
import os
import json

app = Flask(__name__)

# Testing Endpoint.
@app.route("/")
def test():
    return "Flask Server Active!"

# Add User Endpoint.
@app.route("/add_user", methods=['POST'])
def add_user():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'credentials.json'
    gcs = storage.Client()
    bucket = gcs.bucket("ispy-bucket")
    
    fname = str(request.form['fname']).upper()
    lname = str(request.form['lname']).upper()
    email = str(request.form['email'])
    occupation = str(request.form['occupation'])
    location = str(request.form['location'])
    images = request.files.getlist("images")
    
    count = 0
    for image in images:
        image.save("tmp.jpg")
        destination = f"{fname}_{lname}/images/{str(count)}.jpg"
        blob = bucket.blob(destination)
        blob.upload_from_filename("tmp.jpg")
        count += 1
    
    info = {}
    info["fname"] = fname
    info["lname"] = lname
    info["email"] = email
    info["occupation"] = occupation
    info["location"] = location
    info["num_images"] = count
    with open("tmp.json", "w") as f:
        json.dump(info, f, indent=4)
    blob = bucket.blob(f"{fname}_{lname}/metadata.json")
    blob.upload_from_filename("tmp.json")
    
    blob = bucket.get_blob("metadata.json")
    downloaded_json = json.loads(blob.download_as_text(encoding="utf-8"))
    person_name = f"{fname}_{lname}"
    if person_name not in downloaded_json["people"]:
        downloaded_json["people"].append(person_name)
        downloaded_json["num_people"] += 1
        with open("tmp.json", "w") as f:
            json.dump(downloaded_json, f, indent=4)
        blob = bucket.blob("metadata.json")
        blob.upload_from_filename("tmp.json")
    
    return "Added User", 201

# Remove User Endpoint.
@app.route("/remove_user", methods=['POST'])
def remove_user():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'credentials.json'
    gcs = storage.Client()
    bucket = gcs.bucket("ispy-bucket")
    
    fname = str(request.form['fname']).upper()
    lname = str(request.form['lname']).upper()
    
    blobs = bucket.list_blobs(prefix=f'{fname}_{lname}')
    for blob in blobs:
        blob.delete()
    
    blob = bucket.get_blob("metadata.json")
    downloaded_json = json.loads(blob.download_as_text(encoding="utf-8"))
    person_name = f"{fname}_{lname}"
    if person_name in downloaded_json["people"]:
        downloaded_json["people"].remove(person_name)
        downloaded_json["num_people"] -= 1
        with open("tmp.json", "w") as f:
            json.dump(downloaded_json, f, indent=4)
        blob = bucket.blob("metadata.json")
        blob.upload_from_filename("tmp.json")
    
    return "Removed User", 200

# Edit User Endpoint.
@app.route("/edit_user", methods=["POST"])
def edit_user():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'credentials.json'
    gcs = storage.Client()
    bucket = gcs.bucket("ispy-bucket")
    
    fname = str(request.form['fname']).upper()
    lname = str(request.form['lname']).upper()
    option = str(request.form['option'])
    value = str(request.form['value'])
    
    file = f"{fname}_{lname}/metadata.json"
    blob = bucket.get_blob(file)
    downloaded_json = json.loads(blob.download_as_text(encoding="utf-8"))
    downloaded_json[option] = value
    with open("tmp.json", "w") as f:
        json.dump(downloaded_json, f, indent=4)
    blob = bucket.blob(file)
    blob.upload_from_filename("tmp.json")
    
    return "Edited User", 200

# Training Endpoint.
@app.route("/train")
def train():
    return "Training!"

# Detection Endpoint.
@app.route("/detect")
def detect():
    return "Detecting!"

# http://192.168.64.3
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
