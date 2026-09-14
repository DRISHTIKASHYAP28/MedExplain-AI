import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        f"GEMINI_API_KEY is not configured.\n"
        f"Please check your .env file here:\n{ENV_FILE}"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"api_version": "v1"}
)

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# HELPER: CLEAN GEMINI RESPONSE
# ============================================================

def clean_json_response(text):
    """
    Removes markdown code fences if Gemini returns JSON
    inside ```json ... ``` blocks.
    """

    if not text:
        return ""

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


# ============================================================
# EXTRACT MEASUREMENTS FROM IMAGE
# ============================================================

def extract_measurements_from_image(image_bytes, mime_type):
    """
    Uses Gemini Vision to extract laboratory measurements
    from a medical report image.
    """

    prompt = """
You are a medical laboratory report extraction assistant.

Look carefully at the uploaded medical report image.

Extract ONLY laboratory test measurements that are clearly visible.

For every test, return:

- test
- value
- unit
- reference_low
- reference_high

If a reference range is not visible, use null for
reference_low and reference_high.

Do not guess values.

Do not diagnose the patient.

Return ONLY valid JSON.

Expected structure:

[
  {
    "test": "Hemoglobin",
    "value": 10.5,
    "unit": "g/dL",
    "reference_low": 12.0,
    "reference_high": 16.0
  }
]

If no measurements can be identified, return:

[]
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type
                ),
                prompt
            ]
        )

        response_text = clean_json_response(response.text)

        data = json.loads(response_text)

        if isinstance(data, list):
            return data

        return []

    except Exception as e:
        print(
            f"ERROR extracting measurements from image: {str(e)}"
        )
        return []


# ============================================================
# EXTRACT MEASUREMENTS FROM TEXT
# ============================================================

def extract_measurements_from_text_with_gemini(text):
    """
    Uses Gemini to extract laboratory measurements from
    report text when regex extraction is unsuccessful.
    """

    prompt = """
You are a medical laboratory report extraction assistant.

Read the medical report text below.

Extract laboratory test measurements.

For every test, return:

- test
- value
- unit
- reference_low
- reference_high

Important rules:

1. Extract only values that are actually present.
2. Never invent missing values.
3. If the reference range is unavailable, use null.
4. Convert numeric values to numbers where possible.
5. Do not diagnose anything.
6. Return ONLY valid JSON.
7. Return an empty array if no measurements are found.

Expected structure:

[
  {
    "test": "Hemoglobin",
    "value": 10.5,
    "unit": "g/dL",
    "reference_low": 12.0,
    "reference_high": 16.0
  }
]

MEDICAL REPORT TEXT:

""" + text

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        response_text = clean_json_response(response.text)

        data = json.loads(response_text)

        if isinstance(data, list):
            return data

        return []

    except Exception as e:
        print(
            f"ERROR extracting measurements from text with Gemini: {str(e)}"
        )
        return []


# ============================================================
# EXPLAIN MEDICAL RESULTS
# ============================================================

def explain_medical_results(
    results,
    report_text=None,
    patterns=None
):
    """
    Generates a structured, patient-friendly explanation
    of the extracted laboratory results.

    The laboratory reference range is the primary basis
    for LOW / NORMAL / HIGH status.

    ML predictions are supporting information only.

    Pattern detection is educational and does not diagnose
    disease.
    """

    if results is None:
        results = []

    if report_text is None:
        report_text = ""

    if patterns is None:
        patterns = []

    results_json = json.dumps(
        results,
        indent=2
    )

    patterns_json = json.dumps(
        patterns,
        indent=2
    )

    # ========================================================
    # JSON OUTPUT SCHEMA
    # ========================================================

    output_schema = """
{
  "summary": "A short, patient-friendly overview of the report.",
  "key_findings": [
    "Important finding 1",
    "Important finding 2"
  ],
  "normal_results": [
    "Tests that are within their provided reference ranges"
  ],
  "attention_results": [
    "Tests that are outside their provided reference ranges"
  ],
  "meaning": "Explain what the overall pattern may generally mean without making a diagnosis.",
  "next_step": "Give a sensible general next step.",
  "disclaimer": "This explanation is for educational purposes and does not replace professional medical advice."
}
"""

    # ========================================================
    # GEMINI PROMPT
    # ========================================================

    prompt = f"""
You are MedExplain AI, a medical report explanation assistant.

Your job is to explain laboratory results in simple language
that an ordinary patient can understand.

IMPORTANT SAFETY RULES:

- Do not diagnose the patient.
- Do not claim that the patient definitely has a disease.
- Do not invent laboratory values.
- Do not change laboratory values.
- Do not ignore the reference ranges provided in the data.
- If a reference range is missing, do not assume one.
- Use cautious language such as:
  "may be associated with",
  "can sometimes be seen with",
  "can have several causes".
- Encourage discussion with a qualified healthcare professional
  when results are abnormal or concerning.
- Keep the explanation understandable.
- Do not make conclusions that are not supported by the
  provided results.

IMPORTANT ML RULES:

- The "status" field is the PRIMARY classification.
- Status is based on the laboratory's provided reference range.
- "ml_prediction" is an experimental supporting signal.
- "ml_confidence" is an experimental model confidence score.
- Do NOT treat ML prediction as a diagnosis.
- Do NOT claim that the ML model is clinically validated.
- Do NOT allow ML prediction to override the provided
  reference-range status.
- If ML prediction and status disagree, rely on "status".
- ML confidence is NOT a probability of disease.
- Do not unnecessarily mention ML in the patient-facing
  explanation.

IMPORTANT PATTERN RULES:

- The patterns provided below are educational signals only.
- Patterns must NOT be treated as diagnoses.
- Do not claim that a pattern proves a disease.
- Explain possible associations cautiously.
- The individual laboratory reference ranges remain the
  primary basis for interpreting LOW, NORMAL, or HIGH.
- Do not invent patterns.
- Only discuss patterns that are actually provided below.
- If no patterns are provided, do not invent any.

============================================================
LABORATORY RESULTS
============================================================

{results_json}

============================================================
MULTI-RESULT PATTERNS
============================================================

{patterns_json}

============================================================
ORIGINAL REPORT TEXT
============================================================

{report_text}

============================================================
TASK
============================================================

Explain the laboratory report in simple, patient-friendly
language.

Use the actual values and reference ranges.

Identify:

1. Important abnormal findings.
2. Results within their provided reference ranges.
3. General meaning of the findings.
4. Multi-result patterns when appropriate.
5. A reasonable general next step.

Do not diagnose.

============================================================
RETURN FORMAT
============================================================

Return ONLY valid JSON.

Use exactly this structure:

{output_schema}

CONTENT GUIDELINES:

summary:
Give a concise overview of the actual report.

key_findings:
Mention the most important findings from the actual results.

normal_results:
Mention tests that are within their provided reference ranges.

attention_results:
Mention tests that are below or above their provided
reference ranges.

meaning:
Explain the general meaning of the results.
Do not diagnose.

next_step:
Suggest a reasonable general next step.

disclaimer:
Include a clear medical disclaimer.
"""

    # ========================================================
    # CALL GEMINI
    # ========================================================

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        response_text = clean_json_response(
            response.text
        )

        data = json.loads(
            response_text
        )

        if isinstance(data, dict):

            return data

        return {
            "summary": response.text,
            "key_findings": [],
            "normal_results": [],
            "attention_results": [],
            "meaning": "",
            "next_step": "",
            "disclaimer": (
                "This explanation is for educational purposes "
                "and does not replace professional medical advice."
            )
        }

    except Exception as e:

        print(
            f"ERROR generating medical explanation: {str(e)}"
        )

        return {
            "summary": (
                "Unable to generate an AI explanation "
                "at this time."
            ),
            "key_findings": [],
            "normal_results": [],
            "attention_results": [],
            "meaning": "",
            "next_step": (
                "Please review the report with a qualified "
                "healthcare professional."
            ),
            "disclaimer": (
                "This explanation is for educational purposes "
                "and does not replace professional medical advice."
            )
        }


# ============================================================
# CHAT WITH MEDICAL REPORT
# ============================================================

def chat_with_report(
    report_text="",
    results=None,
    question="",
    conversation_history=None
):
    """
    Dynamic AI chatbot for asking questions about the
    uploaded medical report.

    The answer is generated from:

    - actual report
    - extracted laboratory results
    - previous conversation
    - user's current question
    """

    if results is None:
        results = []

    if conversation_history is None:
        conversation_history = []

    results_json = json.dumps(
        results,
        indent=2
    )

    # ========================================================
    # FORMAT PREVIOUS CONVERSATION
    # ========================================================

    history_text = ""

    if conversation_history:

        history_parts = []

        for message in conversation_history:

            if not isinstance(message, dict):
                continue

            role = message.get(
                "role",
                ""
            )

            content = message.get(
                "content",
                ""
            )

            if not content:
                continue

            if role == "user":

                history_parts.append(
                    f"User: {content}"
                )

            elif role == "assistant":

                history_parts.append(
                    f"MedExplain AI: {content}"
                )

        history_text = "\n".join(
            history_parts
        )

    if not history_text:
        history_text = "No previous conversation."


    # ========================================================
    # CHAT PROMPT
    # ========================================================

    prompt = f"""
You are MedExplain AI, an AI assistant that helps users
understand their medical laboratory reports.

The user has uploaded or entered a medical report.

Your task is to answer the user's CURRENT question directly
and naturally using the actual report information.

============================================================
CURRENT USER QUESTION
============================================================

{question}

============================================================
EXTRACTED LAB RESULTS
============================================================

{results_json}

============================================================
ORIGINAL REPORT
============================================================

{report_text}

============================================================
PREVIOUS CONVERSATION
============================================================

{history_text}

============================================================
IMPORTANT INSTRUCTIONS
============================================================

1. Answer the current question directly.

2. Do NOT always use a fixed structure.

3. Do NOT automatically create sections such as:
   - Low Results
   - High Results
   - Summary
   - Next Step

   unless the user's question actually asks for those things.

4. If the user asks about one specific test, focus on that test.

5. If the user asks "what does this mean?", explain the relevant
   result in simple language.

6. If the user asks why something may be abnormal, explain
   possible general associations carefully.

7. Do not diagnose the patient.

8. Do not say the user definitely has a disease.

9. Do not invent values that are not in the report.

10. Use the reference ranges provided in the report/results.

11. If a value is outside its provided reference range, you may
    explain that it is outside that laboratory's stated range.

12. Laboratory reference ranges can vary between laboratories.

13. If the user asks about multiple results, discuss the relevant
    results together.

14. If the user asks a simple question, give a short answer.

15. If the user asks a complex question, give a more detailed answer.

16. Use previous conversation context when the user asks a
    follow-up question.

17. Do not repeat the entire report unless the user asks for it.

18. Do not unnecessarily repeat information from previous messages.

19. Use plain, friendly language.

20. Avoid excessive medical jargon. If medical terminology is
    needed, explain it simply.

21. Do not use fake citations or medical references.

22. If the information is insufficient to answer confidently,
    say so.

23. If a result could be clinically important, recommend discussing
    it with a qualified healthcare professional.

24. This is educational information and not a diagnosis.

25. The "status" field is the primary LOW/NORMAL/HIGH
    classification because it is based on the provided
    laboratory reference range.

26. "ml_prediction" and "ml_confidence" are experimental
    supporting signals only.

27. Do NOT interpret "ml_confidence" as a probability of disease.

28. If ML prediction conflicts with the reference-range status,
    rely on the reference-range status.

29. Do not claim that the ML model is clinically validated.

30. Answer ONLY the user's question. Do not force a generic
    report summary into every answer.

============================================================
RESPONSE STYLE
============================================================

Be conversational and natural.

For example, if the user asks:

"What is hemoglobin?"

Answer the question about hemoglobin.

If the user asks:

"Why is my hemoglobin low?"

Explain possible general reasons for low hemoglobin while
making clear that the report alone cannot determine the cause.

If the user asks:

"Are all my results normal?"

Review the actual extracted results and answer that question.

If the user asks:

"What should I ask my doctor?"

Provide useful questions based on the actual report.

Do not blindly follow a fixed response template.
"""

    # ========================================================
    # CALL GEMINI
    # ========================================================

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        answer = response.text.strip()

        # Remove accidental escaped markdown
        answer = answer.replace(
            "\\###",
            "###"
        )

        answer = answer.replace(
            "\\##",
            "##"
        )

        answer = answer.replace(
            "\\#",
            "#"
        )

        answer = answer.replace(
            "\\*\\*",
            "**"
        )

        answer = answer.replace(
            "\\*",
            "*"
        )

        return answer

    except Exception as e:

        print(
            f"ERROR in chat_with_report: {str(e)}"
        )

        return (
            "I'm sorry, but I couldn't generate an answer "
            "right now. Please try asking your question again."
        )