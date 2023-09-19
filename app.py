import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__) # create an app instance of Flask app

app.secret_key = os.random(12) # set a secret key for the Flask application

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # define max file size

path = os.getcwd() # get current working directory

uploaded_folder = os.path.join(path, 'dataset/test') # store uploaded videos here, edit later

os.mkdir(uploaded_folder) # create uploaded_folder path

app.config['UPLOAD_FOLDER'] = uploaded_folder # edit config path