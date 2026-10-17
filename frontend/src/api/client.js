const API_URL = (import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '')).replace(/\/+$/, '')

export async function api(path, { token, body, headers, ...options } = {}) {
  if (!API_URL) {
    throw new Error('The API URL is not configured. Set VITE_API_URL in the frontend deployment environment.')
  }

  const requestHeaders = new Headers(headers)
  if (token) requestHeaders.set('Authorization', `Bearer ${token}`)
  let requestBody = body
  if (body && !(body instanceof FormData)) { requestHeaders.set('Content-Type', 'application/json'); requestBody = JSON.stringify(body) }
  const response = await fetch(`${API_URL}${path}`, { ...options, headers: requestHeaders, body: requestBody })
  if (response.status === 204) return null
  const payload = await response.json().catch(() => null)
  if (!response.ok) throw new Error(payload?.detail || 'Something went wrong. Please try again.')
  return payload
}
