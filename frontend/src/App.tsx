import { useState } from "react"
import { createCheckIn } from "./api"
import "./App.css"

const feelings = [
  "I'm doing okay",
  "Not really",
  "I'm not sure"
]

function App() {
  const [selectedFeeling, setSelectedFeeling ] = useState<string|null>(null)
  const [saving, setSaving] = useState(false)
  
  async function handleFeelingSelect(feeling:string) {
    setSelectedFeeling(feeling)
    setSaving(true)

    try {
      await createCheckIn(feeling)
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
      </section>
    </main>
  )
}

export default App