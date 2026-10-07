import { useState, useEffect } from "react"
import { createCheckIn, getCheckIn } from "./api"
import "./App.css"

const feelings = [
  "I'm doing okay",
  "Not really",
  "I'm not sure"
]

function App() {
  const [selectedFeeling, setSelectedFeeling ] = useState<string|null>(null)
  const [saving, setSaving] = useState(false)
  const [checkIns, setCheckIns] = useState<any[]>([])

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
  
  async function handleFeelingSelect(feeling:string) {
    setSelectedFeeling(feeling)
    setSaving(true)

    try {
      const newCheckIn = await createCheckIn(feeling)
      
      setCheckIns((currentCheckIns)=> [
        newCheckIn,
        ...currentCheckIns
      ])
    } catch (error) {
      console.log(error)
    } finally {
      setSaving(false)
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

        <div className="feelings">
          {feelings.map((feelings) => (
            <button key={feelings} className = {selectedFeeling === feelings ? "feeling selected" : "feeling"} onClick={() => handleFeelingSelect(feelings)} disabled={saving}>{feelings}</button>
          ))}
        </div>

        {selectedFeeling && !saving && (
          <p className="response">
            Thanks for checking in.
          </p>
        )}

        {saving && (
          <p className="response">
            Saving...
          </p>
        )}

        {checkIns.length > 0 && (
          <div className="history">
            <h2>Recent check-ins</h2>

            {checkIns.map((checkIn) => (
              <div className="history-item" key={checkIn.id}>
                <p>{checkIn.feeling}</p>
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