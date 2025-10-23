import numpy as np

# Pretend this retrieves similar docs from a local store
def retrieve_context(query_vec, top_k=2):
    # In a real app, you’d query FAISS/Chroma here
    dummy_docs = [
        "Document 1: Clinical data about patient A...",
        "Document 2: Recent study on RAG in medicine..."
    ]
    return dummy_docs[:top_k]
