from pathlib import Path

from app.services.pdf_service import extract_text_from_pdf
from app.services.extraction_service import extract_measurements


pdf_path = Path(__file__).parent / "sample_report.pdf"

text = extract_text_from_pdf(str(pdf_path))

measurements = extract_measurements(text)

print("========== EXTRACTED MEASUREMENTS ==========")

for measurement in measurements:
    print(measurement)