import type { CheckIn } from "../types/checkIn"

const API_URL = "http://localhost:8000"

export type MissionFeedback = "helpful" | "not_for_me" | "not_sure"

export interface CheckInInsights {
  check_in_count: number
  most_common_feeling: string | null
}

export interface Mission {
  id: number
  title: string
  description: string
  category: string
  difficulty: string
  social_required: boolean
  energy_required: string
}

export interface TodayMission {
  mission: Mission | null
  status: string
  assignment_id?: number
  message?: string
  feedback?: MissionFeedback | null
  reasons?: string[]
}

export async function createCheckIn(
  feeling: string,
  note?: string
): Promise<CheckIn> {
  const response = await fetch(`${API_URL}/check-ins`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      feeling,
      note: note || null,
    }),
  })

  if (!response.ok) {
    throw new Error("Failed to create check-in")
  }

  return response.json()
}

export async function getCheckIn(): Promise<CheckIn[]> {
  const response = await fetch(`${API_URL}/check-ins`)

  if (!response.ok) {
    throw new Error("Failed to fetch check-ins")
  }

  return response.json()
}

export async function getCheckInInsights(): Promise<CheckInInsights> {
  const response = await fetch(`${API_URL}/check-ins/insights`)

  if (!response.ok) {
    throw new Error("Failed to fetch check-in insights")
  }

  return response.json()
}

export async function getTodayMission(): Promise<TodayMission> {
  const response = await fetch(`${API_URL}/missions/today`)

  if (!response.ok) {
    throw new Error("Failed to fetch today's mission")
  }

  return response.json()
}

export async function startMission(assignmentId: number) {
  const response = await fetch(`${API_URL}/missions/assignments/${assignmentId}/start`, {
    method: "POST",
  })

  if (!response.ok) {
    throw new Error("Failed to start mission")
  }

  return response.json()
}

export async function completeMission(assignmentId: number) {
  const response = await fetch(`${API_URL}/missions/assignments/${assignmentId}/complete`, {
    method: "POST",
  })

  if (!response.ok) {
    throw new Error("Failed to complete mission")
  }

  return response.json()
}

export async function skipMission(assignmentId: number) {
  const response = await fetch(`${API_URL}/missions/assignments/${assignmentId}/skip`, {
    method: "POST",
  })

  if (!response.ok) {
    throw new Error("Failed to skip mission")
  }

  return response.json()
}

export async function submitMissionFeedback(
  assignmentId: number,
  feedback: MissionFeedback
) {
  const response = await fetch(
    `${API_URL}/missions/assignments/${assignmentId}/feedback`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ feedback }),
    }
  )

  if (!response.ok) {
    throw new Error("Failed to submit mission feedback")
  }

  return response.json()
}