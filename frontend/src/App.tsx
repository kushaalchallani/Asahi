import { useState, useEffect } from "react"
import CheckIn from "./components/CheckIn/CheckIn"
import History from "./components/History/History"
import Insights from "./components/Insights/Insights"
import Missions from "./components/Missions/Missions"
import type { CheckIn as CheckInData } from "./types/checkIn"
import type { Mission as MissionData } from "./services/api"
import { getCheckIn, getCheckInInsights, getTodayMission, startMission, completeMission, skipMission } from "./services/api"
import type { CheckInInsights } from "./services/api"

import "./App.css"

function App() {
  const [checkIns, setCheckIns] = useState<CheckInData[]>([])
  const [insights, setInsights] = useState<CheckInInsights | null>(null)
  const [mission, setMission] = useState<MissionData | null>(null)
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
        console.log(data)
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

  async function handleCheckInCreated(newCheckIn: CheckInData) {
    setCheckIns((currentCheckIns) => {
      const alreadyExists = currentCheckIns.some(
        (checkIn) => checkIn.id === newCheckIn.id
      )

      if (alreadyExists) {
        return currentCheckIns
      }

      return [newCheckIn, ...currentCheckIns].sort(
        (a, b) =>
          new Date(b.created_at).getTime() -
          new Date(a.created_at).getTime()
      )
    })

    try {
      const data = await getCheckInInsights()
      setInsights(data)
    } catch (error) {
      console.error("Failed to refresh insights:", error)
    }
  }

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
        <CheckIn onCheckInCreated={handleCheckInCreated} />
        <Missions 
          mission={mission}
          status={missionStatus}
          loading={missionLoading}
          onStart={handleStartMission}
          onComplete={handleCompleteMission}
          onSkip={handleSkipMission}
        />
        <Insights insights={insights}/>
        <History checkIns={checkIns}/>
      </section>
    </main>
  )
}

export default App