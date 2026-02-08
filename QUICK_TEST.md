# 🚀 Quick Testing Commands

Copy and paste these commands to quickly test your chatbot.

## 1. Start Backend
```bash
cd backend
python run.py
```

## 2. Create Sample Data
```bash
cd backend
python create_sample_data.py
```

## 3. Test with Python Script (Recommended for Windows)
```bash
cd backend
python test_chatbot.py
```

## 4. Test with PowerShell (Windows)
```powershell
cd backend
.\test_chatbot.ps1
```

## 5. Batch Test
```bash
cd backend
python batch_test.py
```

## 6. Single Chat Query with curl
```bash
curl -X POST http://127.0.0.1:5000/api/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"patient_id\": \"001\", \"message\": \"What is the diagnosis?\"}"
```

## 7. Single Chat Query with PowerShell
```powershell
$body = @{
    patient_id = "001"
    message = "What is the diagnosis?"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/chat" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body | Select-Object -ExpandProperty Content
```

## 8. Health Check
```bash
curl http://127.0.0.1:5000/api/health
```

## 9. Start Frontend for UI Testing
```bash
cd frontend
npm install
npm run dev
```

Then open: **http://127.0.0.1:5173**

## 10. Test All Patients
```bash
for i in {1..10}; do
  PATIENT=$(printf "%03d" $i)
  echo "Testing Patient $PATIENT..."
  curl -X POST http://127.0.0.1:5000/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"patient_id\": \"$PATIENT\", \"message\": \"Summarize patient info\"}"
done
```

## Expected Success Criteria

✓ **Backend responds** to `/api/health`  
✓ **Chat endpoint** returns 200 status  
✓ **Response includes** `reply` and `sources` fields  
✓ **Frontend** displays responses correctly  
✓ **No errors** in backend logs  

---

## Troubleshooting

### Backend won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000
# Kill process if needed
taskkill /PID <PID> /F
```

### No responses from chat
```bash
# Check database
python -c "from app.db_handler import get_patient; print(get_patient('001'))"
```

### CORS errors
- Ensure backend is running
- Check API_BASE_URL in `frontend/src/api.js` matches `http://127.0.0.1:5000`

### Embeddings not loaded
```bash
cd backend
python create_sample_data.py  # Regenerates embeddings
```

---

📖 **Full Testing Guide**: See `TESTING_GUIDE.md`
