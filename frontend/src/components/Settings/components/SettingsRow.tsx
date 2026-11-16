interface SettingsRowProps {
  label: string
  value?: string | number
  sublabel?: string
  action?: React.ReactNode
  className?: string
}

export default function SettingsRow({ label, value, sublabel, action, className = "" }: SettingsRowProps) {
  return (
    <div className={`settings-row ${className}`}>
      <div className="settings-row-label">
        <span className="settings-row-title">{label}</span>
        {sublabel && <span className="settings-row-subtitle">{sublabel}</span>}
      </div>
      <div className="settings-row-action">
        {action || value}
      </div>
    </div>
  )
}