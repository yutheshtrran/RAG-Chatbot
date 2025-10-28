import os
import logging
import textwrap
import numpy as np
import faiss
from typing import List

# Lazy-load transformers and FAISS required packages for vector search
try:
    from sentence_transformers import SentenceTransformer
    import torch
    CAN_USE_RAG = True
except ImportError:
    print("⚠️ WARNING: SentenceTransformer or PyTorch not installed. RAG will be disabled.")
    CAN_USE_RAG = False

# ================= Logging =================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= Gemini API Setup =================
try:
    import google.generativeai as genai

    # ===== Directly set your Gemini API key here =====
    GEMINI_API_KEY = "AIzaSyCZLETsVrvDtqqndm0aaV6uXdjAUyoZGWE"  # <--- Replace with your actual key

    if GEMINI_API_KEY and GEMINI_API_KEY.strip() and "YOUR_VALID_GEMINI_API_KEY" not in GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        USE_GEMINI = True
        GEM_MODEL = "models/gemini-2.5-pro"
        logger.info("✅ Gemini API key set directly — using model %s", GEM_MODEL)
    else:
        USE_GEMINI = False
        GEM_MODEL = None
        logger.warning("⚠️ Gemini API key not found/invalid — local-only mode.")
except Exception as e:
    USE_GEMINI = False
    GEM_MODEL = None
    logger.warning(f"⚠️ Gemini module not available ({e}) — using local generator.")

# ================= Local RAG Index Setup =================
# 1. Sample internal documents
INTERNAL_DOCUMENTS = [
    "Patient Jane Doe (ID 4452) is currently prescribed Fingolimod 0.5mg daily for Relapsing-Remitting Multiple Sclerosis (RRMS). Initiated 2024-05-10.",
    "Common side effects of Fingolimod include bradycardia, macular edema, and mild headache. It requires a first-dose observation (FDO).",
    "Clinical protocol for RRMS: Start with a moderate-efficacy DMT (e.g., Interferon Beta, Glatiramer Acetate) then escalate to high-efficacy if breakthrough activity occurs.",
    "Dr. Smith recommends yearly MRI scans and quarterly blood tests for all MS patients on disease-modifying agents.",
    "The official hospital drug formulary lists Humira (Adalimumab) as the preferred TNF-alpha inhibitor for Rheumatoid Arthritis (RA) when Methotrexate fails."
]

# 2. Initialize Model and Index
GLOBAL_MODEL = None
GLOBAL_INDEX = None
MODEL_PATH = "all-MiniLM-L6-v2"

if CAN_USE_RAG:
    try:
        logger.info("⏳ Initializing Sentence Transformer and FAISS Index...")
        GLOBAL_MODEL = SentenceTransformer(MODEL_PATH)
        embeddings = GLOBAL_MODEL.encode(INTERNAL_DOCUMENTS, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        GLOBAL_INDEX = faiss.IndexFlatL2(dimension)
        GLOBAL_INDEX.add(embeddings.astype('float32'))
        logger.info(f"✅ FAISS Index created with {len(INTERNAL_DOCUMENTS)} documents.")
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG components: {e}")
        CAN_USE_RAG = False

# ================= Local RAG Retrieval =================
def retrieve_context(query: str, top_k: int = 3) -> List[str]:
    if not CAN_USE_RAG or GLOBAL_INDEX is None:
        return []
    try:
        query_embedding = GLOBAL_MODEL.encode([query], convert_to_numpy=True).astype('float32')
        D, I = GLOBAL_INDEX.search(query_embedding, top_k)
        sources = [INTERNAL_DOCUMENTS[i] for i in I[0] if i < len(INTERNAL_DOCUMENTS)]
        return sources
    except Exception as e:
        logger.error(f"Error during FAISS retrieval: {e}")
        return []

def _local_generate(question: str, sources: List[str]) -> str:
    if not sources:
        return "I don't know. No relevant internal documents found — please consult a clinician."
    lines = ["### 🩺 Answer based on internal documents:\n"]
    for i, s in enumerate(sources, start=1):
        excerpt = s.strip().replace("\n", " ")
        if len(excerpt) > 600:
            excerpt = excerpt[:600].rsplit(" ", 1)[0] + "..."
        wrapped = textwrap.fill(excerpt, width=100)
        lines.append(f"**Document {i}:**\n* {wrapped}\n\n")
    return "\n".join(lines)

# ================= Gemini Generator =================
def _gemini_generate(question: str, local_summary: str = None) -> str:
    if not USE_GEMINI:
        return "⚠️ Gemini not configured or API key missing."
    try:
        model = genai.GenerativeModel(GEM_MODEL)
        if local_summary and "I don't know" not in local_summary:
            context_snippet = " ".join(local_summary.split()[:500])
            prompt = f"""
You are a clinical assistant AI. Base your answer PRIMARILY on the provided 'Internal hospital records', then supplement with general knowledge for context.

Internal hospital records:
{context_snippet}

Question: {question}

Please provide a clear, structured answer in Markdown:
- Rephrase the answer clearly, starting with the patient-specific details if found in the records.
- Include bullet points and concise explanation.
- **Do not invent details not present in the records.**
"""
        else:
            prompt = f"""
You are a clinical assistant AI.

Internal documents did not contain relevant information for this question. You must use general medical knowledge.

Question: {question}

Please provide a complete, clinically accurate answer using general medical knowledge.
- Format in Markdown.
- Use bullet points.
- Always include a strong disclaimer that this is general, non-patient-specific information.
"""
        response = model.generate_content(prompt)
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        else:
            return "⚠️ Gemini did not generate a response."
    except Exception as e:
        logger.exception("Gemini generation failed: %s", e)
        return f"⚠️ Gemini error: {str(e)}"

# ================= Main RAG + Gemini Logic =================
def get_rag_response(user_message: str, top_k: int = 3) -> dict:
    if not user_message or not user_message.strip():
        return {"reply": "Please provide a valid medical question."}
    try:
        sources = retrieve_context(user_message, top_k=top_k)
        local_answer = _local_generate(user_message, sources)
        if "I don't know" in local_answer:
            if USE_GEMINI:
                logger.info("💡 Local retrieval failed — using Gemini fallback.")
                gemini_answer = _gemini_generate(user_message)
                return {"reply": gemini_answer}
            else:
                return {"reply": local_answer}
        if USE_GEMINI:
            gemini_enhanced_answer = _gemini_generate(user_message, local_summary=local_answer)
            return {"reply": gemini_enhanced_answer}
        return {"reply": local_answer}
    except Exception as e:
        logger.exception("Error generating RAG response: %s", e)
        return {"reply": "⚠️ Error occurred while generating the response."}

# ================= Standalone Test =================
if __name__ == "__main__":
    print("\n=============================================")
    print("      Hybrid RAG + Gemini Clinical Assistant")
    print("=============================================")
    if not CAN_USE_RAG:
        print("NOTE: RAG is DISABLED due to missing dependencies.")
    if not USE_GEMINI:
        print("NOTE: GEMINI is DISABLED due to missing/invalid API key.")
    print("=============================================")
    
    while True:
        q = input("\nEnter medical question (or 'exit'): ")
        if q.lower() == "exit":
            break
        result = get_rag_response(q)
        print("\n" + "*"*20 + " RESPONSE " + "*"*20)
        print(result["reply"])
        print("*"*50)
    print("Exiting.")
