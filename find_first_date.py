def find_first_date(date_time, time_list, heart_rate_list):
    """" function that searchs through list of dates and
    and captures the index of the first date that is greater
    than the entered date. Uses this to get all heart rates after
    and on that particular date index

    :param date_time: takes as input a user entered date
    :param time_list: takes as input a time_list (normally from
                      a database) of all dates over which a
                      heart rate was captured
    :param heart_rate_list: takes as input all heart rates entered
                            for a particular patient
    :returns interval_list: returns list of heart rates associated
                            with the entered date and onwards
    """
    final_date_index = None
    for i in range(len(time_list)):
        if date_time <= time_list[i]:
            final_date_index = i
            break
    if final_date_index == None:
        raise ValueError("No heart rate data found since entered date")
    interval_list = []
    for i in range(len(heart_rate_list)):
        if i >= final_date_index:
            interval_list.append(heart_rate_list[i])
    return interval_list
