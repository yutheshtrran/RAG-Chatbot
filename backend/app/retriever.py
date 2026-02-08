from .db_handler import get_patient_records, search_uploaded_documents, get_all_documents_content
from .embedder import get_embedding as local_get_embedding
import numpy as np
import logging

# ================= Logging =================
logger = logging.getLogger(__name__)


def retrieve_patient_context(patient_id: str, query: str, top_k: int = 3):
    """
    Retrieve the top-k most relevant patient records based on the query.
    Falls back to searching uploaded documents if patient not found.

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
        
        # If no records for this patient_id, search uploaded documents
        if not records:
            logger.info(f"No patient records found for patient_id={patient_id}, searching uploaded documents")
            
            # Search uploaded documents by patient_id or name
            uploaded = search_uploaded_documents(patient_id)
            if uploaded:
                documents = [doc["content"] for doc in uploaded]
            else:
                # If no specific match, search by query keywords
                documents = []
                logger.info(f"No uploaded documents found for {patient_id}")
                return []
        else:
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


def retrieve_global_context(query: str, top_k: int = 3):
    """
    Retrieve top-k relevant documents from ALL patients/documents based on query.
    Used when searching across all uploaded documents.
    
    Args:
        query (str): Search query.
        top_k (int): Number of top results to return.
    
    Returns:
        List[str]: Top-k relevant document contents.
    """
    try:
        # Get all document contents
        documents = get_all_documents_content()
        
        if not documents:
            logger.info("No documents found in database")
            return []
        
        # Compute embeddings
        embeddings = np.array([local_get_embedding(doc) for doc in documents], dtype="float32")
        query_vec = np.array(local_get_embedding(query), dtype="float32").reshape(1, -1)
        
        # Handle zero vectors
        if np.linalg.norm(query_vec) == 0 or np.any(np.linalg.norm(embeddings, axis=1) == 0):
            logger.warning("Zero vector encountered during global similarity computation")
            return documents[:top_k]
        
        # Compute cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        query_norm = np.linalg.norm(query_vec)
        sims = (embeddings / norms) @ (query_vec / query_norm).T
        
        # Retrieve top-k indices
        top_idx = np.argsort(-sims.flatten())[:top_k]
        
        return [documents[i] for i in top_idx]
    
    except Exception as e:
        logger.exception(f"Error retrieving global context for query={query}")
        return []
