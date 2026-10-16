import pytest
from backend.ml.dataset import build_dataset

def test_build_dataset_returns_valid_dataframe():
    records = [
        {
        "category": "regulation",
        "difficulty": "low",
        "energy_required": "low",
        "social_required": False,
        "energy_preference": "low",
        "recently_seen": False,
        "preference_match": 1,
        }
    ]

    dataset = build_dataset(records)

    assert len(dataset) == 1
    assert dataset.loc[0, "preference_match"] == 1

def test_rejects_empty_dataset():
    with pytest.raises(ValueError, match="cannot be empty"):
        build_dataset([])

def test_reject_invalid_target():
    records = [
        {
            "category": "regulation",
            "difficulty": "low",
            "energy_required": "low",
            "social_required": False,
            "energy_preference": "low",
            "recently_seen": False,
            "preference_match": 2,   
        }
    ]

    with pytest.raises(ValueError, match="only 0 or 1"):
        build_dataset(records)