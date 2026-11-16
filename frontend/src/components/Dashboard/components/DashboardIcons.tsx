import type { ReactNode } from "react"

type IconProps = {
  size?: number
}

type SvgProps = IconProps & {
  children: ReactNode
}

const Svg = ({ size = 20, children }: SvgProps) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.7"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    {children}
  </svg>
)

export const HomeIcon = (props: IconProps) => (
  <Svg {...props}>
    <path d="M4 11l8-7 8 7" />
    <path d="M6 10v9h12v-9" />
    <path d="M10 19v-5h4v5" />
  </Svg>
)

export const ClockIcon = (props: IconProps) => (
  <Svg {...props}>
    <circle cx="12" cy="12" r="8.5" />
    <path d="M12 7.5V12l3 2" />
  </Svg>
)

export const BarsIcon = (props: IconProps) => (
  <Svg {...props}>
    <path d="M5 20V12M12 20V5M19 20v-6" />
  </Svg>
)

export const BellIcon = (props: IconProps) => (
  <Svg {...props}>
    <path d="M6 16V11a6 6 0 0112 0v5l1.5 2h-15L6 16Z" />
    <path d="M10 20a2 2 0 004 0" />
  </Svg>
)

export const LogoutIcon = (props: IconProps) => (
  <Svg {...props}>
    <path d="M14 5h4a1 1 0 011 1v12a1 1 0 01-1 1h-4" />
    <path d="M10 8l-4 4 4 4M6 12h9" />
  </Svg>
)

export const SunIcon = (props: IconProps) => (
  <Svg {...props}>
    <circle cx="12" cy="12" r="4" />
    <path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6L7 7M17 17l1.4 1.4M18.4 5.6L17 7M7 17l-1.4 1.4" />
  </Svg>
)

export const LeafIcon = (props: IconProps) => (
  <Svg {...props}>
    <path d="M5 19c0-8 5-13 14-14 0 9-5 14-14 14Z" />
    <path d="M5 19c2-4 5-7 9-9" />
  </Svg>
)

export const SettingsIcon = (props: IconProps) => (
  <Svg {...props}>
    <path d="M17.6 15c-.5-.6-1.2-.6-1.7 0L8.4 9.1a.7.7 0 00-.3.9l1.6 3.2a.7.7 0 00.7.7h5.1a.7.7 0 00.6-.9l-1.6-3.1Z" />
    <path d="M1 3a2 2 0 012-2h12a2 2 0 012 2v12a2 2 0 01-2 2H5a2 2 0 01-2-2V3Zm2 4h2v14H3V7Z" />
  </Svg>
)

export const SproutIcon = (props: IconProps) => (
  <Svg {...props}>
    <path d="M12 20v-8" />
    <path d="M12 12c0-3.5-2.5-5.5-6-5.5 0 3.5 2.5 5.5 6 5.5Z" />
    <path d="M12 14c0-3 2.2-5 6-5 0 3.2-2.2 5-6 5Z" />
  </Svg>
)
