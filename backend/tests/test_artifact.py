
import pandas as pd

from backend.ml.train import load_model


def main() -> None:
    model_path = "backend/ml/artifacts/mission_recommender.joblib"
    model = load_model(model_path)

    sample = pd.DataFrame([
        {
            "category": "regulation",
            "difficulty": "low",
            "energy_required": "low",
            "social_required": False,
            "energy_preference": "low",
            "recently_seen": False,
        },
        {
            "category": "connection",
            "difficulty": "medium",
            "energy_required": "high",
            "social_required": True,
            "energy_preference": "low",
            "recently_seen": True,
        },
    ])

    predictions = model.predict(sample)
    probabilities = model.predict_proba(sample)[:, 1]

    for index, (prediction, probability) in enumerate(
        zip(predictions, probabilities), start=1
    ):
        print(f"Sample {index}:")
        print(f"  Predicted preference match: {int(prediction)}")
        print(f"  Model score: {probability:.3f}")


if __name__ == "__main__":
    main()