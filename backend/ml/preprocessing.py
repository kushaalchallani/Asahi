from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import numpy as np


# Categorical features that need one-hot encoding
CATEGORICAL_FEATURES = [
    "category",
    "difficulty",
    "energy_required",
    "energy_preference",
    "preferred_category",
]

# Boolean features passed through as-is
BOOLEAN_FEATURES = [
    "social_required",
    "recently_seen",
]

# Numeric features (passed through)
NUMERIC_FEATURES = [
    "missions_completed_in_category",
    "missions_skipped_in_category",
    "missions_started_in_category",
    "missions_completed_similar",
    "missions_skipped_similar",
    "feedback_positive_ratio",
    "time_since_last_low_energy_mission",
]


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES
            ),
            (
                "boolean",
                "passthrough",
                BOOLEAN_FEATURES,
            ),
            (
                "numeric",
                "passthrough",
                NUMERIC_FEATURES,
            )
        ],
        remainder="drop",
        verbose_feature_names_out=False
    )


def validate_features(features_dict: dict) -> bool:
    # Check required keys
    required_keys = [
        "category", "difficulty", "energy_required", "social_required",
        "energy_preference", "recently_seen",
        "preferred_category", "preferred_difficulty",
    ]

    for key in required_keys:
        if key not in features_dict:
            raise ValueError(f"Missing required feature: {key}")

    # Validate categorical values
    valid_categories = {'regulation', 'connection', 'reflection', 'self-care', 'environment'}
    valid_difficulties = {'low', 'medium', 'high'}
    valid_energies = {'low', 'medium', 'high'}

    if features_dict["category"] not in valid_categories:
        raise ValueError(f"Invalid category: {features_dict['category']}")
    if features_dict["difficulty"] not in valid_difficulties:
        raise ValueError(f"Invalid difficulty: {features_dict['difficulty']}")
    if features_dict["energy_required"] not in valid_energies:
        raise ValueError(f"Invalid energy_required: {features_dict['energy_required']}")
    if features_dict["energy_preference"] not in valid_energies:
        raise ValueError(f"Invalid energy_preference: {features_dict['energy_preference']}")
    if features_dict["preferred_category"] not in valid_categories:
        raise ValueError(f"Invalid preferred_category: {features_dict['preferred_category']}")

    # Validate preferred_difficulty 
    valid_user_difficulties = {'easy', 'moderate', 'challenging'}
    if features_dict.get("preferred_difficulty") not in valid_user_difficulties:
        raise ValueError(f"Invalid preferred_difficulty. Valid: {valid_user_difficulties}")

    # Validate boolean
    if not isinstance(features_dict["social_required"], bool):
        raise ValueError("social_required must be boolean")
    if not isinstance(features_dict["recently_seen"], bool):
        raise ValueError("recently_seen must be boolean")

    # Validate numeric keys exist and are numeric
    numeric_keys = [
        "missions_completed_in_category",
        "missions_skipped_in_category",
        "missions_started_in_category",
        "missions_completed_similar",
        "missions_skipped_similar",
        "feedback_positive_ratio",
        "time_since_last_low_energy_mission",
    ]

    for key in numeric_keys:
        if key not in features_dict:
            raise ValueError(f"Missing required feature: {key}")
        if not isinstance(features_dict[key], (int, float)):
            raise ValueError(f"{key} must be numeric")

    # Validate feedback ratio
    ratio = features_dict.get("feedback_positive_ratio", 0.5)
    if not 0 <= ratio <= 1:
        raise ValueError("feedback_positive_ratio must be between 0 and 1")

    return True