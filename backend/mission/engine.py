import pandas as pd
from pathlib import Path
from backend.ml.train import load_model

MODEL_PATH = (Path(__file__).resolve().parents[1]/ "ml"/ "artifacts"/ "mission_recommender.joblib")

def load_mission_model():
    if not MODEL_PATH.exists():
        return None

    try:
        return load_model(MODEL_PATH)
    except (OSError, ValueError, ImportError):
        return None

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

def filter_suitable_missions(missions, is_low_mood, is_stressed, is_lonely):
    if is_low_mood:
        candidates = [
            mission
            for mission in missions
            if mission.energy_required == "low"
            and not mission.social_required
        ]
    elif is_stressed:
        candidates = [
            mission
            for mission in missions
            if mission.category in [
                "regulation",
                "environment",
                "reflection"
            ]
        ]
    elif is_lonely:
        candidates = [
            mission
            for mission in missions
            if mission.energy_required == 'low'
        ]
    else: 
        candidates = missions.copy()

    return candidates or missions.copy()

def score_mission(mission, is_low_mood, is_stressed, is_lonely, repeated_low_mood, feedback_by_mission):
        score = 0

        if mission.energy_required == "low":
            score += 2

        if not mission.social_required:
            score += 1

        if is_lonely and mission.category == "connection":
            score += 3

        if is_stressed and mission.category == "regulation":
            score += 1

        if is_low_mood and mission.energy_required == "low":
            score += 3

        if repeated_low_mood and mission.energy_required == "low":
            score += 2

        feedback = feedback_by_mission.get(mission.id)

        if feedback == "not_for_me":
            score -= 3
        elif feedback == "helpful":
            score += 2

        return score

def explain_mission_score(mission, is_low_mood, is_stressed, is_lonely, repeated_low_mood, feedback_by_mission,):
    reasons = []

    if mission.energy_required == "low":
        reasons.append("low_energy")

    if not mission.social_required:
        reasons.append("non_social")

    if is_lonely and mission.category == "connection":
        reasons.append("connection_for_loneliness")

    if is_stressed and mission.category == "regulation":
        reasons.append("regulation_for_stress")

    if is_low_mood and mission.energy_required == "low":
        reasons.append("low_energy_for_low_mood")

    if repeated_low_mood and mission.energy_required == "low":
        reasons.append("low_energy_for_repeated_low_mood")

    feedback = feedback_by_mission.get(mission.id)

    if feedback == "helpful":
        reasons.append("previously_helpful")

    if feedback == "not_for_me":
        reasons.append("previously_not_for_me")

    return reasons

def build_recommendation_result(mission, is_low_mood, is_stressed, is_lonely, repeated_low_mood, feedback_by_mission,):
    reasons = explain_mission_score(
        mission,
        is_low_mood,
        is_stressed,
        is_lonely,
        repeated_low_mood,
        feedback_by_mission,
    )

    score = score_mission(
        mission,
        is_low_mood,
        is_stressed,
        is_lonely,
        repeated_low_mood,
        feedback_by_mission,
    )

    return {
        "mission": mission,
        "score": score,
        "reasons": reasons,
    }

def predict_mission_match(model, mission, energy_preference, recently_seen=False):
    features = pd.DataFrame([{
        "category": mission.category,
        "difficulty": mission.difficulty,
        "energy_required": mission.energy_required,
        "social_required": mission.social_required,
        "energy_preference": energy_preference,
        "recently_seen": recently_seen,
    }])

    return float(model.predict_proba(features)[0][1])

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

    candidates = filter_suitable_missions(
        missions,
        is_low_mood,
        is_stressed,
        is_lonely,
    )

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

    model = load_mission_model()

    energy_preference = (
        "low" if is_low_mood or is_stressed
        else "medium"
    )

    def ranking_score(mission):
        rule_score = score_mission(
            mission,
            is_low_mood,
            is_stressed,
            is_lonely,
            repeated_low_mood,
            feedback_by_mission,
        )

        if model is None:
            return rule_score

        try:
            ml_score = predict_mission_match(
                model,
                mission,
                energy_preference,
                recently_seen=mission.id in recent_mission_ids,
            )
        except (ValueError, KeyError, AttributeError, TypeError):
            return rule_score

        return rule_score + ml_score

    candidates.sort(key=ranking_score, reverse=True)

    return candidates[0]