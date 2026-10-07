const API_URL = "http://localhost:8000"

export async function createCheckIn(feeling: string, note?: string) {
    const params = new URLSearchParams({
        feeling,
    })

    if (note) {
        params.append("note", note)
    }

    const response = await fetch(`${API_URL}/check-ins?${params.toString()}`, {
        method: "POST"
    })

    if (!response.ok) {
        throw new Error("Failed to create check-in")
    } 

    return response.json()
}

export async function getCheckIn() {
    const response = await fetch(`${API_URL}/check-ins`)

    if (!response.ok){
        throw new Error("Failed to fetch check-ins")
    }

    return response.json()
}