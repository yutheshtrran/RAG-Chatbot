#!/usr/bin/env python
"""
Initialize the backend environment:
1. Create necessary directories
2. Initialize the database
3. Load embedding model
"""
import os
import sys

# Add backend app to path
sys.path.insert(0, os.path.dirname(__file__))

def init_backend():
    """Initialize the backend."""
    print("🚀 Initializing RAG Chatbot Backend...")
    
    # Create directories
    backend_dir = os.path.dirname(__file__)
    embeddings_dir = os.path.join(backend_dir, "data", "embeddings")
    uploads_dir = os.path.join(backend_dir, "data", "uploads")
    
    os.makedirs(embeddings_dir, exist_ok=True)
    os.makedirs(uploads_dir, exist_ok=True)
    print(f"✅ Created directories: {embeddings_dir}, {uploads_dir}")
    
    # Initialize database
    from app.db_handler import init_db
    init_db()
    print("✅ Database initialized")
    
    # Load embedding model
    from app.embedder import embedding_model
    if embedding_model:
        print("✅ Embedding model loaded successfully")
    else:
        print("⚠️ Embedding model failed to load - will use fallback")
    
    # Test Gemini API connection
    try:
        import google.generativeai as genai
        from app.config import Config
        
        api_key = Config.GEMINI_API_KEY
        if api_key and api_key.strip():
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("models/gemini-2.5-pro")
            response = model.generate_content("Say 'Hello, I am ready to assist'")
            print("✅ Gemini API connection successful")
        else:
            print("⚠️ Gemini API key not configured")
    except Exception as e:
        print(f"⚠️ Gemini API test failed: {e}")
    
    print("\n✅ Backend initialization complete!")
    print("\nNext steps:")
    print("1. Install requirements: pip install -r app/requirements.txt")
    print("2. Run backend: python run.py")
    print("3. Run frontend: cd ../frontend && npm run dev")

if __name__ == "__main__":
    init_backend()
