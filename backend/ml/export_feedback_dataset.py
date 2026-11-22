"""
Export training data from user mission interactions.

This module extracts real user feedback data and generates meaningful
training labels that reflect actual user preferences and satisfaction.
"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional
import models
from ml.dataset import (
    VALID_CATEGORIES,
    VALID_DIFFICULTIES,
    VALID_ENERGY_LEVELS,
)


def compute_user_interaction_stats(
    db: Session,
    user_id: int,
    days_lookback: int = 90
) -> dict:
    """
    Compute interaction statistics for a user from their history.

    Returns stats broken down by category, difficulty, and energy level.
    """
    cutoff_date = datetime.now() - timedelta(days=days_lookback)

    # Get all user missions within lookback period
    user_missions = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.user_id == user_id,
            models.UserMission.assigned_at >= cutoff_date,
        )
        .order_by(models.UserMission.assigned_at.asc())
        .all()
    )

    stats = {
        # Counts by category
        "categories_completed": defaultdict(int),
        "categories_skipped": defaultdict(int),
        "categories_started": defaultdict(int),

        # Total counts
        "total_completed": 0,
        "total_skipped": 0,
        "total_started": 0,
        "total_helpful": 0,
        "total_not_for_me": 0,

        # Time-based
        "last_low_energy_mission_at": None,
    }

    for um in user_missions:
        # Get mission category via mission_id
        mission = db.query(models.Mission).filter(models.Mission.id == um.mission_id).first() if hasattr(um, 'mission_id') and um.mission_id else None
        category = mission.category if mission else "other"

        if um.feedback == "helpful":
            stats["total_helpful"] += 1
            if um.status in ("completed", "started"):
                stats["total_completed"] += 1
                stats["categories_completed"][category] += 1
        elif um.feedback == "not_for_me":
            stats["total_not_for_me"] += 1
            stats["categories_skipped"][category] += 1
        elif um.status == "started":
            stats["total_started"] += 1
            stats["categories_started"][category] += 1
        elif um.status == "skipped":
            stats["total_skipped"] += 1

    return stats


def compute_preferred_category(db: Session, user_id: int, days_lookback: int = 90) -> str:
    """
    Determine user's preferred category based on completed missions.

    Falls back to 'reflection' if no data.
    """
    cutoff_date = datetime.now() - timedelta(days=days_lookback)

    category_counts = defaultdict(int)
    user_missions = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.user_id == user_id,
            models.UserMission.status.in_(["completed", "started"]),
            models.UserMission.assigned_at >= cutoff_date,
        )
        .all()
    )

    for um in user_missions:
        # Get mission category via mission_id
        mission = db.query(models.Mission).filter(models.Mission.id == um.mission_id).first() if hasattr(um, 'mission_id') and um.mission_id else None
        if mission:
            category_counts[mission.category] += 1

    if not category_counts:
        return "reflection"

    return max(category_counts.keys(), key=lambda k: category_counts[k])


def infer_energy_preference_from_history(db: Session, user_id: int) -> str:
    """
    Infer user's current energy preference from recent check-ins.

    Uses the last 3 check-ins, weighting recent ones more heavily.
    """
    recent_check_ins = (
        db.query(models.CheckIn)
        .filter(models.CheckIn.user_id == user_id)
        .order_by(models.CheckIn.created_at.desc())
        .limit(5)
        .all()
    )

    if not recent_check_ins:
        return "medium"

    low_energy_signals = [
        "exhausted", "tired", "fatigue", "no energy",
        "little energy", "drained", "worn out", "low energy"
    ]
    high_energy_signals = [
        "energetic", "full of energy", "lots of energy",
        "ready to be active", "high energy"
    ]

    low_count = 0
    high_count = 0

    # Weight recent check-ins more
    for i, ci in enumerate(recent_check_ins[:3]):
        weight = 3 - i  # Most recent = weight 3
        text = f"{(ci.feeling or '')} {(ci.note or '')}".lower()

        if any(s in text for s in low_energy_signals):
            low_count += weight
        if any(s in text for s in high_energy_signals):
            high_count += weight

    if low_count > high_count:
        return "low"
    elif high_count > low_count:
        return "high"
    return "medium"


def get_latest_check_in_energy_preference(db: Session, user_id: int) -> str:
    """
    Get energy preference from the most recent check-in.
    """
    latest_check_in = (
        db.query(models.CheckIn)
        .filter(models.CheckIn.user_id == user_id)
        .order_by(models.CheckIn.created_at.desc())
        .first()
    )

    if not latest_check_in:
        return "medium"

    text = f"{(latest_check_in.feeling or '')} {(latest_check_in.note or '')}".lower()

    low_energy_signals = [
        "exhausted", "tired", "fatigue", "no energy",
        "little energy", "drained", "worn out", "low energy"
    ]
    high_energy_signals = [
        "energetic", "full of energy", "lots of energy",
        "ready to be active", "high energy"
    ]

    if any(s in text for s in low_energy_signals):
        return "low"
    if any(s in text for s in high_energy_signals):
        return "high"
    return "medium"


def is_mission_recently_seen(db: Session, user_id: int, mission_id: int, days: int = 7) -> bool:
    """Check if a mission was recently assigned to the user."""
    cutoff_date = datetime.now() - timedelta(days=days)

    recent = (
        db.query(models.UserMission)
        .filter(
            models.UserMission.user_id == user_id,
            models.UserMission.mission_id == mission_id,
            models.UserMission.assigned_at >= cutoff_date,
        )
        .first()
    )
    return recent is not None


def export_feedback_dataset(db: Session) -> list[dict]:
    """
    Export training records from user mission feedback.

    Creates labeled examples where:
    - Positive labels (1): missions marked as "helpful"
    - Negative labels (0): missions marked as "not_for_me"
      or skipped without completion

    Features include both mission attributes and derived user statistics.
    """
    records = []
    users = db.query(models.User).all()

    for user in users:
        user_id = user.id

        # Get user statistics
        stats = compute_user_interaction_stats(db, user_id)
        preferred_category = compute_preferred_category(db, user_id)
        inferred_energy_pref = infer_energy_preference_from_history(db, user_id)

        # Get user's explicit difficulty preference (if available)
        difficulty_preference = getattr(user, 'difficulty_preference', 'moderate')

        # Get missions with feedback
        feedback_missions = (
            db.query(models.UserMission)
            .filter(
                models.UserMission.user_id == user_id,
                models.UserMission.feedback.in_(["helpful", "not_for_me"]),
            )
            .order_by(models.UserMission.assigned_at.asc())
            .all()
        )

        for um in feedback_missions:
            mission = (
                db.query(models.Mission)
                .filter(models.Mission.id == um.mission_id)
                .first()
            )

            if mission is None:
                continue

            # Get latest check-in for energy preference
            latest_check_in = (
                db.query(models.CheckIn)
                .filter(models.CheckIn.user_id == user_id)
                .order_by(models.CheckIn.created_at.desc())
                .first()
            )

            if latest_check_in is None:
                continue

            feeling = (latest_check_in.feeling or "").lower()
            note = (latest_check_in.note or "").lower()
            text = f"{feeling} {note}"

            # Infer energy preference from check-in text
            energy_preference = get_latest_check_in_energy_preference(db, user_id)

            # Check if recently seen
            recently_seen = is_mission_recently_seen(db, user_id, mission.id, days=7)

            # Compute category-specific stats
            cat_completed = stats["categories_completed"].get(mission.category, 0)
            cat_skipped = stats["categories_skipped"].get(mission.category, 0)
            cat_started = stats["categories_started"].get(mission.category, 0)

            # Similarity scores
            similar_completed = cat_completed
            similar_skipped = cat_skipped

            # Feedback ratio (helpful / total)
            total_interactions = stats["total_helpful"] + stats["total_not_for_me"]
            if total_interactions > 0:
                feedback_ratio = stats["total_helpful"] / total_interactions
            else:
                feedback_ratio = 0.5

            # Time since last mission in same category (not used currently, kept for future)
            # This would need additional tracking in stats

            record = {
                # Mission features
                "category": mission.category,
                "difficulty": mission.difficulty,
                "energy_required": mission.energy_required,
                "social_required": mission.social_required,
                # User context
                "energy_preference": energy_preference,
                "recently_seen": recently_seen,
                # Historical features
                "missions_completed_in_category": min(cat_completed, 10),
                "missions_skipped_in_category": min(cat_skipped, 10),
                "missions_started_in_category": min(cat_started, 10),
                "missions_completed_similar": min(similar_completed, 10),
                "missions_skipped_similar": min(similar_skipped, 10),
                "feedback_positive_ratio": feedback_ratio,
                "time_since_last_low_energy_mission": 30,  # Default
                # User preferences
                "preferred_category": preferred_category,
                "preferred_difficulty": difficulty_preference,
                # Target
                "preference_match": 1 if um.feedback == "helpful" else 0,
            }

            records.append(record)

    return records


def generate_synthetic_training_data(
    user_profiles: Optional[list[dict]] = None,
    mission_pool: Optional[list] = None,
    num_samples: int = 100,
    randomness: float = 0.3
) -> list[dict]:
    """
    Generate synthetic training data when real data is insufficient.

    This creates training examples based on the principle that:
    - Match: energy matches, difficulty is low, not recently seen, not social
    - Mis-match: various violations of these principles

    Used only when real user feedback data is insufficient for training.
    """
    import random
    from itertools import product

    categories = ['regulation', 'connection', 'reflection', 'self-care', 'environment']
    difficulties = ['low', 'medium', 'high']
    energy_levels = ['low', 'medium', 'high']
    social_options = [False, True]

    records = []

    # Generate base combinations
    for category in categories:
        for difficulty in ['low', 'medium']:  # Focus on achievable difficulties
            for energy_req in energy_levels:
                for social in social_options:
                    for energy_pref in energy_levels:
                        for recently_seen in [False, True]:
                            # Heuristic: match when energy aligns and difficulty is low
                            preference_match = int(
                                energy_req == energy_pref
                                and difficulty == "low"
                                and not recently_seen
                            )

                            records.append({
                                "category": category,
                                "difficulty": difficulty,
                                "energy_required": energy_req,
                                "social_required": social,
                                "energy_preference": energy_pref,
                                "recently_seen": recently_seen,
                                "missions_completed_in_category": 0,
                                "missions_skipped_in_category": 0,
                                "missions_started_in_category": 0,
                                "missions_completed_similar": 0,
                                "missions_skipped_similar": 0,
                                "feedback_positive_ratio": 0.5,
                                "time_since_last_low_energy_mission": 30,
                                "preferred_category": "reflection",
                                "preferred_difficulty": "moderate",
                                "preference_match": preference_match,
                            })

    return records


def has_sufficient_real_data(records: list[dict], min_examples: int = 30) -> bool:
    """
    Check if we have enough real user feedback for training.

    Requires both positive and negative examples.
    """
    if not records:
        return False

    positive = sum(1 for r in records if r.get("preference_match") == 1)
    negative = sum(1 for r in records if r.get("preference_match") == 0)

    has_both = positive >= 2 and negative >= 2
    enough_total = len(records) >= min_examples

    return has_both and enough_total