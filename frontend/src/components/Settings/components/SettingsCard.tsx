interface SettingsCardProps {
  title: string
  description: string
  children: React.ReactNode
}

export default function SettingsCard({ title, description, children }: SettingsCardProps) {
  return (
    <div className="settings-card">
      <div className="settings-card-header">
        <h2 className="settings-card-title">{title}</h2>
        <p className="settings-card-description">{description}</p>
      </div>
      <div className="settings-card-content">
        {children}
      </div>
    </div>
  )
}