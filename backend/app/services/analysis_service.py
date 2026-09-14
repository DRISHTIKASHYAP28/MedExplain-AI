from ml.predictor import predict_result
from ml.pattern_detector import detect_patterns


# ============================================================
# CLASSIFY LABORATORY VALUE
# ============================================================

def classify_value(value, reference_low, reference_high):
    """
    Classify a laboratory value using the reference range
    provided by the laboratory.

    If the reference range is missing, the status is UNKNOWN
    instead of attempting an invalid comparison.
    """

    if value is None:
        return "UNKNOWN"

    if reference_low is None or reference_high is None:
        return "UNKNOWN"

    if value < reference_low:
        return "LOW"

    elif value > reference_high:
        return "HIGH"

    else:
        return "NORMAL"


# ============================================================
# ANALYZE MEASUREMENTS
# ============================================================

def analyze_measurements(measurements):
    """
    Analyze laboratory measurements.

    The laboratory reference range is the primary basis
    for LOW / NORMAL / HIGH status.

    ML prediction is an additional experimental signal.

    Pattern detection looks across multiple results for
    potentially meaningful combinations.

    This system does not make a medical diagnosis.
    """

    analyzed = []

    for measurement in measurements:

        value = measurement.get("value")
        reference_low = measurement.get("reference_low")
        reference_high = measurement.get("reference_high")

        # ----------------------------------------------------
        # PRIMARY STATUS
        # ----------------------------------------------------

        status = classify_value(
            value,
            reference_low,
            reference_high
        )

        result = measurement.copy()

        result["status"] = status

        # ----------------------------------------------------
        # ML PREDICTION
        # ----------------------------------------------------

        if (
            value is not None
            and reference_low is not None
            and reference_high is not None
        ):

            try:

                ml_result = predict_result(
                    test_name=measurement.get("test", ""),
                    value=value,
                    reference_low=reference_low,
                    reference_high=reference_high
                )

                result["ml_prediction"] = ml_result.get(
                    "prediction"
                )

                result["ml_confidence"] = ml_result.get(
                    "confidence"
                )

            except Exception as e:

                print(
                    f"ML prediction failed for "
                    f"{measurement.get('test', 'Unknown Test')}: {e}"
                )

                result["ml_prediction"] = None
                result["ml_confidence"] = None

        else:

            # No valid reference range means we cannot
            # safely use the current ML feature setup.

            result["ml_prediction"] = None
            result["ml_confidence"] = None

        analyzed.append(result)

    # --------------------------------------------------------
    # PATTERN DETECTION
    # --------------------------------------------------------

    try:

        patterns = detect_patterns(
            analyzed
        )

    except Exception as e:

        print(
            f"Pattern detection failed: {e}"
        )

        patterns = []

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {
        "results": analyzed,
        "patterns": patterns
    }