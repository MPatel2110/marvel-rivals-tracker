# Marvel Rivals Performance Tracker

Full-stack web app for looking up Marvel Rivals player stats and match history. Built with Flask + SQLite (Python) on the backend; React frontend coming.

## Status

### Day 1 — Backend foundation (Done!)

- Flask backend running on :5000
- `/api/health` and `/api/player/<username>` endpoints
- Confirmed real data returns from marvelrivalsapi.com
- Initial commit pushed to GitHub

### Day 2 — Database + caching layer (Done!)

- SQLite database with 4 tables: `players`, `matches`, `hero_stats`, `cache_entries`
- Cache layer in `db.py` with TTL-based freshness checks (1 hour for players, 30 days for UID mappings)
- API client extracted into its own module (`api_client.py`)
- Custom `APIError` exception for clean error propagation
- Cache-aside pattern: `/api/player/<name>` checks SQLite first, hits external API only on miss/stale
- Verified end-to-end: first request returns `"source": "api"`, second request returns `"source": "cache"`

### Day 3 — Frontend foundation (Done!)

- React + Vite project set up in `frontend/`
- Player search component with state, controlled input, async fetch
- Polish: Enter key submits, autoFocus, empty state, hover/disabled states
- Tailwind CSS v4 installed and wired up via @tailwindcss/vite
- Search button converted to Tailwind utilities; rest of page still on App.css

### Day 4 — Next

- Convert remaining App.css styles to Tailwind utilities
- Build a proper PlayerCard component instead of raw JSON dump
- Add separate components: SearchBar, PlayerCard, MatchHistory placeholder
- Polish loading and error states with better visual treatment

### Tailwind v4 things to remember

- Preflight resets default heading sizes — need explicit h1/h2 styles in index.css
- Body background needs explicit setting since Tailwind doesn't apply one
- Setup is just `@import "tailwindcss";` + Vite plugin (don't follow v3 tutorials)

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
