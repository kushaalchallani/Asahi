import { useState } from "react"
import { createCheckIn } from "../../services/api"
import type { CheckIn as CheckInData } from "../../types/checkIn"
import "./CheckIn.css"

interface CheckInProps {
  onCheckInCreated: (checkIn: CheckInData) => void
}

const moods = [
  { id: "great", label: "Great", bg: "#f9e3b9", feeling: "Great" },
  { id: "okay", label: "Okay", bg: "#eee8d8", feeling: "Okay" },
  { id: "low", label: "A little low", bg: "#f2d9d1", feeling: "A little low" },
  { id: "stressed", label: "Stressed", bg: "#efcbc3", feeling: "Stressed" },
  { id: "lonely", label: "Lonely", bg: "#e8e3d9", feeling: "Lonely" },
  { id: "unsure", label: "Not sure", bg: "#e9eadc", feeling: "Not sure" },
] as const

type MoodId = (typeof moods)[number]["id"]

const mouths: Record<MoodId, string> = {
  great: "M11 22 Q18 29 25 22",
  okay: "M12 23.5 Q18 26 24 23.5",
  low: "M12 25.5 Q18 21.5 24 25.5",
  stressed: "M12 26 Q18 20.5 24 26",
  lonely: "M13 25 Q18 22.5 23 25",
  unsure: "M12 24 Q15 22 18 24 T24 24",
}

function MoodFace({ id }: { id: MoodId }) {
  return (
    <svg width="36" height="36" viewBox="0 0 36 36" aria-hidden="true">
      <g
        stroke="#5b4a3f"
        strokeWidth="1.6"
        strokeLinecap="round"
        fill="none"
      >
        {id === "stressed" && (
          <path d="M9 10.5L15 12.5M27 10.5L21 12.5" />
        )}
        {id === "low" && (
          <path d="M9.5 12L14.5 11M26.5 12L21.5 11" />
        )}
        <path d={mouths[id]} />
      </g>
      <circle
        cx="12.5"
        cy={id === "lonely" ? 15.5 : 14.5}
        r="1.5"
        fill="#5b4a3f"
      />
      <circle
        cx="23.5"
        cy={id === "lonely" ? 15.5 : 14.5}
        r="1.5"
        fill="#5b4a3f"
      />
    </svg>
  )
}

function LeafSpray() {
  return (
    <svg className="checkin-leaves" viewBox="0 0 160 120" aria-hidden="true">
      <path
        d="M0 120 C30 98 70 96 110 104 C130 108 150 114 160 120Z"
        fill="#ecd9bf"
        opacity=".7"
      />
      <path
        d="M92 118 C92 96 100 80 112 62"
        stroke="#7d9477"
        strokeWidth="1.6"
        fill="none"
        strokeLinecap="round"
      />
      {[
        [112, 62, -10, 1],
        [106, 74, -48, 0.9],
        [104, 76, 30, 0.9],
        [98, 90, -52, 0.85],
        [96, 92, 28, 0.8],
      ].map(([x, y, r, s], i) => (
        <path
          key={i}
          d="M0 0C9-12 9-34 0-50C-9-34-9-12 0 0Z"
          fill={i % 2 ? "#8ea58a" : "#6f8a6c"}
          transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}
        />
      ))}
      <path
        d="M132 118 C132 104 136 94 142 84"
        stroke="#9db398"
        strokeWidth="1.4"
        fill="none"
        strokeLinecap="round"
      />
      {[
        [142, 84, 10, 0.7],
        [136, 96, -35, 0.6],
        [137, 98, 40, 0.6],
      ].map(([x, y, r, s], i) => (
        <path
          key={i}
          d="M0 0C9-12 9-34 0-50C-9-34-9-12 0 0Z"
          fill="#a9bba3"
          transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}
        />
      ))}
    </svg>
  )
}

export default function CheckIn({ onCheckInCreated }: CheckInProps) {
  const [selectedMood, setSelectedMood] = useState<MoodId | null>(null)
  const [checkInOpen, setCheckInOpen] = useState(false)
  const [note, setNote] = useState("")
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")

  async function handleSaveCheckIn() {
    if (!selectedMood) return

    setSaving(true)
    setError("")

    try {
      const mood = moods.find((item) => item.id === selectedMood)
      if (!mood) return

      const newCheckIn = await createCheckIn(mood.feeling, note)
      onCheckInCreated(newCheckIn)

      setSelectedMood(null)
      setCheckInOpen(false)
      setNote("")
    } catch {
      setError("Couldn't save your check-in. Please try again.")
    } finally {
      setSaving(false)
    }
  }

  return (
    <section className="dashboard-panel checkin-panel">
      <div className="panel-content checkin-content">
        <h2>How are you feeling today?</h2>

        <p className="panel-sub">
          Your check-in helps us understand your needs
          <br />
          and suggest the right support.
        </p>

        {!checkInOpen ? (
          <>
            <div
              className="mood-row"
              role="radiogroup"
              aria-label="How are you feeling?"
            >
              {moods.map((mood) => (
                <button
                  key={mood.id}
                  type="button"
                  role="radio"
                  aria-checked={selectedMood === mood.id}
                  className={`mood${selectedMood === mood.id ? " selected" : ""}`}
                  onClick={() => setSelectedMood(mood.id)}
                >
                  <span className="mood-face" style={{ background: mood.bg }}>
                    <MoodFace id={mood.id} />
                  </span>
                  <span className="mood-label">{mood.label}</span>
                </button>
              ))}
            </div>

            <button
              type="button"
              className="button-primary"
              onClick={() => {
                if (selectedMood) setCheckInOpen(true)
              }}
              disabled={!selectedMood}
            >
              Start check-in
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.7"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <path d="M5 12h14M13 6l6 6-6 6" />
              </svg>
            </button>
          </>
        ) : (
          <div className="checkin-form">
            <label htmlFor="checkin-note">
              Want to say a little more? (optional)
            </label>
            <textarea
              id="checkin-note"
              value={note}
              onChange={(event) => setNote(event.target.value)}
              rows={3}
              disabled={saving}
              placeholder="Write whatever feels comfortable..."
            />

            {error && <p className="checkin-error" role="alert">{error}</p>}

            <div className="checkin-actions">
              <button
                type="button"
                className="button-text"
                onClick={() => setCheckInOpen(false)}
                disabled={saving}
              >
                Back
              </button>
              <button
                type="button"
                className="button-primary"
                onClick={handleSaveCheckIn}
                disabled={saving}
              >
                {saving ? "Saving..." : "Save check-in"}
              </button>
            </div>
          </div>
        )}
      </div>

      <LeafSpray />
    </section>
  )
}