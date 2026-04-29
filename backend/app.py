import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("MARVEL_RIVALS_API_KEY")
API_BASE = "https://marvelrivalsapi.com/api/v1"


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "api_key_loaded": bool(API_KEY)})


@app.route("/api/player/<username>")
def get_player(username):
    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    headers = {"x-api-key": API_KEY}
    url = f"{API_BASE}/player/{username}"

    try:
        response = requests.get(url, headers=headers, timeout=15)
        return jsonify({
            "status_code": response.status_code,
            "url_called": url,
            "response": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
        }), 200
    except requests.exceptions.Timeout:
        return jsonify({"error": "API request timed out after 15 seconds"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)