import os
from dotenv import load_dotenv

# Load values from .env
load_dotenv()

class Config:
    """
    Flask configuration.
    Environment-friendly and extendable.
    """
    DEBUG = True
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

    # ================= Gemini API Key =================
    # Must be supplied via .env or system environment variables
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBR4QfAYCH8hDBjKvdiYSvTjjyx1Fg7IEA")

    # ================= Embeddings / Data =================
    EMBEDDINGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "embeddings"))
    DOCS_FILE = os.path.join(EMBEDDINGS_DIR, "docs.pkl")
    EMBEDDINGS_FILE = os.path.join(EMBEDDINGS_DIR, "embeddings.pkl")
