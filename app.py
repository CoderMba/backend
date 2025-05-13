from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/log", methods=["POST"])
def log():
    data = request.json
    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()} - {data}\n")
    return {"status": "logged"}
