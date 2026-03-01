import axios from 'axios'

const client = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

export async function profileCode(code, dataType, inputType = 'array', sizes = null) {
  const response = await client.post('/api/v1/profile', {
    code,
    data_type: dataType,
    input_type: inputType,
    sizes,
  })
  return response.data
}

export async function analyzeCode(code, measurements, complexity) {
  const response = await client.post('/api/v1/analyze', {
    code,
    measurements,
    complexity,
  })
  return response.data
}
