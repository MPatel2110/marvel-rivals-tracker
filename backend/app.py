import os

from flask import Flask, jsonify
from flask_cors import CORS

import api_client
import db
from api_client import APIError

app = Flask(__name__)

allowed_origins = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
).split(",")

CORS(app, origins=allowed_origins)
# Make sure database tables exist whenever the app starts
db.init_schema()


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/player/<username>")
def get_player_route(username):
    """
    Look up a player by username with cache-aside pattern:
    1. Check our local cache for fresh data
    2. If miss/stale, find the UID (cached or fresh)
    3. Fetch full player data from API
    4. Save to cache and return
    """
    # 1. Check cache by username first
    cached = db.get_cached_player(username)
    if cached and cached["is_fresh"]:
        return jsonify({
            "source": "cache",
            "data": cached["raw_data"],
        }), 200

    # 2. Get UID — either from cache or by calling find-player
    uid = db.get_cached_uid(username)
    if not uid:
        try:
            uid = api_client.find_player_uid(username)
            if uid:
                db.save_uid_mapping(username, uid)
        except APIError as e:
            return jsonify({"error": str(e)}), e.status_code or 500

    if not uid:
        return jsonify({"error": "Could not find player UID"}), 404

    # 3. Fetch full player data using the UID
    try:
        player_data = api_client.get_player(uid)
    except APIError as e:
        return jsonify({"error": str(e)}), e.status_code or 500

    # 4. Save to cache
    db.save_player(player_data)

    # 5. Return fresh data
    return jsonify({
        "source": "api",
        "data": player_data,
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)