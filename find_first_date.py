def find_first_date(date_time, time_list, heart_rate_list):
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
        else:
            break
    return interval_list
