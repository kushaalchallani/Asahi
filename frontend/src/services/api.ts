import type { CheckIn } from "../types/checkIn"

const API_URL = "http://localhost:8000"
const TOKEN_KEY = "asahi_access_token"

export function getAccessToken(): string | null {
  return sessionStorage.getItem(TOKEN_KEY)
}

export function saveAccessToken(token: string): void {
  sessionStorage.setItem(TOKEN_KEY, token)
}

export function clearAccessToken(): void {
  sessionStorage.removeItem(TOKEN_KEY)
}

async function apiRequest(path: string, options: RequestInit = {}): Promise<Response> {
  const headers = new Headers(options.headers)
  const token = getAccessToken()

  if (token) {
    headers.set("Authorization", `Bearer ${token}`)
  }

  return fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  })
}

export interface AuthUser {
  id: number
  email: string
  is_active: boolean
}

export interface AuthToken {
  access_token: string
  token_type: string
  user: AuthUser
}

export async function register(
  email: string,
  password: string
): Promise<AuthUser> {
  const response = await apiRequest("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })

  if (!response.ok) {
    throw new Error("Registration failed. Please check your details.")
  }

  return response.json()
}

export async function login(
  email: string,
  password: string
): Promise<AuthToken> {
  const response = await apiRequest("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })

  if (!response.ok) {
    throw new Error("Login failed. Check your email and password.")
  }

  return response.json()
}

export async function getCurrentUser(): Promise<AuthUser> {
  const response = await apiRequest("/auth/me")

  if (!response.ok) {
    throw new Error("Failed to fetch current user")
  }

  return response.json()
}

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
  const response = await apiRequest("/check-ins", {
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
  const response = await apiRequest("/check-ins")

  if (!response.ok) {
    throw new Error("Failed to fetch check-ins")
  }

  return response.json()
}

export async function getCheckInInsights(): Promise<CheckInInsights> {
  const response = await apiRequest("/check-ins/insights")

  if (!response.ok) {
    throw new Error("Failed to fetch check-in insights")
  }

  return response.json()
}

export async function getTodayMission(): Promise<TodayMission> {
  const response = await apiRequest("/missions/today")

  if (!response.ok) {
    throw new Error("Failed to fetch today's mission")
  }

  return response.json()
}

export async function startMission(assignmentId: number) {
  const response = await apiRequest(`/missions/assignments/${assignmentId}/start`, {
    method: "POST",
  })

  if (!response.ok) {
    throw new Error("Failed to start mission")
  }

  return response.json()
}

export async function completeMission(assignmentId: number) {
  const response = await apiRequest(`/missions/assignments/${assignmentId}/complete`, {
    method: "POST",
  })

  if (!response.ok) {
    throw new Error("Failed to complete mission")
  }

  return response.json()
}

export async function skipMission(assignmentId: number) {
  const response = await apiRequest(`/missions/assignments/${assignmentId}/skip`, {
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
  const response = await  apiRequest(`/missions/assignments/${assignmentId}/feedback`, {
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