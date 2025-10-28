import os

class Config:
    """
    Flask configuration.
    Environment-friendly and extendable.
    """
    DEBUG = True
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecretkey")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", None)

    EMBEDDINGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "embeddings"))
    DOCS_FILE = os.path.join(EMBEDDINGS_DIR, "docs.pkl")
    EMBEDDINGS_FILE = os.path.join(EMBEDDINGS_DIR, "embeddings.pkl")
