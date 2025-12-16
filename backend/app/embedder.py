import numpy as np
import logging
from sentence_transformers import SentenceTransformer

# ================= Logging =================
logger = logging.getLogger(__name__)

# ================= Model Initialization =================
# Load the model once when the module is imported
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    logger.info("Embedding model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load embedding model: {e}")
    embedding_model = None

def get_embedding(text: str) -> list:
    """
    Generate an embedding for a given text using SentenceTransformer.
    Falls back to random embedding if model is not available.
    
    Args:
        text (str): The text to embed.
    
    Returns:
        list: A 384-dimensional embedding vector.
    """
    if not text or not isinstance(text, str):
        # Return zero vector for empty input
        return np.zeros(384).tolist()
    
    try:
        if embedding_model:
            # Use SentenceTransformer for better embeddings
            embedding = embedding_model.encode(text.strip(), convert_to_numpy=True)
            return embedding.tolist()
    except Exception as e:
        logger.warning(f"Error generating embedding: {e}. Falling back to random.")
    
    # Fallback: deterministic pseudo-embedding
    seed = abs(hash(text)) % (10 ** 8)
    np.random.seed(seed)
    return np.random.rand(384).tolist()

