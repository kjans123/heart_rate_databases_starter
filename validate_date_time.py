def validate_date_time(date_time):
    type_date = type(date_time)
    if type_date is list:
        type_date_check = True
    else:
        raise TypeError("input date is not of list type")
    for i in range(len(date_time)):
        if isinstance(date_time[i], int) is False:
            raise TypeError("list element is not int")
    len_date = len(date_time)
    if len_date == 3:
        date_time.append(0)
        date_time.append(0)
        date_time.append(0)
        date_time.append(0)
    elif len_date == 4:
        date_time.append(0)
        date_time.append(0)
        date_time.append(0)
    elif len_date == 5:
        date_time.append(0)
        date_time.append(0)
    elif len_date == 6:
        date_time.append(0)
    elif len_date == 7:
        pass
    else:
        raise TypeError("Not enough arguments in date list")
    if len(str(date_time[0])) != 4:
        raise ValueError("year is not 4 digits long")
    else:
        check_len_year = True
    for i in list(range(1, 13)):
        if date_time[1] == i:
            check_month = True
            break
        else:
            check_month = False
    for i in list(range(1, 32)):
        if date_time[2] == i:
            check_day = True
            break
        else:
            check_day = False
    for i in list(range(0, 25)):
        if date_time[3] == i:
            check_hour = True
            break
        else:
            check_hour = False
    for i in list(range(0, 60)):
        if date_time[4] == i:
            check_min = True
            break
        else:
            check_min = False
    for i in list(range(0, 60)):
        if date_time[5] == i:
            check_sec = True
            break
        else:
            check_sec = False
    for i in list(range(0, 1000000)):
        if date_time[6] == i:
            check_micro = True
            break
        else:
            check_micro = False
    if check_month is not True:
        raise ValueError("month is not in range 1-12")
    if check_day is not True:
        raise ValueError("day is not in range 1-31")
    if check_hour is not True:
        raise ValueError("hour is not in range 0-24")
    if check_min is not True:
        raise ValueError("minute is not in range 0-60")
    if check_sec is not True:
        raise ValueError("second is not in range 0-60")
    if check_micro is not True:
        raise ValueError("microsecond is not in range of 0-1000000")
