from flask import Flask, jsonify, request
import requests
import datetime
from pymodm import connect
import models
from main import add_heart_rate, create_user, print_user
app = Flask(__name__)

@app.route("/api/heart_rate", methods=["POST"])
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

@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def all_rates(user_email):
    connect("mongodb://vcm-3594.vm.duke.edu:27017/heart_rate_app")
    user = models.User.objects.raw({"_id": user_email}).first()
    heart_rate_list = user.heart_rate
    #all_average = st.mean(heart_rate_list)
    return_dict = {
        "user": user_email,
        "all_heart_rates": heart_rate_list
                  }
    return jsonify(return_dict)

@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def all_average(user_email):
    import statistics as st
    import json
    heart_rate_array = all_rates(user_email)
    data = json.loads(heart_rate_array)
    all_average = st.mean(data)
    return_dict = {
        "user": user_email,
        "average": all_average
                   }
    return jsonify(return_dict)
