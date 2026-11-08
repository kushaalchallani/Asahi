import { useEffect, useState, useMemo } from "react"
import { getCheckIn } from "../../services/api"
import type { CheckIn } from "../../types/checkIn"
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts"
import "./Insights.css"

const moodColors: Record<string, string> = {
  "Great": "#f9e3b9",
  "Okay": "#8a9a8a",
  "A little low": "#ee8a4f",
  "Stressed": "#e07a3e",
  "Lonely": "#7a817a",
  "Not sure": "#b4c4aa",
}

const defaultColor = "#ee8a4f"

const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

export default function Insights() {
  const [checkIns, setCheckIns] = useState<CheckIn[]>([])
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState<"7d" | "30d" | "all">("all")
  const [reflectionText, setReflectionText] = useState("")
  const [reflectionSaved, setReflectionSaved] = useState(false)

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getCheckIn()
        setCheckIns(data)
      } catch (error) {
        console.error("Failed to load check-ins for insights", error)
      } finally {
        setLoading(false)
      }
    }
    void loadData()
  }, [])

  // Filter check-ins based on selected time range
  const filteredCheckIns = useMemo(() => {
    if (timeRange === "all") return checkIns
    const now = new Date()
    const days = timeRange === "7d" ? 7 : 30
    const cutoff = new Date(now.setDate(now.getDate() - days))
    return checkIns.filter((ci) => new Date(ci.created_at) >= cutoff)
  }, [checkIns, timeRange])

  // Calculated Metrics
  const metrics = useMemo(() => {
    if (filteredCheckIns.length === 0) return null

    // Total check-ins
    const total = filteredCheckIns.length

    // Mood counts & percentages
    const moodCounts: Record<string, number> = {}
    filteredCheckIns.forEach((ci) => {
      moodCounts[ci.feeling] = (moodCounts[ci.feeling] || 0) + 1
    })

    const mostFrequent = Object.entries(moodCounts).sort((a, b) => b[1] - a[1])[0]

    // Streak calculation (consecutive days ending today or yesterday)
    let currentStreak = 0
    if (checkIns.length > 0) {
      const dates = Array.from(
        new Set(
          checkIns.map((ci) => new Date(ci.created_at).toISOString().split("T")[0])
        )
      ).sort((a, b) => new Date(b).getTime() - new Date(a).getTime())

      const today = new Date().toISOString().split("T")[0]
      const yesterday = new Date(Date.now() - 86400000).toISOString().split("T")[0]

      if (dates.includes(today) || dates.includes(yesterday)) {
        let checkDate = dates.includes(today) ? new Date() : new Date(Date.now() - 86400000)
        while (true) {
          const dateStr = checkDate.toISOString().split("T")[0]
          if (dates.includes(dateStr)) {
            currentStreak++
            checkDate.setDate(checkDate.getDate() - 1)
          } else {
            break
          }
        }
      }
    }

    // Days of week distribution
    const dayCounts = [0, 0, 0, 0, 0, 0, 0]
    filteredCheckIns.forEach((ci) => {
      const day = new Date(ci.created_at).getDay()
      dayCounts[day]++
    })
    const busiestDayIndex = dayCounts.indexOf(Math.max(...dayCounts))

    return {
      total,
      mostFrequentFeeling: mostFrequent ? mostFrequent[0] : "N/A",
      mostFrequentCount: mostFrequent ? mostFrequent[1] : 0,
      mostFrequentPct: mostFrequent ? Math.round((mostFrequent[1] / total) * 100) : 0,
      streak: currentStreak,
      busiestDay: daysOfWeek[busiestDayIndex],
      notesCount: filteredCheckIns.filter((ci) => ci.note && ci.note.trim().length > 0).length,
    }
  }, [filteredCheckIns, checkIns])

  // Data Prepping for Charts
  // 1. Activity over time (Grouped by date)
  const activityData = useMemo(() => {
    const grouped: Record<string, number> = {}
    // Sort chronologically
    const sorted = [...filteredCheckIns].sort(
      (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
    )

    sorted.forEach((ci) => {
      const dateLabel = new Date(ci.created_at).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      })
      grouped[dateLabel] = (grouped[dateLabel] || 0) + 1
    })

    return Object.entries(grouped).map(([date, count]) => ({ date, count }))
  }, [filteredCheckIns])

  // 2. Feeling Distribution (Pie / Donut)
  const distributionData = useMemo(() => {
    const grouped: Record<string, number> = {}
    filteredCheckIns.forEach((ci) => {
      grouped[ci.feeling] = (grouped[ci.feeling] || 0) + 1
    })

    return Object.entries(grouped).map(([feeling, value]) => ({
      name: feeling,
      value,
      color: moodColors[feeling] || defaultColor,
    }))
  }, [filteredCheckIns])

  // 3. Mood Trends over time (Multi-line)
  const moodTrendsData = useMemo(() => {
    const grouped: Record<string, Record<string, number>> = {}
    const sorted = [...filteredCheckIns].sort(
      (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
    )

    sorted.forEach((ci) => {
      const dateLabel = new Date(ci.created_at).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      })
      if (!grouped[dateLabel]) {
        grouped[dateLabel] = {}
      }
      grouped[dateLabel][ci.feeling] = (grouped[dateLabel][ci.feeling] || 0) + 1
    })

    const allFeelings = Array.from(new Set(filteredCheckIns.map((ci) => ci.feeling)))

    return Object.entries(grouped).map(([date, feelingsObj]) => {
      const row: Record<string, string | number> = { date }
      allFeelings.forEach((f) => {
        row[f] = feelingsObj[f] || 0
      })
      return row
    })
  }, [filteredCheckIns])

  // 4. Weekly Activity (Bar)
  const weeklyData = useMemo(() => {
    const counts = [0, 0, 0, 0, 0, 0, 0]
    filteredCheckIns.forEach((ci) => {
      const day = new Date(ci.created_at).getDay()
      counts[day]++
    })

    return daysOfWeek.map((day, idx) => ({
      day,
      checkIns: counts[idx],
    }))
  }, [filteredCheckIns])

  // 5. Feeling Frequency (Horizontal Bar)
  const frequencyData = useMemo(() => {
    const grouped: Record<string, number> = {}
    filteredCheckIns.forEach((ci) => {
      grouped[ci.feeling] = (grouped[ci.feeling] || 0) + 1
    })

    return Object.entries(grouped)
      .map(([feeling, count]) => ({
        feeling,
        count,
        color: moodColors[feeling] || defaultColor,
      }))
      .sort((a, b) => b.count - a.count)
  }, [filteredCheckIns])

  const handleSaveReflection = (e: React.FormEvent) => {
    e.preventDefault()
    if (!reflectionText.trim()) return
    setReflectionSaved(true)
    setTimeout(() => setReflectionSaved(false), 3000)
  }

  if (loading) {
    return (
      <section className="insights-container insights-loading">
        <div className="insights-spinner" />
        <p>Gathering your reflection patterns...</p>
      </section>
    )
  }

  if (checkIns.length === 0) {
    return (
      <section className="insights-container insights-empty">
        <div className="insights-empty-card">
          <h2>Your journey, in perspective.</h2>
          <p>
            Insights will naturally appear here once you complete a few daily check-ins.
            Start by recording how you feel on your dashboard!
          </p>
        </div>
      </section>
    )
  }

  return (
    <div className="insights-container">
      {/* Welcome Header */}
      <header className="insights-header">
        <div>
          <h1 className="insights-title">Your journey, in perspective.</h1>
          <p className="insights-subtitle">
            Notice patterns, honor your process, and see your emotional rhythm evolve over time.
          </p>
        </div>
        <div className="insights-filter-group" role="group" aria-label="Time range selector">
          <button
            type="button"
            className={`filter-btn ${timeRange === "7d" ? "active" : ""}`}
            onClick={() => setTimeRange("7d")}
          >
            Last 7 days
          </button>
          <button
            type="button"
            className={`filter-btn ${timeRange === "30d" ? "active" : ""}`}
            onClick={() => setTimeRange("30d")}
          >
            Last 30 days
          </button>
          <button
            type="button"
            className={`filter-btn ${timeRange === "all" ? "active" : ""}`}
            onClick={() => setTimeRange("all")}
          >
            All time
          </button>
        </div>
      </header>

      {/* Overview Cards */}
      {metrics && (
        <div className="insights-overview-grid">
          <div className="overview-card">
            <span className="overview-label">Total Check-Ins</span>
            <span className="overview-value">{metrics.total}</span>
            <span className="overview-hint">Recorded entries</span>
          </div>

          <div className="overview-card">
            <span className="overview-label">Dominant Feeling</span>
            <span className="overview-value">{metrics.mostFrequentFeeling}</span>
            <span className="overview-hint">
              {metrics.mostFrequentPct}% of total check-ins
            </span>
          </div>

          <div className="overview-card">
            <span className="overview-label">Current Streak</span>
            <span className="overview-value">
              {metrics.streak} {metrics.streak === 1 ? "Day" : "Days"}
            </span>
            <span className="overview-hint">Consecutive check-ins</span>
          </div>

          <div className="overview-card">
            <span className="overview-label">Reflective Notes</span>
            <span className="overview-value">{metrics.notesCount}</span>
            <span className="overview-hint">Entries with notes</span>
          </div>
        </div>
      )}

      {/* Charts Grid */}
      <div className="insights-charts-grid">
        {/* 1. Check-in Activity Chart */}
        <section className="chart-card">
          <div className="chart-card-header">
            <h3>Check-in Activity</h3>
            <p>Consistency of check-ins across dates</p>
          </div>
          <div className="chart-body">
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={activityData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <defs>
                  <linearGradient id="activityGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ee8a4f" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#ee8a4f" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" stroke="#7a817a" fontSize={11} tickLine={false} />
                <YAxis stroke="#7a817a" fontSize={11} tickLine={false} allowDecimals={false} />
                <Tooltip
                  contentStyle={{
                    background: "#fff",
                    border: "1px solid #efe5d6",
                    borderRadius: "10px",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
                  }}
                />
                <Area type="monotone" dataKey="count" stroke="#ee8a4f" strokeWidth={2} fillOpacity={1} fill="url(#activityGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* 2. Feeling Distribution (Donut Chart) */}
        <section className="chart-card">
          <div className="chart-card-header">
            <h3>Feeling Distribution</h3>
            <p>Proportion of logged emotional states</p>
          </div>
          <div className="chart-body">
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={distributionData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {distributionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    background: "#fff",
                    border: "1px solid #efe5d6",
                    borderRadius: "10px",
                  }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: "11px", paddingTop: "6px" }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* 3. Mood Trends Chart (Multi-line) */}
        <section className="chart-card chart-card-wide">
          <div className="chart-card-header">
            <h3>Mood Trends</h3>
            <p>Tracking individual feelings over time</p>
          </div>
          <div className="chart-body">
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={moodTrendsData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <XAxis dataKey="date" stroke="#7a817a" fontSize={11} tickLine={false} />
                <YAxis stroke="#7a817a" fontSize={11} tickLine={false} allowDecimals={false} />
                <Tooltip
                  contentStyle={{
                    background: "#fff",
                    border: "1px solid #efe5d6",
                    borderRadius: "10px",
                  }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: "11px" }} />
                {distributionData.map((d) => (
                  <Line
                    key={d.name}
                    type="monotone"
                    dataKey={d.name}
                    stroke={d.color}
                    strokeWidth={2}
                    dot={{ r: 3 }}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* 4. Weekly Activity Chart */}
        <section className="chart-card">
          <div className="chart-card-header">
            <h3>Weekly Rhythm</h3>
            <p>Check-in volume by day of the week</p>
          </div>
          <div className="chart-body">
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={weeklyData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <XAxis dataKey="day" stroke="#7a817a" fontSize={11} tickLine={false} />
                <YAxis stroke="#7a817a" fontSize={11} tickLine={false} allowDecimals={false} />
                <Tooltip
                  contentStyle={{
                    background: "#fff",
                    border: "1px solid #efe5d6",
                    borderRadius: "10px",
                  }}
                />
                <Bar dataKey="checkIns" fill="#8a9a8a" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* 5. Feeling Frequency Chart (Horizontal Bar) */}
        <section className="chart-card">
          <div className="chart-card-header">
            <h3>Feeling Frequency</h3>
            <p>Ranking recorded feelings</p>
          </div>
          <div className="chart-body">
            <ResponsiveContainer width="100%" height={220}>
              <BarChart
                layout="vertical"
                data={frequencyData}
                margin={{ top: 10, right: 10, left: 10, bottom: 0 }}
              >
                <XAxis type="number" stroke="#7a817a" fontSize={11} tickLine={false} allowDecimals={false} />
                <YAxis dataKey="feeling" type="category" stroke="#7a817a" fontSize={11} tickLine={false} width={80} />
                <Tooltip
                  contentStyle={{
                    background: "#fff",
                    border: "1px solid #efe5d6",
                    borderRadius: "10px",
                  }}
                />
                <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                  {frequencyData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
      </div>

      {/* Personal Observations Section */}
      {metrics && (
        <section className="insights-observations">
          <h3>Personal Observations</h3>
          <div className="observations-grid">
            <div className="observation-item">
              <div className="observation-badge">Pattern</div>
              <p>
                Your most frequently recorded feeling is <strong>{metrics.mostFrequentFeeling}</strong>,
                representing <strong>{metrics.mostFrequentPct}%</strong> of all recorded check-ins.
              </p>
            </div>

            <div className="observation-item">
              <div className="observation-badge">Rhythm</div>
              <p>
                You tend to check in most frequently on <strong>{metrics.busiestDay}s</strong>.
              </p>
            </div>

            <div className="observation-item">
              <div className="observation-badge">Reflection</div>
              <p>
                You include written notes in <strong>{Math.round((metrics.notesCount / metrics.total) * 100)}%</strong> of your check-ins, adding context to your journey.
              </p>
            </div>
          </div>
        </section>
      )}

      {/* Optional Self-Reflection Section */}
      <section className="insights-reflection">
        <div className="reflection-content">
          <h3>Gentle Self-Reflection</h3>
          <p>What is one thing you&rsquo;ve noticed about yourself recently?</p>
          <form onSubmit={handleSaveReflection} className="reflection-form">
            <textarea
              className="reflection-input"
              rows={3}
              placeholder="Write a small note to yourself (optional)..."
              value={reflectionText}
              onChange={(e) => setReflectionText(e.target.value)}
            />
            <div className="reflection-actions">
              <button type="submit" className="button-primary reflection-submit" disabled={!reflectionText.trim()}>
                Save Reflection
              </button>
              {reflectionSaved && <span className="reflection-saved-note">Saved for your personal awareness.</span>}
            </div>
          </form>
        </div>
      </section>
    </div>
  )
}
