from models import Mission

def choose_mission(current_check_in, recent_missions, missions):
    if not missions:
        return None

    feeling = current_check_in.feeling.lower()
    note = (current_check_in.note or "").lower()

    candidates = missions.copy()


    #difficult/heavily emotional check-ins
    if any(word in feeling or word in note for word in [
        "low",
        "tired",
        "broken",
        "sad",
        "overwhelmed",
        "heartbroken",
    ]):
        candidates = [
            mission
            for mission in candidates
            if mission.energy_required == 'low'
            and not mission.social_required
        ]

    # Stress-related check-ins
    elif any(word in feeling or word in note for word in [
        "stress",
        "stressed",
        "anxious",
    ]):
        candidates = [
            mission
            for mission in candidates
            if mission.category in ["regulation", "environment", "reflection"]
        ]

    # loneliness != go socialize
    elif "lonely" in feeling or "lonely" in note:
        candidates = [
            mission
            for mission in candidates
            if mission.energy_required == "low"
            or mission.category == "connection"
        ]

    #if none then all missions access
    if not candidates:
        return None

    #avoid giving same mission back to back
    recent_mission_ids= {
        mission.id
        for mission in recent_missions
    }

    fresh_candidates = [
        mission
        for mission in candidates
        if mission.id not in recent_mission_ids
    ]

    if fresh_candidates:
        candidates = fresh_candidates

    def score(mission):
        score = 0

        if mission.energy_required == 'low':
            score += 2

        if not mission.social_required:
            score += 1

        if "lonely" in feeling or "lonely" in note:
            if mission.category == "connection":
                score += 3

        if any(word in feeling or word in note for word in [
            "stress",
            "stressed",
            "anxious",
        ]):
            if mission.category == 'regulation':
                score += 1

        if any(word in feeling or word in note for word in [
            "low",
            "tired",
            "sad",
            "broken",
            "heartbroken",
        ]):
            if mission.energy_required == 'low':
                score +=3

        return score

    candidates.sort(key=score, reverse=True)
    return candidates[0]