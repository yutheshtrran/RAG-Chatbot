"""
Populate database with test patient data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.db_handler import add_patient, add_record

# Add test patients
patients = [
    {"id": "P001", "name": "John Doe", "age": 45, "gender": "Male"},
    {"id": "P002", "name": "Emily Davis", "age": 62, "gender": "Female"},
    {"id": "P003", "name": "Jane Smith", "age": 38, "gender": "Female"},
]

for patient in patients:
    add_patient(patient["id"], patient["name"], patient["age"], patient["gender"])
    print(f"✅ Added patient: {patient['name']} ({patient['id']})")

# Add sample records for each patient
records = {
    "P001": {
        "diagnosis": "Type 2 Diabetes Mellitus",
        "medications": "Metformin 500mg, Lisinopril 10mg",
        "allergies": "Penicillin",
        "notes": "Patient presents with elevated blood glucose levels. Recent HbA1c: 7.8%."
    },
    "P002": {
        "diagnosis": "Hypertension",
        "medications": "Amlodipine 5mg, Atorvastatin 20mg",
        "allergies": "ACE inhibitors",
        "notes": "Chronic hypertension management. Blood pressure readings stable at 135/85 mmHg."
    },
    "P003": {
        "diagnosis": "Asthma",
        "medications": "Albuterol inhaler, Fluticasone inhaler",
        "allergies": "NSAIDs",
        "notes": "Mild persistent asthma. Using rescue inhaler 2-3 times per week."
    }
}

for patient_id, record_data in records.items():
    record_text = f"""
DIAGNOSIS: {record_data['diagnosis']}
MEDICATIONS: {record_data['medications']}
ALLERGIES: {record_data['allergies']}
NOTES: {record_data['notes']}
"""
    add_record(patient_id, f"{patient_id}_record.txt", record_text)
    print(f"✅ Added records for: {patient_id}")

print("\n✅ Test data populated successfully!")
