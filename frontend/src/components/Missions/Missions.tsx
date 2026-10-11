import type { Mission as MissionData} from "../../services/api"

interface MissionProps {
  mission: MissionData | null
  status: string
  loading: boolean
  onStart: () => void
  onComplete: () => void
  onSkip: () => void
}

function Missions({mission, status, loading, onStart, onComplete, onSkip}: MissionProps){
    if (loading || !mission) {
        return null
    }

    return (
        <div className="mission-card">
            <p className="mission-label">Today's Mission</p>

            <h2>{mission.title}</h2>
            <p>{mission.description}</p>

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
        </div>
    )
}

export default Missions