# 🧪 Chatbot Testing Guide

This guide provides multiple ways to test your RAG-based clinical chatbot.

---

## 1️⃣ Quick Setup for Testing

### Start Backend
```bash
cd backend
python run.py
```
Backend will be available at: **http://127.0.0.1:5000**

### Start Frontend (Optional for API Testing)
```bash
cd frontend
npm install  # If first time
npm run dev
```
Frontend will be available at: **http://127.0.0.1:5173**

### Prepare Test Data
```bash
# From backend directory
python create_sample_data.py
```
This creates 10 sample patient records for testing.

---

## 2️⃣ API Testing (Curl/PowerShell)

### Test Health Check
```bash
curl -X GET http://127.0.0.1:5000/api/health
```

Expected response:
```json
{"status": "ok"}
```

### Test Chat Endpoint
```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "001",
    "message": "What is the patient diagnosis?"
  }'
```

### PowerShell Testing
```powershell
$body = @{
    patient_id = "001"
    message = "What medications are they taking?"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/chat" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

### Upload Patient Records
```bash
curl -X POST http://127.0.0.1:5000/api/upload \
  -F "patient_id=011" \
  -F "name=Test Patient" \
  -F "age=45" \
  -F "gender=Male" \
  -F "files=@path/to/test_record.txt"
```

---

## 3️⃣ Python Testing Script

Create a file: `test_chatbot.py`

```python
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

# Test 1: Health Check
print("=" * 50)
print("TEST 1: Health Check")
print("=" * 50)
response = requests.get(f"{BASE_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# Test 2: Chat with Patient 001
print("=" * 50)
print("TEST 2: Chat with Patient 001")
print("=" * 50)
chat_data = {
    "patient_id": "001",
    "message": "What is the patient's diagnosis?"
}
response = requests.post(f"{BASE_URL}/chat", json=chat_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}\n")

# Test 3: Chat with Patient 002
print("=" * 50)
print("TEST 3: Chat with Patient 002 - Medications")
print("=" * 50)
chat_data = {
    "patient_id": "002",
    "message": "What medications is the patient on?"
}
response = requests.post(f"{BASE_URL}/chat", json=chat_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}\n")

# Test 4: Multiple Queries
print("=" * 50)
print("TEST 4: Multiple Patient Queries")
print("=" * 50)
test_queries = [
    ("001", "What is the patient's medical history?"),
    ("002", "List all test results"),
    ("003", "What treatments have been applied?"),
]

for patient_id, message in test_queries:
    chat_data = {"patient_id": patient_id, "message": message}
    response = requests.post(f"{BASE_URL}/chat", json=chat_data)
    print(f"\nPatient {patient_id}: {message}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Reply: {response.json().get('reply', 'No reply')[:200]}...")
    else:
        print(f"Error: {response.json()}")

print("\n" + "=" * 50)
print("TESTING COMPLETE")
print("=" * 50)
```

Run it:
```bash
cd backend
python test_chatbot.py
```

---

## 4️⃣ Frontend UI Testing

### Manual Testing Steps

1. **Open Frontend** → http://127.0.0.1:5173

2. **Test Chat with Patient ID in Message**
   - Message: `Patient 001 what is their diagnosis?`
   - Expected: System extracts "001" and sends query

3. **Test with Different Patients**
   - Try: `Patient 002 what medications are they on?`
   - Try: `Patient 003 what treatments have been applied?`

4. **Test Upload Feature**
   - Click "Upload Patient Records"
   - Fill in patient details
   - Upload a .txt or .pdf file
   - Verify in backend logs

5. **Test Error Handling**
   - Send message without patient ID
   - Expected: Warning message about missing patient ID
   - Ensure backend stays responsive

6. **Test UI Components**
   - Message bubbles appear correctly
   - Loader shows during processing
   - Markdown formatting in responses works
   - Sidebar displays correctly

---

## 5️⃣ Batch Testing Script

Create: `batch_test.py`

```python
import requests
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api"

test_cases = [
    {"patient_id": "001", "message": "What is the patient's diagnosis?"},
    {"patient_id": "001", "message": "List medications"},
    {"patient_id": "002", "message": "What are the test results?"},
    {"patient_id": "002", "message": "Medical history summary"},
    {"patient_id": "003", "message": "What treatments?"},
    {"patient_id": "999", "message": "Who is this patient?"},  # Non-existent
]

print(f"Starting Batch Tests at {datetime.now()}\n")
print(f"{'Patient ID':<12} {'Message':<35} {'Status':<8} {'Response Length':<20}")
print("-" * 80)

passed = 0
failed = 0
errors = []

for test in test_cases:
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/chat", json=test, timeout=30)
        elapsed = time.time() - start_time
        
        status = "✓ PASS" if response.status_code == 200 else "✗ FAIL"
        response_length = len(str(response.json()).get("reply", ""))
        
        print(f"{test['patient_id']:<12} {test['message']:<35} {status:<8} {response_length} chars ({elapsed:.2f}s)")
        
        if response.status_code == 200:
            passed += 1
        else:
            failed += 1
            errors.append(f"{test['patient_id']}: {response.status_code}")
            
    except Exception as e:
        print(f"{test['patient_id']:<12} {test['message']:<35} ✗ ERROR  Exception: {str(e)[:20]}")
        failed += 1
        errors.append(f"{test['patient_id']}: {str(e)}")

print("-" * 80)
print(f"\nResults: {passed} passed, {failed} failed")
if errors:
    print("Errors:")
    for error in errors:
        print(f"  - {error}")
```

Run it:
```bash
python batch_test.py
```

---

## 6️⃣ Load Testing

Create: `load_test.py`

```python
import requests
import concurrent.futures
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api"

def send_chat(patient_id, message):
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"patient_id": patient_id, "message": message},
            timeout=30
        )
        elapsed = time.time() - start
        return {
            "status": response.status_code,
            "time": elapsed,
            "success": response.status_code == 200
        }
    except Exception as e:
        return {"status": 0, "time": 0, "success": False, "error": str(e)}

# Run 20 concurrent requests
print(f"Running load test at {datetime.now()}")
print("Sending 20 concurrent requests...")

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = []
    for i in range(20):
        patient_id = str((i % 10) + 1).zfill(3)
        message = f"Test query {i}"
        futures.append(executor.submit(send_chat, patient_id, message))
    
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

# Analyze results
successful = sum(1 for r in results if r["success"])
failed = sum(1 for r in results if not r["success"])
avg_time = sum(r["time"] for r in results) / len(results)

print(f"\nResults:")
print(f"  Successful: {successful}/20")
print(f"  Failed: {failed}/20")
print(f"  Average response time: {avg_time:.2f}s")
print(f"  Min time: {min(r['time'] for r in results):.2f}s")
print(f"  Max time: {max(r['time'] for r in results):.2f}s")
```

---

## 7️⃣ Debugging & Troubleshooting

### Check Backend Status
```bash
curl -X GET http://127.0.0.1:5000/api/health
```

### View Backend Logs
Check the terminal where `python run.py` is running for error messages.

### Test Database Connection
```bash
cd backend
python -c "from app.db_handler import get_patient; print(get_patient('001'))"
```

### Test Embeddings
```bash
cd backend
python -c "from app.embedder import embed_text; print(embed_text('test query'))"
```

### Check Available Patients
```bash
cd backend
python -c "from app.db_handler import get_all_patients; print(get_all_patients())"
```

---

## 8️⃣ Expected Results

### Sample Output (Chat Endpoint)
```json
{
  "reply": "Based on the patient record, the diagnosis is...",
  "sources": [
    "001_john_doe_record.txt"
  ],
  "patient_id": "001"
}
```

### Error Response
```json
{
  "error": "Both 'patient_id' and 'message' fields are required."
}
```

---

## 📋 Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend connects to backend
- [ ] Health check endpoint responds
- [ ] Chat endpoint processes queries
- [ ] Patient data retrieval works
- [ ] Error handling works (invalid patient ID)
- [ ] Multiple concurrent requests work
- [ ] UI displays responses correctly
- [ ] Upload functionality works
- [ ] Database stores records correctly

---

## 🚀 Start Testing Now!

### Quick Start (All at once):
```bash
# Terminal 1: Backend
cd backend && python run.py

# Terminal 2: Frontend  
cd frontend && npm run dev

# Terminal 3: Run tests
cd backend && python test_chatbot.py
```

Then visit: **http://127.0.0.1:5173**
