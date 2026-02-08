# 🧪 Frontend Testing Guide - New Patient Records

## ✅ Setup Complete!

Your chatbot is fully configured with **5 new patient records** ready for testing:
- **Patient 011**: Robert Thompson (Cardiac Condition)
- **Patient 012**: Sarah Martinez (Respiratory Condition)
- **Patient 013**: Michael Chen (Orthopedic Condition)
- **Patient 014**: Jennifer Wilson (Metabolic Condition)
- **Patient 015**: David Anderson (Neurological Condition)

---

## 🚀 Frontend Access

**Frontend URL**: http://localhost:5174/

The frontend is already running in your browser or you can open it manually.

---

## 💬 Test Queries

Copy and paste these queries into the chat window to test the new patient records:

### Patient 011 - Cardiac Records
```
Patient 011 what is their diagnosis?
Patient 011 what medications are they taking?
Patient 011 what is their heart ejection fraction?
```

### Patient 012 - Respiratory Records
```
Patient 012 why does the patient have a persistent cough?
Patient 012 what is the patient's lung function?
Patient 012 list the medications
```

### Patient 013 - Orthopedic Records
```
Patient 013 what is the knee problem?
Patient 013 what treatments are recommended?
Patient 013 what is the patient's BMI?
```

### Patient 014 - Metabolic Records
```
Patient 014 what is the main diagnosis?
Patient 014 list metabolic test results
Patient 014 what is the HbA1c level?
```

### Patient 015 - Neurological Records
```
Patient 015 what are the symptoms?
Patient 015 what did the MRI brain show?
Patient 015 list current medications
```

---

## 📊 Expected Results

When you query the chatbot, you should receive:

✅ **Response Content**: Detailed medical information from the patient records
✅ **Markdown Formatting**: Proper formatting with headers and bullet points  
✅ **Response Structure**: Information organized in sections

### Example Response for "Patient 011 what is their diagnosis?"

```
### 🩺 Answer based on internal patient records:

**Record 1:**
* PATIENT MEDICAL RECORD Patient ID: 011 Name: Robert Thompson Age: 58 Gender: Male

- Chief Complaint: Shortness of breath during physical activity and occasional chest discomfort
- Diagnosis: Stable coronary artery disease - Grade...
- Medications: Metoprolol 50mg, Lisinopril 10mg, Atorvastatin 40mg, Aspirin 81mg, Metformin 1000mg
```

---

## 🎯 Testing Checklist

- [ ] Patient 011 queries return cardiac information
- [ ] Patient 012 queries return respiratory information
- [ ] Patient 013 queries return orthopedic information
- [ ] Patient 014 queries return metabolic information
- [ ] Patient 015 queries return neurological information
- [ ] Responses include detailed medical information
- [ ] No "patient not found" errors
- [ ] UI displays responses correctly
- [ ] All markdown formatting works properly

---

## 🔧 API Testing (Optional)

You can also test via API if needed:

```bash
# Test Patient 011
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "011", "message": "What is the diagnosis?"}'

# Test Patient 012
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "012", "message": "Why does patient have cough?"}'
```

---

## 📚 Patient Details

### Patient 011 - Robert Thompson (58M) - Cardiac
- **Chief Complaint**: Shortness of breath & chest pain
- **Diagnosis**: Coronary Artery Disease (Grade 2)
- **Key Tests**: ECG, Troponin, BNP, Ejection Fraction (52%)
- **Medications**: 5 cardiac medications

### Patient 012 - Sarah Martinez (45F) - Respiratory  
- **Chief Complaint**: Persistent dry cough (3 weeks)
- **Diagnosis**: Multi-factorial cough, asthma, GERD
- **Key Tests**: Chest X-ray (normal), PFT (FEV1 92%)
- **Medications**: Inhalers, Omeprazole, Cetirizine

### Patient 013 - Michael Chen (52M) - Orthopedic
- **Chief Complaint**: Right knee pain & swelling (6 months)
- **Diagnosis**: Osteoarthritis (Grade 2), previous meniscus tear
- **Key Tests**: X-ray, MRI showing cartilage loss
- **Medications**: NSAIDs, Glucosamine/Chondroitin, Topical Diclofenac

### Patient 014 - Jennifer Wilson (38F) - Metabolic
- **Chief Complaint**: Fatigue, weight gain, irregular cycles
- **Diagnosis**: PCOS, Hypothyroidism, Insulin Resistance
- **Key Tests**: TSH 2.1, HOMA-IR 4.8, Total Testosterone elevated
- **Medications**: Levothyroxine, Metformin, Spironolactone

### Patient 015 - David Anderson (62M) - Neurological
- **Chief Complaint**: Headaches, dizziness, memory lapses (4 months)
- **Diagnosis**: Possible cognitive decline, cerebrovascular disease
- **Key Tests**: MRI (white matter hyperintensities), Carotid ultrasound
- **Medications**: Multiple cardiovascular medications

---

## 🐛 Troubleshooting

### Query returns "Patient not found"
- Ensure you're using the correct patient ID format (011-015)
- Wait a few seconds for the response
- Try refreshing the page and querying again

### Response is very short
- This is normal for some queries; the AI responds based on available data
- Try rephrasing the question
- Add more context: "Patient 011 what is the diagnosis and why?"

### Frontend not loading
- Check if frontend is running: http://localhost:5174/
- Backend should be visible at: http://127.0.0.1:5000/api/health

### No response in chat window
- Open browser console (F12) to check for errors
- Verify backend is running (check terminal)
- Try a simple query: "Patient 001 what is their history?"

---

## 📝 What Was Created

### Patient Record Files (in `/backend/data/uploads/`)
- `011_patient_cardiac.txt` - 2,196 chars
- `012_patient_respiratory.txt` - 2,397 chars
- `013_patient_orthopedic.txt` - 2,571 chars
- `014_patient_metabolic.txt` - 3,084 chars
- `015_patient_neurological.txt` - 3,432 chars

### Database Entries
- 5 new patients added to SQLite database
- 5 new medical records linked to patients

### Embeddings
- All documents (18 total) embedded using `all-MiniLM-L6-v2` model
- Vector indices created for semantic search

### Test Scripts
- `test_new_records.py` - Test all new patients with multiple queries
- `add_new_patients.py` - Add patients to database
- `regenerate_embeddings.py` - Create embeddings for all documents

---

## ✨ Ready to Test!

1. **Open**: http://localhost:5174/
2. **Try a query**: "Patient 011 what is their diagnosis?"
3. **Observe**: Detailed medical response with patient information
4. **Explore**: Test other patients and questions

---

## 📞 Support

If you encounter issues:
1. Check backend logs (terminal where `python run.py` runs)
2. Verify embeddings are regenerated
3. Ensure patient records are in database
4. Run: `python test_new_records.py` for validation
