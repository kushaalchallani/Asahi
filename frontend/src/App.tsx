import { useState, useEffect } from "react"
import { createCheckIn, getCheckIn } from "./api"
import "./App.css"

const feelings = [
  "I'm doing okay",
  "A little low",
  "Stressed",
  "Lonely",
  "Not sure",
]

function App() {
  const [selectedFeeling, setSelectedFeeling ] = useState<string|null>(null)
  const [saving, setSaving] = useState(false)
  const [checkIns, setCheckIns] = useState<any[]>([])
  const [note, setNote] = useState("")

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

  function handleFeelingSelect(feeling: string){
    setSelectedFeeling(feeling)
  }
  
  async function handleSaveCheckIn() {
    if (!selectedFeeling) return

    setSaving(true)

    try {
      const newCheckIn = await createCheckIn(selectedFeeling, note)
      
      setCheckIns((currentCheckIns)=> [
        newCheckIn,
        ...currentCheckIns
      ])

      setNote("")
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

        {selectedFeeling && (
          <div className="note-section">
            <textarea 
              value={note}
              onChange={(event)=> setNote(event.target.value)}
              placeholder="Want to say a little more? (optional)"
              rows={4}
              disabled={saving}
              />
            <button className="save-button" onClick={handleSaveCheckIn} disabled={saving}>{saving ? "Saving..." : "Save check-in"}</button>
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