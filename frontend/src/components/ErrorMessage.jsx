function ErrorMessage({ message }) {
  return (
    <div className="flex gap-3 p-4 border border-red-500/40 bg-red-500/5 text-red-300 rounded-md">
      <div className="flex-shrink-0 w-6 h-6 rounded-full bg-red-500/20 text-red-400 flex items-center justify-center font-semibold text-sm">
        !
      </div>
      <div className="flex-1">
        <p className="font-medium text-red-300">Something went wrong</p>
        <p className="text-sm text-red-400/80 mt-0.5">{message}</p>
      </div>
    </div>
  );
}

export default ErrorMessage;
