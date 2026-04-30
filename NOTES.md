# Marvel Rivals Performance Tracker

Full-stack web app for looking up Marvel Rivals player stats and match history. Built with Flask + SQLite (Python) on the backend; React frontend coming.

## Status

### Day 1 — Backend foundation ✓

- Flask backend running on :5000
- `/api/health` and `/api/player/<username>` endpoints
- Confirmed real data returns from marvelrivalsapi.com
- Initial commit pushed to GitHub

### Day 2 — Database + caching layer ✓

- SQLite database with 4 tables: `players`, `matches`, `hero_stats`, `cache_entries`
- Cache layer in `db.py` with TTL-based freshness checks (1 hour for players, 30 days for UID mappings)
- API client extracted into its own module (`api_client.py`)
- Custom `APIError` exception for clean error propagation
- Cache-aside pattern: `/api/player/<name>` checks SQLite first, hits external API only on miss/stale
- Verified end-to-end: first request returns `"source": "api"`, second request returns `"source": "cache"`

### Day 3 — Next

- Add `/api/player/<name>/match-history` endpoint
- Build basic React frontend with player search
- Display player stats from the API in a real UI

## Architecture

backend/
├── app.py # Flask routes, entry point
├── api_client.py # marvelrivalsapi.com integration with timeout + error handling
├── db.py # SQLite schema + cache read/write functions
├── data/
│ └── tracker.db # SQLite database (gitignored)
├── .env # API keys (gitignored)
└── requirements.txt

## Running locally

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```

Then visit `http://127.0.0.1:5000/api/player/<name>`.

## Known gotchas

- marvelrivalsapi.com is a third-party scraper, not an official API. Players must be searched on their site at least once to be indexed.
- Some players return 403 because their in-game profile is set to private.
- The scraper service occasionally returns generic errors when their backend is overloaded — we handle these with custom `APIError` and clean JSON error responses.

## Tech stack

- Backend: Python 3.14, Flask, Flask-CORS, requests, python-dotenv
- Database: SQLite (built-in, single-file, zero-config)
- Caching: TTL-based cache-aside pattern using SQLite
