import { useEffect, useState } from "react"

export function useSettingsPersistence() {
  const [settings, setSettings] = useState({
    theme: (localStorage.getItem("asahi_theme") as "light" | "dark" | "system") || "system",
    remindersEnabled: localStorage.getItem("asahi_reminders") === "true",
    reminderTime: localStorage.getItem("asahi_reminder_time") || "20:00",
    emailDigest: localStorage.getItem("asahi_email_digest") === "true",
    textSize: (localStorage.getItem("asahi_text_size") as "normal" | "large" | "xlarge") || "normal",
    reducedMotion: localStorage.getItem("asahi_reduced_motion") === "true",
    highContrast: localStorage.getItem("asahi_high_contrast") === "true",
  })

  useEffect(() => {
    const onStorageChange = (e: StorageEvent) => {
      const key = e.key
      if (key && key.startsWith("asahi_")) {
        setSettings((prev) => ({
          ...prev,
          [key.replace("asahi_", "")]: e.newValue,
        }))
      }
    }

    window.addEventListener("storage", onStorageChange)
    return () => window.removeEventListener("storage", onStorageChange)
  }, [])

  const saveSetting = (key: string, value: string) => {
    localStorage.setItem(`asahi_${key}`, value)
    setSettings((prev) => ({ ...prev, [key]: value }))
  }

  return {
    settings,
    saveSetting,
    theme: settings.theme,
    remindersEnabled: settings.remindersEnabled,
    reminderTime: settings.reminderTime,
    emailDigest: settings.emailDigest,
    textSize: settings.textSize,
    reducedMotion: settings.reducedMotion,
    highContrast: settings.highContrast,
  }
}