import pandas as pd
from ml.dataset import build_dataset
from ml.preprocessing import build_preprocessor

def test_preprocessor_produces_numeric_features():
    records = [
        {
            "category": "regulation",
            "difficulty": "low",
            "energy_required": "low",
            "social_required": False,
            "energy_preference": "low",
            "recently_seen": False,
            "preference_match": 1,
        },
        {
            "category": "connection",
            "difficulty": "medium",
            "energy_required": "medium",
            "social_required": True,
            "energy_preference": "medium",
            "recently_seen": True,
            "preference_match": 0,
        },
    ]

    dataset = build_dataset(records)
    X = dataset.drop(columns=['preference_match'])

    preprocessor = build_preprocessor()
    transformed = preprocessor.fit_transform(X)

    assert transformed.shape[0] == 2
    assert transformed.shape[1] > 0
    assert pd.DataFrame(transformed).select_dtypes(
        include="number"
    ).shape == pd.DataFrame(transformed).shape


def test_unknown_categories_do_not_crash():
    training = pd.DataFrame([
        {
            "category": "regulation",
            "difficulty": "low",
            "energy_required": "low",
            "social_required": False,
            "energy_preference": "low",
            "recently_seen": False,
        }
    ])

    unseen = pd.DataFrame([
        {
            "category": "new_category",
            "difficulty": "low",
            "energy_required": "low",
            "social_required": False,
            "energy_preference": "low",
            "recently_seen": False,
        }
    ])

    preprocessor = build_preprocessor()
    preprocessor.fit(training)
    transformed = preprocessor.transform(unseen)

    assert transformed.shape[0] == 1