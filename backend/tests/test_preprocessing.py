"""Tests for the ML preprocessing module."""
import pandas as pd
from ml.dataset import build_dataset, VALID_CATEGORIES
from ml.preprocessing import build_preprocessor, validate_features


def test_preprocessor_produces_numeric_features():
    """Preprocessor should transform features to numeric format."""
    records = [
        {
            "category": "regulation",
            "difficulty": "low",
            "energy_required": "low",
            "social_required": False,
            "energy_preference": "low",
            "recently_seen": False,
            "missions_completed_in_category": 0,
            "missions_skipped_in_category": 0,
            "missions_started_in_category": 0,
            "missions_completed_similar": 0,
            "missions_skipped_similar": 0,
            "feedback_positive_ratio": 0.5,
            "time_since_last_low_energy_mission": 30,
            "preferred_category": "reflection",
            "preferred_difficulty": "moderate",
            "preference_match": 1,
        },
        {
            "category": "connection",
            "difficulty": "medium",
            "energy_required": "medium",
            "social_required": True,
            "energy_preference": "medium",
            "recently_seen": True,
            "missions_completed_in_category": 5,
            "missions_skipped_in_category": 2,
            "missions_started_in_category": 1,
            "missions_completed_similar": 2,
            "missions_skipped_similar": 1,
            "feedback_positive_ratio": 0.75,
            "time_since_last_low_energy_mission": 15,
            "preferred_category": "regulation",
            "preferred_difficulty": "moderate",
            "preference_match": 0,
        },
    ]

    dataset = build_dataset(records)
    X = dataset.drop(columns=['preference_match'])

    preprocessor = build_preprocessor()
    transformed = preprocessor.fit_transform(X)

    assert transformed.shape[0] == 2
    assert transformed.shape[1] > 0
    assert pd.DataFrame(transformed).select_dtypes(
        include="number"
    ).shape == pd.DataFrame(transformed).shape


def test_unknown_categories_do_not_crash():
    """Unknown categories should be handled gracefully by the preprocessor."""
    training = pd.DataFrame([
        {
            "category": "regulation",
            "difficulty": "low",
            "energy_required": "low",
            "social_required": False,
            "energy_preference": "low",
            "recently_seen": False,
            "missions_completed_in_category": 0,
            "missions_skipped_in_category": 0,
            "missions_started_in_category": 0,
            "missions_completed_similar": 0,
            "missions_skipped_similar": 0,
            "feedback_positive_ratio": 0.5,
            "time_since_last_low_energy_mission": 30,
            "preferred_category": "reflection",
            "preferred_difficulty": "moderate",
            "preference_match": 1,
        }
    ])

    unseen = pd.DataFrame([
        {
            "category": "new_category",
            "difficulty": "low",
            "energy_required": "low",
            "social_required": False,
            "energy_preference": "low",
            "recently_seen": False,
            "missions_completed_in_category": 0,
            "missions_skipped_in_category": 0,
            "missions_started_in_category": 0,
            "missions_completed_similar": 0,
            "missions_skipped_similar": 0,
            "feedback_positive_ratio": 0.5,
            "time_since_last_low_energy_mission": 30,
            "preferred_category": "reflection",
            "preferred_difficulty": "moderate",
            "preference_match": 0,
        }
    ])

    preprocessor = build_preprocessor()
    preprocessor.fit(training)
    transformed = preprocessor.transform(unseen)

    assert transformed.shape[0] == 1


def test_validate_features_accepts_valid_data():
    """Feature validation should accept valid feature dictionaries."""
    features = {
        "category": "regulation",
        "difficulty": "low",
        "energy_required": "low",
        "social_required": False,
        "energy_preference": "low",
        "recently_seen": False,
        "missions_completed_in_category": 5,
        "missions_skipped_in_category": 0,
        "missions_started_in_category": 2,
        "missions_completed_similar": 3,
        "missions_skipped_similar": 0,
        "feedback_positive_ratio": 0.75,
        "time_since_last_low_energy_mission": 10,
        "preferred_category": "reflection",
        "preferred_difficulty": "moderate",
    }

    assert validate_features(features) is True


def test_validate_features_rejects_invalid_category():
    """Feature validation should reject invalid categories."""
    features = {
        "category": "invalid_category",
        "difficulty": "low",
        "energy_required": "low",
        "social_required": False,
        "energy_preference": "low",
        "recently_seen": False,
        "missions_completed_in_category": 0,
        "missions_skipped_in_category": 0,
        "missions_started_in_category": 0,
        "missions_completed_similar": 0,
        "missions_skipped_similar": 0,
        "feedback_positive_ratio": 0.5,
        "time_since_last_low_energy_mission": 30,
        "preferred_category": "reflection",
        "preferred_difficulty": "moderate",
    }

    with pytest.raises(ValueError):
        validate_features(features)


def test_validate_features_rejects_invalid_difficulty():
    """Feature validation should reject invalid difficulties."""
    features = {
        "category": "regulation",
        "difficulty": "extreme",
        "energy_required": "low",
        "social_required": False,
        "energy_preference": "low",
        "recently_seen": False,
        "missions_completed_in_category": 0,
        "missions_skipped_in_category": 0,
        "missions_started_in_category": 0,
        "missions_completed_similar": 0,
        "missions_skipped_similar": 0,
        "feedback_positive_ratio": 0.5,
        "time_since_last_low_energy_mission": 30,
        "preferred_category": "reflection",
        "preferred_difficulty": "moderate",
    }

    with pytest.raises(ValueError):
        validate_features(features)


def test_validate_features_rejects_negative_counts():
    """Feature validation should reject negative counts."""
    features = {
        "category": "regulation",
        "difficulty": "low",
        "energy_required": "low",
        "social_required": False,
        "energy_preference": "low",
        "recently_seen": False,
        "missions_completed_in_category": -1,
        "missions_skipped_in_category": 0,
        "missions_started_in_category": 0,
        "missions_completed_similar": 0,
        "missions_skipped_similar": 0,
        "feedback_positive_ratio": 0.5,
        "time_since_last_low_energy_mission": 30,
        "preferred_category": "reflection",
        "preferred_difficulty": "moderate",
    }

    with pytest.raises(ValueError):
        validate_features(features)


def test_validate_features_rejects_invalid_ratio():
    """Feature validation should reject invalid feedback ratios."""
    features = {
        "category": "regulation",
        "difficulty": "low",
        "energy_required": "low",
        "social_required": False,
        "energy_preference": "low",
        "recently_seen": False,
        "missions_completed_in_category": 0,
        "missions_skipped_in_category": 0,
        "missions_started_in_category": 0,
        "missions_completed_similar": 0,
        "missions_skipped_similar": 0,
        "feedback_positive_ratio": 1.5,
        "time_since_last_low_energy_mission": 30,
        "preferred_category": "reflection",
        "preferred_difficulty": "moderate",
    }

    with pytest.raises(ValueError):
        validate_features(features)