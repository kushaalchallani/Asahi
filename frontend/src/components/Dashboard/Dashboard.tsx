import "./Dashboard.css"
import { useEffect, useState } from "react"
import History from "../History/History"
import Insights from "../Insights/Insights"
import { useCheckIns } from "../../hooks/useCheckIns"
import { useMission } from "../../hooks/useMission"
import { useDifficultyPreference } from "../../hooks/useDifficultyPreference"
import DashboardSidebar from "./components/DashboardSidebar"
import DashboardHeader from "./components/DashboardHeader"
import WellbeingBanner from "./components/WellbeingBanner"
import DashboardContent from "./components/DashboardContent"
import DifficultyPreference from "./components/DifficultyPreference"
import Settings from "../Settings/Settings"

interface DashboardProps {
  onLogout: () => void
  name?: string | null
  email?: string
}

type View = "dashboard" | "history" | "insights" | "settings"

export default function Dashboard({
  onLogout,
  name,
  email,
}: DashboardProps) {
  const displayName = name || "XYZ"
  const displayEmail = email || "xyz@example.com"
  const { checkIns, handleCheckInCreated } = useCheckIns()
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
    refresh: refreshMission,
  } = useMission()
  const {
    preference,
    loading: preferenceLoading,
    saving: preferenceSaving,
    error: preferenceError,
    updatePreference,
  } = useDifficultyPreference({
    onPreferenceChange: refreshMission,
  })

  const [view, setView] = useState<View>("dashboard")
  const [showLogoutModal, setShowLogoutModal] = useState(false)

  useEffect(() => {
    if (view === "dashboard") {
      document.title = "Asahi | Dashboard"
    } else if (view === "history") {
      document.title = "Asahi | History"
    } else if (view === "insights") {
      document.title = "Asahi | Insights"
    } else if (view === "settings") {
      document.title = "Asahi | Settings"
    }
  }, [view])

  return (
    <main className="dashboard-layout" id="dashboard">
      <DashboardSidebar
        view={view}
        onViewChange={setView}
        onLogout={() => setShowLogoutModal(true)}
        userName={displayName}
        userEmail={displayEmail}
      />

      <section className="dashboard-main">
        <DashboardHeader userName={displayName} />

        {view === "dashboard" && (
          <>
            <DashboardContent
              onCheckInCreated={handleCheckInCreated}
              missionData={{
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
              }}
            />
            <DifficultyPreference
              preference={preference}
              loading={preferenceLoading}
              saving={preferenceSaving}
              error={preferenceError}
              onChange={updatePreference}
            />
            <WellbeingBanner />
          </>
        )}

        {view === "insights" && (
          <div className="dashboard-secondary" id="insights">
            <Insights />
          </div>
        )}

        {view === "history" && (
          <div className="dashboard-secondary" id="history">
            <History checkIns={checkIns} />
          </div>
        )}

        {view === "settings" && (
          <div className="dashboard-secondary" id="settings">
            <Settings
              userEmail={displayEmail}
              userName={displayName}
              currentDifficulty={preference}
              onDifficultyChange={updatePreference}
              onLogout={() => setShowLogoutModal(true)}
            />
          </div>
        )}
      </section>

      {showLogoutModal && (
        <div className="logout-modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="logout-title">
          <div className="logout-modal-card">
            <h3 id="logout-title">Are you sure you want to log out?</h3>
            <p>You can always sign back in whenever you're ready to continue your wellness journey.</p>
            <div className="logout-modal-actions">
              <button
                type="button"
                className="button-secondary"
                onClick={() => setShowLogoutModal(false)}
              >
                Cancel
              </button>
              <button
                type="button"
                className="button-primary logout-confirm-btn"
                onClick={() => {
                  setShowLogoutModal(false)
                  onLogout()
                }}
              >
                Log out
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  )
}
