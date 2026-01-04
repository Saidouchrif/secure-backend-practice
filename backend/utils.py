def load_user(username):
    fake_db = {
        "admin": {"password": "1234", "role": "admin"},
        "user": {"password": "pass", "role": "user"}
    }
    return fake_db.get(username)
