import type { Mission as MissionData } from "../../services/api"
import "./Missions.css"

interface MissionProps {
  mission: MissionData | null
  status: string
  loading: boolean
  feedbackLoading: boolean
  feedbackSubmitted: boolean
  reasons: string[]
  onFeedback: (feedback: "helpful" | "not_for_me" | "not_sure") => void
  onStart: () => void
  onComplete: () => void
  onSkip: () => void
}

function LeafIcon({ size = 22 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M5 19c0-8 5-13 14-14 0 9-5 14-14 14Z" />
      <path d="M5 19c2-4 5-7 9-9" />
    </svg>
  )
}

function Missions({
  mission,
  status,
  loading,
  feedbackLoading,
  feedbackSubmitted,
  reasons,
  onFeedback,
  onStart,
  onComplete,
  onSkip,
}: MissionProps) {
  if (loading) {
    return (
      <div className="mission-card-state" role="status">
        <span className="mission-state-icon">
          <LeafIcon />
        </span>
        <h3>Finding your mission</h3>
        <p>Looking for a small step that suits you today.</p>
      </div>
    )
  }

  if (!mission) {
    return (
      <div className="mission-card-state">
        <span className="mission-state-icon">
          <LeafIcon />
        </span>
        <h3>Your next small step starts here</h3>
        <p>Complete a check-in to get a mission suited to how you’re feeling today.</p>
      </div>
    )
  }

  const isFinished = status === "completed" || status === "skipped"

  return (
    <article className="mission-card">
      <div className="mission-card-top">
        <span className="mission-icon" aria-hidden="true">
          <LeafIcon />
        </span>

        <span className={`mission-status mission-status-${status}`}>
          {status === "assigned" && "Ready when you are"}
          {status === "started" && "In progress"}
          {status === "completed" && "Completed"}
          {status === "skipped" && "Skipped for today"}
        </span>
      </div>

      <p className="mission-eyebrow">TODAY’S MISSION</p>
      <h3 className="mission-title">{mission.title}</h3>
      <p className="mission-description">{mission.description}</p>

      {reasons.length > 0 && (
        <details className="mission-reasons">
          <summary>Why this was recommended</summary>
          <ul>
            {reasons.map((reason, index) => (
              <li key={`${reason}-${index}`}>{reason}</li>
            ))}
          </ul>
        </details>
      )}

      <div className="mission-actions">
        {status === "assigned" && (
          <button
            type="button"
            className="mission-button mission-button-primary"
            onClick={onStart}
          >
            Start mission
          </button>
        )}

        {status === "started" && (
          <>
            <button
              type="button"
              className="mission-button mission-button-primary"
              onClick={onComplete}
            >
              Complete mission
            </button>

            <button
              type="button"
              className="mission-button mission-button-secondary"
              onClick={onSkip}
            >
              Not today
            </button>
          </>
        )}
      </div>

      {status === "completed" && (
        <div className="mission-result mission-result-completed" role="status">
          <span aria-hidden="true">✓</span>
          <p>Nice work showing up for yourself today.</p>
        </div>
      )}

      {status === "skipped" && (
        <div className="mission-result" role="status">
          <p>No pressure. Some days, taking a step back is okay.</p>
        </div>
      )}

      {isFinished && (
        <div className="mission-feedback">
          {feedbackSubmitted ? (
            <p className="mission-feedback-thanks" role="status">
              Thanks for sharing your feedback.
            </p>
          ) : (
            <>
              <p className="mission-feedback-question">
                How did this mission feel for you?
              </p>

              <div className="mission-feedback-options">
                <button
                  type="button"
                  onClick={() => onFeedback("helpful")}
                  disabled={feedbackLoading}
                >
                  Helpful
                </button>

                <button
                  type="button"
                  onClick={() => onFeedback("not_for_me")}
                  disabled={feedbackLoading}
                >
                  Not for me
                </button>

                <button
                  type="button"
                  onClick={() => onFeedback("not_sure")}
                  disabled={feedbackLoading}
                >
                  Not sure
                </button>
              </div>

              {feedbackLoading && (
                <p className="mission-feedback-loading" role="status">
                  Saving your feedback…
                </p>
              )}
            </>
          )}
        </div>
      )}
    </article>
  )
}

export default Missions
