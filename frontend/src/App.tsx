import { useEffect, useState } from "react"
import Auth from "./components/Auth/Auth"
import Landing from "./components/Landing/Landing"
import Dashboard from "./components/Dashboard/Dashboard"
import { clearAccessToken, getAccessToken, getCurrentUser, type AuthUser} from "./services/api"

function App() {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [checkingSession, setCheckingSession] = useState(true)
  const [publicView, setPublicView] = useState<"landing" | "login" | "register">("landing")

  useEffect(() => {
    if (!user) {
      if (publicView === "landing") {
        document.title = "Asahi — Mental Wellness & Real Connections"
      } else if (publicView === "login") {
        document.title = "Asahi | Log In"
      } else if (publicView === "register") {
        document.title = "Asahi | Get Started"
      }
    }
  }, [user, publicView])

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
    if (publicView === "landing") {
      return (
        <Landing
          onGetStarted={() => setPublicView("register")}
          onLogin={() => setPublicView("login")}
        />
      )
    }

    return (
      <Auth
        key={publicView}
        initialMode={publicView}
        onAuthenticated={setUser}
        onBack={() => setPublicView("landing")}
      />
    )
  }

  return (
      <Dashboard
        onLogout={handleLogout}
        name={user.name}
        email={user.email}
      />
    )
}

export default App