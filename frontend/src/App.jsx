import { useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:5000";

function App() {
  const [username, setUsername] = useState("");
  const [player, setPlayer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  async function handleSearch() {
    if (!username.trim()) return;

    setLoading(true);
    setError(null);
    setPlayer(null);
    setHasSearched(true);

    try {
      const response = await fetch(`${API_BASE}/api/player/${username}`);
      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Something went wrong");
        return;
      }

      setPlayer(data);
    } catch (err) {
      setError("Could not reach the server. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      handleSearch();
    }
  }

  return (
    <div className="container">
      <h1>Marvel Rivals Tracker</h1>
      <p className="subtitle">Look up player stats and match history</p>
      <div className="search">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Enter a username..."
          autoFocus
        />
        <button
          onClick={handleSearch}
          disabled={loading || !username.trim()}
          className="px-5 py-2.5 bg-purple-600 hover:bg-purple-500 disabled:bg-neutral-700 disabled:cursor-not-allowed text-white rounded-md font-medium transition-colors"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>
      {!hasSearched && (
        <div className="empty-state">
          <p>Search for a Marvel Rivals player to see their stats.</p>
          <p className="hint">Try "TenZ" to start.</p>
        </div>
      )}
      {error && <p className="error">Error: {error}</p>}
      {player && (
        <div className="result">
          <p className="source-label">
            Source: <strong>{player.source}</strong>
          </p>
          <pre>{JSON.stringify(player.data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
