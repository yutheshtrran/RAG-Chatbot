import os
import logging
from typing import List
from dotenv import load_dotenv

from .retriever import retrieve_patient_context
from .db_handler import get_patient_info
from .config import Config

# ================= Logging =================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= Load .env =================
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or Config.GEMINI_API_KEY
logger.info(f"GEMINI_API_KEY loaded: {'Yes' if GEMINI_API_KEY else 'No'}")

# ================= Utility Functions =================
def _clean_medical_record(text: str) -> str:
    for sep in ["="*50, "-"*50, "-"*40, "="*40]:
        text = text.replace(sep, "")
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)

def _extract_key_sections(text: str) -> dict:
    sections = {
        "Patient Info": "",
        "Chief Complaint": "",
        "Diagnosis": "",
        "Medications": "",
        "Test Results": "",
        "Assessment": ""
    }
    text_lower = text.lower()

    if "patient" in text_lower and "id:" in text_lower:
        for line in text.split("\n"):
            if any(k in line.lower() for k in ["patient id:", "name:", "age:"]):
                sections["Patient Info"] += line.strip() + "\n"

    if "chief complaint" in text_lower:
        idx = text_lower.index("chief complaint")
        chunk = text[idx:idx+400].split("\n")[0:3]
        sections["Chief Complaint"] = "\n".join(chunk).replace("CHIEF COMPLAINT:", "").strip()

    if "diagnosis:" in text_lower:
        idx = text_lower.index("diagnosis:")
        chunk = text[idx:idx+300].split("\n")[0]
        sections["Diagnosis"] = chunk.replace("DIAGNOSIS:", "").strip()

    if "medication" in text_lower:
        idx = text_lower.index("medication")
        chunk = text[idx:idx+500]
        sections["Medications"] = chunk.replace("CURRENT MEDICATIONS", "").replace("MEDICATIONS:", "").strip()

    if "test result" in text_lower:
        idx = text_lower.index("test result")
        chunk = text[idx:idx+400]
        sections["Test Results"] = chunk.replace("TEST RESULTS", "").replace("DIAGNOSTIC TEST RESULTS", "").strip()

    if "assessment" in text_lower:
        idx = text_lower.index("assessment")
        chunk = text[idx:idx+500]
        sections["Assessment"] = chunk.replace("ASSESSMENT & PLAN", "").replace("ASSESSMENT:", "").strip()

    return {k: v for k, v in sections.items() if v}

# ================= Local RAG Generation =================
def _local_generate(question: str, sources: List[str]) -> str:
    if not sources:
        return "I don't know. No relevant patient records found — please consult a clinician."

    lines = ["### 🩺 Answer based on internal patient records:\n"]
    for i, source in enumerate(sources, start=1):
        cleaned = _clean_medical_record(source)
        sections = _extract_key_sections(cleaned)
        lines.append(f"**Record {i}:**\n")
        for key, val in sections.items():
            if val:
                lines.append(f"**{key}:** {val}\n")
        lines.append("")
    return "\n".join(lines)

# ================= Gemini Generator =================
def _gemini_generate(question: str, local_summary: str = None) -> str:
    if not GEMINI_API_KEY:
        return "⚠️ Gemini not configured."

    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Default fallback model
        model_to_use = "gemini-1.5-flash"
        try:
            for m in client.models.list():
                if "generateContent" in getattr(m, "supported_actions", []):
                    model_to_use = m.name
                    break
            logger.info(f"Using Gemini model: {model_to_use}")
        except Exception as list_err:
            logger.warning(f"Could not list models, defaulting to flash: {list_err}")

        if local_summary and "I don't know" not in local_summary:
            context_snippet = " ".join(local_summary.split()[:800])
            prompt = f"""
You are a clinical assistant AI. Base your answer ONLY on the internal patient records provided below.

Internal patient records:
{context_snippet}

User Question: {question}

Instructions:
- Extract the MOST RELEVANT information from the patient records.
- Format using markdown sections.
- Use bullet points for lists.
- Be concise but comprehensive.
- Add note: "Based on patient records on file."
"""
        else:
            prompt = f"""
You are a clinical assistant AI.
No patient-specific info available. Answer with general medical knowledge.

Question: {question}

Provide clinically accurate answer in markdown.
- Include bullet points.
- Add disclaimer: "General medical information, not patient-specific guidance."
- Recommend consulting healthcare provider.
"""

        response = client.models.generate_content(
            model=model_to_use,
            contents=prompt
        )

        if response and hasattr(response, "text") and response.text:
            return response.text.strip()
        return "⚠️ Gemini did not return a valid response."

    except Exception as e:
        logger.exception("Gemini generation failed: %s", e)
        return f"⚠️ Gemini error: {str(e)}"

# ================= Main RAG Response =================
def get_patient_rag_response(patient_id: str = None, user_message: str = None, top_k: int = 3) -> dict:
    if not user_message or not user_message.strip():
        return {"reply": "Please provide a valid medical question."}

    try:
        sources = []
        local_answer = None

        if patient_id and patient_id.strip():
            # Patient-specific context
            patient_info = get_patient_info(patient_id)
            if patient_info:
                sources = retrieve_patient_context(patient_id, user_message, top_k)
            if sources:
                local_answer = _local_generate(user_message, sources)
        else:
            # No patient ID → general question, skip local RAG
            sources = []
            local_answer = None

        # Generate answer using Gemini (with optional local context)
        gemini_response = _gemini_generate(user_message, local_summary=local_answer)

        # Fallback if Gemini fails
        if gemini_response:
            lower = gemini_response.lower()
            if "⚠️ gemini error" in lower or "not configured" in lower:
                logger.warning("Gemini failed, providing local answer instead.")
                return {"reply": local_answer or gemini_response}

        return {"reply": gemini_response or local_answer or "⚠️ No data available."}

    except Exception as e:
        logger.exception("Error generating patient RAG response: %s", e)
        return {"reply": "⚠️ Error occurred while generating the response."}

# ================= Standalone Test =================
if __name__ == "__main__":
    print("\n=============================================")
    print("    Hybrid RAG + Gemini Clinical Assistant")
    print("=============================================")
    while True:
        p_id = input("\nEnter patient ID (or leave blank for general question, type 'exit' to quit): ").strip()
        if p_id.lower() == "exit":
            break
        q = input("Enter medical question: ").strip()
        if q.lower() == "exit":
            break
        res = get_patient_rag_response(p_id, q)
        print("\n" + "*"*20 + " RESPONSE " + "*"*20)
        print(res["reply"])
        print("*"*50)
    print("Exiting.")
