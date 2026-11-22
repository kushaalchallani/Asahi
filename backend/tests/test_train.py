"""Tests for the ML training module."""
import pytest
import pandas as pd
from ml.train import train_model


def make_records():
    """Create test records with varied features."""
    records = []

    for i in range(20):
        matches = i % 2 == 0

        records.append({
            "category": "regulation" if matches else "connection",
            "difficulty": "low" if matches else "medium",
            "energy_required": "low" if matches else "medium",
            "social_required": not matches,
            "energy_preference": "low" if matches else "medium",
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
            "preference_match": int(matches),
        })

    return records


def test_model_trains_and_predicts():
    """Model should train and make predictions on valid data."""
    model, metrics = train_model(make_records())

    predictions = model.predict(pd.DataFrame([
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
        }
    ]))

    assert len(predictions) == 1
    assert predictions[0] in (0, 1)
    assert 0 <= metrics["accuracy"] <= 1
    assert 0 <= metrics["balanced_accuracy"] <= 1
    assert 0 <= metrics["baseline_accuracy"] <= 1
    assert 0 <= metrics["baseline_balanced_accuracy"] <= 1
    assert (
        metrics["test_class_0_count"]
        + metrics["test_class_1_count"]
        == 5
    )
    assert (
        metrics["true_negative"]
        + metrics["false_positive"]
        + metrics["false_negative"]
        + metrics["true_positive"]
        == 5
    )


def test_training_requires_both_classes():
    """Training should fail if only one class is present."""
    records = make_records()

    for record in records:
        record["preference_match"] = 1

    with pytest.raises(ValueError, match="both target classes"):
        train_model(records)


def test_training_rejects_too_few_examples_per_class():
    """Training should fail if one class has fewer than 2 examples."""
    records = make_records()

    for record in records:
        record["preference_match"] = 0

    records[0]["preference_match"] = 1

    with pytest.raises(ValueError, match='at least two examples'):
        train_model(records)


def test_training_rejects_invalid_test_size():
    """Training should fail with invalid test_size."""
    with pytest.raises(ValueError, match="test_size must be between 0 and 1"):
        train_model(make_records(), test_size=1)


def test_training_rejects_invalid_test_size_zero():
    """Training should fail with zero test_size."""
    with pytest.raises(ValueError, match="test_size must be between 0 and 1"):
        train_model(make_records(), test_size=0)


def test_metrics_include_ndcg():
    """Metrics should include NDCG@5 for ranking quality."""
    model, metrics = train_model(make_records())

    assert "ndcg_at_5" in metrics
    assert 0 <= metrics["ndcg_at_5"] <= 1


def test_metrics_include_f1_score():
    """Metrics should include F1 score."""
    model, metrics = train_model(make_records())

    assert "f1_score" in metrics
    assert 0 <= metrics["f1_score"] <= 1


def test_metrics_include_roc_auc():
    """Metrics should include ROC-AUC."""
    model, metrics = train_model(make_records())

    assert "roc_auc" in metrics
    assert 0 <= metrics["roc_auc"] <= 1