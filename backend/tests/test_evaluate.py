"""Tests for the ML evaluation module."""
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, classification_report, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from ml.evaluate import evaluate_model, create_train_test_split, compute_ndcg_at_k
from ml.preprocessing import build_preprocessor
from ml.dataset import build_dataset
from ml.experiment import make_synthetic_records


def test_evaluate_mode_prints_metrics_and_confusion_matrix(capsys):
    """Evaluate mode should print all metrics."""
    x_train = pd.DataFrame({
        "category": ["regulation", "connection", "reflection", "regulation"],
        "difficulty": ["low", "medium", "low", "medium"],
        "energy_required": ["low", "medium", "high", "low"],
        "social_required": [False, True, False, True],
        "energy_preference": ["low", "medium", "high", "low"],
        "recently_seen": [False, True, False, True],
        "missions_completed_in_category": [0, 0, 0, 0],
        "missions_skipped_in_category": [0, 0, 0, 0],
        "missions_started_in_category": [0, 0, 0, 0],
        "missions_completed_similar": [0, 0, 0, 0],
        "missions_skipped_similar": [0, 0, 0, 0],
        "feedback_positive_ratio": [0.5, 0.5, 0.5, 0.5],
        "time_since_last_low_energy_mission": [30, 30, 30, 30],
        "preferred_category": ["reflection", "reflection", "reflection", "reflection"],
        "preferred_difficulty": ["moderate", "moderate", "moderate", "moderate"],
    })
    y_train = np.array([0, 0, 1, 1])
    x_test = x_train.iloc[:2].copy()
    y_test = np.array([0, 1])

    model = Pipeline([
        ("preprocessor", build_preprocessor()),
        ("classifier", DummyClassifier(strategy="most_frequent")),
    ])

    evaluate_model(
        "Test model",
        model,
        x_train,
        x_test,
        y_train,
        y_test,
    )

    output = capsys.readouterr().out

    assert "--- Test model ---" in output
    assert "Accuracy:" in output
    assert "Balanced accuracy:" in output
    assert "Precision:" in output
    assert "Recall:" in output
    assert "Confusion matrix" in output
    assert "Classification report:" in output


def test_train_test_split_is_reproducible():
    """Train/test split should be reproducible with same random seed."""
    dataset = build_dataset(make_synthetic_records())

    first = create_train_test_split(dataset)
    second = create_train_test_split(dataset)

    for first_part, second_part in zip(first, second):
        assert first_part.equals(second_part)


def test_train_test_split_preserves_both_classes():
    """Train/test split should preserve class distribution."""
    dataset = build_dataset(make_synthetic_records())

    x_train, x_test, y_train, y_test = create_train_test_split(dataset)

    assert set(y_train.unique()) == {0, 1}
    assert set(y_test.unique()) == {0, 1}
    assert len(x_train) + len(x_test) == len(dataset)
    assert len(x_test) == 54


def test_compute_ndcg_at_k_with_perfect_ranking():
    """NDCG@K should be 1.0 for perfect ranking."""
    y_true = np.array([1, 0, 1, 0, 1])
    y_scores = np.array([0.9, 0.1, 0.8, 0.2, 0.7])  # Perfect ranking

    ndcg = compute_ndcg_at_k(y_true, y_scores, k=5)
    assert ndcg == pytest.approx(1.0, rel=0.01)


def test_compute_ndcg_at_k_with_wrong_ranking():
    """NDCG@K should be low for poor ranking."""
    y_true = np.array([1, 0, 1, 0, 1])
    y_scores = np.array([0.1, 0.9, 0.2, 0.8, 0.3])  # Wrong ranking

    ndcg = compute_ndcg_at_k(y_true, y_scores, k=5)
    assert ndcg < 1.0


def test_compute_ndcg_at_k_with_empty_input():
    """NDCG@K should return 0 for empty input."""
    ndcg = compute_ndcg_at_k(np.array([]), np.array([]))
    assert ndcg == 0.0


def test_compute_ndcg_at_k_limits_to_k():
    """NDCG@K should only consider top K items."""
    y_true = np.array([1, 1, 1, 0, 0, 0])
    y_scores = np.array([0.9, 0.8, 0.7, 0.6, 0.5, 0.4])

    ndcg = compute_ndcg_at_k(y_true, y_scores, k=3)
    # With only top 3, all relevant items are in top positions
    assert ndcg > 0.5