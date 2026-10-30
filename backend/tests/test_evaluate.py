import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline
from ml.evaluate import evaluate_model, create_train_test_split
from ml.preprocessing import build_preprocessor
from ml.dataset import build_dataset
from ml.experiment import make_synthetic_records 

def test_evaluate_mode_prints_metrics_and_confusion_matrix(capsys):
    x_train = pd.DataFrame({
        "category": ["regulation", "connection", "reflection", "regulation"],
        "difficulty": ["low", "medium", "low", "medium"],
        "energy_required": ["low", "medium", "high", "low"],
        "social_required": [False, True, False, True],
        "energy_preference": ["low", "medium", "high", "low"],
        "recently_seen": [False, True, False, True],
    })
    y_train = np.array([0,0,1,1])
    x_test = x_train.iloc[:2].copy()
    y_test = np.array([0,1])

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
    dataset = build_dataset(make_synthetic_records())

    first = create_train_test_split(dataset)
    second = create_train_test_split(dataset)

    for first_part, second_part in zip(first, second):
        assert first_part.equals(second_part)


def test_train_test_split_preserves_both_classes():
    dataset = build_dataset(make_synthetic_records())

    x_train, x_test, y_train, y_test = create_train_test_split(dataset)

    assert set(y_train.unique()) == {0, 1}
    assert set(y_test.unique()) == {0, 1}
    assert len(x_train) + len(x_test) == len(dataset)
    assert len(x_test) == 54
