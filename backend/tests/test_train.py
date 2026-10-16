import pytest
import pandas as pd
from backend.ml.train import train_model

def make_records():
    records = []

    for i in range(20):
        matches = i % 2 == 0

        records.append({
            "category": "regulation" if matches else "connection",
            "difficulty": "low" if matches else "medium",
            "energy_required": "low" if matches else "medium",
            "social_required": not matches,
            "energy_preference": "low" if matches else "medium",
            "recently_seen": False,
            "preference_match": int(matches),
        })

    return records

def test_model_trains_and_predicts():
    model, metrics = train_model(make_records())

    predictions = model.predict(pd.DataFrame([
        {
            "category": "regulation",
            "difficulty": "low",
            "energy_required": "low",
            "social_required": False,
            "energy_preference": "low",
            "recently_seen": False,
        }
    ]))

    assert len(predictions) == 1
    assert predictions[0] in (0,1)
    assert 0 <= metrics["accuracy"] <= 1
    assert 0 <= metrics["balanced_accuracy"] <= 1

def test_training_requires_both_classes():
    records = make_records()

    for record in records:
        record["preference_match"] = 1

    with pytest.raises(ValueError, match="both target classes"):
        train_model(records)


def test_training_rejects_too_few_examples_per_class():
    records = make_records()

    for record in records:
        record['preference_match'] = 0

    records[0]["preference_match"] = 1

    with pytest.raises(ValueError, match='at least two examples'):
        train_model(records)