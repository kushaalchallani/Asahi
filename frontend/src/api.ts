const API_URL = "http://localhost:8000"

export async function createCheckIn(feeling: string) {
    const response = await fetch(`${API_URL}/check-ins?feeling=${encodeURIComponent(feeling)}`, {
        method: "POST"
    })

    if (!response.ok) {
        throw new Error("Failed to create check-in")
    } 

    return response.json()
}