from flask import Flask, request
from flask_cors import CORS
import requests
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_real_ip():
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        # take the first public IP from the list
        ip = forwarded.split(",")[0].strip()
    else:
        ip = request.remote_addr
    return ip

def get_geolocation(ip):
    try:
        resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"Geo error: {e}")
    return {}

@app.route("/log", methods=["POST"])
def log():
    try:
        data = request.get_json()
        event = data.get('event')
        event_data = data.get('data')
    except Exception as e:
        print(f"Invalid JSON: {e}")
        return {"error": "Invalid JSON"}, 400

    timestamp = data.get('timestamp') or datetime.utcnow().isoformat()
    ip = get_real_ip()
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

    print(json.dumps(log_entry, indent=2))
    return {"status": "logged"}


