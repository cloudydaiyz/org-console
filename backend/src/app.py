from controller import update_membership_logs

# Run this app by running:
# python3 -m flask --app src/app run --port 5001 --host 0.0.0.0

# NOTE: Need to make flask app publicly available to
# interact with the frontend
# https://flask.palletsprojects.com/en/3.0.x/quickstart/
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/updatelogs")
def update_logs():
    if(update_membership_logs()):
        data = { 
            "result" : "Successfully updated logs"
        } 
        return jsonify(data) 
    else:
        return "Something went wrong"