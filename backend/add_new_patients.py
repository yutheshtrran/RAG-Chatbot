"""
Add new patient records (011-015) to the database
Run from backend directory: python add_new_patients.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.db_handler import add_patient, add_record

# Define new patients from the created files
new_patients = [
    {"id": "011", "name": "Robert Thompson", "age": 58, "gender": "Male"},
    {"id": "012", "name": "Sarah Martinez", "age": 45, "gender": "Female"},
    {"id": "013", "name": "Michael Chen", "age": 52, "gender": "Male"},
    {"id": "014", "name": "Jennifer Wilson", "age": 38, "gender": "Female"},
    {"id": "015", "name": "David Anderson", "age": 62, "gender": "Male"},
]

print("\n" + "="*60)
print("Adding New Patients to Database")
print("="*60 + "\n")

# Add patients
for patient in new_patients:
    try:
        add_patient(patient["id"], patient["name"], patient["age"], patient["gender"])
        print(f"✅ Added patient: {patient['name']} (ID: {patient['id']})")
    except Exception as e:
        print(f"❌ Error adding patient {patient['id']}: {e}")

# Add records from files
records_directory = os.path.join(os.path.dirname(__file__), 'data', 'uploads')
record_files = {
    "011": "011_patient_cardiac.txt",
    "012": "012_patient_respiratory.txt",
    "013": "013_patient_orthopedic.txt",
    "014": "014_patient_metabolic.txt",
    "015": "015_patient_neurological.txt",
}

print("\nAdding Records from Files:")
print("-" * 60)

for patient_id, filename in record_files.items():
    filepath = os.path.join(records_directory, filename)
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        continue
    
    try:
        # Read the file content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add record to database
        add_record(patient_id, filename, content)
        print(f"✅ Added record: {filename} (Patient {patient_id})")
        print(f"   File size: {len(content)} bytes")
    except Exception as e:
        print(f"❌ Error adding record for patient {patient_id}: {e}")

print("\n" + "="*60)
print("✅ New patients and records added successfully!")
print("="*60)
print("\n📝 Next: Run 'python prepare_embeddings.py' to index records")
print("   Or: Run 'python test_new_records.py' to test new patients")
