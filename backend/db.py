import sqlite3
from pathlib import Path

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

if __name__ == "__main__":
    init_schema()