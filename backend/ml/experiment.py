from backend.ml.train import train_model

def make_synthetic_records() -> list[dict]:
    records = []

    categories = ['regulation', 'connection', 'reflection']
    difficulties = ['low', 'medium']
    energy_levels = ['low', 'medium', 'high']

    for i in range(120):
        category = categories[i % len(categories)]
        difficulty = difficulties[i % len(difficulties)]
        energy_required = energy_levels[i % len(energy_levels)]
        energy_preference = energy_levels[(i // 2) % len(energy_levels)]

        social_required = category == 'connection'
        recently_seen = i % 4 == 0

        preference_match = int(
            energy_required == energy_preference
            and difficulty == 'low'
            and not recently_seen
        )

        records.append({
            "category": category,
            "difficulty": difficulty,
            "energy_required": energy_required,
            "social_required": social_required,
            "energy_preference": energy_preference,
            "recently_seen": recently_seen,
            "preference_match": preference_match,
        })

    return records

def main() -> None:
    records = make_synthetic_records()
    model, metrics = train_model(records)

    print(f"Training examples: {len(records)}")
    print("Evaluation Metrics:")

    for metric, value in metrics.items():
        print(f" {metric}: {value:.3f}")

if __name__ == "__main__":
    main()