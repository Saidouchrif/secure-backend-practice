import os

def load_user(username):
    fake_db = {
        "admin": {
            "password": os.getenv("ADMIN_PASSWORD"),
            "role": "admin"
        },
        "user": {
            "password": os.getenv("USER_PASSWORD"),
            "role": "user"
        }
    }
    return fake_db.get(username)
