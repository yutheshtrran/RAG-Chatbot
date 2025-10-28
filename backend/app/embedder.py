import numpy as np

def get_embedding(text: str) -> list:
    """
    Generate a deterministic pseudo-embedding for a given text.
    Fallback stub; replace with a real embedding model in production.
    """
    seed = abs(hash(text)) % (10 ** 8)
    np.random.seed(seed)
    return np.random.rand(768).tolist()
