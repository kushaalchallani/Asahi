from backend.ml.experiment import make_synthetic_records
from backend.ml.train import train_model

def main() -> None:
    records = make_synthetic_records()
    model, metrics = train_model(records)

    preprocessor = model.named_steps['preprocessor']
    classifier = model.named_steps['classifier']

    feature_names = preprocessor.get_feature_names_out()
    coefficients = classifier.coef_[0]
    ranked_features = sorted(zip(feature_names, coefficients), key=lambda item: abs(item[1]), reverse=True)

    print("Evaluation metrics:", metrics)
    print("\n Feature coefficients (largest magnitude first):")

    for feature, coefficient in ranked_features:
        print(f"{feature}: {coefficient:.3f}")

if __name__ == "__main__":
    main()