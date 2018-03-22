from flask import Flask, jsonify, request
import requests
import datetime
from pymodm import connect
import models
from main import add_heart_rate, create_user, print_user
from validate_date_time import validate_date_time
from check_for_user import Check_For_User
app = Flask(__name__)

def get_all_rates(user_email):
    connect("mongodb://vcm-3594.vm.duke.edu:27017/heart_rate_app")
    user = models.User.objects.raw({"_id": user_email}).first()
    heart_rate_list = user.heart_rate
    return heart_rate_list

def get_all_times(user_email):
    connect("mongodb://vcm-3594.vm.duke.edu:27017/heart_rate_app")
    user = models.User.objects.raw({"_id": user_email}).first()
    time_list = user.heart_rate_times
    return time_list

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
def disp_all_rates(user_email):
    heart_rate_list = get_all_rates(user_email)
    return_dict = {
        "user": user_email,
        "all_heart_rates": heart_rate_list
                  }
    return jsonify(return_dict)

@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def all_average(user_email):
    import statistics as st
    import json
    heart_rate_list = get_all_rates(user_email)
    all_average = st.mean(heart_rate_list)
    return_dict = {
        "user": user_email,
        "average": all_average
                   }
    return jsonify(return_dict)

@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_average():
    import statistics as st
    r = request.get_json()
    email = r["user_email"]
    input_date_time = r["date_time"]
    validate_date_time(input_date_time)
    time_list = get_all_times(email)
    for i in range(len(time_list)):
        if date_time <= time_list[i]:
            final_date_index = i
            break
    heart_rate_list = get_all_rates(email)
    interval_list = []
    for i in range(len(heart_rate_list)):
        if i <= final_date_index:
            interval_list.append(heart_rate_list[i])
        else:
            break
    interval_average_post = st.mean(interval_list)
    return_dict = {
        "user_email": email,
        "heart_rate_average_since": str(date_time),
        "heart_rate_average": interval_average_post
                  }
    return jsonify(return_dict)
