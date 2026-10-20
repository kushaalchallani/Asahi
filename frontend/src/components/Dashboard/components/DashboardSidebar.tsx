import "./css/DashboardSidebar.css"
import {
  BarsIcon,
  ClockIcon,
  HomeIcon,
  LogoutIcon,
} from "./DashboardIcons"

type View = "dashboard" | "history" | "insights"

interface DashboardSidebarProps {
  view: View
  onViewChange: (view: View) => void
  onLogout: () => void
  userName: string
  userEmail: string
}

export default function DashboardSidebar({
  view,
  onViewChange,
  onLogout,
  userName,
  userEmail,
}: DashboardSidebarProps) {
  const navItems = [
    { id: "dashboard" as const, label: "Dashboard", icon: <HomeIcon /> },
    { id: "history" as const, label: "History", icon: <ClockIcon /> },
    { id: "insights" as const, label: "Insights", icon: <BarsIcon /> },
  ]

  return (
    <aside className="dashboard-sidebar">
      <a className="sidebar-brand" href="/" aria-label="Asahi home">
        <span className="sidebar-brand-mark" role="img" aria-hidden="true" />
        <span className="sidebar-brand-name">ASAHI</span>
      </a>

      <nav className="sidebar-nav" aria-label="Dashboard navigation">
        {navItems.map((item) => (
          <button
            key={item.id}
            type="button"
            className={`sidebar-link${view === item.id ? " active" : ""}`}
            aria-current={view === item.id ? "page" : undefined}
            onClick={() => onViewChange(item.id)}
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-profile">
        <div className="profile-avatar" aria-hidden="true">
          {userName.charAt(0).toUpperCase()}
        </div>

        <div className="profile-details">
          <strong>{userName}</strong>
          <span>{userEmail}</span>
        </div>

        <button
          className="sidebar-logout"
          type="button"
          onClick={onLogout}
          aria-label="Log out"
          title="Log out"
        >
          <LogoutIcon size={18} />
        </button>
      </div>
    </aside>
  )
}
