from flask import Flask, jsonify, request
import requests
import datetime
from pymodm import connect
from main import add_heart_rate, create_user, print_user
app = Flask(__name__)

@app.route("/new_heart_rate", methods=["POST"])
def add_new_hr():
    r = request.get_json()
    email = r["user_email"]
    age = r["user_age"]
    heart_rate = r["heart_rate"]
    curr_datetime = datetime.datetime.now()
    connect("mongodb://vcm-3594.vm.duke.edu:27017/heart_rate_app")
    add_heart_rate(email, heart_rate, curr_datetime)
    return_dict = {
        "user_email": str(email),
        "user_age": str(age),
        "heart_rate": str(heart_rate)
                }
    return jsonify(return_dict), 200

@app.route("/all_heart_rates/<name>", methods=["GET"])
def all_rates(name):
    connect("mongodb://vcm-3594.vm.duke.edu:27017/heart_rate_app")
    user = models.User.objects.raw({"_id": name}).first()
    return jsonify(user.heart_rate)
