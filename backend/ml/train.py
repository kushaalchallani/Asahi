"""
ML training pipeline for mission recommendation model.

Supports Logistic Regression (primary), Random Forest (comparison),
and Dummy Classifier (baseline).
"""
import joblib
import numpy as np
from typing import Optional, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from ml.dataset import build_dataset, TARGET_COLUMN, FEATURE_COLUMNS
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


def train_model(
    records: list[dict],
    test_size: float = 0.25,
    random_state: int = 42,
    class_weight: Optional[str] = "balanced"
) -> Tuple[Pipeline, dict[str, float | int]]:
    """
    Train the mission recommendation model.

    Returns the trained pipeline and evaluation metrics.
    Includes metrics for classification and ranking quality.
    """
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")

    dataset = build_dataset(records)

    x = dataset.drop(columns=[TARGET_COLUMN])
    y = dataset[TARGET_COLUMN].values

    if len(np.unique(y)) != 2:
        raise ValueError("Training requires examples from both target classes.")

    if np.min(np.bincount(y)) < 2:
        raise ValueError("Each target class needs at least two examples.")

    # Stratified split to maintain class balance
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Baseline: most frequent class
    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(x_train, y_train)
    baseline_predictions = baseline.predict(x_test)

    # Primary model: Logistic Regression
    model = Pipeline([
        ("preprocessor", build_preprocessor()),
        ("classifier", LogisticRegression(
            max_iter=1000,
            class_weight=class_weight,
            random_state=random_state
        ))
    ])

    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]

    # Compute metrics
    baseline_accuracy = accuracy_score(y_test, baseline_predictions)
    baseline_balanced_accuracy = balanced_accuracy_score(y_test, baseline_predictions)

    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_test, predictions, labels=[0, 1]).ravel()

    # NDCG@5 for ranking quality
    ndcg_at_5 = compute_ndcg_at_k(y_test, probabilities, k=5)

    metrics: dict[str, float | int] = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1_score": float(f1_score(y_test, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, probabilities) if len(np.unique(y_test)) > 1 else 0.5),
        "ndcg_at_5": float(ndcg_at_5),
        "baseline_accuracy": float(baseline_accuracy),
        "baseline_balanced_accuracy": float(baseline_balanced_accuracy),
        "test_class_0_count": int((y_test == 0).sum()),
        "test_class_1_count": int((y_test == 1).sum()),
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
    }

    return model, metrics


def save_model(model: Pipeline, path) -> None:
    """Serialize the trained model to disk."""
    joblib.dump(model, path)


def load_model(path) -> Optional[Pipeline]:
    """Load a trained model from disk. Returns None if loading fails."""
    try:
        return joblib.load(path)
    except (OSError, ValueError, ImportError, FileNotFoundError):
        return None


def train_comparison_models(
    records: list[dict],
    test_size: float = 0.25,
    random_state: int = 42
) -> dict[str, Tuple[Pipeline, dict]]:
    """
    Train multiple models for comparison.

    Returns a dictionary mapping model names to (model, metrics) tuples.
    """
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")

    dataset = build_dataset(records)
    x = dataset.drop(columns=[TARGET_COLUMN])
    y = dataset[TARGET_COLUMN].values

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_state, stratify=y
    )

    models = {
        "dummy_most_frequent": DummyClassifier(strategy="most_frequent"),
        "logistic_regression": Pipeline([
            ("preprocessor", build_preprocessor()),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=random_state))
        ]),
        "random_forest": Pipeline([
            ("preprocessor", build_preprocessor()),
            ("classifier", RandomForestClassifier(
                n_estimators=200,
                class_weight="balanced",
                random_state=random_state
            ))
        ]),
        "logistic_balanced": Pipeline([
            ("preprocessor", build_preprocessor()),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=random_state))
        ]),
    }

    results = {}

    for name, model in models.items():
        if name.startswith("dummy"):
            model.fit(x_train, y_train)
        else:
            model.fit(x_train, y_train)

        predictions = model.predict(x_test)
        probabilities = model.predict_proba(x_test)[:, 1] if hasattr(model, 'predict_proba') else np.zeros(len(y_test))

        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "balanced_accuracy": balanced_accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, zero_division=0),
            "recall": recall_score(y_test, predictions, zero_division=0),
            "f1_score": f1_score(y_test, predictions, zero_division=0),
            "ndcg_at_5": compute_ndcg_at_k(y_test, probabilities, k=5),
            "baseline": name == "dummy_most_frequent",
        }

        results[name] = (model, metrics)

    return results


def get_feature_importance(model: Pipeline) -> dict[str, float]:
    """
    Extract feature importance from a trained model.

    For tree-based models, returns feature_importances_.
    For linear models, returns absolute coefficient values.
    """
    classifier = model.named_steps["classifier"]
    preprocessor = model.named_steps["preprocessor"]

    feature_names = preprocessor.get_feature_names_out()

    if hasattr(classifier, "feature_importances_"):
        importances = classifier.feature_importances_
    elif hasattr(classifier, "coef_"):
        importances = np.abs(classifier.coef_[0])
    else:
        return {}

    return dict(zip(feature_names, importances.flatten().tolist()))