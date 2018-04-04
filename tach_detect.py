def tach_detect(age, heart_rate):
    """"function that detects whether or not a users
        heart rate is tachycardic

        :param age: takes as input last recorded age
        :param heart_rate: takes as input calculated
                           heart rate over interval average
        :returns: message regarding whether or not heart rate
                  is tachycardic
    """
    tach_dict = {
                 (1, 2): 151,
                 (3, 4): 137,
                 (5, 7): 133,
                 (8, 11): 130,
                 (12, 15): 119,
                 (15, 200): 100
                 }
    for key, value in tach_dict.items():
        temp_range = list(range(key[0], (key[1]+1)))
        upper_limit = value
        for i in range(len(temp_range)):
            if age == temp_range[i]:
                if heart_rate > upper_limit:
                    return("heart rate IS tachycardic")
                else:
                    return("heart rate IS NOT tachycardic")
