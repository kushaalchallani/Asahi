import "./css/DashboardContent.css"
import "./css/CheckInCard.css"
import "./css/MissionCard.css"
import CheckIn from "../../CheckIn/CheckIn"
import Missions from "../../Missions/Missions"
import type { MissionStatus } from "../../hooks/useMission"
import type { Mission } from "../../services/api"
import type { useCheckIns } from "../../../hooks/useCheckIns"
import { LeafIcon } from "./DashboardIcons"

type CheckInCreatedHandler = ReturnType<
  typeof useCheckIns
>["handleCheckInCreated"]

interface MissionHookData {
  mission: Mission | null
  status: MissionStatus
  loading: boolean
  reasons: string[]
  message?: string
  start: () => Promise<void>
  complete: () => Promise<void>
  skip: () => Promise<void>
  submitFeedback: (feedback: "helpful" | "not_for_me" | "not_sure") => Promise<void>
  feedbackLoading: boolean
  feedbackSubmitted: boolean
  refresh: () => Promise<void>
}

interface DashboardContentProps {
  onCheckInCreated: CheckInCreatedHandler
  missionData: MissionHookData
}

export default function DashboardContent({
  onCheckInCreated,
  missionData,
}: DashboardContentProps) {
  const {
    mission,
    status,
    loading,
    reasons,
    message,
    start,
    complete,
    skip,
    submitFeedback,
    feedbackLoading,
    feedbackSubmitted,
  } = missionData

  return (
    <div className="dashboard-card-grid">
      <CheckIn onCheckInCreated={onCheckInCreated} />

      <section className="dashboard-panel mission-panel">
        <div className="panel-content">
          <div className="mission-heading">
            <span className="mission-heading-icon" aria-hidden="true">
              <LeafIcon size={14} />
            </span>
            <h2>Today&rsquo;s mission</h2>
          </div>

          <p className="panel-sub">
            A small step can make a big difference.
          </p>

          <div className="mission-inner mission-live">
            <Missions
              mission={mission}
              status={status}
              loading={loading}
              onStart={start}
              onComplete={complete}
              onSkip={skip}
              onFeedback={submitFeedback}
              feedbackLoading={feedbackLoading}
              feedbackSubmitted={feedbackSubmitted}
              reasons={reasons}
              message={message}
            />
          </div>
        </div>
      </section>
    </div>
  )
}
