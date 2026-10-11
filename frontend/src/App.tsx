
import CheckIn from "./components/CheckIn/CheckIn"
import History from "./components/History/History"
import Insights from "./components/Insights/Insights"
import Missions from "./components/Missions/Missions"

import { useCheckIns } from "./hooks/useCheckIns"
import { useInsights } from "./hooks/useInsights"
import { useMission } from "./hooks/useMission"

import "./App.css"

function App() {
  const { insights, refreshInsights } = useInsights()
  const { checkIns, handleCheckInCreated } = useCheckIns(refreshInsights)
  const { mission, status, loading, start, complete, skip} = useMission()

  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">ASAHI</p>
        <h1>Good evening.</h1>
        <p className="subtitle">How are you feeling today?</p>

        <CheckIn onCheckInCreated={handleCheckInCreated} />
        <Missions
          mission={mission}
          status={status}
          loading={loading}
          onStart={start}
          onComplete={complete}
          onSkip={skip}
        />
        <Insights insights={insights} />
        <History checkIns={checkIns} />
      </section>
    </main>
  )
}

export default App