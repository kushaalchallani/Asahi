import type { CheckIn } from "../types/checkIn"

const API_URL = "http://localhost:8000"

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

export async function startMission(missionId: number) {
  const response = await fetch(`${API_URL}/missions/${missionId}/start`, {
    method: "POST",
  })

  if (!response.ok) {
    throw new Error("Failed to start mission")
  }

  return response.json()
}

export async function completeMission(missionId: number) {
  const response = await fetch(`${API_URL}/missions/${missionId}/complete`, {
    method: "POST",
  })

  if (!response.ok) {
    throw new Error("Failed to complete mission")
  }

  return response.json()
}

export async function skipMission(missionId: number) {
  const response = await fetch(`${API_URL}/missions/${missionId}/skip`, {
    method: "POST",
  })

  if (!response.ok) {
    throw new Error("Failed to skip mission")
  }

  return response.json()
}