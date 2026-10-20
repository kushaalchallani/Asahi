import "./css/DashboardContent.css"
import "./css/CheckInCard.css"
import "./css/MissionCard.css"
import CheckIn from "../../CheckIn/CheckIn"
import Missions from "../../Missions/Missions"
import type { useCheckIns } from "../../../hooks/useCheckIns"
import type { useMission } from "../../../hooks/useMission"
import { LeafIcon } from "./DashboardIcons"

type CheckInCreatedHandler = ReturnType<
  typeof useCheckIns
>["handleCheckInCreated"]

type MissionHookData = ReturnType<typeof useMission>

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
            />
          </div>
        </div>
      </section>
    </div>
  )
}
