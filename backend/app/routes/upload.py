import os
import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    Form,
    UploadFile,
    HTTPException
)

from pydantic import BaseModel, Field

from app.services.pdf_service import extract_text_from_pdf
from app.services.extraction_service import extract_measurements
from app.services.analysis_service import analyze_measurements

from app.services.gemini_service import (
    explain_medical_results,
    extract_measurements_from_image,
    extract_measurements_from_text_with_gemini,
    chat_with_report
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api",
    tags=["Medical Report"]
)


# ============================================================
# UPLOAD DIRECTORY
# ============================================================

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============================================================
# CHAT REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):
    report_text: str = ""
    results: list = Field(default_factory=list)
    explanation: dict = Field(default_factory=dict)
    question: str
    conversation_history: list = Field(default_factory=list)


# ============================================================
# ANALYZE MEDICAL REPORT
# ============================================================

@router.post("/analyze")
async def analyze_report(
    file: UploadFile | None = File(default=None),
    report_text: str = Form(default="")
):
    try:

        # ----------------------------------------------------
        # INITIAL VALUES
        # ----------------------------------------------------

        extracted_text = ""
        measurements = []
        filename = "Written Report"


        # ====================================================
        # FILE UPLOAD
        # ====================================================

        if file:

            original_filename = Path(
                file.filename or "report"
            ).name

            filename = original_filename

            extension = Path(
                original_filename
            ).suffix.lower()


            # ------------------------------------------------
            # ALLOWED FILE TYPES
            # ------------------------------------------------

            allowed_extensions = {
                ".pdf",
                ".png",
                ".jpg",
                ".jpeg"
            }

            if extension not in allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Unsupported file type. "
                        "Please upload a PDF, PNG, JPG, or JPEG file."
                    )
                )


            # ------------------------------------------------
            # CREATE UNIQUE FILE NAME
            # ------------------------------------------------

            unique_filename = (
                f"{uuid.uuid4().hex}{extension}"
            )

            file_path = os.path.join(
                UPLOAD_DIR,
                unique_filename
            )


            # ------------------------------------------------
            # READ FILE
            # ------------------------------------------------

            file_bytes = await file.read()


            # ------------------------------------------------
            # SAVE FILE
            # ------------------------------------------------

            with open(file_path, "wb") as output_file:
                output_file.write(file_bytes)


            # =================================================
            # PDF REPORT
            # =================================================

            if extension == ".pdf":

                extracted_text = extract_text_from_pdf(
                    file_path
                )


                # ---------------------------------------------
                # FIRST: NORMAL EXTRACTION
                # ---------------------------------------------

                measurements = extract_measurements(
                    extracted_text
                )


                # ---------------------------------------------
                # FALLBACK: GEMINI TEXT EXTRACTION
                # ---------------------------------------------

                if (
                    not measurements
                    and extracted_text.strip()
                ):

                    measurements = (
                        extract_measurements_from_text_with_gemini(
                            extracted_text
                        )
                    )


            # =================================================
            # IMAGE REPORT
            # =================================================

            else:

                measurements = (
                    extract_measurements_from_image(
                        file_bytes,
                        file.content_type or "image/jpeg"
                    )
                )

                extracted_text = (
                    "Medical report provided as an image. "
                    "Laboratory values were extracted from the image."
                )


        # ====================================================
        # WRITTEN REPORT
        # ====================================================

        elif report_text.strip():

            extracted_text = report_text.strip()

            filename = "Written Report"


            # ------------------------------------------------
            # FIRST: NORMAL EXTRACTION
            # ------------------------------------------------

            measurements = extract_measurements(
                extracted_text
            )


            # ------------------------------------------------
            # FALLBACK: GEMINI TEXT EXTRACTION
            # ------------------------------------------------

            if not measurements:

                measurements = (
                    extract_measurements_from_text_with_gemini(
                        extracted_text
                    )
                )


        # ====================================================
        # NO INPUT
        # ====================================================

        else:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Please upload a medical report "
                    "or enter report text."
                )
            )


        # ====================================================
        # ANALYZE MEASUREMENTS
        # ====================================================

        analysis = analyze_measurements(
            measurements
        )


        # ----------------------------------------------------
        # GET ANALYZED RESULTS
        # ----------------------------------------------------

        analyzed_results = analysis.get(
            "results",
            []
        )


        # ----------------------------------------------------
        # GET DETECTED PATTERNS
        # ----------------------------------------------------

        patterns = analysis.get(
            "patterns",
            []
        )


        # ====================================================
        # GEMINI EXPLANATION
        # ====================================================

        explanation = explain_medical_results(
            analyzed_results,
            extracted_text,
            patterns=patterns
        )


        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        return {

            # -----------------------------------------------
            # BASIC REPORT INFORMATION
            # -----------------------------------------------

            "filename": filename,

            "report_text": extracted_text,


            # -----------------------------------------------
            # ANALYZED LAB RESULTS
            # -----------------------------------------------

            "results": analyzed_results,


            # -----------------------------------------------
            # MULTI-RESULT PATTERNS
            # -----------------------------------------------

            "patterns": patterns,


            # -----------------------------------------------
            # GEMINI EXPLANATION
            # -----------------------------------------------

            "explanation": explanation,


            # -----------------------------------------------
            # CONVENIENCE FIELDS
            # -----------------------------------------------

            "summary": explanation.get(
                "summary",
                ""
            ),

            "key_findings": explanation.get(
                "key_findings",
                []
            ),

            "normal_results": explanation.get(
                "normal_results",
                []
            ),

            "attention_results": explanation.get(
                "attention_results",
                []
            ),

            "meaning": explanation.get(
                "meaning",
                ""
            ),

            "next_step": explanation.get(
                "next_step",
                ""
            ),

            "disclaimer": explanation.get(
                "disclaimer",
                ""
            )
        }


    # ========================================================
    # HTTP EXCEPTION
    # ========================================================

    except HTTPException:
        raise


    # ========================================================
    # GENERAL ERROR
    # ========================================================

    except Exception as e:

        print(
            f"ERROR while analyzing report: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# CHAT WITH MEDICAL REPORT
# ============================================================

@router.post("/chat")
async def chat(request: ChatRequest):

    try:

        # ----------------------------------------------------
        # VALIDATE QUESTION
        # ----------------------------------------------------

        if not request.question.strip():

            raise HTTPException(
                status_code=400,
                detail="Please enter a question."
            )


        # ----------------------------------------------------
        # CHAT WITH GEMINI
        # ----------------------------------------------------

        answer = chat_with_report(

            report_text=request.report_text,

            results=request.results,

            question=request.question,

            conversation_history=request.conversation_history
        )


        # ----------------------------------------------------
        # RETURN ANSWER
        # ----------------------------------------------------

        return {
            "answer": answer
        }


    # ========================================================
    # HTTP EXCEPTION
    # ========================================================

    except HTTPException:
        raise


    # ========================================================
    # GENERAL ERROR
    # ========================================================

    except Exception as e:

        print(
            f"ERROR while chatting: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )