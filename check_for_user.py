def check_user_email():
    from main import create_user
    from pymodm import connect
    import models
    import datetime
    """"function that checks to see if user exists. If user does exist,
    returns True for later use. If user does not exists, asks caller
    if they would like to create new user.
    """
    init_prompt = input("Please enter user email: ")
    try:
        user = models.User.objects.raw({"_id": init_prompt}).first()
        user_exists = True
    except:
        new_user_error_prompt = input("User " + init_prompt + " not found. \
Would you like to create new user with that email (Enter y or n)? ")
        if new_user_error_prompt == "y":
            new_user_error_age = input("Please enter age for user.")
            new_user_error_hr = input("Please enter initial heart-rate \
for user")
            create_user(init_prompt, new_user_error_age, new_user_error_hr)
            user_exists = True
        if new_user_error_prompt == "n":
            print("please re-enter user email")
            user_exists = False
            return user_exists
