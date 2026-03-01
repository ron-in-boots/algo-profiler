import { useState } from 'react'
import CodeEditor, { EXAMPLES } from './components/CodeEditor/CodeEditor'
import ComplexityChart from './components/ComplexityChart/ComplexityChart'
import ErrorPanel from './components/ErrorPanel/ErrorPanel'
import { useProfiler } from './hooks/useProfiler'
import { analyzeCode } from './services/api'

const DEFAULT_CODE = `void solve(std::vector<int>& data, int N) {
    std::sort(data.begin(), data.end());
}`

export default function App() {
  const [code, setCode] = useState(DEFAULT_CODE)
  const [inputType, setInputType] = useState('array')
  const [dataType, setDataType] = useState('random')
  const { loading, results, error, runProfile } = useProfiler()
  const [aiAnalysis, setAiAnalysis] = useState(null)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError] = useState(null)

  function handleInputTypeChange(type) {
    setInputType(type)
    const firstExample = Object.values(EXAMPLES[type]?.examples || {})[0]
    if (firstExample) setCode(firstExample)
    setAiAnalysis(null)
  }

  function handleCodeChange(val) {
    setCode(val)
    setAiAnalysis(null)
  }

  function handleRun() {
    setAiAnalysis(null)
    runProfile(code, dataType, inputType)
  }

  async function handleAnalyze() {
    if (!results) return
    setAiLoading(true)
    setAiError(null)
    setAiAnalysis(null)
    try {
      const data = await analyzeCode(code, results.measurements, results.complexity)
      setAiAnalysis(data.analysis)
    } catch (err) {
      setAiError(err.response?.data?.detail || err.message)
    } finally {
      setAiLoading(false)
    }
  }

  return (
    <div className="h-screen bg-[#0a0a0a] text-[#e0e0e0] flex flex-col font-mono overflow-hidden">

      {/* Header */}
      <div className="flex items-center justify-between px-5 h-12 bg-[#111] border-b-2 border-[#00ff88] shrink-0">
        <div className="flex items-center gap-4">
          <span className="text-[#00ff88] text-base font-bold tracking-widest">ALGO PROFILER</span>
          <span className="text-[#444] text-sm">Empirical Big-O Complexity Analyzer</span>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={dataType}
            onChange={e => setDataType(e.target.value)}
            className="bg-[#1a1a1a] border border-[#333] text-[#aaa] text-sm px-3 py-1.5 focus:outline-none focus:border-[#00ff88] font-mono"
          >
            <option value="random">random</option>
            <option value="sorted">sorted</option>
            <option value="reverse_sorted">reverse_sorted</option>
            <option value="nearly_sorted">nearly_sorted</option>
          </select>
          <button
            onClick={handleRun}
            disabled={loading}
            className="flex items-center gap-2 px-5 py-1.5 bg-[#00ff88] hover:bg-[#00cc6a] disabled:bg-[#1a1a1a] disabled:text-[#555] text-[#000] text-sm font-bold tracking-widest transition-colors"
          >
            {loading ? '● RUNNING' : '▶ RUN'}
          </button>
        </div>
      </div>

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">

        {/* LEFT — Editor */}
        <div className="w-1/2 flex flex-col border-r border-[#222]">

          {/* Tab bar */}
          <div className="flex items-center h-10 bg-[#0f0f0f] border-b border-[#222] shrink-0">
            {Object.entries(EXAMPLES).map(([key, val]) => (
              <button
                key={key}
                onClick={() => handleInputTypeChange(key)}
                className={`h-full px-5 text-sm font-bold tracking-widest transition-colors border-r border-[#222] ${
                  inputType === key
                    ? 'text-[#00ff88] bg-[#0a0a0a] border-b-2 border-b-[#00ff88]'
                    : 'text-[#555] hover:text-[#999]'
                }`}
              >
                {key.toUpperCase()}
              </button>
            ))}
            <div className="ml-auto px-3">
              <select
                onChange={e => { if (e.target.value) handleCodeChange(e.target.value) }}
                className="bg-[#0f0f0f] border border-[#333] text-[#888] text-sm px-2 py-1 focus:outline-none font-mono"
                value=""
              >
                <option value="" disabled>load example...</option>
                {Object.entries(EXAMPLES[inputType]?.examples || {}).map(([name, c]) => (
                  <option key={name} value={c}>{name}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Signature hint */}
          <div className="px-4 py-2 bg-[#0a0a0a] border-b border-[#1a1a1a] shrink-0">
            <span className="text-sm text-[#00ff88] opacity-70">
              {({
                array:  'void solve(std::vector<int>& data, int N)',
                string: 'void solve(std::string& data, int N)',
                graph:  'void solve(std::vector<std::vector<int>>& adj, int N)',
                matrix: 'void solve(std::vector<std::vector<int>>& matrix, int N)',
              })[inputType]}
            </span>
          </div>

          {/* Monaco */}
          <div className="flex-1 overflow-hidden">
            <CodeEditor value={code} onChange={handleCodeChange} />
          </div>
        </div>

        {/* RIGHT — Results */}
        <div className="w-1/2 flex flex-col overflow-auto">

          {error && <div className="m-4"><ErrorPanel error={error} /></div>}

          {/* Empty state */}
          {!results && !error && !loading && (
            <div className="flex-1 flex flex-col items-center justify-center gap-3">
              <div className="text-[#1c1c1c] text-8xl font-bold">O(?)</div>
              <p className="text-[#444] text-sm tracking-widest uppercase">awaiting execution</p>
              <p className="text-[#2a2a2a] text-sm">select type → load example → run</p>
            </div>
          )}

          {/* Loading */}
          {loading && (
            <div className="flex-1 flex flex-col items-center justify-center gap-4">
              <div className="text-[#00ff88] text-base font-bold tracking-widest animate-pulse">
                PROFILING...
              </div>
              <div className="text-[#333] text-sm space-y-1 text-center">
                <div>compiling with g++ -O2 -std=c++17</div>
                <div>running 3 trials × 6 input sizes</div>
                <div className="text-[#00ff88] opacity-40">N = 100 → 500 → 1K → 5K → 10K → 50K</div>
              </div>
            </div>
          )}

          {/* Results */}
          {results && !loading && (
            <div className="flex flex-col">

              {/* Complexity row */}
              <div className="flex items-center gap-6 px-5 py-4 border-b border-[#1e1e1e] bg-[#0f0f0f]">
                <div>
                  <div className="text-[#555] text-xs tracking-widest uppercase mb-1">detected complexity</div>
                  <div className="text-[#00ff88] text-3xl font-bold">{results.complexity.best_fit}</div>
                </div>
                <div className="h-10 w-px bg-[#222]" />
                <div className="flex flex-col gap-1">
                  <div className="text-[#555] text-xs tracking-widest uppercase mb-1">curve fit scores</div>
                  <div className="flex gap-3 flex-wrap">
                    {Object.entries(results.complexity.r2_scores || {})
                      .sort((a, b) => b[1] - a[1])
                      .slice(0, 4)
                      .map(([label, score]) => (
                        <div key={label} className="text-xs">
                          <span className="text-[#666]">{label}</span>
                          <span className="text-[#aaa] ml-1">{score.toFixed(3)}</span>
                        </div>
                      ))}
                  </div>
                </div>
              </div>

              {/* Chart */}
              <div className="px-4 pt-3 pb-1 border-b border-[#1a1a1a]">
                <ComplexityChart
                  measurements={results.measurements}
                  complexity={results.complexity}
                />
              </div>

              {/* Table */}
              <div className="border-b border-[#1a1a1a]">
                <table className="w-full text-sm font-mono">
                  <thead>
                    <tr className="bg-[#0f0f0f]">
                      <th className="px-5 py-2.5 text-left text-[#555] font-normal tracking-widest text-xs uppercase">N</th>
                      <th className="px-5 py-2.5 text-left text-[#555] font-normal tracking-widest text-xs uppercase">Time (ms)</th>
                      <th className="px-5 py-2.5 text-left text-[#555] font-normal tracking-widest text-xs uppercase">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.measurements.map((m, i) => (
                      <tr key={i} className="border-t border-[#141414] hover:bg-[#111] transition-colors">
                        <td className="px-5 py-2.5 text-[#777]">{m.n.toLocaleString()}</td>
                        <td className="px-5 py-2.5 text-[#ccc]">{m.time_ms !== null ? m.time_ms.toFixed(4) : '—'}</td>
                        <td className="px-5 py-2.5">
                          <span className={
                            m.status === 'ok' ? 'text-[#00ff88]' :
                            m.status === 'timeout' ? 'text-yellow-400' :
                            'text-red-400'
                          }>{m.status}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* AI Analysis */}
              <div>
                <div className="flex items-center justify-between px-5 py-3 bg-[#0f0f0f] border-b border-[#222]">
                  <div>
                    <span className="text-[#aaa] text-sm font-bold tracking-widest">AI ANALYSIS</span>
                    <span className="ml-2 text-[#444] text-xs">llama-3.3-70b</span>
                  </div>
                  <button
                    onClick={handleAnalyze}
                    disabled={aiLoading}
                    className="text-sm px-4 py-1.5 border border-[#333] text-[#aaa] hover:text-[#00ff88] hover:border-[#00ff88] disabled:opacity-30 transition-all font-mono tracking-wide"
                  >
                    {aiLoading ? 'analyzing...' : '→ analyze'}
                  </button>
                </div>

                <div className="px-5 py-4 text-sm text-[#bbb] leading-relaxed min-h-[80px]">
                  {!aiAnalysis && !aiLoading && !aiError && (
                    <span className="text-[#444] text-sm">
                      Click "→ analyze" to get AI-powered optimization suggestions.
                    </span>
                  )}
                  {aiLoading && (
                    <span className="text-[#555] text-sm animate-pulse">
                      querying llama-3.3-70b-versatile...
                    </span>
                  )}
                  {aiAnalysis && (
                    <pre className="whitespace-pre-wrap font-mono text-sm text-[#ccc] leading-6">
                      {aiAnalysis}
                    </pre>
                  )}
                  {aiError && (
                    <span className="text-red-400 text-sm">{aiError}</span>
                  )}
                </div>
              </div>

            </div>
          )}
        </div>
      </div>
    </div>
  )
}
