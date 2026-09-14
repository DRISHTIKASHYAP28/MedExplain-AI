from app.services.gemini_service import explain_medical_results


test_results = [
    {
        "test": "Hemoglobin",
        "value": 10.5,
        "unit": "g/dL",
        "reference_low": 12.0,
        "reference_high": 16.0,
        "status": "LOW"
    },
    {
        "test": "WBC Count",
        "value": 8500,
        "unit": "/uL",
        "reference_low": 4000,
        "reference_high": 11000,
        "status": "NORMAL"
    }
]


explanation = explain_medical_results(test_results)

print("========== GEMINI EXPLANATION ==========")
print(explanation)