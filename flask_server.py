from flask import Flask, jsonify, request
import requests
import datetime
from pymodm import connect
import models
from main import add_heart_rate, create_user, print_user
from validate_date_time import validate_date_time
from check_for_user import Check_For_User
from find_first_date import find_first_date
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
    try:
        email = r["user_email"]
    except KeyError:
        return jsonify("no email input"), 400
    check_email = Check_For_User(email)
    if check_email.user_exists is False:
        raise LookupError(str(email)+ " was not found. Please re-enter")
    try:
        age = r["user_age"]
    except KeyError:
        return jsonify("no age input"), 400
    try:
        heart_rate = r["heart_rate"]
    except KeyError:
        return jsonify("no heart rate input"), 400
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
    check_email = Check_For_User(user_email)
    if check_email.user_exists is False:
        return jsonify(str(user_email)+ " not found"), 400
        raise LookupError(str(user_email)+ " was not found. Please re-enter")
    heart_rate_list = get_all_rates(user_email)
    return_dict = {
        "user": user_email,
        "all_heart_rates": heart_rate_list
                  }
    return jsonify(return_dict), 200

@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def all_average(user_email):
    import statistics as st
    import json
    check_email = Check_For_User(user_email)
    if check_email.user_exists is False:
        return jsonify(str(user_email)+ " not found"), 400
        raise LookupError(str(user_email)+ " was not found. Please re-enter")
    heart_rate_list = get_all_rates(user_email)
    all_average = st.mean(heart_rate_list)
    return_dict = {
        "user": user_email,
        "average": all_average
                   }
    return jsonify(return_dict), 200

@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_average():
    import statistics as st
    r = request.get_json()
    try:
        email = r["user_email"]
    except KeyError:
        return jsonify("no email input"), 400
    check_email = Check_For_User(email)
    if check_email.user_exists is False:
        raise LookupError(str(email)+ " was not found. Please re-enter"), 400
    try:
        input_date_time = r["date_time"]
    except KeyError:
        return jsonify("no date entered"), 400
    validate_date_time(input_date_time)
    date_time = datetime.datetime(input_date_time[0], input_date_time[1],
                                  input_date_time[2], input_date_time[3],
                                  input_date_time[4], input_date_time[5],
                                  input_date_time[6])
    time_list = get_all_times(email)
    heart_rate_list = get_all_rates(email)
    interval_list = find_first_date(date_time, time_list, heart_rate_list)
    try:
        interval_average_post = st.mean(interval_list)
        return_dict = {
            "user_email": email,
            "heart_rate_average_since": str(date_time),
            "heart_rate_average": interval_average_post
                       }
    except st.StatisticsError:
        interval_average_post = heart_rate_list[len(heart_rate_list)-1]
        return_dict = {
            "user_email": email,
            "heart_rate_average_since": str(date_time),
            "heart_rate_average": interval_average_post
                       }
    return jsonify(return_dict), 200
