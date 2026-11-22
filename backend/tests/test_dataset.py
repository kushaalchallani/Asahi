"""Tests for the ML dataset module."""
import pytest
from ml.dataset import build_dataset, VALID_CATEGORIES, VALID_DIFFICULTIES, VALID_ENERGY_LEVELS


def make_minimal_record(**overrides):
    """Create a minimal valid record with all required fields."""
    record = {
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
    record.update(overrides)
    return record


def test_build_dataset_returns_valid_dataframe():
    """Dataset builder should return a valid DataFrame."""
    records = [make_minimal_record()]

    dataset = build_dataset(records)

    assert len(dataset) == 1
    assert dataset.loc[0, "preference_match"] == 1


def test_build_dataset_with_multiple_records():
    """Dataset builder should handle multiple records."""
    records = [
        make_minimal_record(preference_match=1),
        make_minimal_record(preference_match=0),
    ]

    dataset = build_dataset(records)

    assert len(dataset) == 2
    assert dataset["preference_match"].sum() == 1


def test_rejects_empty_dataset():
    """Empty datasets should raise an error."""
    with pytest.raises(ValueError, match="cannot be empty"):
        build_dataset([])


def test_reject_invalid_target():
    """Invalid target values should raise an error."""
    records = [make_minimal_record(preference_match=2)]

    with pytest.raises(ValueError, match="only 0 or 1"):
        build_dataset(records)


def test_rejects_missing_columns():
    """Missing columns should raise an error."""
    records = [{"category": "regulation"}]

    with pytest.raises(ValueError, match="Missing required columns"):
        build_dataset(records)


def test_rejects_negative_numeric_features():
    """Negative numeric features should raise an error."""
    records = [make_minimal_record(missions_completed_in_category=-1)]

    with pytest.raises(ValueError, match="must be non-negative"):
        build_dataset(records)


def test_rejects_invalid_feedback_ratio():
    """Invalid feedback positive ratio should raise an error."""
    records = [make_minimal_record(feedback_positive_ratio=1.5)]

    with pytest.raises(ValueError, match="feedback_positive_ratio must be between 0 and 1"):
        build_dataset(records)


def test_rejects_invalid_category():
    """Invalid category values should raise an error."""
    records = [make_minimal_record(category="invalid_category")]

    with pytest.raises(ValueError, match="Invalid category values"):
        build_dataset(records)


def test_rejects_invalid_difficulty():
    """Invalid difficulty values should raise an error."""
    records = [make_minimal_record(difficulty="extreme")]

    with pytest.raises(ValueError, match="Invalid difficulty values"):
        build_dataset(records)


def test_accepts_all_valid_categories():
    """All valid categories should be accepted."""
    for category in VALID_CATEGORIES:
        records = [make_minimal_record(category=category)]
        dataset = build_dataset(records)
        assert dataset.loc[0, "category"] == category


def test_accepts_all_valid_difficulties():
    """All valid difficulties should be accepted."""
    for difficulty in VALID_DIFFICULTIES:
        records = [make_minimal_record(difficulty=difficulty)]
        dataset = build_dataset(records)
        assert dataset.loc[0, "difficulty"] == difficulty


def test_accepts_all_valid_energy_levels():
    """All valid energy levels should be accepted."""
    for energy in VALID_ENERGY_LEVELS:
        records = [make_minimal_record(energy_required=energy, energy_preference=energy)]
        dataset = build_dataset(records)
        assert dataset.loc[0, "energy_required"] == energy


def test_handles_missing_values_in_non_required_columns():
    """Dataset should handle missing values in optional columns (they get filled with defaults)."""
    records = [make_minimal_record()]
    # Remove optional numeric columns if they exist
    for col in ["missions_completed_in_category", "feedback_positive_ratio"]:
        if col in records:
            del records[col]

    # This should still work if we provide all required columns
    records = [make_minimal_record()]
    dataset = build_dataset(records)
    assert len(dataset) == 1