from itertools import product
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, precision_score, recall_score, balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from ml.dataset import build_dataset, TARGET_COLUMN
from ml.preprocessing import build_preprocessor

def make_synthetic_records() -> list[dict]:
    records = []

    categories = ['regulation', 'connection', 'reflection']
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
            "preference_match": preference_match,
        })

    return records

def evaluate_model(name: str, model, x, y, cross_validation: StratifiedKFold) -> dict[str | float]:
    scoring = {
        "accuracy": "accuracy",
        "balanced_accuracy": "balanced_accuracy",
        "precision": make_scorer(
            precision_score,
            zero_division=0,
        ),
        "recall": "recall",
    }

    results = cross_validate(model, x, y, cv=cross_validation, scoring=scoring, return_train_score=False)
    metrics = {}

    print(f"\n--- {name} ---")

    for metric in scoring:
        scores = results[f"test_{metric}"]
        print(f"{metric}: {scores.mean():.3f} ± {scores.std():.3f}")

    return metrics

def evaluate_thresholds(x, y) -> None:
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

        precision = precision_score(
            y,
            predictions,
            zero_division=0,
        )
        recall = recall_score(y, predictions, zero_division=0)
        balanced_accuracy = balanced_accuracy_score(y, predictions)

        print(
            f"{threshold:9.2f} | "
            f"{precision:9.3f} | "
            f"{recall:6.3f} | "
            f"{balanced_accuracy:18.3f}"
        )

def inspect_feature_importance(model, x, y) -> None:
    model.fit(x, y)

    classifier =  model.named_steps["classifier"]
    preprocessor = model.named_steps['preprocessor']

    feature_names = preprocessor.get_feature_names_out()
    importances = classifier.feature_importances_

    results = sorted(zip(feature_names, importances), key=lambda item: item[1], reverse=True)

    print("\n--- Random Forest feature importance ---")
    for feature, importance in results:
        print(f"{feature:25s} {importance:.4f}")

def main() -> None:
    dataset = build_dataset(make_synthetic_records())

    x=dataset.drop(columns=[TARGET_COLUMN])
    y=dataset[TARGET_COLUMN]

    cross_validation = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


    print(f"Synthetic examples: {len(dataset)}")
    print(f"Positive examples: {int(y.sum())}")
    print(f"Negative examples: {int((y == 0).sum())}")
    print("\nUsing 5-fold stratified cross-validation.")
    print("Scores show mean across folds ± standard deviation.")

    baseline = DummyClassifier(strategy='most_frequent')

    evaluate_model('Dummy baseline', DummyClassifier(strategy='most_frequent'), x, y, cross_validation)

    
    models = [
        (
            "Standard logistic regression",
            Pipeline([
                ('preprocessor', build_preprocessor()),
                ("classifier", LogisticRegression(max_iter=1000, class_weight=None))
            ])
        ),
        (
            "Balanced Logistic Regression",
            Pipeline([
                ("preprocessor", build_preprocessor()),
                ("classifier", LogisticRegression(max_iter=1000, class_weight='balanced'))
            ])
        ),
        (
            "Random Forest",
            Pipeline([
                ("preprocessor", build_preprocessor()),
                ("classifier", RandomForestClassifier(n_estimators=200, class_weight='balanced',random_state=42))
            ])
        )
    ]

    for name, model in models:
        evaluate_model(name, model, x, y, cross_validation)

    random_forest = next(
        model for name, model in models
        if name == "Random Forest"
    )
    inspect_feature_importance(random_forest, x, y)

    evaluate_thresholds(x,y)

if __name__ == "__main__":
    main()