from flask import Flask
from flask_cors import CORS
from .routes import rag_routes
from .config import Config

def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend
    CORS(app)

    # Register blueprint for RAG API
    app.register_blueprint(rag_routes, url_prefix="/api")

    return app
