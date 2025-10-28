import os
import pickle
from sentence_transformers import SentenceTransformer

PROCESSED_DIR = os.path.abspath("../data/processed")
EMBEDDINGS_DIR = os.path.abspath("../data/embeddings")
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

documents = []
filenames = []

model = SentenceTransformer("all-MiniLM-L6-v2")
processed_count = 0

for filename in os.listdir(PROCESSED_DIR):
    if filename.endswith((".txt", ".csv")):
        file_path = os.path.join(PROCESSED_DIR, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
            if text:
                documents.append(text)
                filenames.append(filename)
                processed_count += 1
        except Exception as e:
            print(f"Failed to read {filename}: {e}")

embeddings = model.encode(documents, convert_to_numpy=True) if documents else []

with open(os.path.join(EMBEDDINGS_DIR, "docs.pkl"), "wb") as f:
    pickle.dump({"documents": documents, "filenames": filenames}, f)

with open(os.path.join(EMBEDDINGS_DIR, "embeddings.pkl"), "wb") as f:
    pickle.dump(embeddings, f)

print(f"Processed {processed_count} documents. Embeddings generated successfully!")
