from flask import Flask, request, render_template, Response
import shutil
from google.cloud import storage
import os
import json
import helpers
import cv2
from PIL import Image
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='./templates', static_folder='./static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Testing Endpoint.
@app.route("/")
def test():
    return "Flask Server Active!"

# Add User Endpoint.
@app.route("/add_user", methods=['POST'])
def add_user():
    fname = str(request.form['fname']).upper()
    lname = str(request.form['lname']).upper()
    email = str(request.form['email'])
    occupation = str(request.form['occupation'])
    location = str(request.form['location'])
    images = request.files.getlist("images")
    num_images = len(images)
    
    if helpers.user_exists(fname, lname):
        return "User already exists in the database.", 400
    else:
        count = 0
        for image in images:
            source = "processed_image.jpg"
            destination = f"{fname}_{lname}/images/{fname}_{lname}_{str(count)}.jpg"
            image = Image.open(image) 
            image.save(source) 
            processed_npimg = helpers.preprocess(source)
            if processed_npimg is None:
                continue
            cv2.imwrite(source, processed_npimg)
            helpers.upload_file(source, destination)
            count += 1
        os.remove(source)
        
        info = {}
        info["fname"] = fname
        info["lname"] = lname
        info["email"] = email
        info["occupation"] = occupation
        info["location"] = location
        info["num_images"] = count
        source = "add_user.json"
        destination = f"{fname}_{lname}/metadata.json"
        with open(source, "w") as f:
            json.dump(info, f, indent=4)
        helpers.upload_file(source, destination)
        os.remove(source)
        
        people_list = helpers.train()
        helpers.upload_file("model.h5", "model.h5")
        os.remove("model.h5")
        helpers.edit_metadata(people_list)    
        return "Added new user!", 201

# Remove User Endpoint.
@app.route("/remove_user", methods=['POST'])
def remove_user():
    fname = str(request.form['fname']).upper()
    lname = str(request.form['lname']).upper()
    
    if not helpers.user_exists(fname, lname):
        return "User does not exist in the database.", 400
    else:
        helpers.delete_person_folder(fname, lname)
        people_list = helpers.train()
        helpers.upload_file("model.h5", "model.h5")
        os.remove("model.h5")
        helpers.edit_metadata(people_list) 
        return "User has been removed!", 201

# Edit User Endpoint.
@app.route("/edit_user", methods=["POST"])
def edit_user():  
    fname = str(request.form['fname']).upper()
    lname = str(request.form['lname']).upper()
    option = str(request.form['option'])
    value = str(request.form['value'])
    
    if not helpers.user_exists(fname, lname):
        return "User does not exist in the database.", 400
    else:
        helpers.edit_user_field(fname, lname, option, value)
        return f"{option} updated to {value} for {fname} {lname}.", 200

# Add Images Endpoint.
@app.route("/add_images", methods=["POST"])
def add_images():
    fname = str(request.form['fname']).upper()
    lname = str(request.form['lname']).upper()
    images = request.files.getlist("images")
    
    if not helpers.user_exists(fname, lname):
        return "User does not exist in the database.", 400
    else:
        count = helpers.get_num_images(fname, lname)
        for image in images:
            source = "add_images.jpg"
            destination = f"{fname}_{lname}/images/{fname}_{lname}_{str(count)}.jpg"
            image = Image.open(image) 
            image.save(source) 
            processed_npimg = helpers.preprocess(source)
            if processed_npimg is None:
                continue
            cv2.imwrite(source, processed_npimg)
            helpers.upload_file(source, destination)
            count += 1
        os.remove(source)
        helpers.edit_user_field(fname, lname, "num_images", count)
        people_list = helpers.train()
        helpers.upload_file("model.h5", "model.h5")
        os.remove("model.h5")
        helpers.edit_metadata(people_list) 
        return "Added images.", 201
    
@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/video_feed')
def video_feed():
    return Response(helpers.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/all_users', methods=["GET"])
@cross_origin()
def all_users():
    data = helpers.get_all_users()
    return data, 200

# http://192.168.64.3
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
