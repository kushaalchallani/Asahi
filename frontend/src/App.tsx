import { useState } from "react"
import "./App.css"

const feelings = [
  "I'm doing okay",
  "Not really",
  "I'm not sure"
]

function App() {
  const [selectedFeeling, setSelectedFeeling ] = useState<string|null>(null)
  
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
            <button key={feelings} className = {selectedFeeling === feelings ? "feeling selected" : "feeling"} onClick={() => setSelectedFeeling(feelings)}>{feelings}</button>
          ))}
        </div>

        {selectedFeeling && (
          <p className="response">
            You selected: {selectedFeeling}
          </p>
        )}
      </section>
    </main>
  )
}

export default App