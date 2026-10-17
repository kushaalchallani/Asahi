from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, classification_report, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from backend.ml.dataset import build_dataset, TARGET_COLUMN
from backend.ml.experiment import make_synthetic_records
from backend.ml.preprocessing import build_preprocessor


def evaluate_model(name, model, x_train, x_test, y_train, y_test):
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    print(f"\n--- {name} ---")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(
        "Balanced accuracy: "
        f"{balanced_accuracy_score(y_test, predictions):.3f}"
    )
    print(f"Precision: {precision_score(y_test, predictions, zero_division=0):.3f}")
    print(f"Recall: {recall_score(y_test, predictions, zero_division=0):.3f}")

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
    dataset = build_dataset(make_synthetic_records())
    x = dataset.drop(columns=[TARGET_COLUMN])
    y = dataset[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

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
        evaluate_model(
            name,
            model,
            x_train,
            x_test,
            y_train,
            y_test,
        )


if __name__ == "__main__":
    main()
