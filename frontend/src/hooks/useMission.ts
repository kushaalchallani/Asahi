
import { useCallback, useEffect, useState } from "react"
import {
  completeMission,
  getTodayMission,
  skipMission,
  startMission,
} from "../services/api"
import type { Mission as MissionData } from "../services/api"

export type MissionStatus = "assigned" | "started" | "completed" | "skipped"

export function useMission() {
  const [mission, setMission] = useState<MissionData | null>(null)
  const [status, setStatus] = useState<MissionStatus>("assigned")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadMission() {
      try {
        const data = await getTodayMission()
        setMission(data.mission)

        if (
          data.status === "assigned" ||
          data.status === "started" ||
          data.status === "completed" ||
          data.status === "skipped"
        ) {
          setStatus(data.status)
        }
      } catch (error) {
        console.error("Failed to load today's mission:", error)
      } finally {
        setLoading(false)
      }
    }

    void loadMission()
  }, [])

  const start = useCallback(async () => {
    if (!mission) return

    try {
      await startMission(mission.id)
      setStatus("started")
    } catch (error) {
      console.error("Failed to start mission:", error)
    }
  }, [mission])

  const complete = useCallback(async () => {
    if (!mission) return

    try {
      await completeMission(mission.id)
      setStatus("completed")
    } catch (error) {
      console.error("Failed to complete mission:", error)
    }
  }, [mission])

  const skip = useCallback(async () => {
    if (!mission) return

    try {
      await skipMission(mission.id)
      setStatus("skipped")
    } catch (error) {
      console.error("Failed to skip mission:", error)
    }
  }, [mission])

  return { mission, status, loading, start, complete, skip }
}
