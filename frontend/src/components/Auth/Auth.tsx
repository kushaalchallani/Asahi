import { useState, type FormEvent } from "react"
import { login, register, saveAccessToken, type AuthUser } from "../../services/api"
import "./Auth.css"

interface AuthProps {
  onAuthenticated: (user: AuthUser) => void
  initialMode?: "login" | "register"
  onBack: () => void
}

/* ---------- small pieces ---------- */

function EyeIcon({ off }: { off: boolean }) {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z" />
      <circle cx="12" cy="12" r="3" />
      {off && <path d="M4 4l16 16" />}
    </svg>
  )
}

const LEAF = "M0 0C9-12 9-34 0-50C-9-34-9-12 0 0Z"

/* hills + leaves in the bottom corner of the card; colours come from CSS variables */
function AuthDecor() {
  const leaves: [number, number, number, number, string][] = [
    [372, 104, -12, 1.05, "var(--leaf-a)"],
    [366, 118, -52, 0.95, "var(--leaf-b)"],
    [366, 120, 28, 0.9, "var(--leaf-a)"],
    [356, 134, -64, 0.8, "var(--leaf-b)"],
    [388, 112, 22, 0.85, "var(--leaf-b)"],
    [340, 138, -38, 0.7, "var(--leaf-c)"],
    [398, 128, 40, 0.7, "var(--leaf-c)"],
  ]

  return (
    <svg
      className="auth-decor"
      viewBox="0 0 420 150"
      preserveAspectRatio="xMaxYMax slice"
      aria-hidden="true"
    >
      <path
        d="M0 150V104C60 84 130 96 210 106C290 116 350 96 420 72V150Z"
        style={{ fill: "var(--hill-1)" }}
      />
      <path
        d="M0 150V124C80 108 170 122 250 128C320 134 380 118 420 104V150Z"
        style={{ fill: "var(--hill-2)" }}
      />
      <path
        d="M372 150C372 130 374 118 380 98"
        stroke="var(--leaf-a)"
        strokeWidth="1.6"
        fill="none"
        strokeLinecap="round"
      />
      {leaves.map(([x, y, r, s, fill], i) => (
        <path
          key={i}
          d={LEAF}
          style={{ fill }}
          transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}
        />
      ))}
    </svg>
  )
}

/* ---------- component ---------- */

function Auth({ onAuthenticated, initialMode = "login", onBack }: AuthProps) {
  const [mode, setMode] = useState<"login" | "register">(initialMode)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError("")

    const normalizedEmail = email.trim().toLowerCase()

    if (mode === "register" && password !== confirmPassword) {
      setError("Your passwords don't match.")
      return
    }

    setLoading(true)

    try {
      if (mode === "register") {
        await register(normalizedEmail, password)
      }

      const result = await login(normalizedEmail, password)
      saveAccessToken(result.access_token)
      onAuthenticated(result.user)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong. Please try again."
      )
    } finally {
      setLoading(false)
    }
  }

  function switchMode() {
    setMode((current) => (current === "login" ? "register" : "login"))
    setError("")
    setPassword("")
    setConfirmPassword("")
    setShowPassword(false)
    setShowConfirm(false)
  }

  const isLogin = mode === "login"

  const aside = isLogin
    ? {
        title: "Pick up where you left off.",
        text: "Your check-ins, missions and progress are right where you left them.",
      }
    : {
        title: "A little more room to be yourself.",
        text: "Check in with how you feel, take small steps at your own pace, and find connection when you\u2019re ready.",
      }

  return (
    <main className="auth-page auth-split">
      <aside className="auth-aside">
        <img src="/images/asahi-landscape.png" alt="" />
        <div className="auth-aside-copy">
          <p className="auth-aside-eyebrow">Mental wellness / real connections</p>
          <h2>{aside.title}</h2>
          <p>{aside.text}</p>
        </div>
      </aside>

      <div className="auth-main">
      <section className={`auth-card ${isLogin ? "is-login" : "is-register"}`}>
        <button className="auth-back" type="button" onClick={onBack}>
          ← Back
        </button>

        <div className="auth-logo" role="img" aria-label="Asahi" />

        <h1>{isLogin ? "Welcome back" : "Create your account"}</h1>

        <p className="auth-subtitle">
          {isLogin
            ? "Good to see you again. Take a moment for yourself."
            : "Start your journey towards better mental well-being."}
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-field">
            <label htmlFor="auth-email">Email address</label>
            <input
              id="auth-email"
              type="email"
              autoComplete="email"
              placeholder="you@example.com"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </div>

          <div className="auth-field">
            <label htmlFor="auth-password">Password</label>
            <div className="auth-password">
              <input
                id="auth-password"
                type={showPassword ? "text" : "password"}
                autoComplete={isLogin ? "current-password" : "new-password"}
                placeholder={isLogin ? "Enter your password" : "At least 8 characters"}
                minLength={isLogin ? 1 : 8}
                maxLength={128}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
              <button
                className="auth-eye"
                type="button"
                onClick={() => setShowPassword((v) => !v)}
                aria-label={showPassword ? "Hide password" : "Show password"}
                aria-pressed={showPassword}
              >
                <EyeIcon off={showPassword} />
              </button>
            </div>
          </div>

          {!isLogin && (
            <div className="auth-field">
              <label htmlFor="auth-confirm-password">Confirm password</label>
              <div className="auth-password">
                <input
                  id="auth-confirm-password"
                  type={showConfirm ? "text" : "password"}
                  autoComplete="new-password"
                  placeholder="Re-enter your password"
                  minLength={8}
                  maxLength={128}
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  required
                />
                <button
                  className="auth-eye"
                  type="button"
                  onClick={() => setShowConfirm((v) => !v)}
                  aria-label={showConfirm ? "Hide password" : "Show password"}
                  aria-pressed={showConfirm}
                >
                  <EyeIcon off={showConfirm} />
                </button>
              </div>
            </div>
          )}

          {error && (
            <p className="auth-error" role="alert">
              {error}
            </p>
          )}

          <button className="auth-submit" type="submit" disabled={loading}>
            {loading ? "Please wait..." : isLogin ? "Log in" : "Create account"}
          </button>
        </form>

        <p className="auth-switch">
          {isLogin ? "Don\u2019t have an account?" : "Already have an account?"}{" "}
          <button type="button" onClick={switchMode}>
            {isLogin ? "Get started" : "Log in"}
          </button>
        </p>

        <AuthDecor />
      </section>
      </div>
    </main>
  )
}

export default Auth