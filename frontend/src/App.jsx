import { useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:5000";

function App() {
  // State: what the user has typed
  const [username, setUsername] = useState("");

  // State: the player data we got back, or null
  const [player, setPlayer] = useState(null);

  // State: loading status
  const [loading, setLoading] = useState(false);

  // State: error message, or null
  const [error, setError] = useState(null);

  // Handle the search button click
  async function handleSearch() {
    if (!username.trim()) return; // ignore empty input

    setLoading(true);
    setError(null);
    setPlayer(null);

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

  return (
    <div className="container">
      <h1>Marvel Rivals Tracker</h1>

      <div className="search">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter a username..."
        />
        <button onClick={handleSearch} disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {error && <p className="error">Error: {error}</p>}

      {player && (
        <div className="result">
          <p>
            <strong>Source:</strong> {player.source}
          </p>
          <pre>{JSON.stringify(player.data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
