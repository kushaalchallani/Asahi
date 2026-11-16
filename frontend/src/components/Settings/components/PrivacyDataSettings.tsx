import SettingsCard from "./SettingsCard"
import SettingsRow from "./SettingsRow"

interface PrivacyDataSettingsProps {
  onExportData: () => void
  onDeleteData: () => void
  onDeleteAccount: () => void
  saving: boolean
}

const PrivacyDataSettings: React.FC<PrivacyDataSettingsProps> = ({
  onExportData,
  onDeleteData,
  onDeleteAccount,
  saving,
}) => {
  return (
    <SettingsCard title="Privacy & Data" description="Download or manage your personal check-in history and account data.">
      <SettingsRow
        label="Download Personal Data"
        sublabel="Export your profile and check-ins in JSON format"
        action={
          <button type="button" className="button-secondary" onClick={onExportData}>
            Download JSON
          </button>
        }
      />
      <SettingsRow
        label="Delete Check-in History"
        sublabel="Permanently remove all logged moments and notes"
        className="text-danger"
        action={
          <button type="button" className="button-secondary button-danger" onClick={onDeleteData} disabled={saving}>
            Clear history
          </button>
        }
      />
      <SettingsRow
        label="Delete Account"
        sublabel="Permanently remove your account and all associated data"
        className="text-danger"
        action={
          <button type="button" className="button-secondary button-danger" onClick={onDeleteAccount} disabled={saving}>
            Delete account
          </button>
        }
      />
    </SettingsCard>
  )
}

export default PrivacyDataSettings