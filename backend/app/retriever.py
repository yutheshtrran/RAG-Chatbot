import os
import pickle
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer
    SENTE_TRANSFORMER_AVAILABLE = True
except ImportError:
    SENTE_TRANSFORMER_AVAILABLE = False

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

try:
    from .embedder import get_embedding as local_get_embedding
    LOCAL_EMBEDDER_AVAILABLE = True
except ImportError:
    LOCAL_EMBEDDER_AVAILABLE = False

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "embeddings"))
EMBEDDINGS_FILE = os.path.join(BASE_DIR, "embeddings.pkl")
DOCS_FILE = os.path.join(BASE_DIR, "docs.pkl")

_embeddings = None
_documents = []
_index = None
_dim = None
_sbert_model = None

def _load_store():
    global _embeddings, _documents, _index, _dim, _sbert_model

    if _embeddings is not None and _documents:
        return

    if not os.path.exists(EMBEDDINGS_FILE) or not os.path.exists(DOCS_FILE):
        logger.warning("Embeddings/docs missing — retrieval will fallback.")
        _embeddings = np.array([])
        _documents = []
        _index = None
        return

    with open(EMBEDDINGS_FILE, "rb") as f:
        _embeddings = pickle.load(f)
    with open(DOCS_FILE, "rb") as f:
        docs_data = pickle.load(f)
        if isinstance(docs_data, dict) and "documents" in docs_data:
            _documents = docs_data["documents"]
        elif isinstance(docs_data, list):
            _documents = docs_data
        else:
            raise ValueError("Unexpected format for docs.pkl")

    _embeddings = np.array(_embeddings, dtype="float32") if isinstance(_embeddings, list) else _embeddings
    if _embeddings.size == 0:
        logger.warning("Embeddings empty.")
        _index = None
        return

    _dim = _embeddings.shape[1]

    if FAISS_AVAILABLE:
        emb_norm = _embeddings.copy()
        faiss.normalize_L2(emb_norm)
        index = faiss.IndexFlatIP(_dim)
        index.add(emb_norm)
        _index = index
    else:
        _index = None

    if SENTE_TRANSFORMER_AVAILABLE and _sbert_model is None:
        try:
            _sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Loaded SBERT model for queries.")
        except Exception as e:
            logger.warning("Failed to load SBERT: %s", e)
            _sbert_model = None

def _embed_query(query: str):
    if SENTE_TRANSFORMER_AVAILABLE:
        global _sbert_model
        if _sbert_model is None:
            try:
                _sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception as e:
                logger.warning("SBERT init failed: %s", e)
                _sbert_model = None
        if _sbert_model:
            return _sbert_model.encode([query], convert_to_numpy=True).astype("float32")

    if LOCAL_EMBEDDER_AVAILABLE:
        vec = local_get_embedding(query)
        return np.array(vec, dtype="float32").reshape(1, -1)

    raise ImportError("No embedding method available.")

def retrieve_context(query: str, top_k: int = 3):
    _load_store()
    if not _documents or (_embeddings is None) or (_embeddings.size == 0):
        return []

    try:
        qvec = _embed_query(query)
    except Exception as e:
        logger.warning("Query embedding failed: %s", e)
        return _documents[:top_k]

    if _index is not None:
        qnorm = qvec.copy()
        faiss.normalize_L2(qnorm)
        distances, indices = _index.search(qnorm, top_k)
        return [_documents[i] for i in indices[0] if i < len(_documents)]

    emb_norms = _embeddings / (np.linalg.norm(_embeddings, axis=1, keepdims=True) + 1e-10)
    qnorm = qvec / (np.linalg.norm(qvec, axis=1, keepdims=True) + 1e-10)
    sims = (emb_norms @ qnorm.T).squeeze()
    top_idxs = np.argsort(-sims)[:top_k]
    return [_documents[i] for i in top_idxs]
