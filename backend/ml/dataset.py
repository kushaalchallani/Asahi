"""
Dataset building utilities for mission recommendation ML model.

Features are designed to capture both user context and mission characteristics
for predicting preference match likelihood.
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional

# Core features used for training
FEATURE_COLUMNS = [
    # Mission features
    "category",
    "difficulty",
    "energy_required",
    "social_required",
    # User context features
    "energy_preference",
    "recently_seen",
    # Historical interaction features
    "missions_completed_in_category",
    "missions_skipped_in_category",
    "missions_started_in_category",
    "missions_completed_similar",
    "missions_skipped_similar",
    "feedback_positive_ratio",
    "time_since_last_low_energy_mission",
    # User preference features (derived from history)
    "preferred_category",
    "preferred_difficulty",
]

# Target column - whether user found mission suitable
TARGET_COLUMN = "preference_match"

REQUIRED_COLUMN = FEATURE_COLUMNS + [TARGET_COLUMN]

# Valid values for categorical features
VALID_CATEGORIES = {'regulation', 'connection', 'reflection', 'self-care', 'environment'}
VALID_DIFFICULTIES = {'low', 'medium', 'high'}
VALID_ENERGY_LEVELS = {'low', 'medium', 'high'}


def build_dataset(records: list[dict]) -> pd.DataFrame:
    """
    Build a pandas DataFrame from training records.

    Validates that all required columns are present and contain valid values.
    """
    if not records:
        raise ValueError("The dataset cannot be empty")

    dataset = pd.DataFrame(records)

    missing_columns = set(REQUIRED_COLUMN) - set(dataset.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    dataset = dataset[REQUIRED_COLUMN].copy()

    # Validate no missing values
    if dataset.isnull().any().any():
        raise ValueError("The dataset cannot contain missing values")

    # Validate target values
    if not dataset[TARGET_COLUMN].isin([0, 1]).all():
        raise ValueError("preference_match must contain only 0 or 1")

    # Validate categorical features
    if not dataset["category"].isin(VALID_CATEGORIES).all():
        raise ValueError(f"Invalid category values. Valid: {VALID_CATEGORIES}")
    if not dataset["difficulty"].isin(VALID_DIFFICULTIES).all():
        raise ValueError(f"Invalid difficulty values. Valid: {VALID_DIFFICULTIES}")
    if not dataset["energy_required"].isin(VALID_ENERGY_LEVELS).all():
        raise ValueError(f"Invalid energy_required values. Valid: {VALID_ENERGY_LEVELS}")
    if not dataset["energy_preference"].isin(VALID_ENERGY_LEVELS).all():
        raise ValueError(f"Invalid energy_preference values. Valid: {VALID_ENERGY_LEVELS}")
    if not dataset["preferred_category"].isin(VALID_CATEGORIES).all():
        raise ValueError(f"Invalid preferred_category values. Valid: {VALID_CATEGORIES}")

    # Validate preferred_difficulty (user preference: easy/moderate/challenging)
    valid_user_difficulties = {'easy', 'moderate', 'challenging'}
    if not dataset["preferred_difficulty"].isin(valid_user_difficulties).all():
        raise ValueError(f"Invalid preferred_difficulty values. Valid: {valid_user_difficulties}")

    # Validate feedback_positive_ratio is between 0 and 1
    if (dataset["feedback_positive_ratio"] < 0).any() or (dataset["feedback_positive_ratio"] > 1).any():
        raise ValueError("feedback_positive_ratio must be between 0 and 1")

    # Validate numeric features are non-negative
    numeric_cols = [
        "missions_completed_in_category",
        "missions_skipped_in_category",
        "missions_started_in_category",
        "missions_completed_similar",
        "missions_skipped_similar",
        "time_since_last_low_energy_mission",
    ]
    for col in numeric_cols:
        if (dataset[col] < 0).any():
            raise ValueError(f"{col} must be non-negative")

    # Validate numeric features are non-negative
    numeric_cols = [
        "missions_completed_in_category",
        "missions_skipped_in_category",
        "missions_started_in_category",
        "missions_completed_similar",
        "missions_skipped_similar",
        "time_since_last_low_energy_mission",
    ]
    for col in numeric_cols:
        if (dataset[col] < 0).any():
            raise ValueError(f"{col} must be non-negative")

    # Validate feedback ratio is between 0 and 1
    if (dataset["feedback_positive_ratio"] < 0).any() or (dataset["feedback_positive_ratio"] > 1).any():
        raise ValueError("feedback_positive_ratio must be between 0 and 1")

    return dataset


def compute_numeric_feature_stats(values: list, max_val: int = 10) -> int:
    """
    Compute a bounded numeric statistic from a list of values.

    Clips to max_val to prevent extreme values from dominating.
    """
    if not values:
        return 0
    result = len(values)
    return min(result, max_val)


def compute_recent_mission_time_delta(last_assigned_at: Optional[datetime]) -> int:
    """
    Compute time since last mission of similar type.

    Returns number of days since, capped at 30.
    """
    if not last_assigned_at:
        return 30  # No recent missions

    delta = datetime.now() - last_assigned_at
    days = delta.days
    return min(days, 30)