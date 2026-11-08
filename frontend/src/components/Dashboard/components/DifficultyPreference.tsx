
import "./css/DifficultyPreference.css"
import type { DifficultyPreference as DifficultyLevel } from "../../../services/api"

interface DifficultyPreferenceProps {
  preference: DifficultyLevel | null
  loading: boolean
  saving: boolean
  error: string
  onChange: (value: DifficultyLevel) => void
}

const options: {
  value: DifficultyLevel
  title: string
  description: string
}[] = [
  {
    value: "easy",
    title: "Easy",
    description: "Small, low-effort activities",
  },
  {
    value: "moderate",
    title: "Moderate",
    description: "A balanced level of effort",
  },
  {
    value: "challenging",
    title: "Challenging",
    description: "Activities that take more effort",
  },
]

export default function DifficultyPreference({
  preference,
  loading,
  saving,
  error,
  onChange,
}: DifficultyPreferenceProps) {
  return (
    <section
      className="difficulty-panel"
      aria-labelledby="difficulty-heading"
    >
      <div className="difficulty-heading">
        <h2 id="difficulty-heading">Activity preferences</h2>
        <p>Choose the level of challenge that feels right for you.</p>
      </div>

      {loading ? (
        <p>Loading preferences...</p>
      ) : (
        <div className="difficulty-options">
          {options.map((option) => (
            <button
              key={option.value}
              type="button"
              className={`difficulty-option ${
                preference === option.value ? "selected" : ""
              }`}
              aria-pressed={preference === option.value}
              disabled={saving}
              onClick={() => onChange(option.value)}
            >
              <strong>{option.title}</strong>
              <span>{option.description}</span>
            </button>
          ))}
        </div>
      )}

      {saving && <p role="status">Saving preference...</p>}

      {error && (
        <p className="difficulty-error" role="alert">
          {error}
        </p>
      )}
    </section>
  )
}
