import { useState, useMemo } from "react"
import type { CheckIn as CheckInData } from "../../types/checkIn"
import "./History.css"

interface HistoryProps {
  checkIns: CheckInData[]
}

const moods = [
  { id: "great", label: "Great", bg: "#f9e3b9", feeling: "Great" },
  { id: "okay", label: "Okay", bg: "#eee8d8", feeling: "Okay" },
  { id: "low", label: "A little low", bg: "#f2d9d1", feeling: "A little low" },
  { id: "stressed", label: "Stressed", bg: "#efcbc3", feeling: "Stressed" },
  { id: "lonely", label: "Lonely", bg: "#e8e3d9", feeling: "Lonely" },
  { id: "unsure", label: "Not sure", bg: "#e9eadc", feeling: "Not sure" },
] as const

type MoodId = (typeof moods)[number]["id"]

const mouths: Record<MoodId, string> = {
  great: "M11 22 Q18 29 25 22",
  okay: "M12 23.5 Q18 26 24 23.5",
  low: "M12 25.5 Q18 21.5 24 25.5",
  stressed: "M12 26 Q18 20.5 24 26",
  lonely: "M13 25 Q18 22.5 23 25",
  unsure: "M12 24 Q15 22 18 24 T24 24",
}

const moodIdMap: Record<string, string> = {
  "Great": "great",
  "Okay": "okay",
  "A little low": "low",
  "Stressed": "stressed",
  "Lonely": "lonely",
  "Not sure": "unsure",
}

const moodColors: Record<string, { bg: string; border: string; text: string }> = {
  "Great": { bg: "#fff8eb", border: "#f9e3b9", text: "#8a5d00" },
  "Okay": { bg: "#f3f6f3", border: "#c8d6c8", text: "#3d523d" },
  "A little low": { bg: "#fdf2ee", border: "#f2d9d1", text: "#9e482b" },
  "Stressed": { bg: "#fcf0ed", border: "#efcbc3", text: "#9a3b26" },
  "Lonely": { bg: "#f5f3f0", border: "#e8e3d9", text: "#5c5243" },
  "Not sure": { bg: "#f4f6f2", border: "#e9eadc", text: "#4a5448" },
}

function MoodFace({ id }: { id: MoodId }) {
  return (
    <svg width="24" height="24" viewBox="0 0 36 36" aria-hidden="true">
      <g stroke="#5b4a3f" strokeWidth="1.6" strokeLinecap="round" fill="none">
        {id === "stressed" && (
          <path d="M9 10.5L15 12.5M27 10.5L21 12.5" />
        )}
        {id === "low" && (
          <path d="M9.5 12L14.5 11M26.5 12L21.5 11" />
        )}
        <path d={mouths[id]} />
      </g>
      <circle cx="12.5" cy={id === "lonely" ? 15.5 : 14.5} r="1.5" fill="#5b4a3f" />
      <circle cx="23.5" cy={id === "lonely" ? 15.5 : 14.5} r="1.5" fill="#5b4a3f" />
    </svg>
  )
}

const defaultMoodStyle = { bg: "#f7f7f7", border: "#e0e0e0", text: "#333333" }

export default function History({ checkIns }: HistoryProps) {
  const [viewMode, setViewMode] = useState<"timeline" | "calendar">("timeline")
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedFeeling, setSelectedFeeling] = useState<string>("all")
  const [expandedNotes, setExpandedNotes] = useState<Record<number, boolean>>({})

  // Calendar State
  const [currentMonth, setCurrentMonth] = useState(() => new Date())
  const [selectedCalendarDate, setSelectedCalendarDate] = useState<string | null>(null)

  // Extract unique feelings present in dataset
  const availableFeelings = useMemo(() => {
    return Array.from(new Set(checkIns.map((c) => c.feeling)))
  }, [checkIns])

  // Filtered check-ins
  const filteredCheckIns = useMemo(() => {
    return checkIns.filter((item) => {
      // Search filter
      const matchesSearch =
        !searchQuery.trim() ||
        item.feeling.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (item.note && item.note.toLowerCase().includes(searchQuery.toLowerCase()))

      // Feeling filter
      const matchesFeeling =
        selectedFeeling === "all" || item.feeling === selectedFeeling

      // Calendar date filter
      let matchesCalendarDate = true
      if (viewMode === "calendar" && selectedCalendarDate) {
        const itemDateStr = new Date(item.created_at).toISOString().split("T")[0]
        matchesCalendarDate = itemDateStr === selectedCalendarDate
      }

      return matchesSearch && matchesFeeling && matchesCalendarDate
    })
  }, [checkIns, searchQuery, selectedFeeling, viewMode, selectedCalendarDate])

  const hasActiveFilters = searchQuery.trim() !== "" || selectedFeeling !== "all" || selectedCalendarDate !== null

  const clearFilters = () => {
    setSearchQuery("")
    setSelectedFeeling("all")
    setSelectedCalendarDate(null)
  }

  const toggleNoteExpanded = (id: number) => {
    setExpandedNotes((prev) => ({ ...prev, [id]: !prev[id] }))
  }

  // Grouping check-ins by bucket for Timeline
  const groupedTimeline = useMemo(() => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    const startOfWeek = new Date(today)
    startOfWeek.setDate(today.getDate() - today.getDay())

    const groups: {
      today: CheckInData[]
      yesterday: CheckInData[]
      thisWeek: CheckInData[]
      older: CheckInData[]
    } = {
      today: [],
      yesterday: [],
      thisWeek: [],
      older: [],
    }

    // Sort reverse chronological
    const sorted = [...filteredCheckIns].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )

    sorted.forEach((item) => {
      const itemDate = new Date(item.created_at)
      const itemDateOnly = new Date(itemDate)
      itemDateOnly.setHours(0, 0, 0, 0)

      if (itemDateOnly.getTime() === today.getTime()) {
        groups.today.push(item)
      } else if (itemDateOnly.getTime() === yesterday.getTime()) {
        groups.yesterday.push(item)
      } else if (itemDateOnly >= startOfWeek) {
        groups.thisWeek.push(item)
      } else {
        groups.older.push(item)
      }
    })

    return groups
  }, [filteredCheckIns])

  // Calendar Days Calculation
  const calendarDays = useMemo(() => {
    const year = currentMonth.getFullYear()
    const month = currentMonth.getMonth()

    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)

    const daysInMonth = lastDay.getDate()
    const startingDayOfWeek = firstDay.getDay()

    // Map of date string YYYY-MM-DD -> array of check-ins
    const checkInsByDateStr: Record<string, CheckInData[]> = {}
    checkIns.forEach((ci) => {
      const dStr = new Date(ci.created_at).toISOString().split("T")[0]
      if (!checkInsByDateStr[dStr]) {
        checkInsByDateStr[dStr] = []
      }
      checkInsByDateStr[dStr].push(ci)
    })

    const days: Array<{
      dateStr: string
      dayNumber: number
      isCurrentMonth: boolean
      hasCheckIn: boolean
      checkInsList: CheckInData[]
    }> = []

    // Previous month padding days
    const prevMonthLastDay = new Date(year, month, 0).getDate()
    for (let i = startingDayOfWeek - 1; i >= 0; i--) {
      const d = new Date(year, month - 1, prevMonthLastDay - i)
      const dStr = d.toISOString().split("T")[0]
      days.push({
        dateStr: dStr,
        dayNumber: prevMonthLastDay - i,
        isCurrentMonth: false,
        hasCheckIn: Boolean(checkInsByDateStr[dStr]),
        checkInsList: checkInsByDateStr[dStr] || [],
      })
    }

    // Current month days
    for (let day = 1; day <= daysInMonth; day++) {
      const monthStr = String(month + 1).padStart(2, "0")
      const dayStr = String(day).padStart(2, "0")
      const dStr = `${year}-${monthStr}-${dayStr}`

      days.push({
        dateStr: dStr,
        dayNumber: day,
        isCurrentMonth: true,
        hasCheckIn: Boolean(checkInsByDateStr[dStr]),
        checkInsList: checkInsByDateStr[dStr] || [],
      })
    }

    // Next month padding to fill out 42 grid slots (6 rows)
    const remainingSlots = 42 - days.length
    for (let day = 1; day <= remainingSlots; day++) {
      const d = new Date(year, month + 1, day)
      const dStr = d.toISOString().split("T")[0]
      days.push({
        dateStr: dStr,
        dayNumber: day,
        isCurrentMonth: false,
        hasCheckIn: Boolean(checkInsByDateStr[dStr]),
        checkInsList: checkInsByDateStr[dStr] || [],
      })
    }

    return days
  }, [currentMonth, checkIns])

  const changeMonth = (offset: number) => {
    setCurrentMonth((prev) => new Date(prev.getFullYear(), prev.getMonth() + offset, 1))
  }

  if (checkIns.length === 0) {
    return (
      <div className="history-page">
        <header className="history-header">
          <div>
            <h1 className="history-title">Your moments, over time.</h1>
            <p className="history-subtitle">A safe space to revisit your thoughts and check-ins.</p>
          </div>
        </header>

        <div className="history-empty-container">
          <div className="history-empty-icon" aria-hidden="true">
            📖
          </div>
          <h3>Your Journal is Ready</h3>
          <p>
            You haven't logged any moments yet. Complete your first daily check-in from your dashboard to start building your personal wellness timeline!
          </p>
        </div>
      </div>
    )
  }

  const renderCheckInCard = (item: CheckInData) => {
    const style = moodColors[item.feeling] || defaultMoodStyle
    const moodId = moodIdMap[item.feeling] as MoodId | undefined
    const isExpanded = Boolean(expandedNotes[item.id])
    const hasLongNote = item.note && item.note.length > 140

    const formattedTime = new Date(item.created_at).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    })

    const formattedDate = new Date(item.created_at).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    })

    return (
      <article className="moment-card" key={item.id}>
        <div className="moment-card-header">
          <span
            className="moment-badge"
            style={{
              backgroundColor: style.bg,
              borderColor: style.border,
              color: style.text,
            }}
          >
            {moodId ? <MoodFace id={moodId} /> : null}
            <span className="moment-feeling-text">{item.feeling}</span>
          </span>
          <span className="moment-timestamp">
            {formattedDate} • {formattedTime}
          </span>
        </div>

        {item.note && (
          <div className="moment-note-body">
            <p className="moment-note-text">
              {hasLongNote && !isExpanded ? `${item.note.slice(0, 140)}...` : item.note}
            </p>
            {hasLongNote && (
              <button
                type="button"
                className="moment-expand-btn"
                onClick={() => toggleNoteExpanded(item.id)}
                aria-expanded={isExpanded}
              >
                {isExpanded ? "Show less" : "Read full note"}
              </button>
            )}
          </div>
        )}
      </article>
    )
  }

  return (
    <div className="history-page">
      {/* Header */}
      <header className="history-header">
        <div>
          <h1 className="history-title">Your moments, over time.</h1>
          <p className="history-subtitle">A safe space to revisit your thoughts and check-ins.</p>
        </div>
        <div className="history-header-actions">
          <span className="history-count-badge">
            {checkIns.length} {checkIns.length === 1 ? "moment" : "moments"}
          </span>

          {/* View Switcher */}
          <div className="view-toggle-group" role="group" aria-label="View Mode">
            <button
              type="button"
              className={`toggle-btn ${viewMode === "timeline" ? "active" : ""}`}
              onClick={() => {
                setViewMode("timeline")
                setSelectedCalendarDate(null)
              }}
            >
              Timeline
            </button>
            <button
              type="button"
              className={`toggle-btn ${viewMode === "calendar" ? "active" : ""}`}
              onClick={() => setViewMode("calendar")}
            >
              Calendar
            </button>
          </div>
        </div>
      </header>

      {/* Filter and Search Bar */}
      <div className="history-controls-card">
        <div className="search-box">
          <svg
            className="search-icon"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            aria-hidden="true"
          >
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
          <input
            type="text"
            className="search-input"
            placeholder="Search notes or feelings..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            aria-label="Search check-ins"
          />
          {searchQuery && (
            <button
              type="button"
              className="clear-search-btn"
              onClick={() => setSearchQuery("")}
              aria-label="Clear search"
            >
              ×
            </button>
          )}
        </div>

        <div className="filter-group">
          <label htmlFor="feeling-filter" className="filter-label">
            Feeling:
          </label>
          <select
            id="feeling-filter"
            className="feeling-select"
            value={selectedFeeling}
            onChange={(e) => setSelectedFeeling(e.target.value)}
          >
            <option value="all">All Feelings</option>
            {availableFeelings.map((f) => (
              <option key={f} value={f}>
                {f}
              </option>
            ))}
          </select>
        </div>

        {hasActiveFilters && (
          <button type="button" className="clear-all-filters-btn" onClick={clearFilters}>
            Clear Filters
          </button>
        )}
      </div>

      {/* Main Content Area */}
      {viewMode === "timeline" ? (
        <div className="timeline-container">
          {filteredCheckIns.length === 0 ? (
            <div className="no-results-card">
              <p>No moments match your current search or filters.</p>
              <button type="button" className="button-secondary" onClick={clearFilters}>
                Clear filters
              </button>
            </div>
          ) : (
            <>
              {groupedTimeline.today.length > 0 && (
                <section className="timeline-group">
                  <h2 className="timeline-group-title">Today</h2>
                  <div className="moments-grid">{groupedTimeline.today.map(renderCheckInCard)}</div>
                </section>
              )}

              {groupedTimeline.yesterday.length > 0 && (
                <section className="timeline-group">
                  <h2 className="timeline-group-title">Yesterday</h2>
                  <div className="moments-grid">{groupedTimeline.yesterday.map(renderCheckInCard)}</div>
                </section>
              )}

              {groupedTimeline.thisWeek.length > 0 && (
                <section className="timeline-group">
                  <h2 className="timeline-group-title">This Week</h2>
                  <div className="moments-grid">{groupedTimeline.thisWeek.map(renderCheckInCard)}</div>
                </section>
              )}

              {groupedTimeline.older.length > 0 && (
                <section className="timeline-group">
                  <h2 className="timeline-group-title">Earlier</h2>
                  <div className="moments-grid">{groupedTimeline.older.map(renderCheckInCard)}</div>
                </section>
              )}
            </>
          )}
        </div>
      ) : (
        <div className="calendar-view-container">
          {/* Calendar Header Navigation */}
          <div className="calendar-card">
            <div className="calendar-nav">
              <button
                type="button"
                className="calendar-nav-btn"
                onClick={() => changeMonth(-1)}
                aria-label="Previous month"
              >
                ‹
              </button>
              <h2 className="calendar-month-title">
                {currentMonth.toLocaleDateString("en-US", { month: "long", year: "numeric" })}
              </h2>
              <button
                type="button"
                className="calendar-nav-btn"
                onClick={() => changeMonth(1)}
                aria-label="Next month"
              >
                ›
              </button>
            </div>

            {/* Calendar Grid */}
            <div className="calendar-grid">
              {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
                <div key={day} className="calendar-day-header">
                  {day}
                </div>
              ))}

              {calendarDays.map((d, index) => {
                const isSelected = selectedCalendarDate === d.dateStr
                return (
                  <button
                    key={`${d.dateStr}-${index}`}
                    type="button"
                    className={`calendar-day-cell ${
                      !d.isCurrentMonth ? "disabled" : ""
                    } ${d.hasCheckIn ? "has-data" : ""} ${isSelected ? "selected" : ""}`}
                    onClick={() => {
                      if (d.hasCheckIn) {
                        setSelectedCalendarDate(isSelected ? null : d.dateStr)
                      }
                    }}
                    disabled={!d.isCurrentMonth}
                    aria-label={`${d.dateStr}${d.hasCheckIn ? ", has check-in" : ""}`}
                  >
                    <span className="calendar-day-num">{d.dayNumber}</span>
                    {d.hasCheckIn && <span className="calendar-dot" />}
                  </button>
                )
              })}
            </div>
          </div>

          {/* Selected Calendar Day Moments */}
          <div className="calendar-selected-moments">
            <div className="selected-day-header">
              <h3>
                {selectedCalendarDate
                  ? `Moments on ${new Date(selectedCalendarDate + "T00:00:00").toLocaleDateString("en-US", {
                      weekday: "long",
                      month: "short",
                      day: "numeric",
                    })}`
                  : "Select a highlighted date to view entries"}
              </h3>
              {selectedCalendarDate && (
                <button
                  type="button"
                  className="clear-selected-date-btn"
                  onClick={() => setSelectedCalendarDate(null)}
                >
                  Show all entries
                </button>
              )}
            </div>

            <div className="moments-grid">
              {filteredCheckIns.length === 0 ? (
                <p className="no-calendar-entries-text">No moments found for this selection.</p>
              ) : (
                filteredCheckIns.map(renderCheckInCard)
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
