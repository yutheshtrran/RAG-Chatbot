# 🚀 RAG Chatbot - Quick Reference

## ⚡ Quick Start (Choose Your OS)

### Windows
```bash
cd d:\IRP_BOT\RAG-Chatbot
quickstart.bat
```

### Mac/Linux
```bash
cd /path/to/RAG-Chatbot
chmod +x quickstart.sh
./quickstart.sh
```

### Manual (Any OS)
```bash
# Terminal 1: Backend
cd backend && pip install -r app/requirements.txt && python run.py

# Terminal 2: Frontend
cd frontend && npm install && npm run dev

# Optional: Create test data (Terminal 3)
python create_sample_data.py
```

---

## 🌐 Access Points

| Service | URL | Notes |
|---------|-----|-------|
| **Frontend** | http://127.0.0.1:5173 | React web app |
| **Backend API** | http://127.0.0.1:5000/api | REST endpoints |
| **Health Check** | http://127.0.0.1:5000/api/health | Test backend |

---

## 💬 How to Chat

### Via Frontend UI
1. Go to Dashboard
2. Upload patient files
3. Type in chat: "Patient 001 what is their diagnosis?"
4. Press Enter

### Via cURL (API)
```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "001",
    "message": "What is their diagnosis?"
  }'
```

### Expected Response
```json
{
  "reply": "Based on patient 001's medical records, they have..."
}
```

---

## 📤 Upload Patient Files

### Via Frontend
1. Go to Dashboard → "Upload Patient Records"
2. Fill Patient ID (e.g., "001")
3. Select TXT/PDF/CSV files
4. Click Upload

### Via cURL
```bash
curl -X POST http://127.0.0.1:5000/api/upload \
  -F "patient_id=001" \
  -F "name=John Doe" \
  -F "age=55" \
  -F "gender=Male" \
  -F "files=@patient_file.txt"
```

---

## 🧪 Test with Sample Data

```bash
python create_sample_data.py
```

Creates 3 test patients:
- **Patient 001**: John Doe (cardiac)
- **Patient 002**: Emily Davis (healthy)
- **Patient 003**: Jane Smith (geriatric)

---

## 📝 Common Queries to Try

```
"Patient 001 what is their diagnosis?"
"Patient 002 show me their medications"
"Patient 003 do they have memory problems?"
"Patient 001 lab results please"
"Patient 002 family history"
"Patient 003 treatment recommendations"
```

---

## 🔧 System Requirements

| Component | Requirement |
|-----------|-------------|
| Python | 3.8+ |
| Node.js | 16+ |
| RAM | 4GB minimum |
| Disk | 2GB available |
| Network | Internet (for Gemini API) |

---

## ⚙️ Configuration Files

### Backend Configuration
**File**: `backend/app/config.py`
- Change DEBUG mode
- Modify API settings

### Environment Variables
**File**: `backend/.env`
```env
GEMINI_API_KEY=AIzaSyAnmUhxiPahrebRQxj36OwgPf7ILtlTAqs
FLASK_SECRET_KEY=your-secret-key
DEBUG=True
```

### Frontend Configuration
**File**: `frontend/src/api.js`
- Change backend URL if needed
- Modify API endpoints

---

## 📊 Project Structure (Key Files)

```
Backend:
  backend/app/main.py           → Run this
  backend/app/routes.py         → API endpoints
  backend/app/chatbot_engine.py → RAG logic
  backend/app/requirements.txt  → Dependencies
  backend/.env                  → Secrets

Frontend:
  frontend/src/App.jsx          → Main component
  frontend/src/api.js           → API calls
  frontend/src/components/      → UI components
  frontend/package.json         → Dependencies
```

---

## 🐛 Troubleshooting

### Can't connect to backend
```bash
# Check if backend is running
curl http://127.0.0.1:5000/api/health

# If not, start backend
cd backend && python run.py
```

### Module not found errors
```bash
# Install requirements
cd backend && pip install -r app/requirements.txt
```

### "Patient not found" error
```bash
# Create sample data
python create_sample_data.py

# Or upload via frontend UI
```

### CORS errors
- CORS is enabled by default
- Make sure frontend runs on http://127.0.0.1:5173
- Try clearing browser cache

### Slow first request
- First run downloads embedding model (~80MB)
- Subsequent requests are fast
- This is normal, wait 1-2 minutes

---

## 📊 API Reference

### POST /api/chat
**Upload**: Patient question
**Response**: AI-generated answer

### POST /api/upload
**Upload**: Patient files
**Response**: Upload confirmation

### GET /api/health
**Response**: Server status

---

## 🎯 Features

- ✅ Real-time chat
- ✅ Patient record upload (TXT, PDF, CSV)
- ✅ Semantic search (embeddings)
- ✅ AI answer generation (Gemini)
- ✅ Markdown response formatting
- ✅ SQLite database
- ✅ CORS enabled

---

## 🔒 Important

- **API Key**: `AIzaSyAnmUhxiPahrebRQxj36OwgPf7ILtlTAqs` (included)
- **Database**: Auto-created in `backend/data/`
- **Uploads**: Stored in `backend/data/uploads/`

---

## 📚 Documentation

- **[README.md](README.md)** - Full project overview
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup
- **[IMPLEMENTATION.md](IMPLEMENTATION.md)** - What was fixed
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - This file

---

## 🎓 How It Works

```
Your Question
    ↓
Convert to embeddings (384-dim vector)
    ↓
Search patient records (cosine similarity)
    ↓
Get top-3 most relevant documents
    ↓
Send to Gemini API with context
    ↓
Gemini generates AI answer
    ↓
Display formatted response
```

---

## ✨ Ready to Go!

1. Run `quickstart.bat` or `quickstart.sh`
2. Open http://127.0.0.1:5173
3. Upload patient files
4. Ask questions!

**Need help?** Check the full documentation files.

---

*Last Updated: January 2025*
*Status: ✅ Fully Functional*
