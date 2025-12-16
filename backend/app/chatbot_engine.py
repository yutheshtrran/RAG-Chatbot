import os
import logging
import textwrap
from typing import List
from .retriever import retrieve_patient_context
from .db_handler import get_patient_info
from .config import Config

# ================= Logging =================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= Local RAG Generation =================
def _local_generate(question: str, sources: List[str]) -> str:
    """Generate answer based on local patient records."""
    if not sources:
        return "I don't know. No relevant patient records found — please consult a clinician."

    lines = ["### 🩺 Answer based on internal patient records:\n"]
    for i, s in enumerate(sources, start=1):
        excerpt = s.strip().replace("\n", " ")
        if len(excerpt) > 600:
            excerpt = excerpt[:600].rsplit(" ", 1)[0] + "..."
        wrapped = textwrap.fill(excerpt, width=100)
        lines.append(f"**Record {i}:**\n* {wrapped}\n\n")
    return "\n".join(lines)

# ================= Gemini Generator =================
def _gemini_generate(question: str, local_summary: str = None) -> str:
    """Generate answer using Gemini, optionally with local context."""
    try:
        import google.generativeai as genai

        # Read API key dynamically each call
        gemini_api_key = os.getenv("GEMINI_API_KEY") or Config.GEMINI_API_KEY
        if not gemini_api_key or not gemini_api_key.strip():
            return "⚠️ Gemini not configured or API key missing."

        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("models/gemini-2.5-pro")

        if local_summary and "I don't know" not in local_summary:
            context_snippet = " ".join(local_summary.split()[:500])
            prompt = f"""
You are a clinical assistant AI. Base your answer PRIMARILY on the provided 'Internal patient records', then supplement with general knowledge.

Internal patient records:
{context_snippet}

Question: {question}

Provide a clear, structured answer in Markdown:
- Start with patient-specific details if available.
- Use bullet points and concise explanations.
- Do not invent details not in the records.
"""
        else:
            prompt = f"""
You are a clinical assistant AI.

Internal documents did not contain relevant information for this question. Use general medical knowledge.

Question: {question}

Provide a clinically accurate answer in Markdown:
- Include bullet points.
- Add a disclaimer: this is general information, not patient-specific.
"""

        response = model.generate_content(prompt)
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        return "⚠️ Gemini did not generate a response."

    except Exception as e:
        logger.exception("Gemini generation failed: %s", e)
        return f"⚠️ Gemini error: {str(e)}"

# ================= Main Patient RAG Logic =================
def get_patient_rag_response(patient_id: str, user_message: str, top_k: int = 3) -> dict:
    """
    Retrieve patient-specific context and generate RAG-enhanced response.
    """
    if not user_message.strip():
        return {"reply": "Please provide a valid medical question."}

    # Verify patient exists
    patient_info = get_patient_info(patient_id)
    if not patient_info:
        return {"reply": f"Patient ID '{patient_id}' not found in database."}

    try:
        # Retrieve top-k relevant patient records
        sources = retrieve_patient_context(patient_id, user_message, top_k)
        # Generate local answer
        local_answer = _local_generate(user_message, sources)
        # If Gemini is available, enhance the answer
        gemini_response = _gemini_generate(user_message, local_summary=local_answer)

        # If Gemini returns an error (expired/invalid API key or other failure),
        # gracefully fall back to the locally generated answer so the system
        # remains usable even without a working Gemini key.
        if gemini_response:
            lower = gemini_response.lower()
            if lower.startswith("⚠️ gemini error") or "api key expired" in lower or "api_key_invalid" in lower or "api key invalid" in lower:
                logger.warning("Gemini returned an error; falling back to local answer.")
                return {"reply": local_answer}

        return {"reply": gemini_response or local_answer}
    except Exception as e:
        logger.exception("Error generating patient RAG response: %s", e)
        return {"reply": "⚠️ Error occurred while generating the response."}

# ================= Standalone Test =================
if __name__ == "__main__":
    print("\n=============================================")
    print("      Hybrid RAG + Gemini Clinical Assistant")
    print("=============================================")
    while True:
        patient_id = input("\nEnter patient ID (or 'exit'): ").strip()
        if patient_id.lower() == "exit":
            break
        question = input("Enter medical question: ").strip()
        if question.lower() == "exit":
            break
        response = get_patient_rag_response(patient_id, question)
        print("\n" + "*"*20 + " RESPONSE " + "*"*20)
        print(response["reply"])
        print("*"*50)
    print("Exiting.")
