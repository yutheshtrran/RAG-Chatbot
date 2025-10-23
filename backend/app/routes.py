from flask import Blueprint, request, jsonify
from .chatbot_engine import get_ai_response  # Import your chatbot logic

rag_routes = Blueprint('rag_routes', __name__)

# Health check endpoint
@rag_routes.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# Chat endpoint
@rag_routes.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"reply": "Please send a valid message."})
    
    # Get AI response from your chatbot engine
    ai_reply = get_ai_response(user_message)
    
    return jsonify({"reply": ai_reply})
