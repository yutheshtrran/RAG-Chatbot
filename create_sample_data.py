#!/usr/bin/env python
"""
Test script to populate the database with sample patient data
and test the chatbot with sample queries.
"""
import os
import sys
import json

# Add backend app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def create_sample_data():
    """Create sample patient data in the database."""
    from backend.app.db_handler import add_patient, add_record
    
    print("📝 Creating sample patient data...")
    
    # Sample patients
    patients = [
        {
            "patient_id": "001",
            "name": "John Doe",
            "age": 55,
            "gender": "Male"
        },
        {
            "patient_id": "002",
            "name": "Emily Davis",
            "age": 42,
            "gender": "Female"
        },
        {
            "patient_id": "003",
            "name": "Jane Smith",
            "age": 68,
            "gender": "Female"
        }
    ]
    
    # Sample medical records content
    records_data = {
        "001": [
            {
                "filename": "medical_history.txt",
                "content": """PATIENT MEDICAL RECORD
Patient ID: 001
Name: John Doe
Age: 55
Gender: Male
Date: 2024-01-15

CHIEF COMPLAINT:
Chest pain and shortness of breath

MEDICAL HISTORY:
- Type 2 Diabetes (diagnosed 2015)
- Hypertension (diagnosed 2018)
- High Cholesterol (diagnosed 2019)
- Previous MI in 2020 (treated with angioplasty)

MEDICATIONS:
- Metformin 1000mg twice daily
- Lisinopril 10mg daily
- Atorvastatin 40mg daily
- Aspirin 100mg daily

VITAL SIGNS:
- BP: 145/92 mmHg
- HR: 88 bpm
- Temp: 98.6°F
- RR: 18 breaths/min

PHYSICAL EXAMINATION:
- General: Alert and oriented
- Cardiovascular: Regular rate and rhythm, no murmurs
- Lungs: Clear bilaterally
- Abdomen: Soft, non-tender

ASSESSMENT:
Acute coronary syndrome - rule out MI

PLAN:
- ECG and troponin levels
- Admission to cardiac ICU
- Cardiology consultation"""
            },
            {
                "filename": "lab_results.txt",
                "content": """LABORATORY RESULTS
Date: 2024-01-15
Patient: John Doe (001)

CARDIAC MARKERS:
- Troponin I: 0.05 ng/mL (Normal <0.04)
- CK-MB: 8.5 ng/mL (Elevated)
- Myoglobin: 120 ng/mL (Normal <90)

BLOOD COUNT:
- WBC: 12.5 K/uL (Slightly elevated)
- RBC: 4.8 M/uL
- Hemoglobin: 14.2 g/dL
- Hematocrit: 42%
- Platelets: 220 K/uL

CHEMISTRY:
- Glucose: 285 mg/dL (Elevated)
- Creatinine: 1.2 mg/dL (Slightly elevated)
- BUN: 24 mg/dL (Slightly elevated)
- Sodium: 138 mEq/L
- Potassium: 4.2 mEq/L

LIPID PANEL:
- Total Cholesterol: 215 mg/dL
- LDL: 145 mg/dL
- HDL: 38 mg/dL
- Triglycerides: 195 mg/dL

LIVER FUNCTION:
- ALT: 28 U/L
- AST: 32 U/L
- Bilirubin: 0.9 mg/dL"""
            }
        ],
        "002": [
            {
                "filename": "patient_record.txt",
                "content": """PATIENT INFORMATION
ID: P002
Name: Emily Davis
Age: 42
Gender: Female
Date of Record: 2024-01-10

REASON FOR VISIT:
Routine annual physical examination

MEDICAL HISTORY:
- Asthma (well-controlled with inhalers)
- Hypothyroidism (on levothyroxine)
- Seasonal allergies

MEDICATIONS:
- Levothyroxine 75 mcg daily
- Albuterol inhaler as needed
- Cetirizine 10mg daily during allergy season

ALLERGIES:
- Penicillin (rash)
- Latex (reaction unknown - avoid exposure)

FAMILY HISTORY:
- Mother: Hypertension, Type 2 Diabetes
- Father: Heart disease
- Sister: Breast cancer

LIFESTYLE:
- Non-smoker
- Moderate exercise (3x per week)
- Social alcohol use

VITAL SIGNS:
- Height: 5'6"
- Weight: 130 lbs
- BMI: 21.0 (Normal)
- BP: 118/76 mmHg
- HR: 72 bpm

PHYSICAL EXAM:
- General: Healthy appearance
- Cardiovascular: Normal
- Respiratory: Clear to auscultation bilaterally
- Abdomen: Normal
- Neuro: Alert and oriented x3

ASSESSMENT:
Healthy female for routine preventive care

RECOMMENDATIONS:
- Continue current medications
- Annual mammogram starting age 40
- Colonoscopy at age 50
- Maintain healthy lifestyle"""
            }
        ],
        "003": [
            {
                "filename": "geriatric_assessment.txt",
                "content": """GERIATRIC PATIENT ASSESSMENT
Patient ID: 003
Name: Jane Smith
Age: 68
Gender: Female
Assessment Date: 2024-01-12

CHIEF COMPLAINT:
Mild memory issues and joint pain

MEDICAL CONDITIONS:
- Osteoarthritis (hands, knees)
- Type 2 Diabetes (diagnosed 2010)
- Mild cognitive impairment
- Osteoporosis
- Hypothyroidism

MEDICATIONS:
- Metformin 500mg twice daily
- Levothyroxine 50 mcg daily
- Glucosamine 500mg three times daily
- Vitamin D 1000 IU daily
- Calcium supplement 500mg twice daily
- Omeprazole 20mg daily

RECENT LABS (2024-01-12):
- Fasting glucose: 156 mg/dL
- HbA1c: 7.2%
- TSH: 2.5 mIU/L
- Vitamin B12: 410 pg/mL (Low-normal)
- Hemoglobin: 13.2 g/dL

FUNCTIONAL STATUS:
- ADL: Independent
- IADL: Requires assistance with finances
- Gait: Steady with slight limp (right knee)
- Balance: Good

COGNITIVE ASSESSMENT:
- MMSE: 24/30 (Mild impairment)
- Memory: Difficulty with recent events
- Orientation: Oriented to person and place

DEPRESSION SCREENING:
- PHQ-9: 5 (Minimal symptoms)

RECOMMENDATIONS:
- Monitor blood glucose control
- Physical therapy for arthritis
- Neuropsychological testing
- B12 supplementation
- Continue osteoporosis management"""
            }
        ]
    }
    
    # Create patients and add records
    for patient in patients:
        try:
            add_patient(
                patient["patient_id"],
                patient["name"],
                patient["age"],
                patient["gender"]
            )
            print(f"✅ Created patient: {patient['name']} ({patient['patient_id']})")
            
            # Add records for this patient
            if patient["patient_id"] in records_data:
                for record in records_data[patient["patient_id"]]:
                    add_record(
                        patient["patient_id"],
                        record["filename"],
                        record["content"]
                    )
                    print(f"   📄 Added record: {record['filename']}")
        except Exception as e:
            print(f"❌ Error creating patient {patient['patient_id']}: {e}")
    
    print("\n✅ Sample data created successfully!")

if __name__ == "__main__":
    create_sample_data()
    print("\n💡 Tip: Try asking questions like:")
    print("   - 'Patient 001 what is their diagnosis?'")
    print("   - 'Patient 002 what medications are they taking?'")
    print("   - 'Patient 003 what cognitive issues do they have?'")
