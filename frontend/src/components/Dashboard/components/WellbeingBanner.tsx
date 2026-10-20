import "./css/WellbeingBanner.css"
import { SproutIcon } from "./DashboardIcons"

export default function WellbeingBanner() {
  return (
    <section className="wellbeing-banner">
      <div className="wellbeing-symbol" aria-hidden="true">
        <SproutIcon size={26} />
      </div>

      <div className="wellbeing-text">
        <h2>Your well-being matters</h2>
        <p>
          Progress isn&rsquo;t always about being perfect, it&rsquo;s
          about showing up,
          <br />
          even in small ways.
        </p>
      </div>

      <svg
        className="banner-landscape"
        viewBox="0 0 420 112"
        preserveAspectRatio="xMaxYMax slice"
        aria-hidden="true"
      >
        <circle cx="292" cy="46" r="15" fill="#f0a468" />
        <path
          d="M120 112 C160 78 220 66 280 74 C340 82 380 70 420 56 L420 112Z"
          fill="#cdd8c3"
        />
        <path
          d="M60 112 C110 84 170 80 230 90 C290 100 330 84 420 76 L420 112Z"
          fill="#b4c4aa"
        />
        <path
          d="M180 112 C230 92 290 88 340 96 C380 102 400 96 420 90 L420 112Z"
          fill="#9db293"
        />
        <path
          d="M262 112 C310 100 360 98 420 104 L420 112Z"
          fill="#7f967a"
        />
      </svg>
    </section>
  )
}
