from pathlib import Path

from app.services.pdf_service import extract_text_from_pdf
from app.services.extraction_service import extract_measurements
from app.services.analysis_service import analyze_measurements


pdf_path = Path(__file__).parent / "sample_report.pdf"

text = extract_text_from_pdf(str(pdf_path))

measurements = extract_measurements(text)

analyzed_results = analyze_measurements(measurements)

print("========== MEDICAL ANALYSIS ==========")

for result in analyzed_results:
    print(
        f"{result['test']}: "
        f"{result['value']} {result['unit']} "
        f"-> {result['status']}"
    )