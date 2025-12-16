# 🏥 RAG-Based Clinical Chatbot

A production-ready **Retrieval-Augmented Generation (RAG)** chatbot system for querying patient medical records using artificial intelligence. This system allows healthcare professionals to upload patient documentation and receive intelligent, context-aware answers about patient care.

## ✨ Key Features

- **📤 Patient Record Upload**: Upload medical documents (TXT, PDF, CSV) for any patient
- **🤖 AI-Powered Responses**: Uses Google Gemini 2.5 Pro for intelligent analysis
- **🔍 Semantic Search**: Retrieves most relevant patient records using embeddings
- **📊 Patient Management**: SQLite database for secure patient data storage
- **🎨 Modern UI**: React-based frontend with real-time chat interface
- **🔐 CORS Enabled**: Secure cross-origin communication
- **⚡ Fast Embeddings**: Uses lightweight sentence-transformers (all-MiniLM-L6-v2)

## 🎯 Use Cases

- **Doctors**: Quickly access patient medical history and summaries
- **Clinicians**: Ask specific clinical questions about patient conditions
- **Researchers**: Analyze aggregated patient data patterns
- **Administrative Staff**: Retrieve patient information efficiently

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
Node.js 16+
```

### Backend Setup (< 5 minutes)
```bash
cd backend
pip install -r app/requirements.txt
python init.py
python run.py
```

Backend runs on: **http://127.0.0.1:5000**

### Frontend Setup (< 3 minutes)
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: **http://127.0.0.1:5173**

### Create Sample Data (Optional)
```bash
python create_sample_data.py
```

Then test with questions like:
- "Patient 001 what is their diagnosis?"
- "Patient 002 what medications are they taking?"

---

## 📖 How It Works

### Architecture

```
User Question
     ↓
[Frontend] → Extracts Patient ID
     ↓
[Backend API] → /api/chat endpoint
     ↓
[Embeddings] → Convert question to vector
     ↓
[Retriever] → Find top-3 most relevant patient records
     ↓
[Gemini AI] → Generate answer with retrieved context
     ↓
[Response] → Formatted markdown answer with sources
     ↓
[User] ← Displays in chat window
```

### RAG Pipeline

1. **Input Processing**: User question is extracted with patient ID
2. **Embedding**: Question converted to 384-dimensional vector
3. **Retrieval**: Cosine similarity search finds matching records
4. **Augmentation**: Top results are provided as context
5. **Generation**: Gemini AI generates answer using context + general knowledge
6. **Output**: Markdown-formatted response displayed to user

---

## 📁 Project Structure

```
RAG-Chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py              # Flask app factory
│   │   ├── main.py                  # Entry point (run this)
│   │   ├── routes.py                # API endpoints
│   │   ├── chatbot_engine.py        # RAG logic + Gemini integration
│   │   ├── retriever.py             # Semantic search using embeddings
│   │   ├── embedder.py              # Embedding generation (sentence-transformers)
│   │   ├── db_handler.py            # SQLite database operations
│   │   ├── config.py                # Configuration and API keys
│   │   ├── requirements.txt         # Python dependencies
│   │   └── ...
│   ├── data/
│   │   ├── uploads/                 # Uploaded patient medical documents
│   │   ├── embeddings/              # Cache for embeddings (if implemented)
│   │   └── patient_records.db       # SQLite database (auto-created)
│   ├── .env                         # Environment variables (Gemini API key)
│   ├── init.py                      # Backend initialization script
│   ├── run.py                       # Development server launcher
│   └── Dockerfile                   # Docker configuration
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # Main app component
│   │   ├── api.js                   # API client (sendMessage, uploadFiles)
│   │   ├── components/
│   │   │   ├── chatWindow.jsx       # Chat interface with markdown rendering
│   │   │   ├── PatientUploader.jsx  # File upload form
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── ...
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx        # Main dashboard
│   │   │   ├── Evaluation.jsx       # Evaluation metrics
│   │   │   └── About.jsx            # Documentation
│   │   ├── main.jsx
│   │   └── App.css
│   ├── package.json
│   ├── vite.config.js               # Vite configuration
│   ├── tailwind.config.js           # Tailwind CSS configuration
│   └── ...
│
├── evaluation/
│   ├── evaluation.py
│   ├── evaluation_data.json
│   └── metrics_results.json
│
├── SETUP_GUIDE.md                   # Detailed setup instructions
├── create_sample_data.py             # Script to populate test data
└── README.md                         # This file
```

---

## 🔧 API Endpoints

### 1. Chat with Patient Records
**POST** `/api/chat`

**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "001",
    "message": "What is the patient medical history?"
  }'
```

**Response:**
```json
{
  "reply": "Based on patient 001's records, they have a history of Type 2 Diabetes (since 2015)..."
}
```

---

### 2. Upload Patient Records
**POST** `/api/upload`

**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/upload \
  -F "patient_id=001" \
  -F "name=John Doe" \
  -F "age=55" \
  -F "gender=Male" \
  -F "files=@medical_record.txt" \
  -F "files=@lab_results.pdf"
```

**Response:**
```json
{
  "status": "success",
  "message": "Files uploaded and saved for patient 001: medical_record.txt, lab_results.pdf"
}
```

---

### 3. Health Check
**GET** `/api/health`

**Response:**
```json
{
  "status": "ok"
}
```

---

## 🔑 Configuration

### Environment Variables (backend/.env)
```env
GEMINI_API_KEY=AIzaSyAnmUhxiPahrebRQxj36OwgPf7ILtlTAqs
FLASK_SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Backend Configuration (backend/app/config.py)
- `DEBUG`: Enable/disable Flask debug mode
- `SECRET_KEY`: Session secret key
- `GEMINI_API_KEY`: Google Gemini API key (from environment or hardcoded)
- `EMBEDDINGS_DIR`: Directory for storing embeddings
- `DOCS_FILE`: Path to pickled documents cache
- `EMBEDDINGS_FILE`: Path to pickled embeddings cache

---

## 🧠 AI Models Used

1. **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
   - 384-dimensional vectors
   - Fast inference (<10ms per document)
   - Good semantic understanding
   - Lightweight (~80MB)

2. **LLM**: `Google Gemini 2.5 Pro`
   - State-of-the-art language understanding
   - Medical knowledge aware
   - Context-aware response generation
   - Supports markdown formatting

---

## 📊 Database Schema

### Patients Table
```sql
CREATE TABLE patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT CHECK(gender IN ('Male', 'Female', 'Other'))
);
```

### Records Table
```sql
CREATE TABLE records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    filename TEXT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);
```

---

## 🧪 Testing

### Test Backend API
```bash
# Health check
curl http://127.0.0.1:5000/api/health

# Chat endpoint (requires patient in database first)
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id":"001",
    "message":"What is their diagnosis?"
  }'
```

### Create Test Data
```bash
python create_sample_data.py
```

Creates 3 sample patients with realistic medical records:
- **Patient 001**: John Doe (cardiac issues)
- **Patient 002**: Emily Davis (healthy)
- **Patient 003**: Jane Smith (geriatric)

---

## 🐛 Troubleshooting

### Issue: "Could not connect to the backend"
**Solution:**
```bash
# Ensure backend is running
cd backend
python run.py

# Check if server is responding
curl http://127.0.0.1:5000/api/health
```

### Issue: "Gemini API key missing"
**Solution:**
```bash
# Verify .env file exists
ls backend/.env

# Check API key is set
grep GEMINI_API_KEY backend/.env

# Restart backend server
```

### Issue: "Patient not found"
**Solution:**
```bash
# Upload patient records first via frontend UI
# Or create sample data
python create_sample_data.py
```

### Issue: Embeddings taking too long
**Solution:**
- First run downloads the model (~80MB) - takes 1-2 minutes
- Subsequent runs are fast (<10ms per document)
- Check disk space if download fails

### Issue: CORS errors
**Solution:**
- CORS is enabled by default in `backend/app/__init__.py`
- Check frontend URL matches `http://127.0.0.1:5173`
- Verify backend is serving requests (not using cached data)

---

## 🔐 Security Notes

⚠️ **Before Production Deployment**:

- [ ] Change `FLASK_SECRET_KEY` in production
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/TLS
- [ ] Implement authentication (JWT tokens)
- [ ] Add authorization (role-based access)
- [ ] Enable rate limiting
- [ ] Validate all file uploads
- [ ] Sanitize user inputs
- [ ] Implement audit logging
- [ ] Regular security updates

---

## 📈 Performance Optimization

### Current Optimizations:
- Lightweight embedding model (384-dim instead of 768-dim)
- Top-3 retrieval (adjustable in chatbot_engine.py)
- Cosine similarity for fast search
- Streaming markdown responses

### Potential Improvements:
- [ ] Implement embedding caching
- [ ] Add FAISS vector indexing (included in requirements)
- [ ] Query result caching
- [ ] Batch processing for multiple queries
- [ ] Async request handling

---

## 🚀 Deployment Options

### Option 1: Docker (Recommended)
```bash
# Build image
docker build -t rag-chatbot:latest .

# Run container
docker run -p 5000:5000 -p 5173:5173 rag-chatbot:latest
```

### Option 2: Cloud Deployment
- **Backend**: AWS EC2, Google Cloud Run, Azure App Service, Heroku
- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
- **Database**: AWS RDS, Google Cloud SQL, Azure Database

### Option 3: Local Development
```bash
# Terminal 1: Backend
cd backend && python run.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

---

## 📚 Dependencies

### Backend
- **Flask** 3.0.0 - Web framework
- **Flask-CORS** 4.0.0 - CORS support
- **sentence-transformers** 2.2.2 - Embedding model
- **numpy** 1.24.3 - Numerical computation
- **faiss-cpu** 1.7.4 - Vector similarity search
- **google-generativeai** 0.3.0 - Gemini API
- **python-dotenv** 1.0.0 - Environment variables
- **pdfplumber** 0.10.3 - PDF parsing

### Frontend
- **React** 19.1.1 - UI framework
- **React Router** 7.9.4 - Navigation
- **Axios** 1.13.1 - HTTP client
- **Tailwind CSS** 4.1.15 - Styling
- **React Markdown** 10.1.0 - Markdown rendering
- **Lucide React** 0.546.0 - Icons

---

## 📝 Sample Questions

Try these questions with the sample data:

```
Patient 001 what is their diagnosis?
Patient 002 what medications are they taking?
Patient 003 do they have cognitive issues?
Patient 001 show me lab results
Patient 002 what is their family history?
Patient 003 what is their treatment plan?
```

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📞 Support

For issues or questions:
1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed documentation
2. Review troubleshooting section above
3. Check backend logs (terminal where `python run.py` runs)
4. Check frontend logs (browser developer console)

---

## 🎯 Roadmap

- [x] Core RAG functionality
- [x] Gemini API integration
- [x] Patient upload system
- [x] Modern React UI
- [ ] Authentication system
- [ ] User roles and permissions
- [ ] Advanced search filters
- [ ] Conversation history
- [ ] Export to PDF
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Mobile app (React Native)

---

**Built with ❤️ for healthcare professionals**

*Last Updated: January 2025*
