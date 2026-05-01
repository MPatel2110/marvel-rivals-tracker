function LoadingCard() {
  return (
    <div className="space-y-4 animate-pulse">
      <div className="flex items-baseline justify-between">
        <div className="space-y-2">
          <div className="h-8 w-48 bg-neutral-800 rounded"></div>
          <div className="h-4 w-32 bg-neutral-800 rounded"></div>
        </div>
        <div className="h-4 w-24 bg-neutral-800 rounded"></div>
      </div>

      <div className="grid grid-cols-3 gap-3">
        <div className="bg-neutral-900 border border-neutral-800 rounded-md p-4 h-20"></div>
        <div className="bg-neutral-900 border border-neutral-800 rounded-md p-4 h-20"></div>
        <div className="bg-neutral-900 border border-neutral-800 rounded-md p-4 h-20"></div>
      </div>
    </div>
  );
}

export default LoadingCard;
