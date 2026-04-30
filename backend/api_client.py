import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MARVEL_RIVALS_API_KEY")
API_BASE = "https://marvelrivalsapi.com/api/v1"
DEFAULT_TIMEOUT = 15  # seconds


class APIError(Exception):
    """Raised when the external API returns an error or fails."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


def _get(endpoint):
    """
    Internal helper: makes a GET request to the API and returns the JSON.
    Raises APIError on any failure.
    """
    if not API_KEY:
        raise APIError("API key not configured", status_code=500)

    headers = {"x-api-key": API_KEY}
    url = f"{API_BASE}{endpoint}"

    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
    except requests.exceptions.Timeout:
        raise APIError("API request timed out", status_code=504)
    except requests.exceptions.RequestException as e:
        raise APIError(f"Request failed: {str(e)}", status_code=500)

    # Try to parse JSON regardless of status code — most APIs return JSON errors
    try:
        data = response.json()
    except ValueError:
        raise APIError(f"API returned non-JSON response: {response.text[:200]}",
                       status_code=response.status_code)

    if response.status_code >= 400:
        message = data.get("message") if isinstance(data, dict) else "API error"
        raise APIError(message or "API error", status_code=response.status_code)

    return data


def find_player_uid(username):
    """
    Look up a player's UID by their username.
    Returns the UID as a string, or raises APIError.
    """
    data = _get(f"/find-player/{username}")
    # The API response shape: {"uid": "...", "name": "..."}
    # Adjust if needed based on actual response structure
    return str(data.get("uid") or data.get("id") or "")


def get_player(query):
    """
    Get full player data by either UID or username.
    Returns the player dict, or raises APIError.
    """
    return _get(f"/player/{query}")


def get_match_history(query):
    """
    Get match history for a player by UID or username.
    Returns the match history data, or raises APIError.
    """
    return _get(f"/player/{query}/match-history")