import { useState } from "react"
import { createCheckIn } from "../../services/api"
import type { CheckIn as CheckInData } from "../../types/checkIn"

interface CheckInProps {
    onCheckInCreated: (checkIn: CheckInData) => void
}

const feelings = [
  "I'm doing okay",
  "A little low",
  "Stressed",
  "Lonely",
  "Not sure",
]

function CheckIn({ onCheckInCreated }: CheckInProps) {
      
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
        const newCheckIn = await createCheckIn(selectedFeeling, note)   
        onCheckInCreated(newCheckIn)
        setSelectedFeeling(null)
        setNote("")
    } catch (error) {
        console.log(error)
    } finally {
        setSaving(false)
    }   
}

    return (
      <>
        <div className="feelings">
            {feelings.map((feeling) => (
                <button
                    key={feeling}
                    className={
                        selectedFeeling === feeling
                            ? "feeling selected"
                            : "feeling"
                    }
                    onClick={() => handleFeelingSelect(feeling)}
                    disabled={saving}
                >
                    {feeling}
                </button>
            ))}
        </div>

        {selectedFeeling && (
            <div className="note-section">
                <textarea
                    value={note}
                    onChange={(event) => setNote(event.target.value)}
                    placeholder="Want to say a little more? (optional)"
                    rows={4}
                    disabled={saving}
                />

                <button
                    className="save-button"
                    onClick={handleSaveCheckIn}
                    disabled={saving}
                >
                    {saving ? "Saving..." : "Save check-in"}
                </button>
            </div>
        )}
    </>
  )
}

export default CheckIn