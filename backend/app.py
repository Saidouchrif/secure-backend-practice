import os
import datetime
import jwt
import bcrypt
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import load_user

load_dotenv()

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://127.0.0.1:5500",
                "http://localhost:5500",
                "http://127.0.0.1:5000",
                "http://localhost:5000"
            ]
        }
    }
)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ACCESS_TOKEN_EXPIRES_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRES_MIN", 60))


def create_token(username, role):
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": username,
        "role": role,
        "iat": now,
        "exp": now+ datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRES_MIN),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def get_current_user():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None, jsonify({"error": "Missing token"}), 401

    token = auth.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload, None, None
    except jwt.ExpiredSignatureError:
        return None, jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return None, jsonify({"error": "Invalid token"}), 401


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = load_user(data.get("username"))

    if not user or user["password"] != data.get("password"):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_token(data["username"], user["role"])
    return jsonify({"token": token})


@app.route("/profile")
def profile():
    payload, err, code = get_current_user()
    if err:
        return err, code

    return jsonify({
        "username": payload["sub"],
        "role": payload["role"],
        "message": "Profile OK"
    })


@app.route("/me")
def me():
    payload, err, code = get_current_user()
    if err:
        return err, code

    return jsonify(payload)


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)
