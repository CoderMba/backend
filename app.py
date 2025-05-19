from flask import Flask, request
from flask_cors import CORS
import requests
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # enable CORS for all routes

@app.route("/")
def home():
    return "Backend is running!"


def get_geolocation(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
    except:
        return {}
    return {}

@app.route("/log", methods=["POST"])
def log():
    data = request.json
    if not data:
        return {"error": "No data"}, 400

    event = data.get('event')
    event_data = data.get('data')
    timestamp = data.get('timestamp') or datetime.utcnow().isoformat()

    # Get IP (from X-Forwarded-For)
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    user_agent = request.headers.get("User-Agent", "Unknown")
    geo = get_geolocation(ip)

    log_entry = {
        "timestamp": timestamp,
        "event": event,
        "data": event_data,
        "ip": ip,
        "user_agent": user_agent,
        "geo": geo
    }

    # Print to Render logs
    print(json.dumps(log_entry, indent=2))

    return {"status": "logged"}




@app.route("/view-logs", methods=["GET"])
def view_logs():
    try:
        with open("log.txt", "r") as f:
            return "<pre>" + f.read() + "</pre>"
    except FileNotFoundError:
        return "No logs yet."


