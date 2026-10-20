import "./Dashboard.css"
import { useState } from "react"
import History from "../History/History"
import Insights from "../Insights/Insights"
import { useCheckIns } from "../../hooks/useCheckIns"
import { useInsights } from "../../hooks/useInsights"
import { useMission } from "../../hooks/useMission"
import DashboardSidebar from "./components/DashboardSidebar"
import DashboardHeader from "./components/DashboardHeader"
import WellbeingBanner from "./components/WellbeingBanner"
import DashboardContent from "./components/DashboardContent"

interface DashboardProps {
  onLogout: () => void
  userName?: string
  userEmail?: string
}

type View = "dashboard" | "history" | "insights"

export default function Dashboard({
  onLogout,
  userName = "XYZ",
  userEmail = "xyz@example.com",
}: DashboardProps) {
  const { insights, refreshInsights } = useInsights()
  const { checkIns, handleCheckInCreated } = useCheckIns(refreshInsights)
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
  } = useMission()

  const [view, setView] = useState<View>("dashboard")

  return (
    <main className="dashboard-layout" id="dashboard">
      <DashboardSidebar
        view={view}
        onViewChange={setView}
        onLogout={onLogout}
        userName={userName}
        userEmail={userEmail}
      />

      <section className="dashboard-main">
        <DashboardHeader userName={userName} />

        {view === "dashboard" && (
          <>
            <DashboardContent
              onCheckInCreated={handleCheckInCreated}
              missionData={{
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
              }}
            />
            <WellbeingBanner />
          </>
        )}

        {view === "insights" && (
          <div className="dashboard-secondary" id="insights">
            <Insights insights={insights} />
          </div>
        )}

        {view === "history" && (
          <div className="dashboard-secondary" id="history">
            <History checkIns={checkIns} />
          </div>
        )}
      </section>
    </main>
  )
}
