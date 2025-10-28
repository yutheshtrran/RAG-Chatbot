import os
import logging
from typing import List
from .retriever import retrieve_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USE_GEMINI = False
GEN_MODEL = "models/gemini-2.5-pro"

# Try to configure Gemini API
try:
    import google.generativeai as genai
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        USE_GEMINI = True
        logger.info(f"Gemini API key detected — using Gemini model {GEN_MODEL}.")
    else:
        logger.info("Gemini API key not set — falling back to local generator.")
except Exception as e:
    logger.warning(f"Gemini not available ({e}) — using local generator.")

PROMPT_TEMPLATE = """
You are a clinical assistant. Use ONLY the provided sources (below) to answer the question.
If the answer cannot be found in the sources, say "I don't know" and recommend consulting a clinician.
Cite source numbers in brackets.

Sources:
{sources}

Question:
{question}

Answer concisely with citations.
"""

def _local_generate(question: str, sources: List[str]) -> str:
    if not sources:
        return "I don't know. No relevant documents are available; please consult a clinician."

    lines = [f"I found {len(sources)} relevant document(s). Excerpts:"]
    for i, s in enumerate(sources, start=1):
        excerpt = s.strip().replace("\n", " ")
        if len(excerpt) > 400:
            excerpt = excerpt[:400].rsplit(" ", 1)[0] + "..."
        lines.append(f"[{i}] {excerpt}")

    lines.append("\nReview sources for more details. Request 'summarize' for specific source IDs if needed.")
    return "\n".join(lines)

def _gemini_generate(question: str, sources: List[str], model_name: str = GEN_MODEL) -> str:
    try:
        model = genai.Model(model_name)
        sources_text = ""
        for i, s in enumerate(sources, start=1):
            excerpt = s.strip().replace("\n", " ")
            if len(excerpt) > 800:
                excerpt = excerpt[:800].rsplit(" ", 1)[0] + "..."
            sources_text += f"[{i}] {excerpt}\n"

        prompt = PROMPT_TEMPLATE.format(sources=sources_text, question=question)
        response = model.generate_content(prompt)

        return response.text.strip() if response and response.text else "Could not generate response."
    except Exception as e:
        logger.exception("Gemini generation failed: %s", e)
        return _local_generate(question, sources)

def get_rag_response(user_message: str, top_k: int = 3) -> str:
    if not user_message or not user_message.strip():
        return "Please provide a valid question."

    sources = retrieve_context(user_message, top_k=top_k)
    return _gemini_generate(user_message, sources) if USE_GEMINI else _local_generate(user_message, sources)
