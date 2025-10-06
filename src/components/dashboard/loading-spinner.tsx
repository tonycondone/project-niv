'use client';

export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center h-96">
      <div className="text-center">
        <div className="relative">
          <div className="h-16 w-16 border-4 border-primary-500/20 rounded-full animate-spin">
            <div className="absolute top-0 left-0 h-16 w-16 border-4 border-transparent border-t-primary-500 rounded-full animate-spin"></div>
          </div>
        </div>
        <h3 className="text-xl font-semibold mt-4 mb-2">Loading Dashboard</h3>
        <p className="text-muted-foreground">Processing your data...</p>
      </div>
    </div>
  );
}