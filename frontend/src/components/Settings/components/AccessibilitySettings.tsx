import { type TextSize } from "../../../services/api"
import SettingsCard from "./SettingsCard"
import SettingsRow from "./SettingsRow"

interface AccessibilitySettingsProps {
  preferences: {
    theme: string
    text_size: TextSize
    reduced_motion: boolean
    high_contrast: boolean
  }
  onPreferenceChange: (key: string, value: unknown) => void
  saving: boolean
}

const AccessibilitySettings: React.FC<AccessibilitySettingsProps> = ({
  preferences,
  onPreferenceChange,
  saving,
}) => {
  return (
    <SettingsCard title="Accessibility" description="Adjust text scaling, motion, and contrast for visual comfort.">
      <SettingsRow
        label="Text Size"
        action={
          <select
            className="settings-select"
            value={preferences.text_size}
            onChange={(e) => onPreferenceChange("text_size", e.target.value as TextSize)}
            disabled={saving}
          >
            <option value="normal">Normal (100%)</option>
            <option value="large">Large (110%)</option>
            <option value="xlarge">Extra Large (125%)</option>
          </select>
        }
      />
      <SettingsRow
        label="Reduced Motion"
        sublabel="Minimize interface animations"
        action={
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={preferences.reduced_motion}
              onChange={(e) => onPreferenceChange("reduced_motion", e.target.checked)}
              disabled={saving}
            />
            <span className="slider" />
          </label>
        }
      />
      <SettingsRow
        label="High Contrast Mode"
        sublabel="Enhance text and border definition"
        action={
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={preferences.high_contrast}
              onChange={(e) => onPreferenceChange("high_contrast", e.target.checked)}
              disabled={saving}
            />
            <span className="slider" />
          </label>
        }
      />
    </SettingsCard>
  )
}

export default AccessibilitySettings