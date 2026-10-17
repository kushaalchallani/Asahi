def choose_mission(current_check_in, recent_missions, missions, recent_feedback=None, recent_check_ins=None,):
    if not missions:
        return None

    feeling = current_check_in.feeling.lower()
    note = (current_check_in.note or "").lower()

    candidates = missions.copy()

    low_mood_words = [
        "low",
        "tired",
        "broken",
        "sad",
        "overwhelmed",
        "heartbroken",
    ]

    stress_words = ["stress", "stressed", "anxious"]

    is_low_mood = any(
        word in feeling or word in note
        for word in low_mood_words
    )

    is_stressed = any(
        word in feeling or word in note
        for word in stress_words
    )

    is_lonely = "lonely" in feeling or "lonely" in note

    # Filter missions according to the latest check-in.
    if is_low_mood:
        candidates = [
            mission
            for mission in candidates
            if mission.energy_required == "low"
            and not mission.social_required
        ]

    elif is_stressed:
        candidates = [
            mission
            for mission in candidates
            if mission.category in [
                "regulation",
                "environment",
                "reflection",
            ]
        ]

    elif is_lonely:
        candidates = [
            mission
            for mission in candidates
            if mission.energy_required == "low"
        ]

    if not candidates:
        return None

    # Avoid repeating recently assigned missions when alternatives exist.
    recent_mission_ids = {
        mission.id for mission in recent_missions
    }

    fresh_candidates = [
        mission
        for mission in candidates
        if mission.id not in recent_mission_ids
    ]

    if fresh_candidates:
        candidates = fresh_candidates

    # Detect repeated low mood using recent feelings and notes.
    recent_check_ins = recent_check_ins or []

    recent_low_mood_words = [
        "low",
        "tired",
        "sad",
        "broken",
        "overwhelmed",
        "heartbroken",
    ]

    recent_mood_signals = [
    (getattr(check_in, "feeling", None) or "").lower()
    + " "
    + (getattr(check_in, "note", None) or "").lower()
    for check_in in recent_check_ins[:3]
    ]

    repeated_low_mood = (
        len(recent_mood_signals) >= 2
        and all(
            any(
                word in signal
                for word in recent_low_mood_words
            )
            for signal in recent_mood_signals
        )
    )

    feedback_by_mission = recent_feedback or {}

    def score(mission):
        mission_score = 0

        if mission.energy_required == "low":
            mission_score += 2

        if not mission.social_required:
            mission_score += 1

        if is_lonely and mission.category == "connection":
            mission_score += 3

        if is_stressed and mission.category == "regulation":
            mission_score += 1

        if is_low_mood and mission.energy_required == "low":
            mission_score += 3

        if repeated_low_mood and mission.energy_required == "low":
            mission_score += 2

        if feedback_by_mission.get(mission.id) == "not_for_me":
            mission_score -= 3

        return mission_score

    candidates.sort(key=score, reverse=True)

    return candidates[0]