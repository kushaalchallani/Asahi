"""
Script to train and save the mission recommendation model artifact

Attempts to load real user feedback data
Falls back to synthetic data if insufficient
Trains a LogisticRegression model (primary) with RandomForest comparison
Saves the trained model to artifacts/mission_recommender.joblib

Use:
    python -m backend.ml.train_artifact
    or
    python backend/ml/train_artifact.py
"""
from pathlib import Path
from datetime import datetime
from ml.dataset import build_dataset, TARGET_COLUMN
from ml.experiment import make_synthetic_records
from ml.preprocessing import build_preprocessor
from ml.train import save_model, train_model, train_comparison_models, get_feature_importance
from ml.export_feedback_dataset import export_feedback_dataset, has_sufficient_real_data
from dependencies.database import SessionLocal
import json


def main() -> None:
    """Train and save the mission recommendation model."""
    artifact_dir = Path(__file__).parent / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    db = SessionLocal()

    try:
        real_records = export_feedback_dataset(db)
    finally:
        db.close()

    use_synthetic = not has_sufficient_real_data(real_records)

    if use_synthetic:
        print("Using synthetic training data (insufficient real feedback).")
        dataset = build_dataset(make_synthetic_records())
        data_source = "synthetic"
        print("WARNING: Model trained on synthetic data. Results are experimental.")
    else:
        dataset = build_dataset(real_records)
        data_source = "real"
        print(f"Using real user feedback data ({len(real_records)} records).")

    X = dataset.drop(columns=[TARGET_COLUMN])
    y = dataset[TARGET_COLUMN]

    print(f"\nTraining data: {len(dataset)} examples")
    print(f"  Positive (helpful): {int(y.sum())}")
    print(f"  Negative (not_for_me): {int((y == 0).sum())}")

    # Train primary model
    model, metrics = train_model(real_records if data_source == "real" else make_synthetic_records())

    # Save model
    artifact_path = artifact_dir / "mission_recommender.joblib"
    save_model(model, artifact_path)

    print(f"\nModel saved to: {artifact_path}")

    # Print metrics
    print("\n=== Training Metrics ===")
    print(f"Accuracy: {metrics['accuracy']:.3f}")
    print(f"Balanced Accuracy: {metrics['balanced_accuracy']:.3f}")
    print(f"Precision: {metrics['precision']:.3f}")
    print(f"Recall: {metrics['recall']:.3f}")
    print(f"F1 Score: {metrics['f1_score']:.3f}")
    print(f"ROC-AUC: {metrics['roc_auc']:.3f}")
    print(f"NDCG@5: {metrics['ndcg_at_5']:.3f}")

    # Compare models if we have real data
    if data_source == "real":
        print("\n=== Model Comparison ===")
        results = train_comparison_models(real_records)

        print(f"{'Model':<25} {'Acc':>6} {'BalAcc':>8} {'Precision':>9} {'Recall':>8} {'NDCG@5':>8}")
        print("-" * 70)

        for name, (trained_model, model_metrics) in results.items():
            print(
                f"{name:<25} "
                f"{model_metrics['accuracy']:>6.3f} "
                f"{model_metrics['balanced_accuracy']:>8.3f} "
                f"{model_metrics['precision']:>9.3f} "
                f"{model_metrics['recall']:>8.3f} "
                f"{model_metrics['ndcg_at_5']:>8.3f}"
            )

    # Print feature importance
    print("\n=== Feature Importance ===")
    importance = get_feature_importance(model)
    for feature, score in sorted(importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {feature}: {score:.4f}")

    # Save training metadata for auditing
    metadata = {
        "trained_at": datetime.now().isoformat(),
        "data_source": data_source,
        "training_examples": len(dataset),
        "positive_examples": int(y.sum()),
        "negative_examples": int((y == 0).sum()),
        "metrics": metrics,
    }

    metadata_path = artifact_dir / "training_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nTraining metadata saved to: {metadata_path}")


if __name__ == "__main__":
    main()