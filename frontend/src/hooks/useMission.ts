
import { useCallback, useEffect, useState } from "react"
import { completeMission, getTodayMission, skipMission, startMission, submitMissionFeedback} from "../services/api"
import type { Mission as MissionData, MissionFeedback } from "../services/api"

export type MissionStatus = "assigned" | "started" | "completed" | "skipped"

export function useMission() {
  const [mission, setMission] = useState<MissionData | null>(null)
  const [status, setStatus] = useState<MissionStatus>("assigned")
  const [loading, setLoading] = useState(true)
  const [assignmentId, setAssignmentId] = useState<number | null>(null)
  const [feedbackLoading, setFeedbackLoading] = useState(false)
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false)
  const [reasons, setReasons] = useState<string[]>([])
  const [message, setMessage] = useState<string | undefined>(undefined)

  const loadMission = useCallback(async () => {
    setLoading(true)
    try {
      const data = await getTodayMission()
      setMission(data.mission)
      setReasons(data.reasons ?? [])
      setAssignmentId(data.assignment_id ?? null)
      setFeedbackSubmitted(data.feedback != null)
      setMessage(data.message)

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
  }, [])

  useEffect(() => {
    void loadMission()
  }, [loadMission])

  const start = useCallback(async () => {
    if (!assignmentId) return

    try {
      await startMission(assignmentId)
      setStatus("started")
    } catch (error) {
      console.error("Failed to start mission:", error)
    }
  }, [assignmentId])

  const complete = useCallback(async () => {
    if (!assignmentId) return

    try {
      await completeMission(assignmentId)
      setStatus("completed")
    } catch (error) {
      console.error("Failed to complete mission:", error)
    }
  }, [assignmentId])

  const skip = useCallback(async () => {
    if (!assignmentId) return

    try {
      await skipMission(assignmentId)
      setStatus("skipped")
    } catch (error) {
      console.error("Failed to skip mission:", error)
    }
  }, [assignmentId])

  const submitFeedback = useCallback( async (feedback: MissionFeedback) => {
    if (!assignmentId || feedbackLoading || feedbackSubmitted) return

    setFeedbackLoading(true)

    try {
      await submitMissionFeedback(assignmentId, feedback)
      setFeedbackSubmitted(true)
    } catch (error) {
      console.error("Failed to submit mission feedback:", error)
    } finally {
      setFeedbackLoading(false)
    }
  },
  [assignmentId, feedbackLoading, feedbackSubmitted]
)

  return { mission, status, loading, start, complete, skip, submitFeedback, feedbackLoading, feedbackSubmitted, reasons, message, refresh: loadMission}
}
