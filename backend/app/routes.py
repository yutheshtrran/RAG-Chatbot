from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging

from .chatbot_engine import get_patient_rag_response
from .db_handler import add_patient, add_record

# ================= Blueprint =================
rag_routes = Blueprint("rag_routes", __name__)

# ================= Logging =================
logger = logging.getLogger(__name__)

# ================= Config =================
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf", "txt", "csv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ================= Health Check =================
@rag_routes.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# ================= Chat Endpoint =================
@rag_routes.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        patient_id = data.get("patient_id", "").strip()
        message = data.get("message", "").strip()

        if not patient_id or not message:
            return jsonify({"error": "Both 'patient_id' and 'message' fields are required."}), 400

        response = get_patient_rag_response(patient_id, message)
        return jsonify(response), 200

    except Exception as e:
        logger.exception("Error in /chat endpoint")
        return jsonify({"error": "An unexpected error occurred while processing your request."}), 500

# ================= Upload Patient Record =================
@rag_routes.route("/upload", methods=["POST"])
def upload():
    """
    Upload patient file(s) (PDF, TXT, CSV) and optionally create patient entry.
    Form fields:
        - patient_id: str
        - name: str (optional)
        - age: int (optional)
        - gender: str (optional)
        - files: file upload(s)
    """
    try:
        patient_id = request.form.get("patient_id", "").strip()
        name = request.form.get("name", "").strip()
        age = request.form.get("age")
        gender = request.form.get("gender", "").strip()
        uploaded_files = request.files.getlist("files")

        if not patient_id:
            return jsonify({"error": "patient_id is required."}), 400
        if not uploaded_files or len(uploaded_files) == 0:
            return jsonify({"error": "No files uploaded."}), 400

        # Create patient if info provided
        if name and age and gender:
            add_patient(patient_id, name, int(age), gender)

        saved_files = []

        for file in uploaded_files:
            if not file or file.filename == "":
                continue

            if not allowed_file(file.filename):
                logger.warning(f"Skipped file {file.filename}: Not allowed extension")
                continue

            try:
                filename = secure_filename(file.filename)
                save_path = os.path.join(UPLOAD_DIR, f"{patient_id}_{filename}")
                file.save(save_path)
                saved_files.append(filename)  # Append immediately after saving

                # Read content for DB storage
                content = ""
                if filename.lower().endswith("pdf"):
                    try:
                        import pdfplumber
                        with pdfplumber.open(save_path) as pdf:
                            for page in pdf.pages:
                                content += page.extract_text() or ""
                    except Exception as e:
                        logger.warning(f"Failed to read PDF {filename}: {e}")
                else:
                    try:
                        with open(save_path, "r", encoding="utf-8") as f:
                            content = f.read()
                    except Exception as e:
                        logger.warning(f"Failed to read file {filename}: {e}")

                # Store in database
                add_record(patient_id, filename, content)

            except Exception as e:
                logger.exception(f"Failed to save file {file.filename}")

        if not saved_files:
            return jsonify({"error": "No valid files were uploaded."}), 400

        return jsonify({
            "status": "success",
            "message": f"Files uploaded and saved for patient {patient_id}: {', '.join(saved_files)}"
        }), 200

    except Exception as e:
        logger.exception("Error in /upload endpoint")
        return jsonify({"error": "An error occurred while uploading the file."}), 500
