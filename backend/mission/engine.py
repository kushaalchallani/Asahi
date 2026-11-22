"""
Mission Recommendation Engine

Combines rule-based filtering with machine learning predictions
for personalized mission recommendations.

Architecture:
1. Safety filters (mood, stress, energy state)
2. Rule-based candidate ranking
3. ML model scoring (when available)
4. Final ranking combining all signals
"""
import pandas as pd
import re
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass

from ml.train import load_model

MODEL_PATH = Path(__file__).resolve().parents[1] / "ml" / "artifacts" / "mission_recommender.joblib"

# Mood detection keywords
LOW_MOOD_WORDS = [
    "low",
    "tired",
    "broken",
    "sad",
    "overwhelmed",
    "heartbroken",
]

STRESS_WORDS = ["stress", "stressed", "anxious"]


def load_mission_model():
    """Load the trained mission recommendation model.

    Returns None if model doesn't exist or fails to load.
    This enables graceful fallback to rule-based recommendations.
    """
    if not MODEL_PATH.exists():
        return None

    try:
        return load_model(MODEL_PATH)
    except (OSError, ValueError, ImportError):
        return None


def build_feedback_history(feedback_rows):
    """Build a dictionary mapping mission_id to feedback history list."""
    feedback_by_mission = {}

    for user_mission in feedback_rows:
        feedback_by_mission.setdefault(
            user_mission.mission_id, []
        ).append(user_mission.feedback)

    return feedback_by_mission


def score_feedback(feedback_history):
    """
    Score feedback history with recency weighting.

    Earlier feedback is weighted more (more recent = higher weight).
    Score range: -6 to +6
    """
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


def contains_mood_signal(text: str, words: List[str]) -> bool:
    """Check if text contains mood-indicating words, accounting for negation."""
    negations = {
        "not", "no", "never", "don't", "do not",
        "doesn't", "does not", "isn't", "is not",
        "aren't", "are not", "no longer",
    }

    for word in words:
        pattern = rf"\b{re.escape(word)}\b"

        for match in re.finditer(pattern, text):
            preceding_text = text[max(0, match.start() - 20):match.start()]

            # Only consider negation in the same short phrase
            preceding_text = re.split(
                r"[,.;!?]|\bbut\b|\bhowever\b",
                preceding_text,
            )[-1]

            preceding_words = set(preceding_text.split())

            if not preceding_words.intersection(negations):
                return True

    return False


def detect_mood(check_in) -> Dict[str, bool]:
    """Detect mood states from check-in text."""
    feeling = (getattr(check_in, "feeling", None) or "").lower()
    note = (getattr(check_in, "note", None) or "").lower()
    text = f"{feeling} {note}"

    return {
        "is_low_mood": contains_mood_signal(text, LOW_MOOD_WORDS),
        "is_stressed": contains_mood_signal(text, STRESS_WORDS),
        "is_lonely": contains_mood_signal(text, ["lonely"]),
    }


def infer_energy_preference(check_in) -> str:
    """Infer user's current energy preference from check-in text."""
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


def detect_repeated_low_mood(recent_check_ins) -> bool:
    """Detect if user has had multiple low mood check-ins recently."""
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


def filter_suitable_missions(
    missions: List,
    is_low_mood: bool,
    is_stressed: bool,
    is_lonely: bool
) -> List:
    """
    Apply safety filters to mission candidates.

    These filters ensure recommendations are appropriate for user's
    current mental state. These are hard constraints that cannot be
    overridden by ML predictions.
    """
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


def score_difficulty_preference(mission, difficulty_preference: str) -> int:
    """Score how well mission difficulty matches user's preference."""
    preferred_difficulty = {
        "easy": "low",
        "moderate": "medium",
        "challenging": "high",
    }.get(difficulty_preference)

    if not preferred_difficulty:
        return 0

    return 3 if getattr(mission, "difficulty", None) == preferred_difficulty else 0


def score_mission(
    mission,
    is_low_mood: bool,
    is_stressed: bool,
    is_lonely: bool,
    repeated_low_mood: bool,
    feedback_by_mission: Dict,
    difficulty_preference: str = "moderate",
) -> int:
    """
    Calculate rule-based score for a mission.

    Higher scores indicate better fit based on:
    - Energy alignment
    - Social preference
    - Mood-specific adaptations
    - Historical feedback
    - Difficulty preference
    """
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
    is_low_mood: bool,
    is_stressed: bool,
    is_lonely: bool,
    repeated_low_mood: bool,
    feedback_by_mission: Dict,
    difficulty_preference: str = "moderate",
) -> List[str]:
    """Generate reason codes for why a mission was recommended."""
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


# Mapping from reason codes to human-readable explanations
REASON_MESSAGES = {
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
    "ml_energy_match": (
        "Based on your current energy level."
    ),
    "ml_category_match": (
        "Similar to activities you've enjoyed before."
    ),
    "ml_feedback_aligned": (
        "Consistent with your past preferences."
    ),
}


def format_mission_reasons(reasons: List[str]) -> List[str]:
    """Convert reason codes to human-readable messages."""
    return [
        REASON_MESSAGES[reason]
        for reason in reasons
        if reason in REASON_MESSAGES
    ]


def build_recommendation_result(
    mission,
    is_low_mood: bool,
    is_stressed: bool,
    is_lonely: bool,
    repeated_low_mood: bool,
    feedback_by_mission: Dict,
    difficulty_preference: str = "moderate",
) -> Dict:
    """Build the recommendation result with mission, score, and explanations."""
    reasons = explain_mission_score(
        mission,
        is_low_mood=is_low_mood,
        is_stressed=is_stressed,
        is_lonely=is_lonely,
        repeated_low_mood=repeated_low_mood,
        feedback_by_mission=feedback_by_mission,
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


def predict_mission_match(
    model,
    mission,
    energy_preference: str,
    recently_seen: bool = False,
    feedback_history: List[str] = None,
    user_stats: Dict = None,
) -> float:
    """
    Predict the probability that a user will like a mission.

    Uses the ML model to predict preference_match probability.
    Falls back to heuristics if model fails.

    Args:
        model: Trained sklearn Pipeline
        mission: Mission object with category, difficulty, energy_required, social_required
        energy_preference: User's current energy preference (low/medium/high)
        recently_seen: Whether mission was recently assigned
        feedback_history: List of feedback for this mission
        user_stats: Additional user statistics

    Returns:
        Probability in [0, 1] that user will find mission suitable
    """
    # Build feature dictionary
    features_dict = {
        "category": mission.category,
        "difficulty": mission.difficulty,
        "energy_required": mission.energy_required,
        "social_required": mission.social_required,
        "energy_preference": energy_preference,
        "recently_seen": recently_seen,
        "missions_completed_in_category": user_stats.get("missions_completed_in_category", 0) if user_stats else 0,
        "missions_skipped_in_category": user_stats.get("missions_skipped_in_category", 0) if user_stats else 0,
        "missions_started_in_category": user_stats.get("missions_started_in_category", 0) if user_stats else 0,
        "missions_completed_similar": user_stats.get("missions_completed_similar", 0) if user_stats else 0,
        "missions_skipped_similar": user_stats.get("missions_skipped_similar", 0) if user_stats else 0,
        "feedback_positive_ratio": user_stats.get("feedback_positive_ratio", 0.5) if user_stats else 0.5,
        "time_since_last_low_energy_mission": user_stats.get("time_since_last_low_energy_mission", 30) if user_stats else 30,
        "preferred_category": user_stats.get("preferred_category", "reflection") if user_stats else "reflection",
        "preferred_difficulty": user_stats.get("preferred_difficulty", "moderate") if user_stats else "moderate",
    }

    features_df = pd.DataFrame([features_dict])

    try:
        proba = model.predict_proba(features_df)
        return float(proba[0][1])
    except Exception:
        # Fallback to heuristic scoring
        return _heuristic_ml_score(
            mission,
            energy_preference,
            recently_seen,
            feedback_history,
        )


def _heuristic_ml_score(
    mission,
    energy_preference: str,
    recently_seen: bool,
    feedback_history: List[str] = None,
) -> float:
    """
    Heuristic fallback for ML prediction when model unavailable.

    This provides consistent behavior when the model isn't loaded.
    """
    score = 0.5  # Base probability

    # Energy match bonus
    if mission.energy_required == energy_preference:
        score += 0.3
    else:
        score -= 0.2

    # Recently seen penalty
    if recently_seen:
        score -= 0.2

    # Feedback adjustment
    if feedback_history:
        helpful_count = sum(1 for f in feedback_history if f == "helpful")
        not_for_me_count = sum(1 for f in feedback_history if f == "not_for_me")
        total = len(feedback_history)

        if total > 0:
            feedback_ratio = helpful_count / total
            score = 0.3 + 0.4 * feedback_ratio  # Scale to [0.3, 0.7]

    return max(0.0, min(1.0, score))


def get_ml_explanations(
    model,
    mission,
    energy_preference: str,
    recently_seen: bool = False,
) -> List[str]:
    """
    Generate explanations based on ML model feature contributions.

    Provides explainability for why the ML model scored a mission highly.
    """
    explanations = []

    # Energy preference match
    if mission.energy_required == energy_preference:
        explanations.append("ml_energy_match")

    # Category preference match
    if hasattr(mission, 'category') and mission.category:
        # This would require storing user preferences; for now use a simple heuristic
        explanations.append("ml_category_match")

    return explanations


def choose_mission(
    current_check_in,
    recent_missions: List,
    missions: List,
    recent_feedback: Dict = None,
    recent_check_ins: List = None,
    difficulty_preference: str = "moderate",
) -> Optional[Any]:
    """
    Select the best mission for the user.

    Algorithm:
    1. Apply safety filters based on mood/stress
    2. Prioritize missions user hasn't seen recently
    3. Penalize missions with negative feedback
    4. Combine rule-based and ML scores for final ranking
    5. Return top-ranked mission

    Safety constraints are never overridden by ML predictions.
    """
    if not missions:
        return None

    candidates = missions.copy()
    mood = detect_mood(current_check_in)

    is_low_mood = mood["is_low_mood"]
    is_stressed = mood["is_stressed"]
    is_lonely = mood["is_lonely"]

    # Keep original list for fallback
    all_candidates = candidates.copy()

    # Apply safety filters
    candidates = filter_suitable_missions(
        missions,
        is_low_mood,
        is_stressed,
        is_lonely,
    )

    # Fall back if filters find nothing
    if not candidates:
        candidates = all_candidates

    # Avoid repeating recently assigned missions
    recent_mission_ids = {mission.id for mission in recent_missions}

    fresh_candidates = [
        mission
        for mission in candidates
        if mission.id not in recent_mission_ids
    ]

    if fresh_candidates:
        candidates = fresh_candidates

    # Apply negative feedback filtering
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
    energy_preference = infer_energy_preference(current_check_in)

    # Load ML model (gracefully handle failures)
    try:
        model = load_mission_model()
    except Exception:
        model = None

    def ranking_score(mission):
        """Calculate combined ranking score for a mission."""
        # Rule-based difficulty match bonus
        difficulty_match = score_difficulty_preference(
            mission,
            difficulty_preference,
        )

        # Rule-based score
        rule_score = score_mission(
            mission,
            is_low_mood,
            is_stressed,
            is_lonely,
            repeated_low_mood,
            feedback_by_mission,
            difficulty_preference=difficulty_preference,
        )

        # ML score (0 if model unavailable)
        if model is None:
            return (difficulty_match, rule_score, 0.0)

        try:
            ml_score = predict_mission_match(
                model,
                mission,
                energy_preference,
                recently_seen=mission.id in recent_mission_ids,
                feedback_history=feedback_by_mission.get(mission.id),
            )
        except (ValueError, KeyError, AttributeError, TypeError):
            ml_score = 0.0

        return (difficulty_match, rule_score, ml_score)

    # Sort by combined score (highest first)
    candidates.sort(key=ranking_score, reverse=True)

    return candidates[0]