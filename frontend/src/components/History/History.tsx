import type { CheckIn as CheckInData } from "../../types/checkIn";

interface HistoryProps {
  checkIns: CheckInData[]
}

function History({ checkIns }: HistoryProps) {
  if (checkIns.length === 0) {
    return null
  }

  return (
    <div className="history">
      <h2>Recent check-ins</h2>

      {checkIns.map((checkIn) => (
        <div className="history-item" key={checkIn.id}>
          <p>{checkIn.feeling}</p>

          {checkIn.note && (
            <p className="history-note">{checkIn.note}</p>
          )}

          <small>
            {new Date(checkIn.created_at).toLocaleString()}
          </small>
        </div>
      ))}
    </div>
  )
}

export default History