import { type DifficultyPreference as DifficultyLevel, type Theme, type TextSize } from "../../../services/api"
import SettingsCard from "./SettingsCard"
import SettingsRow from "./SettingsRow"

interface PersonalizationSettingsProps {
  currentDifficulty: DifficultyLevel | null
  onDifficultySelect: (diff: DifficultyLevel) => void
  preferences: {
    theme: Theme
    reminders_enabled: boolean
    reminder_time: string
    email_digest: boolean
    text_size: TextSize
  }
  onPreferenceChange: (key: string, value: unknown) => void
  saving: boolean
}

const PersonalizationSettings: React.FC<PersonalizationSettingsProps> = ({
  currentDifficulty,
  onDifficultySelect,
  preferences,
  onPreferenceChange,
  saving,
}) => {
  return (
    <SettingsCard title="Personalization" description="Customize your difficulty level, appearance, and reminders.">
      <div className="settings-group-block">
        <label className="settings-label">Mission Difficulty Preference</label>
        <p className="settings-sublabel">Choose the level of challenge that feels right for you.</p>
        <div className="difficulty-pill-group" role="radiogroup" aria-label="Difficulty Preference">
          {(["easy", "moderate", "challenging"] as const).map((level) => (
            <button
              key={level}
              type="button"
              role="radio"
              aria-checked={currentDifficulty === level}
              className={`diff-pill ${currentDifficulty === level ? "active" : ""}`}
              onClick={() => onDifficultySelect(level)}
              disabled={saving}
            >
              {level.charAt(0).toUpperCase() + level.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="settings-group-block">
        <label className="settings-label">Appearance Theme</label>
        <div className="difficulty-pill-group" role="radiogroup" aria-label="Appearance Theme">
          {(["light", "dark", "system"] as const).map((t) => (
            <button
              key={t}
              type="button"
              role="radio"
              aria-checked={preferences.theme === t}
              className={`diff-pill ${preferences.theme === t ? "active" : ""}`}
              onClick={() => onPreferenceChange("theme", t)}
              disabled={saving}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <SettingsRow
        label="Daily Check-in Reminders"
        sublabel="Receive a gentle daily notification"
        action={
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={preferences.reminders_enabled}
              onChange={(e) => onPreferenceChange("reminders_enabled", e.target.checked)}
              disabled={saving}
            />
            <span className="slider" />
          </label>
        }
      />

      {preferences.reminders_enabled && (
        <SettingsRow
          label="Reminder Time"
          action={
            <input
              type="time"
              className="settings-time-input"
              value={preferences.reminder_time}
              onChange={(e) => onPreferenceChange("reminder_time", e.target.value)}
              disabled={saving}
            />
          }
        />
      )}

      <SettingsRow
        label="Weekly Insight Digest"
        sublabel="Receive a summary of your emotional rhythm"
        action={
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={preferences.email_digest}
              onChange={(e) => onPreferenceChange("email_digest", e.target.checked)}
              disabled={saving}
            />
            <span className="slider" />
          </label>
        }
      />
    </SettingsCard>
  )
}

export default PersonalizationSettings