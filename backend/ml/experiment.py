"""
Experimentation module for comparing ML models and training data strategies.

Includes:
- Synthetic data generation
- Model comparison (Logistic Regression, Random Forest, Dummy)
- Feature importance analysis
- Threshold tuning
"""
from itertools import product
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    make_scorer,
    precision_score,
    recall_score,
    balanced_accuracy_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from ml.dataset import build_dataset, TARGET_COLUMN
from ml.preprocessing import build_preprocessor


def make_synthetic_records() -> list[dict]:
    """
    Generate synthetic training records for model development.

    Uses a heuristic that matches user preference when:
    - Energy requirement matches user's energy preference
    - Difficulty is low
    - Mission not recently seen
    - No social requirement

    Returns list of records with all required features.
    """
    records = []

    categories = ['regulation', 'environment', 'reflection', 'self-care', 'connection']
    difficulties = ['low', 'medium']
    energy_levels = ['low', 'medium', 'high']
    social_options = [False, True]
    recently_seen_options = [False, True]

    for (
        category,
        difficulty,
        energy_required,
        energy_preference,
        social_required,
        recently_seen,
    ) in product(
        categories,
        difficulties,
        energy_levels,
        energy_levels,
        social_options,
        recently_seen_options,
    ):
        preference_match = int(
            energy_required == energy_preference
            and difficulty == "low"
            and not recently_seen
            and not social_required
        )

        records.append({
            "category": category,
            "difficulty": difficulty,
            "energy_required": energy_required,
            "social_required": social_required,
            "energy_preference": energy_preference,
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


def evaluate_model(
    name: str,
    model,
    x,
    y,
    cross_validation: StratifiedKFold,
) -> dict[str | float]:
    """Evaluate a model using cross-validation and print results."""
    scoring = {
        "accuracy": "accuracy",
        "balanced_accuracy": "balanced_accuracy",
        "precision": make_scorer(precision_score, zero_division=0),
        "recall": "recall",
        "f1_score": "f1",
        "roc_auc": "roc_auc",
    }

    results = cross_validate(model, x, y, cv=cross_validation, scoring=scoring, return_train_score=False)
    metrics = {}

    print(f"\n--- {name} ---")

    for metric in scoring:
        scores = results[f"test_{metric}"]
        print(f"{metric}: {scores.mean():.3f} ± {scores.std():.3f}")

    return metrics


def evaluate_ndcg(
    model,
    x,
    y,
    cross_validation: StratifiedKFold,
) -> float:
    """Evaluate ranking quality using NDCG@5."""
    import numpy as np

    ndcg_scores = []

    for train_idx, test_idx in cross_validation.split(x, y):
        x_train, x_test = x.iloc[train_idx], x.iloc[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model.fit(x_train, y_train)
        probabilities = model.predict_proba(x_test)[:, 1]

        # Compute NDCG@5
        k = 5
        n = len(y_test)

        # Sort by predicted scores
        indices = np.argsort(probabilities)[::-1]
        ranks = np.empty_like(indices)
        ranks[indices] = np.arange(len(indices)) + 1

        # DCG
        dcg = np.sum((2 ** y_test[indices[:min(k, n)]] - 1) / np.log2(ranks[:min(k, n)] + 1))

        # Ideal DCG
        ideal_indices = np.argsort(y_test)[::-1]
        ideal_dcg = np.sum((2 ** y_test[ideal_indices[:min(k, n)]] - 1) / np.log2(ranks[:min(k, n)] + 1))

        if ideal_dcg > 0:
            ndcg_scores.append(dcg / ideal_dcg)

    if ndcg_scores:
        print(f"NDCG@5: {np.mean(ndcg_scores):.3f} ± {np.std(ndcg_scores):.3f}")

    return ndcg_scores[0] if ndcg_scores else 0.0


def evaluate_thresholds(x, y) -> None:
    """Compare model performance across different classification thresholds."""
    cross_validation = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    model = Pipeline([
        ('preprocessor', build_preprocessor()),
        ('classifier', LogisticRegression(max_iter=1000, class_weight='balanced'))
    ])

    probabilities = cross_val_predict(model, x, y, cv=cross_validation, method='predict_proba')[:, 1]

    print("\n--- Threshold comparison ---")
    print("Threshold | Precision | Recall | Balanced accuracy")

    for threshold in [0.30, 0.40, 0.50, 0.60, 0.70]:
        predictions = (probabilities >= threshold).astype(int)

        precision = precision_score(y, predictions, zero_division=0)
        recall = recall_score(y, predictions, zero_division=0)
        balanced_accuracy = balanced_accuracy_score(y, predictions)

        print(
            f"{threshold:9.2f} | "
            f"{precision:9.3f} | "
            f"{recall:6.3f} | "
            f"{balanced_accuracy:18.3f}"
        )


def inspect_feature_importance(model, x, y) -> None:
    """Print feature importance for tree-based models."""
    model.fit(x, y)

    classifier = model.named_steps["classifier"]
    preprocessor = model.named_steps['preprocessor']

    feature_names = preprocessor.get_feature_names_out()

    if hasattr(classifier, 'feature_importances_'):
        importances = classifier.feature_importances_
    elif hasattr(classifier, 'coef_'):
        importances = np.abs(classifier.coef_[0])
    else:
        print("Model has no feature importance attribute")
        return

    results = sorted(zip(feature_names, importances), key=lambda item: item[1], reverse=True)

    print("\n--- Feature Importance ---")
    for feature, importance in results:
        print(f"{feature:35s} {importance:.4f}")


def main() -> None:
    """Run comprehensive model experiments."""
    dataset = build_dataset(make_synthetic_records())

    x = dataset.drop(columns=[TARGET_COLUMN])
    y = dataset[TARGET_COLUMN]

    cross_validation = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    print(f"Synthetic examples: {len(dataset)}")
    print(f"Positive examples: {int(y.sum())}")
    print(f"Negative examples: {int((y == 0).sum())}")
    print("\nUsing 5-fold stratified cross-validation.")
    print("Scores show mean across folds ± standard deviation.")

    models = [
        (
            "Dummy baseline (most_frequent)",
            DummyClassifier(strategy='most_frequent'),
        ),
        (
            "Logistic Regression (standard)",
            Pipeline([
                ('preprocessor', build_preprocessor()),
                ("classifier", LogisticRegression(max_iter=1000, class_weight=None))
            ])
        ),
        (
            "Logistic Regression (balanced)",
            Pipeline([
                ("preprocessor", build_preprocessor()),
                ("classifier", LogisticRegression(max_iter=1000, class_weight='balanced'))
            ])
        ),
        (
            "Random Forest",
            Pipeline([
                ("preprocessor", build_preprocessor()),
                ("classifier", RandomForestClassifier(
                    n_estimators=200,
                    class_weight='balanced',
                    random_state=42
                ))
            ])
        ),
    ]

    print("\n" + "=" * 70)
    print("Model Comparison")
    print("=" * 70)

    for name, model in models:
        evaluate_model(name, model, x, y, cross_validation)
        if name.startswith("Logistic") or name == "Random Forest":
            evaluate_ndcg(model, x, y, cross_validation)

    print("\n" + "=" * 70)
    print("Threshold Analysis")
    print("=" * 70)
    evaluate_thresholds(x, y)

    print("\n" + "=" * 70)
    print("Feature Importance (Random Forest)")
    print("=" * 70)
    random_forest = next(
        model for name, model in models
        if name == "Random Forest"
    )
    inspect_feature_importance(random_forest, x, y)


if __name__ == "__main__":
    main()