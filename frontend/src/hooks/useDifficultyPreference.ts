
import { useEffect, useState } from "react"
import {
  getDifficultyPreference,
  updateDifficultyPreference,
  type DifficultyPreference,
} from "../services/api"

export function useDifficultyPreference(
  options?: {
    onPreferenceChange?: () => void
  }
) {
  const { onPreferenceChange } = options || {}

  const [preference, setPreference] =
    useState<DifficultyPreference | null>(null)

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    let active = true

    async function loadPreference() {
      try {
        const data = await getDifficultyPreference()

        if (active) {
          setPreference(data.difficulty_preference)
        }
      } catch {
        if (active) {
          setError("Couldn't load your activity preference.")
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadPreference()

    return () => {
      active = false
    }
  }, [])

  async function updatePreference(value: DifficultyPreference) {
    if (saving || value === preference) return

    setSaving(true)
    setError("")

    try {
      const data = await updateDifficultyPreference(value)
      setPreference(data.difficulty_preference)

      // Trigger refresh callback if provided
      if (onPreferenceChange) {
        onPreferenceChange()
      }
    } catch {
      setError("Couldn't update your preference. Please try again.")
    } finally {
      setSaving(false)
    }
  }

  return {
    preference,
    loading,
    saving,
    error,
    updatePreference,
  }
}
