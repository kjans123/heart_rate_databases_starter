from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import datetime
from pymodm import connect
import models
from main import add_heart_rate, create_user, print_user, get_all_users
from validate_date_time import validate_date_time
from check_for_user import Check_For_User
from find_first_date import find_first_date
app = Flask(__name__)
CORS(app)


def get_all_rates(user_email):
    """"function that gets all heart rates for user from mongo database
    """
    connect("mongodb://vcm-3594.vm.duke.edu:27017/heart_rate_app")
    user = models.User.objects.raw({"_id": user_email}).first()
    heart_rate_list = user.heart_rate
    return heart_rate_list


def get_all_times(user_email):
    """"function that gets all dates for user from mongo database
    """
    connect("mongodb://vcm-3594.vm.duke.edu:27017/heart_rate_app")
    user = models.User.objects.raw({"_id": user_email}).first()
    time_list = user.heart_rate_times
    return time_list


@app.route("/api/heart_rate/all_users", methods=["GET"])
def get_every_user():
    """"function that gets all users from mongo database
    """
    connect("mongodb://vcm-3594.vm.duke.edu:27017/heart_rate_app")
    user_list = get_all_users()
    return_dict = {
        "user_emails": user_list
                  }
    return jsonify(return_dict),200


@app.route("/api/heart_rate", methods=["POST"])
def add_new_hr():
    """"function that posts a new heart rate through URL to the mongo
        database for specified user
    """
    r = request.get_json()
    try:
        email = r["user_email"]
    except KeyError:
        return jsonify("no email input"), 400
        raise LookupError("no email input")
    check_email = Check_For_User(email)
    if check_email.user_exists is False:
        return jsonify(str(email) + " was not found. Please re-enter"), 400
        raise LookupError(str(user_email) + " was not found. Please re-enter")
    try:
        age = r["user_age"]
    except KeyError:
        return jsonify("no age input"), 400
        raise LookupError("no age input")
    try:
        heart_rate = r["heart_rate"]
    except KeyError:
        return jsonify("no heart rate input"), 400
        raise LookUpError("no heart rate input")
    curr_datetime = datetime.datetime.now()
    connect("mongodb://vcm-3594.vm.duke.edu:27017/heart_rate_app")
    add_heart_rate(email, heart_rate, curr_datetime, age)
    return_dict = {
        "user_email": str(email),
        "user_age": str(age),
        "heart_rate": str(heart_rate)
                }
    return jsonify(return_dict), 200


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def disp_all_rates(user_email):
    """"function that gets all heart rates for user from mongo
        database and outputs to URL web page
    """
    check_email = Check_For_User(user_email)
    if check_email.user_exists is False:
        return jsonify(str(user_email) + " not found"), 400
        raise LookupError(str(user_email) + " was not found. Please re-enter")
    heart_rate_list = get_all_rates(user_email)
    date_list = get_all_times(user_email)
    return_dict = {
        "user": user_email,
        "all_heart_rates": heart_rate_list,
        "all_times": date_list
                  }
    return jsonify(return_dict), 200


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def all_average(user_email):
    """"function that calculates average over all heart
        rates from mongo database for specified user and
        outputs to URL web page
    """
    import statistics as st
    import json
    check_email = Check_For_User(user_email)
    if check_email.user_exists is False:
        return jsonify(str(user_email) + " not found"), 400
        raise LookupError(str(user_email) + " was not found. Please re-enter")
    heart_rate_list = get_all_rates(user_email)
    all_average = st.mean(heart_rate_list)
    return_dict = {
        "user": user_email,
        "average": all_average
                   }
    return jsonify(return_dict), 200


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_average():
    """"function that POSTS specified date to URL web page
        and calculates user heart rate average from that
        specified date. Pulls heart rate and date data from mongo database.
        Also outputs whether or not inerval average is tachycardic
        based on users last recorded age
    """
    import statistics as st
    from tach_detect import tach_detect
    r = request.get_json()
    try:
        email = r["user_email"]
    except KeyError:
        return jsonify("no email input"), 400
        raise LookupError("no email input")
    check_email = Check_For_User(email)
    if check_email.user_exists is False:
        return jsonify(str(email) + " was not found. Please re-enter"), 400
        raise LookupError(str(user_email) + " was not found. Please re-enter")
    try:
        input_date_time = r["date_time"]
    except KeyError:
        return jsonify("no date entered"), 400
        raise LookupError("no date entered")
    try:
        validate_date_time(input_date_time)
    except (ValueError, TypeError) as error:
        return jsonify("date entered is invalid. Please re-type."), 400
    date_time = datetime.datetime(input_date_time[0], input_date_time[1],
                                  input_date_time[2], input_date_time[3],
                                  input_date_time[4], input_date_time[5],
                                  input_date_time[6])
    time_list = get_all_times(email)
    heart_rate_list = get_all_rates(email)
    interval_list = find_first_date(date_time, time_list, heart_rate_list)
    try:
        interval_average_post = st.mean(interval_list)
        user = models.User.objects.raw({"_id": email}).first()
        curr_age = user.age
        tach_test = tach_detect(curr_age, interval_average_post)
        return_dict = {
            "user_email": email,
            "heart_rate_average_since": str(date_time),
            "heart_rate_average": interval_average_post,
            "is_heart rate_tachycardic": str(tach_test)
                       }
    except st.StatisticsError:
        interval_average_post = heart_rate_list[len(heart_rate_list)-1]
        user = models.User.objects.raw({"_id": email}).first()
        curr_age = user.age
        tach_test = tach_detect(curr_age, interval_average_post)
        return_dict = {
            "user_email": email,
            "heart_rate_average_since": str(date_time),
            "heart_rate_average": interval_average_post,
            "is_heart rate_tachycardic": str(tach_test)
                       }
    return jsonify(return_dict), 200
