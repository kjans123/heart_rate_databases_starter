def test_check_for_user(monkeypatch):
    from main import create_user
    from pymodm import connect
    import models
    import datetime
    from check_for_user import Check_For_User
    newClass = Check_For_User("kj123@duke.edu")
    assert newClass.user_exists is True
    newClass2 = Check_For_User("n@n.com")
    assert newClass2.user_exists is False
