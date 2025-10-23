from flask import Flask, jsonify
from routes import api_bp

app = Flask(__name__)

# Register API routes
app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
