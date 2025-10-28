import os
import pickle
from sentence_transformers import SentenceTransformer

# PDF library
try:
    import fitz  # PyMuPDF
    PDF_LIB = "fitz"
except ImportError:
    try:
        import pdfplumber
        PDF_LIB = "pdfplumber"
    except ImportError:
        PDF_LIB = None

if PDF_LIB is None:
    raise ImportError("Install PyMuPDF (`pip install PyMuPDF`) or pdfplumber (`pip install pdfplumber`)")

PROCESSED_DIR = os.path.abspath("../data/processed")
EMBEDDINGS_DIR = os.path.abspath("../data/embeddings")
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

def extract_pdf_text(file_path):
    text = ""
    if PDF_LIB == "fitz":
        import fitz
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    elif PDF_LIB == "pdfplumber":
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + " "
    return text.strip()

# Initialize the model
model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
filenames = []
processed_count = 0

for filename in os.listdir(PROCESSED_DIR):
    file_path = os.path.join(PROCESSED_DIR, filename)
    text = ""
    try:
        if filename.endswith((".txt", ".csv")):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
        elif filename.endswith(".pdf"):
            text = extract_pdf_text(file_path)

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
