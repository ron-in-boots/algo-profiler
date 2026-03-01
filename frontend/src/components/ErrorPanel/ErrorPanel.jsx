export default function ErrorPanel({ error }) {
  if (!error) return null

  const isValidation = error.toLowerCase().includes('blocked') ||
                       error.toLowerCase().includes('signature') ||
                       error.toLowerCase().includes('not allowed')

  return (
    <div className={`p-4 rounded-lg border ${
      isValidation
        ? 'bg-yellow-950 border-yellow-800'
        : 'bg-red-950 border-red-800'
    }`}>
      <p className={`font-medium text-sm mb-1 ${
        isValidation ? 'text-yellow-400' : 'text-red-400'
      }`}>
        {isValidation ? '🚫 Security Violation' : '⚠ Compilation Error'}
      </p>
      <pre className={`text-xs whitespace-pre-wrap ${
        isValidation ? 'text-yellow-300' : 'text-red-300'
      }`}>
        {error}
      </pre>
    </div>
  )
}
