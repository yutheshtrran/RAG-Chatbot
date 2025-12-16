# RAG Chatbot - Setup & Deployment Guide

## 📋 Project Overview

This is a **Retrieval-Augmented Generation (RAG) Chatbot** that:
- Allows doctors to upload patient medical records (TXT, PDF, CSV)
- Answers questions about patient medical history using AI
- Uses **Gemini API** for intelligent response generation
- Uses **sentence-transformers** for semantic search
- Provides a modern React frontend

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Setup

#### 1. Install Python Dependencies
```bash
cd backend
pip install -r app/requirements.txt
```

#### 2. Initialize Backend (Optional - Auto-run first time)
```bash
python init.py
```

This will:
- Create necessary directories
- Initialize SQLite database
- Load embedding model
- Test Gemini API connection

#### 3. Run Backend Server
```bash
python run.py
```

Server will start on: **http://127.0.0.1:5000**

---

### Frontend Setup

#### 1. Install Dependencies
```bash
cd frontend
npm install
```

#### 2. Run Development Server
```bash
npm run dev
```

Frontend will be available on: **http://127.0.0.1:5173**

---

## 📝 How to Use

### 1. Upload Patient Records
1. Go to Dashboard → "Upload Patient Records"
2. Fill in:
   - **Patient ID** (required): e.g., "001", "P002"
   - **Name** (optional): e.g., "John Doe"
   - **Age** (optional): e.g., "45"
   - **Gender** (optional): "Male", "Female", or "Other"
3. Upload medical files (TXT, PDF, CSV)
4. Click "Upload"

### 2. Ask Questions About Patients
1. In the chat box, ask questions about patients:
   - "Patient 001 what is their diagnosis?"
   - "Patient P002 show me their medical history"
   - "Patient 003 what medications are they taking?"

2. The chatbot will:
   - Retrieve relevant patient records
   - Generate an AI-powered answer using Gemini
   - Display formatted response with sources

---

## 🔧 API Endpoints

### Chat Endpoint
**POST** `/api/chat`

Request:
```json
{
  "patient_id": "001",
  "message": "What is their medical history?"
}
```

Response:
```json
{
  "reply": "Based on patient records, [AI-generated answer]"
}
```

### Upload Endpoint
**POST** `/api/upload`

Form Data:
- `patient_id` (required): Patient ID
- `name` (optional): Patient name
- `age` (optional): Patient age
- `gender` (optional): Patient gender
- `files` (required): Patient record files

Response:
```json
{
  "status": "success",
  "message": "Files uploaded and saved for patient 001"
}
```

### Health Check
**GET** `/api/health`

Response:
```json
{
  "status": "ok"
}
```

---

## 🗂️ Project Structure

```
RAG-Chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── main.py              # Entry point
│   │   ├── routes.py            # API endpoints
│   │   ├── chatbot_engine.py    # RAG logic & Gemini integration
│   │   ├── retriever.py         # Semantic search & retrieval
│   │   ├── embedder.py          # Embedding generation
│   │   ├── db_handler.py        # SQLite database operations
│   │   ├── config.py            # Configuration
│   │   ├── requirements.txt     # Python dependencies
│   │   └── ...
│   ├── data/
│   │   ├── uploads/             # Uploaded patient records
│   │   ├── embeddings/          # Cached embeddings
│   │   └── patient_records.db   # SQLite database
│   ├── .env                     # Environment variables
│   ├── init.py                  # Initialization script
│   └── run.py                   # Development server
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main app component
│   │   ├── api.js               # API client functions
│   │   ├── components/
│   │   │   ├── chatWindow.jsx   # Chat interface
│   │   │   ├── PatientUploader.jsx
│   │   │   └── ...
│   │   └── pages/
│   │       ├── Dashboard.jsx
│   │       ├── Evaluation.jsx
│   │       └── About.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── ...
```

---

## 🔑 Configuration

### Environment Variables (.env)
```
GEMINI_API_KEY=AIzaSyAnmUhxiPahrebRQxj36OwgPf7ILtlTAqs
FLASK_SECRET_KEY=your-secret-key
DEBUG=True
```

### Backend Config (backend/app/config.py)
- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Flask secret key
- `GEMINI_API_KEY`: Google Gemini API key (hardcoded + .env override)

---

## 🔍 How RAG Works

### 1. **Embedding Generation**
- Uses `sentence-transformers` (all-MiniLM-L6-v2)
- Converts text documents to 384-dimensional vectors
- Semantic similarity-based retrieval

### 2. **Document Retrieval**
- When a question is asked, it's converted to embeddings
- Cosine similarity search finds most relevant patient records
- Top-3 most relevant documents are retrieved

### 3. **AI Response Generation**
- Retrieved context is sent to Google Gemini 2.5 Pro
- Gemini generates comprehensive, clinically-aware answers
- Responses include source citations

### 4. **Database Storage**
- SQLite stores patient records and metadata
- Supports relationships between patients and multiple records
- Automatic timestamp tracking

---

## ✅ Testing

### Test the Backend API
```bash
# Test health check
curl http://127.0.0.1:5000/api/health

# Test chat (requires patient to exist)
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"patient_id":"001","message":"What is the patient history?"}'
```

### Test Upload
```bash
curl -X POST http://127.0.0.1:5000/api/upload \
  -F "patient_id=001" \
  -F "name=John Doe" \
  -F "age=45" \
  -F "gender=Male" \
  -F "files=@patient_file.txt"
```

---

## 🐛 Troubleshooting

### Backend won't start
- **Error**: `ModuleNotFoundError: No module named 'google.generativeai'`
  - **Fix**: Run `pip install -r app/requirements.txt`

- **Error**: `Gemini API key missing`
  - **Fix**: Check `.env` file has `GEMINI_API_KEY` set correctly

### Frontend can't connect to backend
- **Error**: `⚠️ Could not connect to the backend`
  - **Fix**: Ensure backend is running on `http://127.0.0.1:5000`
  - **Fix**: Check CORS is enabled (it is by default)

### Embeddings not working
- **Error**: Zero vectors returned
  - **Fix**: Sentence-transformer model should auto-download on first use

### Patient not found
- **Error**: "Patient ID 'xxx' not found in database"
  - **Fix**: Upload patient records first using the uploader

---

## 📊 Performance Tips

1. **Embedding Caching**: Embeddings are computed on-the-fly (can be cached)
2. **Top-K Selection**: Currently returns top-3 results (adjustable in chatbot_engine.py)
3. **Model Size**: Using lightweight "all-MiniLM-L6-v2" for fast inference
4. **Gemini Model**: Using gemini-2.5-pro for accurate medical context understanding

---

## 🔐 Security Considerations

- [ ] Change `FLASK_SECRET_KEY` in production
- [ ] Use environment variables for API keys (not hardcoded)
- [ ] Implement authentication for patient data access
- [ ] Use HTTPS in production
- [ ] Sanitize file uploads (already done with `secure_filename`)
- [ ] Add rate limiting to API endpoints
- [ ] Validate and sanitize all user inputs

---

## 📈 Future Enhancements

- [ ] Add authentication/authorization
- [ ] Implement caching for embeddings
- [ ] Support multiple file formats (DOCX, XLS, etc.)
- [ ] Add conversation history
- [ ] Implement feedback loop for response quality
- [ ] Add support for multiple AI models
- [ ] Create admin dashboard for analytics
- [ ] Add multi-language support
- [ ] Implement HIPAA compliance
- [ ] Add audit logging

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review console logs (backend: terminal, frontend: browser dev tools)
3. Verify API endpoints are responding with `/health` endpoint
4. Check `.env` file configuration

---

## 📄 License

Your License Here

---

**Happy Chatting! 🚀**
