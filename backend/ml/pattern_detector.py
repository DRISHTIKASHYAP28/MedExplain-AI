def detect_patterns(results):
    """
    Detects simple multi-test laboratory patterns.

    This is an educational pattern-detection layer.
    It does NOT diagnose diseases.
    """

    patterns = []

    # Create easy lookup by test name
    result_map = {}

    for result in results:
        test_name = str(result.get("test", "")).strip().lower()

        if test_name:
            result_map[test_name] = result

    # ---------------------------------------------------------
    # Red blood cell pattern
    # ---------------------------------------------------------
    hemoglobin = result_map.get("hemoglobin")
    mcv = result_map.get("mcv")
    mch = result_map.get("mch")

    if hemoglobin and mcv and mch:

        hb_status = str(hemoglobin.get("status", "")).upper()
        mcv_status = str(mcv.get("status", "")).upper()
        mch_status = str(mch.get("status", "")).upper()

        if (
            hb_status == "LOW"
            and mcv_status == "LOW"
            and mch_status == "LOW"
        ):
            patterns.append({
                "pattern": "Multiple red blood cell measurements are below their provided reference ranges.",
                "related_tests": [
                    "Hemoglobin",
                    "MCV",
                    "MCH"
                ],
                "interpretation": (
                    "This combination can sometimes be seen with certain "
                    "types of anemia or nutritional problems, but laboratory "
                    "results alone cannot determine the cause."
                )
            })

    # ---------------------------------------------------------
    # White blood cell pattern
    # ---------------------------------------------------------
    wbc = result_map.get("wbc")

    if wbc:
        wbc_status = str(wbc.get("status", "")).upper()

        if wbc_status == "LOW":
            patterns.append({
                "pattern": "White blood cell count is below the provided reference range.",
                "related_tests": ["WBC"],
                "interpretation": (
                    "A low white blood cell count can have several possible "
                    "causes and should be interpreted in clinical context."
                )
            })

        elif wbc_status == "HIGH":
            patterns.append({
                "pattern": "White blood cell count is above the provided reference range.",
                "related_tests": ["WBC"],
                "interpretation": (
                    "A high white blood cell count can occur for several "
                    "reasons and does not by itself establish a diagnosis."
                )
            })

    # ---------------------------------------------------------
    # Platelet pattern
    # ---------------------------------------------------------
    platelets = result_map.get("platelets")

    if platelets:
        platelet_status = str(
            platelets.get("status", "")
        ).upper()

        if platelet_status == "LOW":
            patterns.append({
                "pattern": "Platelet count is below the provided reference range.",
                "related_tests": ["Platelets"],
                "interpretation": (
                    "A low platelet count can have several possible causes "
                    "and should be reviewed in clinical context."
                )
            })

        elif platelet_status == "HIGH":
            patterns.append({
                "pattern": "Platelet count is above the provided reference range.",
                "related_tests": ["Platelets"],
                "interpretation": (
                    "A high platelet count can have several possible causes "
                    "and should be interpreted alongside other findings."
                )
            })

    # ---------------------------------------------------------
    # Glucose pattern
    # ---------------------------------------------------------
    glucose = result_map.get("glucose")

    if glucose:
        glucose_status = str(
            glucose.get("status", "")
        ).upper()

        if glucose_status == "LOW":
            patterns.append({
                "pattern": "Glucose is below the provided reference range.",
                "related_tests": ["Glucose"],
                "interpretation": (
                    "A low glucose result may have several possible causes "
                    "and should be interpreted according to the patient's "
                    "circumstances and clinical context."
                )
            })

        elif glucose_status == "HIGH":
            patterns.append({
                "pattern": "Glucose is above the provided reference range.",
                "related_tests": ["Glucose"],
                "interpretation": (
                    "A high glucose result can have several possible causes "
                    "and should be interpreted in clinical context."
                )
            })

    # ---------------------------------------------------------
    # Creatinine pattern
    # ---------------------------------------------------------
    creatinine = result_map.get("creatinine")

    if creatinine:
        creatinine_status = str(
            creatinine.get("status", "")
        ).upper()

        if creatinine_status == "HIGH":
            patterns.append({
                "pattern": "Creatinine is above the provided reference range.",
                "related_tests": ["Creatinine"],
                "interpretation": (
                    "An elevated creatinine result can have several possible "
                    "causes. It should be interpreted together with other "
                    "clinical information."
                )
            })

    return patterns