import { useState, useEffect } from "react"
import CheckIn from "./components/CheckIn/CheckIn"
import { getCheckIn, getCheckInInsights, getTodayMission, startMission, completeMission, skipMission } from "./api"
import "./App.css"



function App() {

  const [checkIns, setCheckIns] = useState<any[]>([])
  const [insights, setInsights] = useState<{
    check_in_count: number
    most_common_feeling: string|null
  } | null>(null)
  const [mission, setMission] = useState<any>(null)
  const [missionStatus, setMissionStatus] =  useState("assigned")
  const [missionLoading, setMissionLoading] = useState(true)

  useEffect(()=> {
    async function loadCheckIns() {
      try{
        const data = await getCheckIn()
        setCheckIns(data)
      }  catch (error) {
        console.log(error)
      }
    }

    loadCheckIns()
  }, [])

  useEffect(()=> {
    async function loadInsights() {
      try{
        const data = await getCheckInInsights()
        setInsights(data)
      }  catch (error) {
        console.log(error)
      }
    }

    loadInsights()
  }, [])

  useEffect(()=> {
    async function loadMission() {
      try{
        const data = await getTodayMission()
        setMission(data.mission)

        if (data.status) {
          setMissionStatus(data.status)
        }
      }  catch (error) {
        console.log(error)
      } finally {
        setMissionLoading(false)
      }
    }

    loadMission()
  }, [])


  async function handleStartMission(){
    if (!mission) return

    try {
      await startMission(mission.id)
      setMissionStatus("started")
    } catch (error) {
      console.log(error)
    }
  }

  async function handleCompleteMission() {
    if (!mission) return

    try{
      await completeMission(mission.id)
      setMissionStatus("completed")
    } catch (error) {
      console.log(error)
    }
  }

  async function handleSkipMission() {
    if (!mission) return

    try{
      await skipMission(mission.id)
      setMission(null)
      setMissionStatus("skipped")
    } catch (error) {
      console.log(error)
    }
  }
  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">ASAHI</p>

        <h1>
          Good evening.
        </h1>

        <p className="subtitle">
          How are you feeling today?
        </p>

        <CheckIn/>

        {!missionLoading && mission && (
          <div className="mission-card">
            <p className="mission-label">Today's Mission</p>
            <h2>{mission.title}</h2>
            <p>{mission.description}</p>

            {missionStatus === 'assigned' && (
              <button onClick={handleStartMission}>Start</button>
            )}

            {missionStatus === 'started' && (
              <>
              <button onClick={handleCompleteMission}>Complete</button>
              <button onClick={handleSkipMission}>Not today</button>
              </>
            )}

            {missionStatus === 'completed' && (
              <p>Completed. Nice work!</p>
            )}

            {missionStatus === 'skipped' && (
              <p>No pressure. You can leave it for today.</p>
            )}
          </div>
        )}

        {insights && insights.check_in_count >0 && (
          <div className="insights">
            <h2>Your recent check-ins</h2>

            <p>You've checked in {insights.check_in_count}{" "}{insights.check_in_count === 1 ? "time" : "times"}</p>

            {insights.most_common_feeling && (
              <p>You've mostly been feeling{""} <strong>{insights.most_common_feeling.toLowerCase()}</strong></p>
            )}
          </div>
        )}

        {checkIns.length > 0 && (
          <div className="history">
            <h2>Recent check-ins</h2>

            {checkIns.map((checkIn) => (
              <div className="history-item" key={checkIn.id}>
                <p>{checkIn.feeling}</p>

                {checkIn.note && (
                  <p className="history-note">{checkIn.note}</p>
                )}
                <small>{new Date(checkIn.created_at).toLocaleString()}</small>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  )
}

export default App