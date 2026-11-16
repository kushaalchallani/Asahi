import SettingsCard from "./SettingsCard"
import SettingsRow from "./SettingsRow"

interface AccountSectionProps {
  userEmail: string
  userName: string
  onEditName: () => void
  onChangeEmail: () => void
  onChangePassword: () => void
}

const AccountSection: React.FC<AccountSectionProps> = ({
  userEmail,
  userName,
  onEditName,
  onChangeEmail,
  onChangePassword,
}) => {
  return (
    <>
      {/*account Section */}
      <SettingsCard title="Account" description="Manage your account credentials.">
        <SettingsRow
          label="Display Name"
          value={userName}
          action={
            <button type="button" className="button-secondary" onClick={onEditName}>
              Edit name
            </button>
          }
        />
        <SettingsRow
          label="Email Address"
          value={userEmail}
          action={
            <button type="button" className="button-secondary" onClick={onChangeEmail}>
              Change email
            </button>
          }
        />
        <SettingsRow
          label="Password"
          value="••••••••••••"
          action={
            <button type="button" className="button-secondary" onClick={onChangePassword}>
              Change password
            </button>
          }
        />
      </SettingsCard>
    </>
  )
}

export default AccountSection