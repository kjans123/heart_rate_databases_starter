def test_validate_date_time():
    from validate_date_time import validate_date_time
    import datetime
    import pytest
    with pytest.raises(TypeError, message = "Expecting TypeEror"):
        test_date_tuple = (2018, 3, 21)
        validate_date_time(test_date_tuple)
    with pytest.raises(TypeError, message = "Expecting Type Error"):
        test_date_string = [2018, "March", 21]
        validate_date_time(test_date_string)
    with pytest.raises(TypeError, message = "Expecting Type Error"):
        test_date_not_enough = [2018, 3]
        validate_date_time(test_date_not_enough)
    with pytest.raises(ValueError, message = "Expecting Value Error"):
        test_date_short_year = [201, 3, 21]
        validate_date_time(test_date_short_year)
    with pytest.raises(ValueError, message = "Expecting Value Error"):
        test_date_bad_month = [2018, 500, 21]
        validate_date_time(test_date_bad_month)
    with pytest.raises(ValueError, message = "Expecting Value Error"):
        test_date_bad_day = [2018, 3, 500]
        validate_date_time(test_date_bad_day)
    with pytest.raises(ValueError, message = "Expecting Value Error"):
        test_date_bad_hour = [2018, 3, 21, 500]
        validate_date_time(test_date_bad_hour)
    with pytest.raises(ValueError, message = "Expecting Value Error"):
        test_date_bad_min = [2018, 3, 21, 11, 500]
        validate_date_time(test_date_bad_min)
    with pytest.raises(ValueError, message = "Expecting Value Error"):
        test_date_bad_sec = [2018, 3, 21, 11, 50, 500]
        validate_date_time(test_date_bad_sec)
    with pytest.raises(ValueError, message = "Expecting Value Error"):
        test_date_bad_micro = [2018, 3, 21, 11, 50, 43, 999999999999]
        validate_date_time(test_date_bad_micro)
