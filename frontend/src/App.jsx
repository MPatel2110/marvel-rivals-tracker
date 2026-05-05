import { useState } from "react";
import SearchBar from "./components/SearchBar";
import PlayerCard from "./components/PlayerCard";
import LoadingCard from "./components/LoadingCard";
import ErrorMessage from "./components/ErrorMessage";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:5000";

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

  return (
    <div className="max-w-3xl mx-auto px-6 py-8 text-neutral-200 font-sans">
      <h1 className="text-4xl font-bold mb-1">Marvel Rivals Tracker</h1>
      <p className="text-neutral-500 mb-8">
        Look up player stats and match history
      </p>

      <SearchBar
        username={username}
        setUsername={setUsername}
        onSearch={handleSearch}
        loading={loading}
      />

      {!hasSearched && !loading && (
        <div className="text-center py-12 text-neutral-500">
          <p>Search for a Marvel Rivals player to see their stats.</p>
          <p className="text-sm text-neutral-600 mt-2">Try "TenZ" to start.</p>
        </div>
      )}

      {loading && <LoadingCard />}

      {error && !loading && <ErrorMessage message={error} />}

      {player && !loading && <PlayerCard player={player} />}
    </div>
  );
}

export default App;
