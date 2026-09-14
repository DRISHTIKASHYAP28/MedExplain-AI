from pathlib import Path

import joblib
import pandas as pd

from ml.feature_engineering import create_features


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    BASE_DIR /
    "models" /
    "medical_result_classifier.pkl"
)


_model = None


def load_model():

    global _model

    if _model is None:

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"ML model not found: {MODEL_PATH}"
            )

        _model = joblib.load(
            MODEL_PATH
        )

    return _model


def predict_result(
    test_name,
    value,
    reference_low,
    reference_high
):
    """
    Predict LOW, NORMAL, or HIGH
    for a laboratory result.

    Educational classification only.
    """

    model = load_model()

    data = pd.DataFrame(
        [
            {
                "test_name": test_name,
                "value": value,
                "reference_low": reference_low,
                "reference_high": reference_high
            }
        ]
    )

    features = create_features(
        data.assign(
            status="NORMAL"
        )
    )

    prediction = model.predict(
        features
    )[0]

    confidence = None

    if hasattr(
        model,
        "predict_proba"
    ):

        probabilities = (
            model.predict_proba(features)[0]
        )

        confidence = float(
            max(probabilities)
        )

    return {
        "test": test_name,
        "prediction": prediction,
        "confidence": confidence
    }