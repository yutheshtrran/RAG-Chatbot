from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging

from .chatbot_engine import get_patient_rag_response
from .db_handler import add_patient, add_record, add_uploaded_document
from .document_parser import extract_patient_info

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
        patient_id = data.get("patient_id", "").strip() if data.get("patient_id") else None
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Message field is required."}), 400

        # patient_id is now optional - allows searching uploaded documents
        response = get_patient_rag_response(patient_id, message)
        return jsonify(response), 200

    except Exception as e:
        logger.exception("Error in /chat endpoint")
        return jsonify({"error": "An unexpected error occurred while processing your request."}), 500

# ================= Upload Patient Record =================
@rag_routes.route("/upload", methods=["POST"])
def upload():
    """
    Upload patient file(s) (PDF, TXT, CSV) with or without patient ID.
    
    Form fields:
        - patient_id: str (optional)
        - name: str (optional)
        - age: int (optional)
        - gender: str (optional)
        - files: file upload(s) (required)
    
    If patient_id not provided, extracts info from document automatically.
    """
    try:
        patient_id = request.form.get("patient_id", "").strip()
        name = request.form.get("name", "").strip()
        age = request.form.get("age")
        gender = request.form.get("gender", "").strip()
        uploaded_files = request.files.getlist("files")

        if not uploaded_files or len(uploaded_files) == 0:
            return jsonify({"error": "No files uploaded."}), 400

        saved_files = []
        extracted_patients = []

        for file in uploaded_files:
            if not file or file.filename == "":
                continue

            if not allowed_file(file.filename):
                logger.warning(f"Skipped file {file.filename}: Not allowed extension")
                continue

            try:
                filename = secure_filename(file.filename)
                
                # Read content for processing
                content = ""
                if filename.lower().endswith("pdf"):
                    try:
                        import pdfplumber
                        pdf_path = os.path.join(UPLOAD_DIR, filename)
                        file.save(pdf_path)
                        with pdfplumber.open(pdf_path) as pdf:
                            for page in pdf.pages:
                                content += page.extract_text() or ""
                    except Exception as e:
                        logger.warning(f"Failed to read PDF {filename}: {e}")
                else:
                    try:
                        with open("/tmp/" + filename, "w") as tmp_file:
                            file.save("/tmp/" + filename)
                        with open("/tmp/" + filename, "r", encoding="utf-8") as f:
                            content = f.read()
                    except Exception as e:
                        logger.warning(f"Failed to read file {filename}: {e}")
                
                if not content:
                    logger.warning(f"No content extracted from {filename}")
                    continue
                
                # If patient_id provided, use traditional approach
                if patient_id:
                    save_path = os.path.join(UPLOAD_DIR, f"{patient_id}_{filename}")
                    if not os.path.exists(save_path):
                        with open(save_path, "w") as f:
                            f.write(content)
                    
                    # Create patient if info provided
                    if name and age and gender:
                        add_patient(patient_id, name, int(age), gender)
                    
                    # Store in database
                    add_record(patient_id, filename, content)
                    saved_files.append((filename, patient_id))
                
                else:
                    # Extract patient info from document
                    extracted_info = extract_patient_info(content)
                    
                    # Save file
                    save_path = os.path.join(UPLOAD_DIR, filename)
                    if not os.path.exists(save_path):
                        with open(save_path, "w") as f:
                            f.write(content)
                    
                    # Store in uploaded_documents table
                    doc_id = add_uploaded_document(
                        filename=filename,
                        content=content,
                        extracted_name=extracted_info.get("name"),
                        extracted_age=int(extracted_info.get("age")) if extracted_info.get("age") else None,
                        extracted_gender=extracted_info.get("gender"),
                        extracted_id=extracted_info.get("patient_id")
                    )
                    
                    saved_files.append((filename, extracted_info.get("name", "Unknown")))
                    extracted_patients.append({
                        "doc_id": doc_id,
                        "filename": filename,
                        "name": extracted_info.get("name", "Unknown"),
                        "age": extracted_info.get("age"),
                        "gender": extracted_info.get("gender"),
                        "patient_id": extracted_info.get("patient_id")
                    })

            except Exception as e:
                logger.exception(f"Failed to save file {file.filename}")

        if not saved_files:
            return jsonify({"error": "No valid files were uploaded."}), 400

        response_data = {
            "status": "success",
            "message": f"Successfully uploaded {len(saved_files)} file(s)",
            "files_uploaded": saved_files
        }
        
        if extracted_patients:
            response_data["extracted_patients"] = extracted_patients
        
        return jsonify(response_data), 200

    except Exception as e:
        logger.exception("Error in /upload endpoint")
        return jsonify({"error": "An error occurred while uploading the file."}), 500
