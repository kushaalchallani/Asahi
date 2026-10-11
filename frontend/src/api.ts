import type { CheckIn } from "./types/checkIn"

const API_URL = "http://localhost:8000"

export async function createCheckIn(feeling: string, note?: string): Promise<CheckIn> {

    const response = await fetch(`${API_URL}/check-ins`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            feeling,
            note: note || null
        })
    });

    if (!response.ok) {
        throw new Error("Failed to create check-in");
    } 

    return response.json();
}

export async function getCheckIn(): Promise<CheckIn[]> {
    const response = await fetch(`${API_URL}/check-ins`);

    if (!response.ok){
        throw new Error("Failed to fetch check-ins");
    }

    return response.json();
}

export async function getCheckInInsights() {
    const response = await fetch(`${API_URL}/check-ins/insights`);

    if (!response.ok){
        throw new Error("Failed to fetch check-ins");
    }

    return response.json();
}

export async function getTodayMission() {
    const reponse = await fetch(`${API_URL}/missions/today`);
    
    if (!reponse.ok) {
        throw new Error("Failed to get today's mission");
    }

    return reponse.json();
}

export async function startMission(missionId:Number) {
    const response = await fetch(`${API_URL}/missions/${missionId}/start`, {
        method: "POST",
    });

    if (!response.ok)  {
        throw new Error("Failed to start mission");
    }

    return response.json();
}

export async function completeMission(missionId:Number) {
    const response = await fetch(`${API_URL}/missions/${missionId}/complete`, {
        method: "POST",
    });

    if (!response.ok)  {
        throw new Error("Failed to complete mission");
    }

    return response.json();
}

export async function skipMission(missionId:Number) {
    const response = await fetch(`${API_URL}/missions/${missionId}/skip`, {
        method: "POST",
    });

    if (!response.ok)  {
        throw new Error("Failed to skip mission");
    }

    return response.json();
}