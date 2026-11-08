import "./css/DashboardHeader.css"
import { BellIcon, SunIcon } from "./DashboardIcons"

interface DashboardHeaderProps {
  userName: string
}

export default function DashboardHeader({
  userName,
}: DashboardHeaderProps) {
  const hour = new Date().getHours()

  const greeting =
    hour >= 5 && hour < 12
      ? "Good morning"
      : hour >= 12 && hour < 18
        ? "Good afternoon"
        : "Good evening"

  const today = new Date().toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  })

  return (
    <header className="dashboard-topbar">
      <div className="topbar-greeting">
        <span className="topbar-sun" aria-hidden="true">
          <SunIcon size={30} />
        </span>

        <div>
          <h1>
            {greeting}, {userName}
          </h1>
          <p>Take a moment. You&rsquo;re doing better than you think.</p>
        </div>
      </div>

      <div className="topbar-actions">
        <span className="dashboard-date">{today}</span>

        <button
          className="topbar-bell"
          type="button"
          aria-label="Notifications"
        >
          <BellIcon size={20} />
          <i aria-hidden="true" />
        </button>
      </div>
    </header>
  )
}
