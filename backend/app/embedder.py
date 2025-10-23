import numpy as np

# Minimal fake embedder (replace with actual model later)
def get_embedding(text):
    np.random.seed(abs(hash(text)) % (10 ** 8))
    return np.random.rand(768).tolist()
