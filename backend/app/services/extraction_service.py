import re


# ============================================================
# HELPER: CONVERT VALUE TO FLOAT
# ============================================================

def _to_float(value):
    try:
        if value is None:
            return None

        return float(value)

    except (TypeError, ValueError):
        return None


# ============================================================
# HELPER: NORMALIZE TEXT
# ============================================================

def _normalize_text(text):
    """
    Normalize common formatting differences in medical reports.
    """

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Normalize different dash characters.
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("−", "-")

    return text


# ============================================================
# EXTRACT MEASUREMENTS
# ============================================================

def extract_measurements(text):
    """
    Extract laboratory measurements from common report formats.

    Supported examples:

    Hemoglobin: 10.5 g/dL (12 - 16)

    Hemoglobin: 10.5 g/dL (12 - 16 g/dL)

    Hemoglobin: 10.5 g/dL
    Reference Range: 12 - 16 g/dL

    The laboratory's own reference range is preserved.

    If a reference range cannot be found, the measurement is
    still returned with reference_low/reference_high as None.
    """

    text = _normalize_text(text)

    if not text.strip():
        return []

    measurements = []

    # ========================================================
    # FORMAT 1
    # Same-line format:
    #
    # Hemoglobin: 10.5 g/dL (12 - 16)
    #
    # Also supports:
    #
    # Hemoglobin: 10.5 g/dL (12 - 16 g/dL)
    # ========================================================

    same_line_pattern = re.compile(
        r"""
        ^\s*
        (?P<test>
            [A-Za-z][A-Za-z0-9 ()/%µ_^.-]*
        )
        \s*:\s*

        (?P<value>
            [-+]?\d+(?:\.\d+)?
        )
        \s*

        (?P<unit>
            [A-Za-zµ%][A-Za-z0-9µ%/^.*_-]*
        )

        \s*

        \(
        \s*

        (?:
            Reference(?:\s+Range)?
            \s*:?\s*
        )?

        (?P<reference_low>
            [-+]?\d+(?:\.\d+)?
        )

        \s*-\s*

        (?P<reference_high>
            [-+]?\d+(?:\.\d+)?
        )

        (?:
            \s*
            [A-Za-zµ%][A-Za-z0-9µ%/^.*_-]*
        )?

        \s*
        \)

        \s*$
        """,
        re.IGNORECASE | re.VERBOSE | re.MULTILINE,
    )

    for match in same_line_pattern.finditer(text):

        measurements.append(
            {
                "test": match.group("test").strip(),
                "value": _to_float(match.group("value")),
                "unit": match.group("unit").strip(),
                "reference_low": _to_float(
                    match.group("reference_low")
                ),
                "reference_high": _to_float(
                    match.group("reference_high")
                ),
            }
        )

    if measurements:
        return measurements

    # ========================================================
    # FORMAT 2
    #
    # Hemoglobin: 10.5 g/dL
    # Reference Range: 12 - 16 g/dL
    #
    # The reference range can be on the next line.
    # ========================================================

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    i = 0

    while i < len(lines):

        line = lines[i]

        result_match = re.match(
            r"""
            ^
            (?P<test>
                [A-Za-z][A-Za-z0-9 ()/%µ_^.-]*
            )
            \s*:\s*

            (?P<value>
                [-+]?\d+(?:\.\d+)?
            )
            \s*

            (?P<unit>
                [A-Za-zµ%][A-Za-z0-9µ%/^.*_-]*
            )
            \s*$
            """,
            line,
            re.IGNORECASE | re.VERBOSE,
        )

        if result_match:

            test_name = result_match.group("test").strip()
            value = _to_float(
                result_match.group("value")
            )
            unit = result_match.group("unit").strip()

            reference_low = None
            reference_high = None

            # ------------------------------------------------
            # Look at the following line for reference range.
            # ------------------------------------------------

            if i + 1 < len(lines):

                reference_line = lines[i + 1]

                reference_match = re.search(
                    r"""
                    Reference
                    (?:\s+Range)?
                    \s*:?\s*

                    (?P<low>
                        [-+]?\d+(?:\.\d+)?
                    )

                    \s*-\s*

                    (?P<high>
                        [-+]?\d+(?:\.\d+)?
                    )
                    """,
                    reference_line,
                    re.IGNORECASE | re.VERBOSE,
                )

                if reference_match:

                    reference_low = _to_float(
                        reference_match.group("low")
                    )

                    reference_high = _to_float(
                        reference_match.group("high")
                    )

                    i += 1

            measurements.append(
                {
                    "test": test_name,
                    "value": value,
                    "unit": unit,
                    "reference_low": reference_low,
                    "reference_high": reference_high,
                }
            )

        i += 1

    if measurements:
        return measurements

    # ========================================================
    # FORMAT 3
    #
    # More flexible fallback.
    #
    # Example:
    #
    # Hemoglobin: 10.5 g/dL [12 - 16]
    #
    # or
    #
    # Hemoglobin: 10.5 g/dL 12 - 16
    # ========================================================

    flexible_pattern = re.compile(
        r"""
        (?P<test>
            [A-Za-z][A-Za-z0-9 ()/%µ_^.-]*
        )
        \s*:\s*

        (?P<value>
            [-+]?\d+(?:\.\d+)?
        )
        \s*

        (?P<unit>
            [A-Za-zµ%][A-Za-z0-9µ%/^.*_-]*
        )

        (?:
            \s*
            [(\[]?
            \s*

            (?:
                Reference(?:\s+Range)?
                \s*:?\s*
            )?

            (?P<reference_low>
                [-+]?\d+(?:\.\d+)?
            )

            \s*-\s*

            (?P<reference_high>
                [-+]?\d+(?:\.\d+)?
            )

            (?:
                \s*
                [A-Za-zµ%][A-Za-z0-9µ%/^.*_-]*
            )?

            \s*
            [)\]]?
        )?
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    for match in flexible_pattern.finditer(text):

        value = _to_float(
            match.group("value")
        )

        if value is None:
            continue

        measurements.append(
            {
                "test": match.group("test").strip(),
                "value": value,
                "unit": match.group("unit").strip(),
                "reference_low": _to_float(
                    match.group("reference_low")
                ),
                "reference_high": _to_float(
                    match.group("reference_high")
                ),
            }
        )

    return measurements