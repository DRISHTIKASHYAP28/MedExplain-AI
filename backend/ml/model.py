from pathlib import Path

import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from ml.feature_engineering import create_features


BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    BASE_DIR /
    "datasets" /
    "medical_results.csv"
)

MODEL_DIR = (
    BASE_DIR /
    "models"
)

MODEL_PATH = (
    MODEL_DIR /
    "medical_result_classifier.pkl"
)


def train_model():

    print("Loading dataset...")

    df = pd.read_csv(DATASET_PATH)

    print(
        f"Loaded {len(df)} synthetic records."
    )

    X = create_features(df)

    y = df["status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("Training Random Forest model...")

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=6
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print()
    print("=" * 50)
    print("MODEL EVALUATION")
    print("=" * 50)

    print(
        f"Accuracy: {accuracy:.2%}"
    )

    print()
    print(
        classification_report(
            y_test,
            predictions
        )
    )

    MODEL_DIR.mkdir(
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    print("=" * 50)

    print(
        f"Model saved to:\n{MODEL_PATH}"
    )

    print("=" * 50)


if __name__ == "__main__":
    train_model()