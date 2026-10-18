import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, confusion_matrix, precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyClassifier
from backend.ml.dataset import build_dataset, TARGET_COLUMN
from backend.ml.preprocessing import build_preprocessor

def train_model(records: list[dict], test_size: float = 0.25, random_state: int = 42, class_weight: str | None = None) -> tuple[Pipeline, dict[str, float | int]]:
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")

    dataset = build_dataset(records)

    x = dataset.drop(columns=[TARGET_COLUMN])
    y = dataset[TARGET_COLUMN]

    if y.nunique() != 2:
        raise ValueError("Training requires examples from both target classes.")

    if y.value_counts().min() < 2:
        raise ValueError("Each target class needs at least two examples.")

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state, stratify=y)

    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(x_train, y_train)
    baseline_predictions = baseline.predict(x_test)

    model = Pipeline([
        ("preprocessor", build_preprocessor()),
        ("classifier", LogisticRegression(max_iter=1000, class_weight=class_weight))
    ])

    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    baseline_accuracy = accuracy_score(y_test, baseline_predictions)
    baseline_balanced_accuracy = balanced_accuracy_score(y_test, baseline_predictions)

    tn, fp, fn, tp = confusion_matrix(y_test, predictions, labels=[0, 1]).ravel()

    metrics: dict[str, float | int] = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "balanced_accuracy": float(
            balanced_accuracy_score(y_test, predictions)
        ),
        "precision": float(
            precision_score(y_test, predictions, zero_division=0)
        ),
        "recall": float(
            recall_score(y_test, predictions, zero_division=0)
        ),
        "baseline_accuracy": float(baseline_accuracy),
        "baseline_balanced_accuracy": float(
            baseline_balanced_accuracy
        ),
        "test_class_0_count": int((y_test == 0).sum()),
        "test_class_1_count": int((y_test == 1).sum()),
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
    }

    return model, metrics

def save_model(model, path):
    joblib.dump(model, path)


def load_model(path):
    return joblib.load(path)