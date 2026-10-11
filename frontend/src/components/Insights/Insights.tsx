import type { CheckInInsights } from "../../services/api"

interface InsightsProps {
    insights: CheckInInsights | null
}

function Insights ({ insights }: InsightsProps){

    if (!insights || insights.check_in_count === 0) {
        return null
    }

    return (
        <div className="insights">
            <h2>Your recent check-ins</h2>

            <p>You've checked in {insights.check_in_count}{" "}{insights.check_in_count === 1 ? "time" : "times"}</p>

            {insights.most_common_feeling && (
              <p>You've mostly been feeling{""} <strong>{insights.most_common_feeling.toLowerCase()}</strong></p>
            )}
          </div>
    )
}

export default Insights