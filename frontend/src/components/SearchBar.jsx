function SearchBar({ username, setUsername, onSearch, loading }) {
  function handleKeyDown(e) {
    if (e.key === "Enter") {
      onSearch();
    }
  }

  return (
    <div className="flex gap-2 mb-6">
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Enter a username..."
        autoFocus
        className="flex-1 px-3 py-2.5 bg-neutral-900 text-neutral-200 border border-neutral-700 rounded-md focus:outline-none focus:border-purple-500 transition-colors"
      />
      <button
        onClick={onSearch}
        disabled={loading || !username.trim()}
        className="px-5 py-2.5 bg-purple-600 hover:bg-purple-500 disabled:bg-neutral-700 disabled:cursor-not-allowed text-white rounded-md font-medium transition-colors"
      >
        {loading ? "Searching..." : "Search"}
      </button>
    </div>
  );
}

export default SearchBar;
