from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from backend.ml.dataset import build_dataset, TARGET_COLUMN
from backend.ml.preprocessing import build_preprocessor

def train_model(records: list[dict], test_size: float = 0.25, random_state: int = 42) -> tuple[Pipeline, dict[str, float]]:
    dataset = build_dataset(records)

    x = dataset.drop(columns=[TARGET_COLUMN])
    y = dataset[TARGET_COLUMN]

    if y.nunique() != 2:
        raise ValueError("Training requires examples from both target classes.")

    if y.value_counts().min() < 2:
        raise ValueError("Each target class needs at least two examples.")

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state, stratify=y)

    model = Pipeline([
        ("preprocessor", build_preprocessor()),
        ("classifier", LogisticRegression(max_iter=1000))
    ])

    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(y_test, predictions))
    }

    return model, metrics