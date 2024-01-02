from flask import Flask, request

app = Flask(__name__)

# Testing Endpoint.
@app.route("/")
def test():
    return "Flask Server Active!"

# Add User Endpoint.
@app.route("/add_user", methods=['GET', 'POST'])
def add_user():
    return "Add User!"

# Remove User Endpoint.
@app.route("/remove_user")
def remove_user():
    return "Remove User!"

# Edit User Endpoint.
@app.route("/edit_user")
def edit_user():
    return "Edit User!"

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
