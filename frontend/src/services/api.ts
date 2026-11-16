import type { CheckIn } from "../types/checkIn"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"
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
  name?: string | null
}

export interface AuthToken {
  access_token: string
  token_type: string
  user: AuthUser
}

export type DifficultyPreference = "easy" | "moderate" | "challenging";
export interface DifficultyPreferenceResponse {
  difficulty_preference: DifficultyPreference;
}


export async function register(
  email: string,
  password: string,
  name?: string
): Promise<AuthUser> {
  const body: { email: string; password: string; name?: string } = { email, password }
  if (name) {
    body.name = name
  }

  const response = await apiRequest("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
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

export async function getDifficultyPreference(): Promise<DifficultyPreferenceResponse> {
  const response = await apiRequest("/preferences/difficulty");

  if (!response.ok) {
    throw new Error("Failed to fetch difficulty preference");
  }

  return response.json();
}

export async function updateDifficultyPreference(
  difficulty_preference: DifficultyPreference
): Promise<DifficultyPreferenceResponse> {
  const response = await apiRequest("/preferences/difficulty", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ difficulty_preference }),
  });

  if (!response.ok) {
    throw new Error("Failed to update difficulty preference");
  }

  return response.json();
}

// settings
export type Theme = "light" | "dark" | "system"
export type TextSize = "normal" | "large" | "xlarge"

export interface UserPreferences {
  theme: Theme
  reminders_enabled: boolean
  reminder_time: string
  email_digest: boolean
  text_size: TextSize
  reduced_motion: boolean
  high_contrast: boolean
}

export interface UpdateUserPreferences {
  theme?: Theme
  reminders_enabled?: boolean
  reminder_time?: string
  email_digest?: boolean
  text_size?: TextSize
  reduced_motion?: boolean
  high_contrast?: boolean
}

export async function getUserPreferences(): Promise<UserPreferences> {
  const response = await apiRequest("/preferences/settings");

  if (!response.ok) {
    throw new Error("Failed to fetch user preferences");
  }

  return response.json();
}

export async function updateUserPreferences(
  preferences: UpdateUserPreferences
): Promise<UserPreferences> {
  const response = await apiRequest("/preferences/settings", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(preferences),
  });

  if (!response.ok) {
    throw new Error("Failed to update user preferences");
  }

  return response.json();
}

export async function updateEmail(newEmail: string): Promise<AuthUser> {
  const response = await apiRequest("/preferences/email", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email: newEmail }),
  });

  if (!response.ok) {
    throw new Error("Failed to update email");
  }

  return response.json();
}

export interface UpdatePasswordRequest {
  current_password: string
  new_password: string
}

export async function updatePassword(data: UpdatePasswordRequest): Promise<AuthUser> {
  const response = await apiRequest("/preferences/password", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Failed to update password");
  }

  return response.json();
}