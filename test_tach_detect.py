def test_tach_detect():
    from tach_detect import tach_detect
    test_age = 25
    test_hr = 75
    test_message = tach_detect(test_age, test_hr)
    valid_message = "heart rate IS NOT tachycardic"
    assert test_message == valid_message
    test_age = 25
    test_hr = 200
    test_message = tach_detect(test_age, test_hr)
    valid_message = "heart rate IS tachycardic"
    assert test_message == valid_message
