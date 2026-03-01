import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from 'recharts'

export default function ComplexityChart({ measurements }) {
  const chartData = measurements
    .filter(m => m.status === 'ok' && m.time_ms !== null)
    .map(m => ({ n: m.n, ms: m.time_ms }))

  return (
    <div style={{ height: 220 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 8, right: 16, left: 0, bottom: 20 }}>
          <CartesianGrid strokeDasharray="1 4" stroke="#1a1a1a" />
          <XAxis
            dataKey="n"
            stroke="#333"
            tick={{ fill: '#444', fontSize: 10, fontFamily: 'monospace' }}
            label={{ value: 'N', position: 'insideBottom', offset: -8, fill: '#444', fontSize: 10 }}
          />
          <YAxis
            stroke="#333"
            tick={{ fill: '#444', fontSize: 10, fontFamily: 'monospace' }}
            label={{ value: 'ms', angle: -90, position: 'insideLeft', offset: 10, fill: '#444', fontSize: 10 }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#111',
              border: '1px solid #2a2a2a',
              borderRadius: 0,
              fontSize: 11,
              fontFamily: 'monospace',
            }}
            labelStyle={{ color: '#555' }}
            itemStyle={{ color: '#00ff88' }}
            formatter={(val) => [`${val.toFixed(4)}ms`, 'time']}
            labelFormatter={(n) => `N = ${Number(n).toLocaleString()}`}
          />
          <Line
            type="monotone"
            dataKey="ms"
            stroke="#00ff88"
            strokeWidth={1.5}
            dot={{ fill: '#00ff88', r: 3, strokeWidth: 0 }}
            activeDot={{ r: 5, fill: '#00ff88' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
