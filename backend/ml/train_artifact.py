from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from backend.ml.dataset import build_dataset, TARGET_COLUMN
from backend.ml.experiment import make_synthetic_records
from backend.ml.preprocessing import build_preprocessor
from backend.ml.train import save_model
from backend.dependencies.database import SessionLocal
from backend.ml.export_feedback_dataset import export_feedback_dataset


def main() -> None:
    artifact_dir = Path(__file__).parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    db = SessionLocal()

    try:
        real_records = export_feedback_dataset(db)
    finally:
        db.close()

    has_both_classes = (
        len(real_records) >= 30
        and {record[TARGET_COLUMN] for record in real_records} == {0, 1}
    )

    if has_both_classes:
        dataset = build_dataset(real_records)
        data_source = "real user feedback"
    else:
        dataset = build_dataset(make_synthetic_records())
        data_source = "synthetic fallback"

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

    print(f"Training data source: {data_source}")
    print(f"Training examples: {len(dataset)}")
    print(f"Positive examples: {int(y.sum())}")
    print(f"Negative examples: {int((y == 0).sum())}")

    if data_source == "synthetic fallback":
        print("Real feedback is insufficient; synthetic data was used.")
        print("Training results do not establish real-world performance.")


if __name__ == "__main__":
    main()
