from .db_handler import get_patient_records
from .embedder import get_embedding as local_get_embedding
import numpy as np
import logging

# ================= Logging =================
logger = logging.getLogger(__name__)


def retrieve_patient_context(patient_id: str, query: str, top_k: int = 3):
    """
    Retrieve the top-k most relevant patient records based on the query.

    Args:
        patient_id (str): ID of the patient.
        query (str): Doctor's question or prompt.
        top_k (int): Number of top relevant records to return.

    Returns:
        List[str]: Top-k relevant patient record contents.
    """
    try:
        # --- Load patient records ---
        records = get_patient_records(patient_id)
        if not records:
            logger.info(f"No records found for patient_id={patient_id}")
            return []

        # --- Convert records to text list ---
        documents = [r["content"] for r in records]

        # --- Compute embeddings ---
        embeddings = np.array([local_get_embedding(doc) for doc in documents], dtype="float32")
        query_vec = np.array(local_get_embedding(query), dtype="float32").reshape(1, -1)

        # --- Handle zero vectors ---
        if np.linalg.norm(query_vec) == 0 or np.any(np.linalg.norm(embeddings, axis=1) == 0):
            logger.warning("Zero vector encountered during similarity computation")
            return documents[:top_k]

        # --- Compute cosine similarity ---
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        query_norm = np.linalg.norm(query_vec)
        sims = (embeddings / norms) @ (query_vec / query_norm).T

        # --- Retrieve top-k indices ---
        top_idx = np.argsort(-sims.flatten())[:top_k]

        return [documents[i] for i in top_idx]

    except Exception as e:
        logger.exception(f"Error retrieving patient context for patient_id={patient_id}")
        return []
