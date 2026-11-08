import pandas as pd
import re
from pathlib import Path
from ml.train import load_model

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
        feedback_by_mission.setdefault(
            user_mission.mission_id, []
        ).append(user_mission.feedback)

    return feedback_by_mission

def score_feedback(feedback_history):
    if not feedback_history:
        return 0

    score = 0

    for index, feedback in enumerate(feedback_history[:5]):
        weight = max(1, 3 - index)

        if feedback == "helpful":
            score += weight
        elif feedback == "not_for_me":
            score -= weight

    return max(-6, min(score, 6))

LOW_MOOD_WORDS = [
    "low",
    "tired",
    "broken",
    "sad",
    "overwhelmed",
    "heartbroken",
]

STRESS_WORDS = ["stress", "stressed", "anxious"]

def contains_mood_signal(text, words):
    negations = {
        "not", "no", "never", "don't", "do not",
        "doesn't", "does not", "isn't", "is not",
        "aren't", "are not", "no longer",
    }

    for word in words:
        pattern = rf"\b{re.escape(word)}\b"

        for match in re.finditer(pattern, text):
            preceding_text = text[max(0, match.start() - 20):match.start()]

            # Only consider negation in the same short phrase.
            preceding_text = re.split(
                r"[,.;!?]|\bbut\b|\bhowever\b",
                preceding_text,
            )[-1]

            preceding_words = set(preceding_text.split())

            if not preceding_words.intersection(negations):
                return True

    return False


def detect_mood(check_in):
    feeling = (getattr(check_in, "feeling", None) or "").lower()
    note = (getattr(check_in, "note", None) or "").lower()
    text = f"{feeling} {note}"

    return {
        "is_low_mood": contains_mood_signal(text, LOW_MOOD_WORDS),
        "is_stressed": contains_mood_signal(text, STRESS_WORDS),
        "is_lonely": contains_mood_signal(text, ["lonely"]),
    }

def infer_energy_preference(check_in):
    feeling = (getattr(check_in, "feeling", None) or "").lower()
    note = (getattr(check_in, "note", None) or "").lower()
    text = f"{feeling} {note}"

    low_energy_signals = (
        "exhausted",
        "tired",
        "fatigue",
        "no energy",
        "little energy",
        "drained",
        "worn out",
    )

    high_energy_signals = (
        "energetic",
        "full of energy",
        "lots of energy",
        "ready to be active",
    )

    if any(signal in text for signal in low_energy_signals):
        return "low"

    if any(signal in text for signal in high_energy_signals):
        return "high"

    if any(signal in feeling for signal in ("a little low", "stressed", "lonely")):
        return "low"

    return "medium"

def detect_repeated_low_mood(recent_check_ins):
    recent_check_ins = (recent_check_ins or [])[:3]

    if len(recent_check_ins) < 2:
        return False

    low_mood_count = 0

    for check_in in recent_check_ins:
        feeling = (getattr(check_in, "feeling", None) or "").lower()
        note = (getattr(check_in, "note", None) or "").lower()
        text = f"{feeling} {note}"

        if any(word in text for word in LOW_MOOD_WORDS):
            low_mood_count += 1

    return low_mood_count >= 2


def filter_suitable_missions(missions, is_low_mood, is_stressed, is_lonely):
    candidates = missions.copy()

    if is_low_mood or is_lonely:
        candidates = [
            mission
            for mission in candidates
            if mission.energy_required == "low"
            and not mission.social_required
        ]

    if is_stressed:
        candidates = [
            mission
            for mission in candidates
            if mission.category in ("regulation", "environment", "reflection")
        ]

    return candidates

def score_difficulty_preference(mission, difficulty_preference):
    preferred_difficulty = {
        "easy": "low",
        "moderate": "medium",
        "challenging": "high",
    }.get(difficulty_preference)

    if not preferred_difficulty:
        return 0

    return (
        3
        if getattr(mission, "difficulty", None) == preferred_difficulty
        else 0
    )

def score_mission(mission, is_low_mood, is_stressed, is_lonely, repeated_low_mood, feedback_by_mission, difficulty_preference="moderate"):
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

        score += score_feedback(
            feedback_by_mission.get(mission.id, [])
        )

        score += score_difficulty_preference(
            mission,
            difficulty_preference,
        )

        return score

def explain_mission_score(
    mission,
    is_low_mood,
    is_stressed,
    is_lonely,
    repeated_low_mood,
    feedback_by_mission,
    difficulty_preference="moderate",
):
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

    if score_difficulty_preference(
        mission,
        difficulty_preference,
    ) > 0:
        reasons.append("difficulty_match")

    feedback_history = feedback_by_mission.get(mission.id, [])

    if feedback_history:
        feedback_score = score_feedback(feedback_history)
        if feedback_score > 0:
            reasons.append("previously_helpful")
        elif feedback_score < 0:
            reasons.append("mixed_or_negative_feedback")

    return reasons

def format_mission_reasons(reasons):
    messages = {
        "low_energy": "This activity requires little energy.",
        "non_social": "You can do this activity on your own.",
        "connection_for_loneliness": (
            "This activity offers an opportunity for connection."
        ),
        "regulation_for_stress": (
            "This activity may help you pause and unwind."
        ),
        "low_energy_for_low_mood": (
            "This is a manageable activity for a difficult day."
        ),
        "low_energy_for_repeated_low_mood": (
            "This activity keeps the effort manageable."
        ),
        "previously_helpful": (
            "You've found this activity helpful before."
        ),
        "difficulty_match": (
            "This activity matches your preferred difficulty level."
        ),
        "mixed_or_negative_feedback": (
            "Your previous feedback suggests this activity may not be the best fit."
        ),
    }

    return [
        messages[reason]
        for reason in reasons
        if reason in messages
    ]


def build_recommendation_result(mission, is_low_mood, is_stressed, is_lonely, repeated_low_mood, feedback_by_mission, difficulty_preference="moderate"):
    reasons = explain_mission_score(
        mission,
        is_low_mood,
        is_stressed,
        is_lonely,
        repeated_low_mood,
        feedback_by_mission,
        difficulty_preference=difficulty_preference,
    )

    score = score_mission(
        mission,
        is_low_mood,
        is_stressed,
        is_lonely,
        repeated_low_mood,
        feedback_by_mission,
        difficulty_preference=difficulty_preference,
    )

    return {
        "mission": mission,
        "score": score,
        "reasons": reasons,
        "explanations": format_mission_reasons(reasons),
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

def choose_mission(current_check_in, recent_missions, missions, recent_feedback=None, recent_check_ins=None, difficulty_preference="moderate"):
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

    feedback_by_mission = recent_feedback or {}

    disliked_candidates = [
        mission
        for mission in candidates
        if score_feedback(
            feedback_by_mission.get(mission.id, [])
        ) < 0
    ]

    if len(disliked_candidates) < len(candidates):
        candidates = [
            mission
            for mission in candidates
            if mission not in disliked_candidates
        ]
    else:
        candidates = [
            mission
            for mission in candidates
            if not (
                feedback_by_mission.get(mission.id)
                and feedback_by_mission[mission.id][0] == "not_for_me"
            )
        ]

    repeated_low_mood = detect_repeated_low_mood(recent_check_ins)

    try:
        model = load_mission_model()
    except Exception:
        model = None

    energy_preference = infer_energy_preference(current_check_in)

    
    def ranking_score(mission):
        difficulty_match = (
            score_difficulty_preference(
                mission,
                difficulty_preference,
            )
        )

        rule_score = score_mission(
            mission,
            is_low_mood,
            is_stressed,
            is_lonely,
            repeated_low_mood,
            feedback_by_mission,
            difficulty_preference=difficulty_preference,
        )

        if model is None:
            return (difficulty_match, rule_score, 0.0)

        try:
            ml_score = predict_mission_match(
                model,
                mission,
                energy_preference,
                recently_seen=mission.id in recent_mission_ids,
            )
        except (ValueError, KeyError, AttributeError, TypeError):
            ml_score = 0.0

        return (difficulty_match, rule_score, ml_score)

    candidates.sort(key=ranking_score, reverse=True)

    return candidates[0]