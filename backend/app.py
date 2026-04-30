from flask import Flask, jsonify
from flask_cors import CORS

import api_client
from api_client import APIError

app = Flask(__name__)
CORS(app)


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/player/<username>")
def get_player_route(username):
    try:
        data = api_client.get_player(username)
        return jsonify(data), 200
    except APIError as e:
        return jsonify({"error": str(e)}), e.status_code or 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)