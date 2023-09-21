import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__) # create instance
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB is the max file size

# Get path to database
path = os.getcwd()
database = os.path.join(path, 'dataset')

# Allowed image extensions, add more later
ALLOWED_EXTENSIONS = set(['jpg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/', methods=['POST'])
def process_form():
    # make folder for new person if dne
    fname = request.form['first-name'].replace(" ", "").lower()
    lname = request.form['last-name'].replace(" ", "").lower()
    full_name = fname + "-" + lname
    destination_folder = os.path.join(database, full_name)
    if not os.path.isdir(destination_folder):
        os.mkdir(destination_folder)
    app.config['UPLOAD_FOLDER'] = destination_folder

    # add files to folder
    files = request.files.getlist('files[]')
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # clean the filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # train with newly loaded data
    subprocess.run(['python3', 'training_script.py'])

    # detect faces
    subprocess.run(['python3', 'face_detect.py'])

    return redirect('/')

if __name__ == "__main__":
    app.run()
