import pandas as pd

FEATURE_COLUMNS = [
    "category",
    "difficulty",
    "energy_required",
    "social_required",
    "energy_preference",
    "recently_seen"
]

TARGET_COLUMN="preference_match"

REQUIRED_COLUMN = FEATURE_COLUMNS + [TARGET_COLUMN]

def build_dataset(records: list[dict]) -> pd.DataFrame:
    if not records:
        raise ValueError("The dataset cannot be empty")

    dataset = pd.DataFrame(records)

    missing_columns = set(REQUIRED_COLUMN) - set(dataset.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    dataset = dataset[REQUIRED_COLUMN].copy()

    if dataset.isnull().any().any():
        raise ValueError("The dataset cannot contain missing values")

    if not dataset[TARGET_COLUMN].isin([0,1]).all():
        raise ValueError("preference_match must contain only 0 or 1")

    return dataset