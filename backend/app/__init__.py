from flask import Flask
from flask_cors import CORS

from .routes import rag_routes
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # Enable CORS for your frontend
    app.register_blueprint(rag_routes, url_prefix="/api")
    return app
