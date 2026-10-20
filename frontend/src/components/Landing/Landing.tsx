import "./Landing.css"

interface LandingProps {
  onGetStarted: () => void
  onLogin: () => void
}

const features = [
  {
    title: "Daily check-ins",
    text: "Understand how you feel and what you need.",
    icon: <path d="M5 19c0-8 5-13 14-14 0 9-5 14-14 14Zm0 0c2-4 5-7 9-9" />,
  },
  {
    title: "Personalized missions",
    text: "Small, meaningful steps for your well-being.",
    icon: (
      <>
        <circle cx="12" cy="12" r="8" />
        <circle cx="12" cy="12" r="4" />
        <circle cx="12" cy="12" r="0.8" />
      </>
    ),
  },
  {
    title: "Track your journey",
    text: "See your growth over time with gentle insights.",
    icon: <path d="M4 17l5-5 4 3 7-8M15 7h5v5" />,
  },
  {
    title: "Feel less alone",
    text: "A supportive space, whenever you need it.",
    icon: (
      <>
        <circle cx="12" cy="8" r="3.5" />
        <path d="M5 20c0-4 3-6.5 7-6.5s7 2.5 7 6.5" />
      </>
    ),
  },
]

export default function Landing({ onGetStarted, onLogin }: LandingProps) {
  return (
    <main className="landing" id="home">
      <div className="landing-art" aria-hidden="true">
        <img src="/images/asahi-landscape.png" alt="" />
      </div>

      <header className="landing-nav">
        <a className="landing-brand" href="/" aria-label="Asahi home">
          <span className="landing-brand-mark" role="img" aria-hidden="true" />
          <span className="landing-brand-name">ASAHI</span>
        </a>

        <nav className="landing-nav-links" aria-label="Main navigation">
          <a href="#home">Home</a>
          <a href="#about">About</a>
          <a href="#features">Features</a>
          <button className="button-primary" onClick={onGetStarted}>
            Get started
          </button>
        </nav>
      </header>

      <section className="landing-hero" id="about">
        <div className="landing-copy">
          <p className="landing-eyebrow">A brighter mind, one step at a time</p>

          <h1>You don&rsquo;t have to figure it all out today.</h1>

          <p className="landing-description">
            Asahi is your safe space for mental wellness. Check in with
            yourself, take small steps, and feel more connected &mdash; at your
            own pace.
          </p>

          <div className="landing-actions">
            <button className="button-primary" onClick={onGetStarted}>
              Get started
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <path d="M5 12h14M13 6l6 6-6 6" />
              </svg>
            </button>
            <button className="button-secondary" onClick={onLogin}>
              Log in
            </button>
          </div>
        </div>
      </section>

      <section className="landing-features" id="features">
        {features.map((f) => (
          <article className="feature" key={f.title}>
            <span className="feature-icon">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.7"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                {f.icon}
              </svg>
            </span>
            <h2>{f.title}</h2>
            <p>{f.text}</p>
          </article>
        ))}
      </section>
    </main>
  )
}