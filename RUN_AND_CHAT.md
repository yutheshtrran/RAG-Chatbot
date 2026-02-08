# 🚀 QUICK RUN & CHAT GUIDE

## Step 1: Start Backend
```bash
cd D:\IRP_RAG_BOT\RAG-Chatbot\backend
python run.py
```
Wait for message: `Running on http://127.0.0.1:5000`

---

## Step 2: Start Frontend
Open **new terminal**:
```bash
cd D:\IRP_RAG_BOT\RAG-Chatbot\frontend
npm run dev
```
Wait for message: `Local: http://localhost:5174/` or `http://localhost:5175/`

---

## Step 3: Open in Browser
Click or paste in browser:
```
http://localhost:5174/
```
or
```
http://localhost:5175/
```

---

## Step 4: Copy & Paste These Chat Messages

### Test Original Patients (001-003)
```
Patient 001 what is their diagnosis?
```
```
Patient 002 what medications are they taking?
```
```
Patient 003 provide a patient summary
```

### Test New Patients (011-015)
```
Patient 011 what is Robert Thompson's diagnosis?
```
```
Patient 012 why does Sarah Martinez have a cough?
```
```
Patient 013 what is Michael Chen's knee problem?
```
```
Patient 014 what is Jennifer Wilson's main condition?
```
```
Patient 015 what did David Anderson's MRI show?
```

### Additional Test Messages
```
Patient 011 what medications are prescribed?
```
```
Patient 012 what are the lung function test results?
```
```
Patient 013 what treatments are recommended?
```
```
Patient 014 list the metabolic test results
```
```
Patient 015 what are the neurological symptoms?
```

---

## ✅ What to Expect

Each query should return:
- **Medical information** from the patient record
- **Symptoms, diagnosis, medications**
- **Test results and assessment**
- **Treatment plans**

---

## 🔍 Example Response

**Query**: `Patient 011 what is their diagnosis?`

**Response**:
```
### 🩺 Answer based on internal patient records:

**Record 1:**
* Patient ID: 011
* Name: Robert Thompson
* Age: 58
* Gender: Male

CHIEF COMPLAINT: Shortness of breath during physical activity and occasional chest discomfort

MEDICAL HISTORY:
- Coronary Artery Disease (diagnosed 2020)
- Hypertension
- High Cholesterol
- Type 2 Diabetes
- Previous heart attack (2021)

DIAGNOSIS: Stable coronary artery disease

MEDICATIONS:
- Metoprolol 50mg (Heart)
- Lisinopril 10mg (Blood pressure)
- Atorvastatin 40mg (Cholesterol)
- Aspirin 81mg (Blood thinner)
- Metformin 1000mg (Diabetes)

PLAN: Continue medications, cardiac rehabilitation
```

---

## ⚡ Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check port 5000 is free: `netstat -ano \| findstr :5000` |
| Frontend won't load | Try port 5175 instead of 5174 |
| No response to chat | Reload page (F5), check backend terminal |
| Patient not found | Use correct ID: 001-003 or 011-015 |
| Slow response | Wait 5 seconds, backend may be processing |

---

## 📋 One-Liner Setup

```bash
# Terminal 1
cd D:\IRP_RAG_BOT\RAG-Chatbot\backend && python run.py

# Terminal 2  
cd D:\IRP_RAG_BOT\RAG-Chatbot\frontend && npm run dev

# Then open: http://localhost:5174/
```

---

## 💬 Chat Messages Summary

### Cardiac (011)
- What is Robert Thompson's diagnosis?
- What medications is patient 011 on?
- What is the ejection fraction?

### Respiratory (012)
- Why does Sarah have a cough?
- What's the lung function status?
- List Sarah's medications

### Orthopedic (013)
- What is Michael's knee problem?
- What treatments recommended?
- What is BMI?

### Metabolic (014)
- What is Jennifer's diagnosis?
- List metabolic test results
- What is HbA1c level?

### Neurological (015)
- What are David's symptoms?
- What did MRI brain show?
- List medications

---

**🎉 DONE! Just run the commands and chat!**
