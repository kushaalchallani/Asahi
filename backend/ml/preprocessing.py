from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

CATEGORICAL_FEATURES = [
    "category",
    "difficulty",
    "energy_required",
    "energy_preference"
]

BOOLEAN_FEATURES = [
    "social_required",
    "recently_seen"
]

def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES
            ),
            (
                "boolean",
                "passthrough",
                BOOLEAN_FEATURES,
            )
        ],
        remainder="drop",
        verbose_feature_names_out=False
    )