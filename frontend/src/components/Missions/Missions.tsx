import type { Mission as MissionData} from "../../services/api"

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

function Missions({mission, status, loading, feedbackLoading, feedbackSubmitted, reasons, onStart, onComplete, onSkip, onFeedback}: MissionProps){
    if (loading || !mission) {
        return null
    }

    return (
        <div className="mission-card">
            <p className="mission-label">Today's Mission</p>

            <h2>{mission.title}</h2>
            <p>{mission.description}</p>

            {reasons.length > 0 && (
                <div className="mission-reasons">
                    <p>Why this was recommended</p>
                    <ul>
                    {reasons.map((reason) => (
                        <li key={reason}>{reason}</li>
                    ))}
                    </ul>
                </div>
            )}

            {status === "assigned" && (
            <button onClick={onStart}>Start mission</button>
            )}

            {status === "started" && (
            <>
                <button onClick={onComplete}>Complete mission</button>
                <button onClick={onSkip}>Not today</button>
            </>
            )}

            {status === "completed" && (
            <p>Completed. Nice work!</p>
            )}

            {status === "skipped" && (
            <p>No pressure. You can leave it for today.</p>
            )}

            {(status === "completed" || status === "skipped") && !feedbackSubmitted && (
                <div className="mission-feedback">
                {!feedbackSubmitted ? (
                    <>
                    <p>How was this mission for you?</p>

                    <button onClick={() => onFeedback("helpful")} disabled={feedbackLoading}>
                        Helpful
                    </button>

                    <button onClick={() => onFeedback("not_for_me")} disabled={feedbackLoading}>
                        Not for me
                    </button>

                    <button onClick={() => onFeedback("not_sure")} disabled={feedbackLoading}>
                        Not sure
                    </button>

                    {feedbackLoading && <p>Submitting feedback...</p>}
                    </>
                ) : (
                    <p>Thanks for sharing your feedback.</p>
                )}
                </div>
                )}
        </div>
    )
}

export default Missions