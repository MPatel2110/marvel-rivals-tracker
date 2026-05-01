function StatBlock({ label, value }) {
  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-md p-4">
      <p className="text-xs text-neutral-500 uppercase tracking-wide">
        {label}
      </p>
      <p className="text-2xl font-semibold text-neutral-100 mt-1">
        {value ?? "—"}
      </p>
    </div>
  );
}

function PlayerCard({ player }) {
  const data = player.data;
  const name = data.name || data.username || "Unknown";
  const level = data.level ?? data.player?.level ?? "—";
  const rank = data.rank?.rank ?? data.player?.rank?.rank ?? "Unranked";

  const stats = data.overall_stats?.ranked ?? {};
  const totalMatches = stats.total_matches ?? 0;
  const totalWins = stats.total_wins ?? 0;
  const winRate =
    totalMatches > 0 ? `${Math.round((totalWins / totalMatches) * 100)}%` : "—";

  return (
    <div className="space-y-4">
      <div className="flex items-baseline justify-between">
        <div>
          <h2 className="text-3xl font-bold text-neutral-100">{name}</h2>
          <p className="text-neutral-500 mt-1">
            Level {level} · {rank}
          </p>
        </div>
        <span className="text-xs uppercase tracking-wide text-purple-400 font-semibold">
          Source: {player.source}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-3">
        <StatBlock label="Matches" value={totalMatches} />
        <StatBlock label="Wins" value={totalWins} />
        <StatBlock label="Win Rate" value={winRate} />
      </div>

      <details className="bg-neutral-900 border border-neutral-800 rounded-md p-4">
        <summary className="cursor-pointer text-sm text-neutral-500 hover:text-neutral-300">
          Show raw data
        </summary>
        <pre className="text-xs overflow-x-auto whitespace-pre-wrap mt-3 text-neutral-400">
          {JSON.stringify(data, null, 2)}
        </pre>
      </details>
    </div>
  );
}

export default PlayerCard;
