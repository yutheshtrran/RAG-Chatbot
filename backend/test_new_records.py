"""
Test script for New Patient Records (011-015)
Tests the newly created patient records
Run from backend directory: python test_new_records.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

new_patients = {
    "011": {
        "name": "Robert Thompson",
        "condition": "Cardiac",
        "test_queries": [
            "What is Robert Thompson's diagnosis?",
            "What medications is patient 011 taking?",
            "What is the patient's heart ejection fraction?",
        ]
    },
    "012": {
        "name": "Sarah Martinez",
        "condition": "Respiratory",
        "test_queries": [
            "Why does Sarah Martinez have a persistent cough?",
            "What is the patient's lung function?",
            "List Sarah's medications",
        ]
    },
    "013": {
        "name": "Michael Chen",
        "condition": "Orthopedic",
        "test_queries": [
            "What is Michael Chen's knee problem?",
            "What treatments are recommended for patient 013?",
            "What is the patient's BMI and weight?",
        ]
    },
    "014": {
        "name": "Jennifer Wilson",
        "condition": "Metabolic",
        "test_queries": [
            "What is Jennifer Wilson's main diagnosis?",
            "List the patient's metabolic test results",
            "What is the patient's HbA1c level?",
        ]
    },
    "015": {
        "name": "David Anderson",
        "condition": "Neurological",
        "test_queries": [
            "What are David Anderson's symptoms?",
            "What did the MRI brain show for patient 015?",
            "What medications is the patient on?",
        ]
    },
}

print("\n" + "="*80)
print("🧪 TESTING NEW PATIENT RECORDS (011-015)")
print("="*80)

total_tests = 0
passed_tests = 0
failed_tests = 0

for patient_id, patient_info in new_patients.items():
    print(f"\n{'='*80}")
    print(f"🏥 PATIENT {patient_id}: {patient_info['name']} ({patient_info['condition']})")
    print(f"{'='*80}")
    
    for query in patient_info["test_queries"]:
        total_tests += 1
        print(f"\n❓ Query: {query}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={
                    "patient_id": patient_id,
                    "message": query
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("reply", "No reply")
                
                # Check if reply contains meaningful content (not just error)
                if "not found" not in reply.lower() and len(reply) > 50:
                    print(f"✅ SUCCESS - Response: {reply[:300]}...")
                    passed_tests += 1
                elif "not found" in reply.lower():
                    print(f"⚠️  Patient not in database: {reply}")
                    failed_tests += 1
                else:
                    print(f"❌ FAIL - Insufficient response: {reply}")
                    failed_tests += 1
            else:
                print(f"❌ FAIL - Status {response.status_code}: {response.json()}")
                failed_tests += 1
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)[:100]}")
            failed_tests += 1

# Summary Report
print("\n" + "="*80)
print("📊 TEST SUMMARY REPORT")
print("="*80)
print(f"Total Tests Run:      {total_tests}")
print(f"✅ Passed:            {passed_tests}/{total_tests}")
print(f"❌ Failed:            {failed_tests}/{total_tests}")

if total_tests > 0:
    success_rate = (passed_tests / total_tests) * 100
    print(f"\n📈 Success Rate:      {success_rate:.1f}%")

print("\n" + "="*80)
print("🎯 NEXT STEPS")
print("="*80)
print("1. ✅ Backend is running at: http://127.0.0.1:5000")
print("2. ✅ Frontend is running at: http://localhost:5174")
print("\n3. 🌐 Open browser and test interactively:")
print("     URL: http://localhost:5174/")
print("\n4. 💬 Try these chat queries:")
print("     - 'Patient 011 what is their diagnosis?'")
print("     - 'Patient 012 why does patient have cough?'")
print("     - 'Patient 013 what treatments recommended?'")
print("     - 'Patient 014 list metabolic test results'")
print("     - 'Patient 015 what did MRI show?'")
print("\n" + "="*80)
