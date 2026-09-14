import pandas as pd


def create_features(dataframe):
    """
    Convert laboratory results into numerical ML features.

    This model is designed for educational classification of
    laboratory results as LOW, NORMAL, or HIGH.

    It is NOT a diagnostic model.
    """

    df = dataframe.copy()

    # Convert numerical columns
    numerical_columns = [
        "value",
        "reference_low",
        "reference_high"
    ]

    for column in numerical_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Avoid division by zero
    reference_width = (
        df["reference_high"] -
        df["reference_low"]
    )

    reference_width = reference_width.replace(
        0,
        1
    )

    # Distance from the middle of the reference range
    reference_midpoint = (
        df["reference_low"] +
        df["reference_high"]
    ) / 2

    df["relative_position"] = (
        (df["value"] - reference_midpoint)
        / reference_width
    )

    # Distance below/above range
    df["distance_from_low"] = (
        df["value"] -
        df["reference_low"]
    )

    df["distance_from_high"] = (
        df["value"] -
        df["reference_high"]
    )

    features = df[
        [
            "value",
            "reference_low",
            "reference_high",
            "relative_position",
            "distance_from_low",
            "distance_from_high"
        ]
    ]

    return features