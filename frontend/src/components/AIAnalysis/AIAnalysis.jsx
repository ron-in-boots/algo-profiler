export default function AIAnalysis({ analysis, loading, onAnalyze, hasResults }) {
  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-lg">🤖</span>
          <span className="font-semibold text-gray-200">AI Analysis</span>
          <span className="text-xs px-2 py-0.5 rounded-full bg-purple-900 text-purple-300">
            Llama-3 70B
          </span>
        </div>
        <button
          onClick={onAnalyze}
          disabled={loading || !hasResults}
          className="flex items-center gap-2 px-4 py-1.5 bg-purple-700 hover:bg-purple-600 disabled:bg-gray-700 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-3 w-3" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              Analyzing...
            </>
          ) : '✨ Analyze with AI'}
        </button>
      </div>

      {!hasResults && !analysis && (
        <div className="p-4 bg-gray-800 rounded-lg border border-gray-700 text-gray-500 text-sm text-center">
          Run the profiler first, then click Analyze with AI
        </div>
      )}

      {hasResults && !analysis && !loading && (
        <div className="p-4 bg-gray-800 rounded-lg border border-dashed border-purple-800 text-gray-400 text-sm text-center">
          Click "✨ Analyze with AI" to get optimization suggestions
        </div>
      )}

      {loading && (
        <div className="p-4 bg-gray-800 rounded-lg border border-gray-700 flex items-center gap-3">
          <svg className="animate-spin h-5 w-5 text-purple-400 shrink-0" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
          </svg>
          <span className="text-gray-400 text-sm">Llama-3 is analyzing your algorithm...</span>
        </div>
      )}

      {analysis && !loading && (
        <div className="p-4 bg-gray-800 rounded-lg border border-purple-900 text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
          {analysis}
        </div>
      )}
    </div>
  )
}
