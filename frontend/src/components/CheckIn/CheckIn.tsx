import { useState } from "react"
import { createCheckIn } from "../../api"

const feelings = [
  "I'm doing okay",
  "A little low",
  "Stressed",
  "Lonely",
  "Not sure",
]

function CheckIn() {
      
    const [selectedFeeling, setSelectedFeeling ] = useState<string|null>(null)
    const [saving, setSaving] = useState(false)
    const [note, setNote] = useState("")

    function handleFeelingSelect(feeling: string){
        setSelectedFeeling(feeling)
    }

    async function handleSaveCheckIn() {
    if (!selectedFeeling) return

    setSaving(true)

    try {
        await createCheckIn(selectedFeeling, note)
        setSelectedFeeling(null)
        setNote("")
    } catch (error) {
        console.log(error)
    } finally {
        setSaving(false)
    }
    }

    return(
        <>
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
        </>
    )
}

export default CheckIn