"""Tests for the export_feedback_dataset module."""
import pytest
from datetime import datetime, timedelta
from ml.export_feedback_dataset import (
    has_sufficient_real_data,
    generate_synthetic_training_data,
)
from ml.experiment import make_synthetic_records


def test_has_sufficient_real_data_returns_false_for_empty():
    """Should return False for empty records."""
    assert has_sufficient_real_data([]) is False


def test_has_sufficient_real_data_requires_both_classes():
    """Should return False if only one class is present."""
    records = [{"preference_match": 1}] * 30
    assert has_sufficient_real_data(records) is False

    records = [{"preference_match": 0}] * 30
    assert has_sufficient_real_data(records) is False


def test_has_sufficient_real_data_requires_minimum_count():
    """Should return False if too few examples."""
    records = [{"preference_match": 0}] * 15 + [{"preference_match": 1}] * 15
    assert has_sufficient_real_data(records) is False


def test_has_sufficient_real_data_returns_true_when_sufficient():
    """Should return True when sufficient data with both classes."""
    records = [{"preference_match": 0}] * 30 + [{"preference_match": 1}] * 30
    assert has_sufficient_real_data(records) is True


def test_make_synthetic_records_includes_all_features():
    """Synthetic records should include all required features."""
    records = make_synthetic_records()

    expected_features = [
        "category", "difficulty", "energy_required", "social_required",
        "energy_preference", "recently_seen",
        "missions_completed_in_category", "missions_skipped_in_category",
        "missions_started_in_category", "missions_completed_similar",
        "missions_skipped_similar", "feedback_positive_ratio",
        "time_since_last_low_energy_mission",
        "preferred_category", "preferred_difficulty",
        "preference_match",
    ]

    assert len(records) > 0
    for feature in expected_features:
        assert feature in records[0], f"Missing feature: {feature}"


def test_make_synthetic_records_has_balanced_classes():
    """Synthetic records should have both positive and negative examples."""
    records = make_synthetic_records()

    positive = sum(1 for r in records if r.get("preference_match") == 1)
    negative = sum(1 for r in records if r.get("preference_match") == 0)

    assert positive > 0
    assert negative > 0


def test_generate_synthetic_training_data_includes_all_features():
    """Generated synthetic data should include all required features."""
    records = generate_synthetic_training_data(num_samples=50)

    expected_features = [
        "category", "difficulty", "energy_required", "social_required",
        "energy_preference", "recently_seen",
        "missions_completed_in_category", "missions_skipped_in_category",
        "missions_started_in_category", "missions_completed_similar",
        "missions_skipped_similar", "feedback_positive_ratio",
        "time_since_last_low_energy_mission",
        "preferred_category", "preferred_difficulty",
        "preference_match",
    ]

    assert len(records) > 0
    for feature in expected_features:
        assert feature in records[0], f"Missing feature: {feature}"