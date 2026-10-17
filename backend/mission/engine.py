def build_feedback_history(feedback_rows):
    feedback_by_mission = {}

    for user_mission in feedback_rows:
        if user_mission.mission_id not in feedback_by_mission:
            feedback_by_mission[user_mission.mission_id] = (
                user_mission.feedback
            )

    return feedback_by_mission

LOW_MOOD_WORDS = [
    "low",
    "tired",
    "broken",
    "sad",
    "overwhelmed",
    "heartbroken",
]

STRESS_WORDS = ["stress", "stressed", "anxious"]


def detect_mood(check_in):
    feeling = (getattr(check_in, "feeling", None) or "").lower()
    note = (getattr(check_in, "note", None) or "").lower()
    text = f"{feeling} {note}"

    return {
        "is_low_mood": any(word in text for word in LOW_MOOD_WORDS),
        "is_stressed": any(word in text for word in STRESS_WORDS),
        "is_lonely": "lonely" in text,
    }


def detect_repeated_low_mood(recent_check_ins):
    recent_check_ins = recent_check_ins or []

    recent_mood_signals = [
        (
            (getattr(check_in, "feeling", None) or "").lower()
            + " "
            + (getattr(check_in, "note", None) or "").lower()
        )
        for check_in in recent_check_ins[:3]
    ]

    return (
        len(recent_mood_signals) >= 2
        and all(
            any(word in signal for word in LOW_MOOD_WORDS)
            for signal in recent_mood_signals
        )
    )


def choose_mission(current_check_in, recent_missions, missions, recent_feedback=None, recent_check_ins=None,):
    if not missions:
        return None

    candidates = missions.copy()
    mood = detect_mood(current_check_in)

    is_low_mood = mood["is_low_mood"]
    is_stressed = mood["is_stressed"]
    is_lonely = mood["is_lonely"]

    # Keep the original mission list for fallback recommendations.
    all_candidates = candidates.copy()

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

    # Fall back to all missions if the strict filter finds no matches.
    if not candidates:
        candidates = all_candidates

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

    repeated_low_mood = detect_repeated_low_mood(recent_check_ins)

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

        feedback = feedback_by_mission.get(mission.id)

        if feedback == "not_for_me":
            mission_score -= 3
        elif feedback == "helpful":
            mission_score += 2

        return mission_score

    candidates.sort(key=score, reverse=True)

    return candidates[0]