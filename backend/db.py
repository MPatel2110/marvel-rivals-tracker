import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta

# Where the database file is
DB_PATH = Path(__file__).parent / "data" / "tracker.db"


def get_connection():
    """
    Returns a connection to the SQLite database.
    Creates the database file if it doesn't exist yet.
    """
    # Data folder exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema():
    """
    Creates all tables if they don't already exist.
    Safe to run multiple times — IF NOT EXISTS prevents errors.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS players (
            uid TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            level INTEGER,
            rank TEXT,
            total_matches INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            raw_data TEXT
        );

        CREATE TABLE IF NOT EXISTS matches (
            match_id TEXT PRIMARY KEY,
            player_uid TEXT NOT NULL,
            hero TEXT,
            map TEXT,
            result TEXT,
            kills INTEGER,
            deaths INTEGER,
            assists INTEGER,
            match_date TIMESTAMP,
            raw_data TEXT,
            FOREIGN KEY (player_uid) REFERENCES players(uid)
        );

        CREATE TABLE IF NOT EXISTS hero_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_uid TEXT NOT NULL,
            hero_name TEXT NOT NULL,
            matches_played INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            total_kills INTEGER DEFAULT 0,
            total_deaths INTEGER DEFAULT 0,
            total_assists INTEGER DEFAULT 0,
            FOREIGN KEY (player_uid) REFERENCES players(uid),
            UNIQUE(player_uid, hero_name)
        );

        CREATE TABLE IF NOT EXISTS cache_entries (
            cache_key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            expires_at TIMESTAMP NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_matches_player ON matches(player_uid);
        CREATE INDEX IF NOT EXISTS idx_hero_stats_player ON hero_stats(player_uid);
        CREATE INDEX IF NOT EXISTS idx_cache_expires ON cache_entries(expires_at);
    """)

    conn.commit()
    conn.close()
    print("✓ Database schema initialized")

PLAYER_CACHE_TTL_SECONDS = 3600


def is_fresh(timestamp_str, max_age_seconds=PLAYER_CACHE_TTL_SECONDS):
    """
    Returns True if the given timestamp is recent enough to use cached data.
    timestamp_str: a string from SQLite like '2026-04-29 18:49:00'
    max_age_seconds: how old is "too old"
    """
    if not timestamp_str:
        return False
    cached_time = datetime.fromisoformat(timestamp_str)
    age= datetime.now() - cached_time
    return age.total_seconds() < max_age_seconds



def save_player(player_data):
     """
    Save (or update) a player in the database.
    player_data: a dict from the marvelrivalsapi.com API response.
    """
     conn = get_connection()
     curser = conn.cursor()

     # Extract fields from API response.
     # The actual structure depends on the API (can adjust if needed)
     uid = str(player_data.get("uid") or player_data.get("id") or "")
     username = player_data.get("name") or player_data.get("username") or ""
     level = player_data.get("level")
     rank = player_data.get("rank") or player_data.get("rank_name")
     total_matches = player_data.get("total_matches", 0)
     wins = player_data.get("wins", 0)

     # Either insert or replaces. If a player with this uid exists, update; else insert new
     curser.execute("""
        INSERT OR REPLACE INTO players
        (uid, username, level, rank, total_matches, wins, last_updated, raw_data)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
    """, (uid, username, level, rank, total_matches, wins, json.dumps(player_data)))
     conn.commit()
     conn.close()
     return uid



def get_cached_player(identifier):
    """
    Look up a player in our cache by either UID or username.
    Returns a dict with player data + 'is_fresh' boolean, or None if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Try uid first, then username after
    cursor.execute("""
        SELECT * FROM players WHERE uid = ? OR username = ?
    """, (str(identifier), str(identifier)))

    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    
    return {
        "uid": row["uid"],
        "username": row["username"],
        "level": row["level"],
        "rank": row["rank"],
        "total_matches": row["total_matches"],
        "wins": row["wins"],
        "last_updated": row["last_updated"],
        "raw_data": json.loads(row["raw_data"]) if row["raw_data"] else None,
        "is_fresh": is_fresh(row["last_updated"]),
    }

def save_uid_mapping(username, uid):
    """
    Save the username -> UID mapping in the cache_entries table.
    Allows to skip the find-player API call next time.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cache_key = f"uid_mapping:{username.lower()}"
    expires_at =  (datetime.now() + timedelta(days=30)).isoformat()

    cursor.execute("""
        INSERT OR REPLACE INTO cache_entries (cache_key, value, expires_at)
        VALUES (?, ?, ?)
    """, (cache_key, str(uid), expires_at))

    conn.commit()
    conn.close()

def get_cached_uid(username):
    """
    Look up a previously cached UID for a username.
    Returns the UID string or None if not cached or expired.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cache_key = f"uid_mapping:{username.lower()}"
    cursor.execute("""
        SELECT value, expires_at FROM cache_entries WHERE cache_key = ?
    """, (cache_key,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None
    
    # Checks expire
    if datetime.fromisoformat(row["expires_at"]) < datetime.now():
        return None
    
    return row["value"]





if __name__ == "__main__":
    init_schema()