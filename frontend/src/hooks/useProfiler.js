import { useState } from 'react'
import { profileCode } from '../services/api'

export function useProfiler() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  async function runProfile(code, dataType, inputType = 'array') {
    setLoading(true)
    setError(null)
    setResults(null)
    try {
      const data = await profileCode(code, dataType, inputType)
      setResults(data)
    } catch (err) {
      const detail = err.response?.data?.detail
      if (typeof detail === 'object') {
        setError(detail.message || JSON.stringify(detail))
      } else {
        setError(detail || err.message || 'Unknown error')
      }
    } finally {
      setLoading(false)
    }
  }

  return { loading, results, error, runProfile }
}
