import { useCallback, useEffect, useState } from "react"
import { getCheckInInsights } from "../services/api"
import type { CheckInInsights } from "../services/api"

export function useInsights() {
  const [insights, setInsights] = useState<CheckInInsights | null>(null)

  const refreshInsights = useCallback(async () => {
    try {
      const data = await getCheckInInsights()
      setInsights(data)
    } catch (error) {
      console.error("Failed to load check-in insights:", error)
    }
  }, [])

  useEffect(() => {
    void refreshInsights()
  }, [refreshInsights])

  return { insights, refreshInsights }
}
