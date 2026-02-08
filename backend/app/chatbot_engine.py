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

# ================= Clean Medical Record =================
def _clean_medical_record(text: str) -> str:
    """Clean and format medical record for better readability."""
    # Remove excessive separators
    text = text.replace("=" * 50, "")
    text = text.replace("-" * 50, "")
    text = text.replace("-" * 40, "")
    text = text.replace("=" * 40, "")
    
    # Remove extra whitespace
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)

def _extract_key_sections(text: str) -> dict:
    """Extract key sections from medical record."""
    sections = {
        "Patient Info": "",
        "Chief Complaint": "",
        "Diagnosis": "",
        "Medications": "",
        "Test Results": "",
        "Assessment": ""
    }
    
    text_lower = text.lower()
    
    # Extract key information
    if "patient" in text_lower and "id:" in text_lower:
        for line in text.split("\n"):
            if "patient id:" in line.lower() or "name:" in line.lower() or "age:" in line.lower():
                if sections["Patient Info"]:
                    sections["Patient Info"] += "\n" + line.strip()
                else:
                    sections["Patient Info"] = line.strip()
    
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
        chunk = text[idx:idx+500].split("\nCURRENT" if "CURRENT" in text else "\n\n")[0]
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
    """Generate answer based on local patient records."""
    if not sources:
        return "I don't know. No relevant patient records found — please consult a clinician."

    lines = ["### 🩺 Answer based on internal patient records:\n"]
    
    for i, source in enumerate(sources, start=1):
        # Clean the medical record
        cleaned = _clean_medical_record(source)
        
        # Extract key sections
        sections = _extract_key_sections(cleaned)
        
        # Format nicely
        lines.append(f"**Record {i}:**\n")
        
        if sections.get("Patient Info"):
            lines.append(f"**Patient:** {sections['Patient Info']}\n")
        
        if sections.get("Chief Complaint"):
            lines.append(f"**Chief Complaint:** {sections['Chief Complaint']}\n")
        
        if sections.get("Diagnosis"):
            lines.append(f"**Diagnosis:** {sections['Diagnosis']}\n")
        
        if sections.get("Medications"):
            lines.append(f"**Medications:**\n{sections['Medications']}\n")
        
        if sections.get("Test Results"):
            lines.append(f"**Test Results:**\n{sections['Test Results']}\n")
        
        if sections.get("Assessment"):
            lines.append(f"**Assessment & Plan:**\n{sections['Assessment']}\n")
        
        lines.append("")
    
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
            context_snippet = " ".join(local_summary.split()[:800])
            prompt = f"""
You are a clinical assistant AI. Base your answer PRIMARILY on the provided 'Internal patient records', then supplement with general knowledge.

Internal patient records:
{context_snippet}

User Question: {question}

Instructions:
- Extract and present the MOST RELEVANT information from the patient records
- Format using clear markdown with sections:
  * Patient Information
  * Chief Complaint/Symptoms
  * Diagnosis/Conditions
  * Current Medications
  * Key Test Results
  * Assessment/Treatment Plan
- Use bullet points for lists
- Be concise but comprehensive
- Only include information present in the records, do NOT invent details
- Add a note: "Based on patient records on file"

Provide your answer now:
"""
        else:
            prompt = f"""
You are a clinical assistant AI.

The internal patient records did not contain relevant information for this question. Use general medical knowledge.

Question: {question}

Provide a clinically accurate but general answer in Markdown:
- Include relevant bullet points
- Add disclaimer: "This is general medical information, not patient-specific guidance"
- Recommend consulting with healthcare provider for specific conditions
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
