from pymodm import connect
import models
import datetime


def add_heart_rate(email, heart_rate, time, age):
    user = models.User.objects.raw({"_id": email}).first()
    # Get the first user where _id=email
    user.heart_rate.append(heart_rate)
    # Append the heart_rate to the user's list of heart rates
    user.heart_rate_times.append(time)
    # append the current time to the user's list of heart rate times
    user.age = age
    # update users current age
    user.save()
    # save the user to the database


def get_all_users():
    result = []
    for u in models.User.objects.all():
        result.append(u.email)
    return(result)


def create_user(email, age, heart_rate):
    u = models.User(email, age, [], [])
    # create a new User instance
    u.heart_rate.append(heart_rate)
    # add initial heart rate
    u.heart_rate_times.append(datetime.datetime.now())
    # add initial heart rate time
    u.save()
    # save the user to the database


def print_user(email):
    user = models.User.objects.raw({"_id": email}).first()
    # Get the first user where _id=email
    print(user.email)
    print(user.heart_rate)
    print(user.heart_rate_times)
    print(user.age)

if __name__ == "__main__":
    connect("mongodb://vcm-3594.vm.duke.edu:27017/heart_rate_app")
    # open up connection to db
    # create_user(email="suyash@suyashkumar.com", age=24, heart_rate=60)
    # we should only do this once, otherwise will overwrite existing user
    # add_heart_rate("suyash@suyashkumar.com", 60, datetime.datetime.now())
    print_user("kj123@duke.edu")
