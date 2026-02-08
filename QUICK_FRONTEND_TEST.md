# 🎯 Quick Frontend Testing Checklist

## ✅ System Status
- ✅ Backend running at: `http://127.0.0.1:5000`
- ✅ Frontend running at: `http://localhost:5174`
- ✅ 5 new patients in database (011-015)
- ✅ All embeddings created and indexed

---

## 🧪 Copy-Paste Test Queries

### Test 1: Cardiac Patient (011)
```
Patient 011 what is their diagnosis?
```
**Expected**: Robert Thompson's cardiac condition information

### Test 2: Respiratory Patient (012)
```
Patient 012 why does patient have a cough?
```
**Expected**: Sarah Martinez's respiratory issues and treatment

### Test 3: Orthopedic Patient (013)  
```
Patient 013 what is wrong with their knee?
```
**Expected**: Michael Chen's knee problem and recommendations

### Test 4: Metabolic Patient (014)
```
Patient 014 what metabolic tests were done?
```
**Expected**: Jennifer Wilson's metabolic panel results

### Test 5: Neurological Patient (015)
```
Patient 015 what did the brain MRI show?
```
**Expected**: David Anderson's neurological findings

---

## 🎨 Frontend UI Components

The interface should show:
- **Chat Window**: Messages and responses
- **Input Field**: Where you type queries
- **Message Bubbles**: Your questions and AI answers
- **Loading Indicator**: While processing responses
- **Markdown Formatting**: Properly formatted medical information

---

## 🔄 Testing Workflow

1. **Open Frontend**
   - Go to: http://localhost:5174/

2. **Type Query**
   - Example: "Patient 011 what is their diagnosis?"

3. **Submit**
   - Press Enter or click Send

4. **View Response**
   - AI retrieves patient data
   - Displays formatted medical information
   - Shows relevant medical record excerpts

5. **Verify Content**
   - Check if information matches patient conditions
   - Verify all key details are present
   - Confirm proper formatting

---

## ✨ Expected Response Format

```
### 🩺 Answer based on internal patient records:

**Record 1:**
* PATIENT MEDICAL RECORD
  Patient ID: 011
  Name: Robert Thompson
  Age: 58
  Gender: Male
  
CHIEF COMPLAINT: [Details]
  
DIAGNOSIS: [Details]

MEDICATIONS:
- [Med 1]
- [Med 2]
- etc.

TEST RESULTS: [Results]

ASSESSMENT & PLAN: [Plan information]
```

---

## 🎓 What to Look For

### ✅ Good Response Indicators
- Relevant medical information for the patient
- Proper markdown formatting
- Clear section headers
- Comprehensive details
- No error messages

### ❌ Problem Indicators  
- "Patient not found" message
- Incomplete or very short responses
- Unrelated information
- Error in browser console (F12)

---

## 📝 Sample Test Record

### Patient 011: Robert Thompson (58M)
**Quick Summary**:
- Condition: Coronary Artery Disease
- Key Symptoms: Shortness of breath, chest pain
- Medications: 5 heart medications
- Key Test: Ejection Fraction 52%
- Treatment: Continue meds + cardiac rehab

### Patient 012: Sarah Martinez (45F)
**Quick Summary**:
- Condition: Respiratory issues (persistent cough)
- Key Symptoms: 3-week dry cough
- Medications: Inhalers, GERD med
- Key Test: FEV1 92% (good lungs)
- Treatment: Monitor, optimize GERD treatment

### Patient 013: Michael Chen (52M)
**Quick Summary**:
- Condition: Knee osteoarthritis (Grade 2)
- Key Symptoms: Swelling, pain on movement
- Medications: Pain relief, joint supplements
- Key Test: X-ray shows cartilage loss
- Treatment: Physical therapy, weight loss

### Patient 014: Jennifer Wilson (38F)
**Quick Summary**:
- Condition: PCOS + Thyroid + Insulin Resistance
- Key Symptoms: Fatigue, weight gain
- Medications: Thyroid, diabetes, hormonal meds
- Key Test: HbA1c 7.8%, HOMA-IR 4.8
- Treatment: Increase meds, lifestyle change

### Patient 015: David Anderson (62M)
**Quick Summary**:
- Condition: Possible cognitive decline
- Key Symptoms: Headaches, dizziness, memory problems
- Medications: Multiple heart medications
- Key Test: MRI shows white matter changes
- Treatment: Cognitive testing, med optimization

---

## 🔍 Debugging Tips

### If query gets no response
1. Check backend is running: `python run.py`
2. Verify embeddings exist: Check `backend/data/embeddings/`
3. Try different wording
4. Refresh the page

### If response is irrelevant
1. Make sure patient ID is correct (011-015)
2. Try more specific question
3. Check backend logs for errors

### If frontend won't load
1. Port might be taken
2. Try: http://localhost:5174/ or http://localhost:5175/
3. Check terminal for frontend errors

---

## 📊 Success Metrics

Track these to ensure system is working:

- [x] All 5 new patients queryable
- [x] Responses retrieve correct patient data
- [x] Response time < 5 seconds
- [x] Markdown formatting works
- [x] No database errors
- [x] No API errors
- [x] Frontend displays answers correctly
- [x] All test queries pass

---

## 🎉 You're Ready!

1. Open: **http://localhost:5174/**
2. Try query: **"Patient 011 what is their diagnosis?"**
3. Observe the AI response with medical information
4. Try other patients and enjoy testing!

---

## 📞 Quick Help

| Issue | Solution |
|-------|----------|
| Patient not found | Use IDs 011-015, ensure backend running |
| No response | Reload page, check backend logs |
| Slow response | Backend may be processing, wait 5 sec |
| Frontend down | Try port 5175 instead of 5174 |
| Wrong information | Rephrase question or try different patient |

---

**Happy Testing! 🚀**
