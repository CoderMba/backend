from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend is running!"

from flask import Flask, request
import json
import requests
from datetime import datetime



def get_geolocation(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country"),
                "loc": data.get("loc"),  # latitude,longitude
                "org": data.get("org"),
                "postal": data.get("postal"),
            }
    except Exception as e:
        print(f"Geo lookup failed: {e}")
    return {}

@app.route("/log", methods=["POST"])
def log():
    data = request.json
    event = data.get('event')
    event_data = data.get('data')
    timestamp = data.get('timestamp') or datetime.utcnow().isoformat()

    # IP address
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    # User-Agent (device info)
    user_agent = request.headers.get("User-Agent", "Unknown")

    # Get geolocation data
    geo_data = get_geolocation(ip)

    # Combine all log data
    log_entry = {
        "timestamp": timestamp,
        "event": event,
        "data": event_data,
        "ip": ip,
        "user_agent": user_agent,
        "geo": geo_data
    }

    # Print to logs (Render log dashboard)
    print(json.dumps(log_entry, indent=2))

    return {"status": "logged"}



@app.route("/view-logs", methods=["GET"])
def view_logs():
    try:
        with open("log.txt", "r") as f:
            return "<pre>" + f.read() + "</pre>"
    except FileNotFoundError:
        return "No logs yet."


