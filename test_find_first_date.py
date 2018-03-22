def test_find_first_date():
    from find_first_date import find_first_date
    import pytest
    import datetime
    init_date = datetime.datetime(2018, 3, 19)
    tues_date = datetime.datetime(2018, 3, 20)
    wed_date = datetime.datetime(2018, 3, 21)
    thu_date = datetime.datetime(2018, 3, 22)
    fri_date = datetime.datetime(2018, 3, 23)
    sat_date = datetime.datetime(2018, 3, 24)
    sun_date = datetime.datetime(2018, 3, 25)
    time_list = (init_date, tues_date, wed_date, thu_date,
                 fri_date, sat_date, sun_date)
    test_date = sat_date
    test_heart_rate_list = [75,74,80,85,70,71,73]
    interval_list = find_first_date(test_date, time_list, test_heart_rate_list)
    assert interval_list == [71, 73]

def test_correct_excp():
    from find_first_date import find_first_date
    import pytest
    import datetime
    init_date = datetime.datetime(2018, 3, 19)
    tues_date = datetime.datetime(2018, 3, 20)
    wed_date = datetime.datetime(2018, 3, 21)
    thu_date = datetime.datetime(2018, 3, 22)
    fri_date = datetime.datetime(2018, 3, 23)
    sat_date = datetime.datetime(2018, 3, 24)
    sun_date = datetime.datetime(2018, 3, 25)
    time_list = (init_date, tues_date, wed_date, thu_date,
                 fri_date, sat_date, sun_date)
    test_date = datetime.datetime(2019, 12, 19)
    test_heart_rate_list = [75,74,80,85,70,71,73]
    with pytest.raises(ValueError, message = "Expecting ValueError"):
        interval_list = find_first_date(test_date, time_list, test_heart_rate_list)
