from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from backend.ml.dataset import build_dataset, TARGET_COLUMN
from backend.ml.experiment import make_synthetic_records
from backend.ml.preprocessing import build_preprocessor
from backend.ml.train import save_model


def main() -> None:
    artifact_dir = Path(__file__).parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    dataset = build_dataset(make_synthetic_records())
    X = dataset.drop(columns=[TARGET_COLUMN])
    y = dataset[TARGET_COLUMN]

    model = Pipeline([
        ("preprocessor", build_preprocessor()),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=42,
        )),
    ])

    model.fit(X, y)

    artifact_path = artifact_dir / "mission_recommender.joblib"
    save_model(model, artifact_path)

    print(f"Model saved to: {artifact_path}")
    print(f"Training examples: {len(dataset)}")
    print(f"Positive examples: {int(y.sum())}")
    print(f"Negative examples: {int((y == 0).sum())}")
    print("Note: This model was trained on synthetic data.")
    print("Its training results do not establish real-world performance.")


if __name__ == "__main__":
    main()
