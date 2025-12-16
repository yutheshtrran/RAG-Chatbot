# 🆘 Troubleshooting & FAQ

## Common Issues & Solutions

### 🔴 Backend Issues

#### Issue: "ModuleNotFoundError: No module named 'google.generativeai'"

**Cause**: Dependencies not installed

**Solution**:
```bash
cd backend
pip install -r app/requirements.txt
```

**Verify**:
```bash
python -c "import google.generativeai; print('✓ OK')"
```

---

#### Issue: "Could not connect to the backend - 127.0.0.1:5000"

**Cause**: Backend server not running

**Solution**:
```bash
cd backend
python run.py
```

**Verify**:
```bash
curl http://127.0.0.1:5000/api/health
# Expected output: {"status": "ok"}
```

---

#### Issue: "Gemini API key missing or invalid"

**Cause**: API key not configured

**Solution**:
1. Check `.env` file exists: `backend/.env`
2. Verify it contains: `GEMINI_API_KEY=AIzaSyAnmUhxiPahrebRQxj36OwgPf7ILtlTAqs`
3. Restart backend: `python run.py`

**Verify**:
```python
from app.config import Config
print(Config.GEMINI_API_KEY)  # Should print API key
```

---

#### Issue: "Patient ID 'xxx' not found in database"

**Cause**: Patient hasn't been uploaded yet

**Solution**:
```bash
# Option 1: Create sample data
python create_sample_data.py

# Option 2: Upload via frontend
# Go to Dashboard → Upload Patient Records
```

---

#### Issue: Embedding model taking very long to load

**Cause**: First-time download of 80MB model

**Solution**:
- Normal behavior on first run
- Takes 1-2 minutes
- Subsequent runs are instant
- Check disk space (need ~2GB)

**Verify**:
```python
from app.embedder import embedding_model
print(embedding_model)  # Should print model info
```

---

#### Issue: "Port 5000 already in use"

**Cause**: Another process using port 5000

**Solution (Windows)**:
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual PID)
taskkill /PID <PID> /F

# Then run backend
python run.py
```

**Solution (Mac/Linux)**:
```bash
# Find process
lsof -i :5000

# Kill process (replace PID)
kill -9 <PID>

# Run backend
python run.py
```

---

### 🔴 Frontend Issues

#### Issue: "Could not connect to the backend"

**Cause**: Backend not running or wrong URL

**Solution**:
1. Ensure backend is running: `python run.py`
2. Check backend is responding:
   ```bash
   curl http://127.0.0.1:5000/api/health
   ```
3. Check frontend URL in `frontend/src/api.js`:
   ```javascript
   const API_BASE_URL = "http://127.0.0.1:5000/api";
   ```

---

#### Issue: "Module not found: axios" or other npm errors

**Cause**: Node dependencies not installed

**Solution**:
```bash
cd frontend
npm install
npm run dev
```

---

#### Issue: "Port 5173 already in use" (Frontend)

**Cause**: Another process using port 5173

**Solution (Windows)**:
```powershell
netstat -ano | findstr :5173
taskkill /PID <PID> /F
npm run dev
```

**Solution (Mac/Linux)**:
```bash
lsof -i :5173
kill -9 <PID>
npm run dev
```

---

#### Issue: Chat window shows "Typing..." forever

**Cause**: Backend not responding

**Solution**:
1. Check backend is running
2. Check error logs in backend terminal
3. Verify Gemini API key is correct
4. Check patient exists in database

---

#### Issue: CORS error in browser console

**Cause**: CORS not properly configured

**Solution**:
1. Verify CORS is enabled in `backend/app/__init__.py`
2. Make sure frontend URL is `http://127.0.0.1:5173`
3. Clear browser cache
4. Restart both frontend and backend

---

### 🔴 Database Issues

#### Issue: "Database is locked" error

**Cause**: Another process accessing database

**Solution**:
1. Stop all backend processes
2. Delete `backend/data/patient_records.db`
3. Restart backend (database auto-recreates)

```bash
# Kill all python processes
taskkill /IM python.exe /F  # Windows

# Or on Mac/Linux
killall python
```

---

#### Issue: Patient records not saving

**Cause**: Database write permission issue

**Solution**:
```bash
# Check directory permissions
ls -la backend/data/

# Fix if needed (Unix/Mac)
chmod 755 backend/data/
chmod 755 backend/data/uploads/
```

---

#### Issue: "Duplicate patient ID" error

**Cause**: Trying to create patient that already exists

**Solution**:
1. Update existing patient instead
2. Or delete database and recreate:
   ```bash
   rm backend/data/patient_records.db
   python init.py
   ```

---

### 🔴 File Upload Issues

#### Issue: "File extension not allowed"

**Cause**: Uploading unsupported file type

**Solution**:
Only upload these formats:
- `.txt` - Text files
- `.pdf` - PDF documents
- `.csv` - CSV spreadsheets

---

#### Issue: "No files uploaded" error

**Cause**: File selection issue

**Solution**:
1. Make sure file is selected
2. Check file size (should be < 50MB)
3. Try different file
4. Refresh page and try again

---

#### Issue: Large PDF files timing out

**Cause**: PDF parsing takes too long

**Solution**:
1. Try smaller PDF files first
2. Or use TXT format instead
3. Consider splitting large PDF

---

### 🔴 Performance Issues

#### Issue: Very slow response time (>10 seconds)

**Cause**: Network latency or Gemini API delay

**Solution**:
1. Check internet connection
2. Try again (Gemini may be slow)
3. Check system resources (RAM, CPU)
4. Reduce top_k in `chatbot_engine.py` from 3 to 1

---

#### Issue: High CPU usage

**Cause**: Embedding generation intensive

**Solution**:
1. Normal during first model load
2. Should stabilize after
3. If persistent, close other programs
4. Check for memory leaks

---

#### Issue: Out of memory error

**Cause**: Insufficient RAM

**Solution**:
1. Minimum 4GB RAM required
2. Close other applications
3. Restart backend and frontend
4. Reduce model size (change embedding model)

---

## ❓ Frequently Asked Questions

### Q: Can I use a different API key?
**A**: Yes, replace the key in:
1. `backend/.env` - `GEMINI_API_KEY=your-key`
2. `backend/app/config.py` - Change default value

---

### Q: Can I use a different embedding model?
**A**: Yes, modify `backend/app/embedder.py`:
```python
embedding_model = SentenceTransformer('your-model-name')
```

Available models: https://huggingface.co/sentence-transformers

---

### Q: Can I use a different LLM instead of Gemini?
**A**: Yes, modify `backend/app/chatbot_engine.py`:
```python
# Replace Gemini calls with your LLM API
```

---

### Q: How do I add authentication?
**A**: Add JWT or Flask-Login to routes.py:
```python
from flask_jwt_extended import jwt_required

@rag_routes.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    # Your code
```

---

### Q: Can I deploy to production?
**A**: Yes, see [SETUP_GUIDE.md](SETUP_GUIDE.md) for:
- Docker deployment
- Cloud deployment (AWS, GCP, Azure)
- Security hardening

---

### Q: How do I increase retrieval accuracy?
**A**: Options:
1. Adjust `top_k` in `chatbot_engine.py` (default: 3)
2. Change similarity threshold
3. Use better embedding model
4. Index records with FAISS (already in requirements)

---

### Q: Can I store conversation history?
**A**: Yes, add to database:
```python
# Add conversations table
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    patient_id TEXT,
    timestamp DATETIME,
    question TEXT,
    answer TEXT
);
```

---

### Q: How do I handle patient privacy?
**A**: Implement:
- [ ] HIPAA compliance
- [ ] Data encryption
- [ ] Access control
- [ ] Audit logging
- [ ] Data retention policies

---

### Q: Can I use this in production for real patients?
**A**: Not yet. Need:
- [ ] HIPAA compliance
- [ ] Medical board approval
- [ ] Professional liability insurance
- [ ] Regulatory review
- [ ] Security audit

---

### Q: How do I backup the database?
**A**: Simple backup:
```bash
# Copy database file
cp backend/data/patient_records.db backup/patient_records_$(date +%Y%m%d).db

# Or use Python
import shutil
shutil.copy('backend/data/patient_records.db', 'backup/database.db')
```

---

### Q: Can I use SQLite in production?
**A**: Not recommended. Use instead:
- PostgreSQL
- MySQL
- MongoDB
- Cloud databases (AWS RDS, GCP CloudSQL)

---

### Q: How do I scale this system?
**A**: Options:
1. **Horizontal**: Deploy multiple backend instances
2. **Caching**: Add Redis for response caching
3. **Vector DB**: Use FAISS or Pinecone
4. **Async**: Use Celery for background tasks
5. **Load Balancer**: Use nginx or cloud load balancer

---

## 🔧 Advanced Troubleshooting

### Enable Debug Logging

**Backend**:
```python
# In backend/app/config.py
DEBUG = True
TESTING = False

# In any module
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

**Frontend**:
```javascript
// In browser console
localStorage.setItem('debug', 'api:*');
```

---

### Monitor Backend Logs

```bash
cd backend
python run.py 2>&1 | tee backend.log

# Then analyze
tail -f backend.log
grep "ERROR" backend.log
```

---

### Test API Manually

```bash
# Test all endpoints
curl -v http://127.0.0.1:5000/api/health

# Test chat
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "001",
    "message": "test"
  }' -v

# Test upload
curl -X POST http://127.0.0.1:5000/api/upload \
  -F "patient_id=test" \
  -F "files=@testfile.txt" -v
```

---

### Check System Resources

```bash
# CPU & Memory (Windows)
tasklist /v | grep python

# CPU & Memory (Mac/Linux)
ps aux | grep python

# Disk space
df -h

# Network
netstat -an | grep 5000
```

---

## 📞 Getting Help

### Check These First:
1. **README.md** - Project overview
2. **SETUP_GUIDE.md** - Setup instructions
3. **IMPLEMENTATION.md** - Technical details
4. **QUICK_REFERENCE.md** - Quick commands
5. **This File** - Troubleshooting

### Still Need Help?
1. Check browser console (F12)
2. Check terminal output (backend logs)
3. Check .env file configuration
4. Verify all dependencies installed
5. Try recreating database

---

## 🐛 Reporting Issues

When reporting issues include:
1. **Error message** (full text)
2. **OS and Python version**
3. **Steps to reproduce**
4. **Backend logs** (last 50 lines)
5. **Browser console errors** (if frontend)

Example:
```
OS: Windows 11
Python: 3.11.0
Error: ModuleNotFoundError: No module named 'google.generativeai'
Steps: 1) pip install -r requirements.txt 2) python run.py 3) Error occurs
```

---

**Most issues are resolved by:**
1. Installing dependencies: `pip install -r app/requirements.txt`
2. Restarting backend: `python run.py`
3. Clearing browser cache (Ctrl+Shift+Delete)
4. Checking logs for errors

**If all else fails**: Delete database and reinitialize
```bash
rm backend/data/patient_records.db
python init.py
```

---

*Last Updated: January 2025*
