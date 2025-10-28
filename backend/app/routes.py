from flask import Blueprint, request, jsonify
from .chatbot_engine import get_rag_response

rag_routes = Blueprint("rag_routes", __name__)

@rag_routes.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@rag_routes.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Message cannot be empty."}), 400

        reply = get_rag_response(message)
        return jsonify({"reply": reply}), 200

    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500
