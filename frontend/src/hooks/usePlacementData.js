import { useCallback, useEffect, useState } from 'react'
import { api } from '../api/client'

const empty = { dashboard: null, applications: [], companies: [], notes: [], resumes: [] }

async function loadPlacementData(token) {
  const [dashboard, page, companies, notes, resumes] = await Promise.all([
    api('/dashboard/', { token }),
    api('/applications/?page=1&limit=100', { token }),
    api('/companies/', { token }),
    api('/notes/', { token }),
    api('/resumes/', { token }),
  ])

  return { dashboard, applications: page.items, companies, notes, resumes }
}

export function usePlacementData(token) {
  const [data, setData] = useState(empty)
  const [loading, setLoading] = useState(Boolean(token))
  const [error, setError] = useState(null)

  const refresh = useCallback(async () => {
    if (!token) return

    setLoading(true)
    setError(null)
    try {
      setData(await loadPlacementData(token))
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }, [token])

  useEffect(() => {
    if (!token) return

    let isCurrent = true

    async function load() {
      try {
        const nextData = await loadPlacementData(token)
        if (isCurrent) setData(nextData)
      } catch (requestError) {
        if (isCurrent) setError(requestError.message)
      } finally {
        if (isCurrent) setLoading(false)
      }
    }

    load()

    return () => {
      isCurrent = false
    }
  }, [token])

  return { data, loading, error, refresh }
}
