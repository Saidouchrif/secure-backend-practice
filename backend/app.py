import os
import datetime
import subprocess
import hashlib
from flask import Flask, request, jsonify
import jwt
from utils import load_user

app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRES_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRES_MIN"))

def create_token(username, role):
    payload = {
        "sub": username,
        "role": role,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRES_MIN)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = load_user(data.get("username"))
    if not user or user["password"] != data.get("password"):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_token(data["username"], user["role"])
    return jsonify({"token": token})

@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return result

@app.route("/hash")
def hash_pwd():
    pwd = request.args.get("pwd", "admin")
    return hashlib.md5(pwd.encode()).hexdigest()

@app.route("/hello")
def hello():
    name = request.args.get("name", "user")
    return f"<h1>Hello {name}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
