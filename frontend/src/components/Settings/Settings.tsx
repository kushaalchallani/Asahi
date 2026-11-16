import { type DifficultyPreference as DifficultyLevel } from "../../services/api"
import { useSettings } from "../../hooks/useSettings"
import AccountSection from "./components/AccountSection"
import PersonalizationSettings from "./components/PersonalizationSettings"
import AccessibilitySettings from "./components/AccessibilitySettings"
import PrivacyDataSettings from "./components/PrivacyDataSettings"
import AboutSection from "./components/AboutSection"
import SettingsModal from "./components/SettingsModal"
import "./Settings.css"

interface SettingsProps {
  userEmail: string
  userName: string
  currentDifficulty: DifficultyLevel | null
  onDifficultyChange: (newPref: DifficultyLevel) => void
  onLogout: () => void
}

export default function Settings({
  userEmail,
  userName,
  currentDifficulty,
  onDifficultyChange,
  onLogout,
}: SettingsProps) {
  const {
    preferences,
    loading,
    saving,
    saveMessage,
    activeModal,
    emailInput,
    emailError,
    emailInfo,
    nameError,
    nameSuccess,
    newName,
    currentPassword,
    newPassword,
    confirmPassword,
    passwordError,
    passwordSuccess,
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
  } = useSettings({
    userEmail,
    userName,
    currentDifficulty,
    onDifficultyChange,
    onLogout,
  })

  if (loading) {
    return <div className="settings-page"><p>Loading settings...</p></div>
  }

  const p = preferences || {
    theme: "system",
    reminders_enabled: true,
    reminder_time: "20:00",
    email_digest: true,
    text_size: "normal",
    reduced_motion: false,
    high_contrast: false,
  }

  return (
    <div className="settings-page">
      <header className="settings-header">
        <div>
          <h1 className="settings-title">Settings & Preferences</h1>
          <p className="settings-subtitle">Tailor your Asahi experience to your calm and well-being.</p>
        </div>
        {saveMessage && <div className="settings-toast" role="status">{saveMessage}</div>}
      </header>

      <div className="settings-sections">
        <AccountSection
          userEmail={userEmail}
          userName={userName}
          onEditName={() => setActiveModal("name")}
          onChangeEmail={() => setActiveModal("email")}
          onChangePassword={() => setActiveModal("password")}
        />

        <PersonalizationSettings
          currentDifficulty={currentDifficulty}
          onDifficultySelect={handleDifficultySelect}
          preferences={p}
          onPreferenceChange={handlePreferenceChange}
          saving={saving}
        />

        <AccessibilitySettings
          preferences={p}
          onPreferenceChange={handlePreferenceChange}
          saving={saving}
        />

        <PrivacyDataSettings
          onExportData={handleExportData}
          onDeleteData={handleDeleteData}
          onDeleteAccount={handleDeleteAccount}
          saving={saving}
        />

        <AboutSection />
      </div>
      
      <SettingsModal open={activeModal === "name"} title="Edit Name">
        <form onSubmit={handleNameSubmit} className="settings-modal-form">
          <div className="auth-field">
            <label>Display Name</label>
            <input type="text" value={newName} onChange={(e) => setNewName(e.target.value)} required />
          </div>
          {nameError && <p className="auth-error">{nameError}</p>}
          {nameSuccess && <p className="settings-success-text">Name updated!</p>}
          <div className="logout-modal-actions">
            <button type="button" className="button-secondary" onClick={() => setActiveModal(null)}>Cancel</button>
            <button type="submit" className="button-primary" disabled={saving}>
              {saving ? "Updating..." : "Save name"}
            </button>
          </div>
        </form>
      </SettingsModal>

      <SettingsModal open={activeModal === "email"} title="Change Email Address">
        <form onSubmit={handleEmailSubmit} className="settings-modal-form">
          <div className="auth-field">
            <label>Current Email</label>
            <input type="email" value={userEmail} readOnly style={{ backgroundColor: "#f2efe7", fontWeight: 500 }} />
          </div>
          <div className="auth-field">
            <label>New Email</label>
            <input type="email" value={emailInput} onChange={(e) => setEmailInput(e.target.value)} placeholder="Enter your new email" required />
          </div>
          {emailError && <p className="auth-error">{emailError}</p>}
          {emailInfo && <p className="settings-success-text">{emailInfo}</p>}
          <div className="logout-modal-actions">
            <button type="button" className="button-secondary" onClick={() => setActiveModal(null)}>Cancel</button>
            <button type="submit" className="button-primary" disabled={saving}>
              {saving ? "Updating..." : "Update email"}
            </button>
          </div>
        </form>
      </SettingsModal>

      <SettingsModal open={activeModal === "password"} title="Change Password">
        <form onSubmit={handlePasswordSubmit} className="settings-modal-form">
          <div className="auth-field">
            <label>Current Password</label>
            <input type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} required />
          </div>
          <div className="auth-field">
            <label>New Password (min 8 chars)</label>
            <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} minLength={8} required />
          </div>
          <div className="auth-field">
            <label>Confirm New Password</label>
            <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
          </div>
          {passwordError && <p className="auth-error">{passwordError}</p>}
          {passwordSuccess && <p className="settings-success-text">Password updated successfully!</p>}
          <div className="logout-modal-actions">
            <button type="button" className="button-secondary" onClick={() => setActiveModal(null)}>Cancel</button>
            <button type="submit" className="button-primary">Save password</button>
          </div>
        </form>
      </SettingsModal>

      <SettingsModal open={activeModal === "deleteData"} title="Delete Check-In History?">
        <p>This action cannot be undone. All your logged check-ins and notes will be permanently removed.</p>
        <div className="logout-modal-actions">
          <button type="button" className="button-secondary" onClick={() => setActiveModal(null)}>Cancel</button>
          <button type="button" className="button-primary logout-confirm-btn" onClick={handleDeleteData}>
            Yes, clear history
          </button>
        </div>
      </SettingsModal>

      <SettingsModal open={activeModal === "deleteAccount"} title="Delete Account Permanently?">
        <p>This will permanently erase your Asahi account, profile, and all associated data. Are you absolutely sure?</p>
        <div className="logout-modal-actions">
          <button type="button" className="button-secondary" onClick={() => setActiveModal(null)}>Cancel</button>
          <button type="button" className="button-primary logout-confirm-btn" onClick={handleDeleteAccount}>
            Permanently delete
          </button>
        </div>
      </SettingsModal>
    </div>
  )
}