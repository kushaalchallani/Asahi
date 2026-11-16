import { useEffect, useRef } from "react"

interface SettingsModalProps {
  open: boolean
  title: string
  children: React.ReactNode
}

export default function SettingsModal({ open, title, children }: SettingsModalProps) {
  const modalRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        // close handler needed here
      }
    }

    if (open) {
      document.addEventListener("keydown", handleEscape)
    }

    return () => {
      document.removeEventListener("keydown", handleEscape)
    }
  }, [open])

  if (!open) return null

  return (
    <div className="settings-modal-overlay">
      <div className="settings-modal" ref={modalRef}>
        <div className="settings-modal-header">
          <h2 className="settings-modal-title">{title}</h2>
        </div>
        <div className="settings-modal-content">
          {children}
        </div>
      </div>
    </div>
  )
}