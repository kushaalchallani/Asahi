"""
Model evaluation utilities for mission recommendation ML.

Provides train/test split, model evaluation with multiple metrics,
and ranking quality assessment.
"""
import numpy as np
from typing import Tuple
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from ml.dataset import build_dataset, TARGET_COLUMN
from ml.preprocessing import build_preprocessor


def compute_ndcg_at_k(y_true: np.ndarray, y_scores: np.ndarray, k: int = 5) -> float:
    """
    Compute Normalized Discounted Cumulative Gain at K.

    Used for evaluating ranking quality of recommendations.
    Higher scores indicate better ranking of relevant items.
    """
    if len(y_true) == 0:
        return 0.0

    n = len(y_true)
    k = min(k, n)

    if k == 0:
        return 0.0

    # Sort by predicted scores (descending)
    indices = np.argsort(y_scores)[::-1][:k]

    # DCG at K - calculate ranks based on prediction ordering
    # Rank 1 is the highest predicted score
    ranks_pred = np.arange(1, k + 1)
    dcg = np.sum((2 ** y_true[indices] - 1) / np.log2(ranks_pred + 1))

    # Ideal DCG - items sorted by true relevance
    ideal_indices = np.argsort(y_true)[::-1][:k]

    # Rank 1 is the most relevant item in ideal ordering
    ranks_ideal = np.arange(1, k + 1)
    ideal_dcg = np.sum((2 ** y_true[ideal_indices] - 1) / np.log2(ranks_ideal + 1))

    if ideal_dcg == 0:
        return 0.0

    return dcg / ideal_dcg


def create_train_test_split(dataset, test_size: float = 0.25, random_state: int = 42):
    """Create stratified train/test split."""
    x = dataset.drop(columns=[TARGET_COLUMN])
    y = dataset[TARGET_COLUMN]

    return train_test_split(x, y, test_size=test_size, random_state=random_state, stratify=y)


def evaluate_model(
    name: str,
    model,
    x_train,
    x_test,
    y_train,
    y_test,
) -> None:
    """Print evaluation metrics for a trained model."""
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1] if hasattr(model, 'predict_proba') else np.zeros(len(y_test))

    print(f"\n--- {name} ---")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(f"Balanced accuracy: {balanced_accuracy_score(y_test, predictions):.3f}")
    print(f"Precision: {precision_score(y_test, predictions, zero_division=0):.3f}")
    print(f"Recall: {recall_score(y_test, predictions, zero_division=0):.3f}")
    print(f"F1 Score: {f1_score(y_test, predictions, zero_division=0):.3f}")

    if len(np.unique(y_test)) > 1:
        print(f"ROC-AUC: {roc_auc_score(y_test, probabilities):.3f}")

    print(f"NDCG@5: {compute_ndcg_at_k(y_test.values, probabilities):.3f}")

    print("\nConfusion matrix (rows = actual, columns = predicted):")
    print(confusion_matrix(y_test, predictions, labels=[0, 1]))

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=["Not a match", "Match"],
            zero_division=0,
        )
    )


def main():
    """Run model evaluation on synthetic data."""
    from ml.experiment import make_synthetic_records

    dataset = build_dataset(make_synthetic_records())
    x = dataset.drop(columns=[TARGET_COLUMN])
    y = dataset[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = create_train_test_split(dataset)

    print(f"Total examples: {len(dataset)}")
    print(f"Training examples: {len(x_train)}")
    print(f"Held-out test examples: {len(x_test)}")
    print(f"Training positive examples: {int(y_train.sum())}")
    print(f"Test positive examples: {int(y_test.sum())}")

    models = [
        (
            "Dummy baseline",
            DummyClassifier(strategy="most_frequent"),
        ),
        (
            "Balanced logistic regression",
            Pipeline([
                ("preprocessor", build_preprocessor()),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=1000,
                        class_weight="balanced",
                    ),
                ),
            ]),
        ),
        (
            "Random Forest",
            Pipeline([
                ("preprocessor", build_preprocessor()),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=200,
                        class_weight="balanced",
                        random_state=42,
                    ),
                ),
            ]),
        ),
    ]

    for name, model in models:
        evaluate_model(name, model, x_train, x_test, y_train, y_test)


if __name__ == "__main__":
    main()