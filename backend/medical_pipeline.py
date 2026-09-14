from pathlib import Path

from app.services.pdf_service import extract_text_from_pdf
from app.services.extraction_service import extract_measurements
from app.services.analysis_service import analyze_measurements
from app.services.gemini_service import explain_medical_results


def run_medical_pipeline(pdf_path):

    # Step 1: Extract text from PDF
    print("Reading PDF...")
    text = extract_text_from_pdf(str(pdf_path))

    # Step 2: Extract medical measurements
    print("Extracting medical measurements...")
    measurements = extract_measurements(text)

    # Step 3: Analyze measurements
    print("Analyzing results...")
    analyzed_results = analyze_measurements(measurements)

    # Step 4: Ask Gemini to explain results
    print("Generating AI explanation...")
    explanation = explain_medical_results(analyzed_results)

    return analyzed_results, explanation


if __name__ == "__main__":

    pdf_path = Path(__file__).parent / "sample_report.pdf"

    results, explanation = run_medical_pipeline(pdf_path)

    print("\n========== ANALYZED RESULTS ==========")

    for result in results:
        print(
            f"{result['test']}: "
            f"{result['value']} {result['unit']} "
            f"-> {result['status']}"
        )

    print("\n========== GEMINI EXPLANATION ==========")
    print(explanation)