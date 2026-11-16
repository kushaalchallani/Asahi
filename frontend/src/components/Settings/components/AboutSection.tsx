import SettingsCard from "./SettingsCard"
import SettingsRow from "./SettingsRow"

const AboutSection = () => {
  return (
    <SettingsCard title="About Asahi" description="Information, support, and legal notices.">
      <SettingsRow label="Version" value="Asahi Prototype v1.0.0 (Partnership Edition)" />
      <SettingsRow
        label="Contact & Feedback"
        sublabel="Get in touch with the Asahi team"
        action={
          <a href="mailto:support@asahi.app" className="settings-link-btn">
            Email Support
          </a>
        }
      />
      <SettingsRow
        label="Privacy Policy & Terms"
        sublabel="Review our data protection commitment"
        action={
          <a
            href="#privacy"
            onClick={(e) => {
              e.preventDefault()
              alert("Asahi is committed to keeping your mental wellness data private, encrypted, and secure.")
            }}
            className="settings-link-btn"
          >
            View Notice
          </a>
        }
      />
    </SettingsCard>
  )
}

export default AboutSection