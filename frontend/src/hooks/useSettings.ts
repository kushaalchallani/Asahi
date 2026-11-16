import { useEffect, useState, useCallback } from "react"
import {
  type DifficultyPreference as DifficultyLevel,
  updateDifficultyPreference,
  getUserPreferences,
  updateUserPreferences,
  updateEmail,
  updatePassword,
  type UserPreferences,
} from "../services/api"

export interface SettingsState {
  preferences: UserPreferences | null
  loading: boolean
  saving: boolean
  saveMessage: string
  activeModal: "name" | "password" | "email" | "deleteData" | "deleteAccount" | null
  emailInput: string
  emailError: string
  emailInfo: string | null
  nameError: string
  nameSuccess: boolean
  newName: string
  currentPassword: string
  newPassword: string
  confirmPassword: string
  passwordError: string
  passwordSuccess: boolean
}

export interface UseSettingsReturn {
  state: SettingsState
  preferences: UserPreferences | null
  loading: boolean
  saving: boolean
  saveMessage: string
  activeModal: SettingsState["activeModal"]
  emailInput: string
  emailError: string
  emailInfo: string | null
  nameError: string
  nameSuccess: boolean
  newName: string
  currentPassword: string
  newPassword: string
  confirmPassword: string
  passwordError: string
  passwordSuccess: boolean
  setEmailInput: (value: string) => void
  setNewName: (value: string) => void
  setCurrentPassword: (value: string) => void
  setNewPassword: (value: string) => void
  setConfirmPassword: (value: string) => void
  setActiveModal: (modal: SettingsState["activeModal"]) => void
  handlePreferenceChange: (key: string, value: unknown) => Promise<void>
  handleDifficultySelect: (diff: DifficultyLevel) => Promise<void>
  handleExportData: () => void
  handleDeleteData: () => void
  handleDeleteAccount: () => void
  handleNameSubmit: (e: React.FormEvent) => Promise<void>
  handleEmailSubmit: (e: React.FormEvent) => Promise<void>
  handlePasswordSubmit: (e: React.FormEvent) => Promise<void>
}

export function useSettings({
  userEmail,
  userName,
  currentDifficulty,
  onDifficultyChange,
  onLogout,
}: {
  userEmail: string
  userName: string
  currentDifficulty: DifficultyLevel | null
  onDifficultyChange: (newPref: DifficultyLevel) => void
  onLogout: () => void
}): UseSettingsReturn {
  const [state, setState] = useState<SettingsState>({
    preferences: null,
    loading: true,
    saving: false,
    saveMessage: "",
    activeModal: null,
    emailInput: "",
    emailError: "",
    emailInfo: null,
    nameError: "",
    nameSuccess: false,
    newName: userName,
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
    passwordError: "",
    passwordSuccess: false,
  })

  // load user prefs from api
  useEffect(() => {
    let active = true
    async function loadPreferences() {
      try {
        const data = await getUserPreferences()
        if (active) {
          setState(prev => ({ ...prev, preferences: data, loading: false }))
        }
      } catch {
        if (active) {
          setState(prev => ({
            ...prev,
            saveMessage: "Couldn't load preferences. Using defaults.",
            preferences: {
              theme: "system",
              reminders_enabled: true,
              reminder_time: "20:00",
              email_digest: true,
              text_size: "normal",
              reduced_motion: false,
              high_contrast: false,
            },
            loading: false,
          }))
        }
      }
    }
    loadPreferences()
    return () => { active = false }
  }, [userEmail, userName, currentDifficulty, onDifficultyChange, onLogout])

  // show saved msgs
  const showMessage = useCallback((message: string) => {
    setState(prev => ({ ...prev, saveMessage: message }))
    setTimeout(() => setState(prev => ({ ...prev, saveMessage: "" })), 3000)
  }, [])

  // udpate prefs vals
  const handlePreferenceChange = useCallback(async (key: string, value: unknown) => {
    if (!state.preferences || state.saving) return
    setState(prev => ({ ...prev, saving: true }))
    try {
      const updated = await updateUserPreferences({ [key]: value } as Partial<UserPreferences>)
      setState(prev => ({ ...prev, preferences: updated }))
      showMessage(`${key} updated.`)
    } catch {
      showMessage("Failed to update preference. Please try again.")
    } finally {
      setState(prev => ({ ...prev, saving: false }))
    }
  }, [state.preferences, state.saving, showMessage])

  // change difficulty lvl
  const handleDifficultySelect = useCallback(async (diff: DifficultyLevel) => {
    try {
      await updateDifficultyPreference(diff)
      onDifficultyChange(diff)
      showMessage("Activity difficulty updated.")
    } catch {
      showMessage("Failed to update difficulty preference.")
    }
  }, [onDifficultyChange, showMessage])

  // export user data as JSON
  const handleExportData = useCallback(() => {
    if (!state.preferences) return
    const data = {
      user: { name: userName, email: userEmail },
      exportedAt: new Date().toISOString(),
      difficulty: currentDifficulty,
      preferences: state.preferences,
    }
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `asahi-personal-data-${new Date().toISOString().split("T")[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
    showMessage("Personal data downloaded successfully.")
  }, [state.preferences, userName, userEmail, currentDifficulty, showMessage])

  // close the delete confirmation modal
  const handleDeleteData = useCallback(() => {
    setState(prev => ({ ...prev, activeModal: null }))
    showMessage("Check-in history cleared (UI demo).")
  }, [showMessage])

  // close the delete account modal and trigger logout
  const handleDeleteAccount = useCallback(() => {
    setState(prev => ({ ...prev, activeModal: null }))
    onLogout()
  }, [onLogout])

  // Handle name change form submission
  const handleNameSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    setState(prev => ({ ...prev, nameError: "" }))
    if (!state.newName.trim()) {
      setState(prev => ({ ...prev, nameError: "Name cannot be empty." }))
      return
    }
    setState(prev => ({ ...prev, saving: true }))
    try {
      setState(prev => ({ ...prev, nameSuccess: true }))
      setTimeout(() => setState(prev => ({ ...prev, nameSuccess: false })), 3000)
    } catch {
      setState(prev => ({ ...prev, nameError: "Failed to update name." }))
    } finally {
      setState(prev => ({ ...prev, saving: false }))
    }
  }, [state.newName])

  // Handle email change form submission
  const handleEmailSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    setState(prev => ({ ...prev, emailError: "", emailInfo: null }))
    if (!state.emailInput || !state.emailInput.includes("@")) {
      setState(prev => ({ ...prev, emailError: "Please enter a valid email address." }))
      return
    }
    setState(prev => ({ ...prev, saving: true }))
    try {
      await updateEmail(state.emailInput)
      setState(prev => ({ ...prev, emailInput: "", emailInfo: "Email updated successfully." }))
    } catch (err: any) {
      setState(prev => ({ ...prev, emailError: err.message || "Failed to update email." }))
    } finally {
      setState(prev => ({ ...prev, saving: false }))
    }
  }, [state.emailInput])

  // Handle password change form submission
  const handlePasswordSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    setState(prev => ({ ...prev, passwordError: "" }))
    if (state.newPassword.length < 8) {
      setState(prev => ({ ...prev, passwordError: "New password must be at least 8 characters." }))
      return
    }
    if (state.newPassword !== state.confirmPassword) {
      setState(prev => ({ ...prev, passwordError: "New passwords do not match." }))
      return
    }
    setState(prev => ({ ...prev, saving: true }))
    try {
      await updatePassword({ current_password: state.currentPassword, new_password: state.newPassword })
      setState(prev => ({
        ...prev,
        passwordSuccess: true,
        activeModal: null,
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
        saveMessage: "Password updated successfully.",
      }))
      setTimeout(() => {
        setState(prev => ({ ...prev, passwordSuccess: false, saveMessage: "" }))
      }, 1200)
    } catch (err: any) {
      setState(prev => ({ ...prev, passwordError: err.message || "Failed to update password." }))
    } finally {
      setState(prev => ({ ...prev, saving: false }))
    }
  }, [state.newPassword, state.confirmPassword, state.currentPassword])

  // Simple setter for email input field
  const setEmailInput = useCallback((value: string) => {
    setState(prev => ({ ...prev, emailInput: value }))
  }, [])

  // Simple setter for display name field
  const setNewName = useCallback((value: string) => {
    setState(prev => ({ ...prev, newName: value }))
  }, [])

  // Simple setter for current password field
  const setCurrentPassword = useCallback((value: string) => {
    setState(prev => ({ ...prev, currentPassword: value }))
  }, [])

  // Simple setter for new password field
  const setNewPassword = useCallback((value: string) => {
    setState(prev => ({ ...prev, newPassword: value }))
  }, [])

  // Simple setter for confirm password field
  const setConfirmPassword = useCallback((value: string) => {
    setState(prev => ({ ...prev, confirmPassword: value }))
  }, [])

  // Open or close a modal dialog
  const setActiveModal = useCallback((modal: SettingsState["activeModal"]) => {
    setState(prev => ({ ...prev, activeModal: modal }))
  }, [])

  return {
    state,
    preferences: state.preferences,
    loading: state.loading,
    saving: state.saving,
    saveMessage: state.saveMessage,
    activeModal: state.activeModal,
    emailInput: state.emailInput,
    emailError: state.emailError,
    emailInfo: state.emailInfo,
    nameError: state.nameError,
    nameSuccess: state.nameSuccess,
    newName: state.newName,
    currentPassword: state.currentPassword,
    newPassword: state.newPassword,
    confirmPassword: state.confirmPassword,
    passwordError: state.passwordError,
    passwordSuccess: state.passwordSuccess,
    setEmailInput,
    setNewName,
    setCurrentPassword,
    setNewPassword,
    setConfirmPassword,
    setActiveModal,
    handlePreferenceChange,
    handleDifficultySelect,
    handleExportData,
    handleDeleteData,
    handleDeleteAccount,
    handleNameSubmit,
    handleEmailSubmit,
    handlePasswordSubmit,
  }
}

// done with this bro i am soo doneee with settings