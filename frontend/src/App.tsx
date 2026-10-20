import { useEffect, useState } from "react"
import Auth from "./components/Auth/Auth"
import CheckIn from "./components/CheckIn/CheckIn"
import History from "./components/History/History"
import Insights from "./components/Insights/Insights"
import Missions from "./components/Missions/Missions"
import { useCheckIns } from "./hooks/useCheckIns"
import { useInsights } from "./hooks/useInsights"
import { useMission } from "./hooks/useMission"
import { clearAccessToken, getAccessToken, getCurrentUser, type AuthUser} from "./services/api"
import "./App.css"

function Dashboard({ onLogout }: { onLogout: () => void }) {
  const { insights, refreshInsights } = useInsights()
  const { checkIns, handleCheckInCreated } = useCheckIns(refreshInsights)
  const { mission, status, loading, reasons, start, complete, skip, submitFeedback, feedbackLoading, feedbackSubmitted} = useMission()

  return (
    <main className="app">
      <section className="hero">
        <div className="dashboard-header">
          <p className="eyebrow">ASAHI</p>

          <button type="button" onClick={onLogout}>
            Log out
          </button>
        </div>

        <h1>Good evening.</h1>
        <p className="subtitle">How are you feeling today?</p>

        <CheckIn onCheckInCreated={handleCheckInCreated} />
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
        <Insights insights={insights} />
        <History checkIns={checkIns} />
      </section>
    </main>
  )
}

function App() {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [checkingSession, setCheckingSession] = useState(true)

  useEffect(() => {
    let cancelled = false

    async function restoreSession() {
      if (!getAccessToken()) {
        setCheckingSession(false)
        return
      }

      try {
        const currentUser = await getCurrentUser()

        if (!cancelled) {
          setUser(currentUser)
        }
      } catch {
        clearAccessToken()
      } finally {
        if (!cancelled) {
          setCheckingSession(false)
        }
      }
    }

    void restoreSession()

    return () => {
      cancelled = true
    }
  }, [])

  function handleLogout() {
    clearAccessToken()
    setUser(null)
  }

  if (checkingSession) {
    return <main className="auth-page">Loading Asahi...</main>
  }

  if (!user) {
    return <Auth onAuthenticated={setUser} />
  }

  return <Dashboard onLogout={handleLogout} />
}

export default App