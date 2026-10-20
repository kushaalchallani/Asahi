import { useState, type FormEvent } from "react"
import { login, register, saveAccessToken, type AuthUser} from "../../services/api"

interface AuthProps {
  onAuthenticated: (user: AuthUser) => void
}

function Auth({ onAuthenticated }: AuthProps) {
  const [mode, setMode] = useState<"login" | "register">("login")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
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
    setMode((current) => current === "login" ? "register" : "login")
    setError("")
    setPassword("")
    setConfirmPassword("")
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <p className="eyebrow">ASAHI</p>

        <h1>{mode === "login" ? "Welcome back." : "A fresh start."}</h1>

        <p className="auth-subtitle">
          {mode === "login" ? "Make a little room for yourself." : "Your space to check in, reflect, and grow."}
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label htmlFor="auth-email">Email address</label>
          <input
            id="auth-email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />

          <label htmlFor="auth-password">Password</label>
          <input
            id="auth-password"
            type="password"
            autoComplete={ mode === "login" ? "current-password" : "new-password"}
            minLength={mode === "register" ? 8 : 1}
            maxLength={128}
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />

          {mode === "register" && (
            <>
              <label htmlFor="auth-confirm-password">Confirm password</label>
              <input
                id="auth-confirm-password"
                type="password"
                autoComplete="new-password"
                minLength={8}
                maxLength={128}
                value={confirmPassword}
                onChange={(event) => setConfirmPassword(event.target.value)}
                required
              />
            </>
          )}

          {error && (
            <p className="auth-error" role="alert">
              {error}
            </p>
          )}

          <button className="auth-submit" type="submit" disabled={loading}>
            {loading ? "Please wait..." : mode === "login" ? "Log in" : "Create account"}
          </button>
        </form>

        <p className="auth-switch">
          {mode === "login" ? "New to Asahi?" : "Already have an account?"}{" "}
          <button type="button" onClick={switchMode}>
            {mode === "login" ? "Create an account" : "Log in"}
          </button>
        </p>
      </section>
    </main>
  )
}

export default Auth
