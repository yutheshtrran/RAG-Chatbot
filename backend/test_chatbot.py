"""
Simple script to test the chatbot API endpoints
Run from backend directory: python test_chatbot.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

# Test 1: Health Check
print("\n" + "="*60)
print("TEST 1: Health Check")
print("="*60)
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Response: {response.json()}")
except Exception as e:
    print(f"✗ Error: {e}")
    print("❌ Backend not running. Start it with: python run.py")
    exit(1)

# Test 2: Chat with Patient 001
print("\n" + "="*60)
print("TEST 2: Chat - Patient 001 Diagnosis")
print("="*60)
try:
    chat_data = {
        "patient_id": "001",
        "message": "What is the patient's diagnosis?"
    }
    response = requests.post(f"{BASE_URL}/chat", json=chat_data)
    print(f"✓ Status: {response.status_code}")
    data = response.json()
    print(f"✓ Reply: {data.get('reply', 'No reply')[:300]}...")
    print(f"✓ Sources: {data.get('sources', [])}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Chat with Patient 002
print("\n" + "="*60)
print("TEST 3: Chat - Patient 002 Medications")
print("="*60)
try:
    chat_data = {
        "patient_id": "002",
        "message": "What medications is the patient on?"
    }
    response = requests.post(f"{BASE_URL}/chat", json=chat_data)
    print(f"✓ Status: {response.status_code}")
    data = response.json()
    print(f"✓ Reply: {data.get('reply', 'No reply')[:300]}...")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: Invalid Patient
print("\n" + "="*60)
print("TEST 4: Error Handling - Invalid Patient")
print("="*60)
try:
    chat_data = {
        "patient_id": "999",
        "message": "Who is this patient?"
    }
    response = requests.post(f"{BASE_URL}/chat", json=chat_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 5: Multiple Patients
print("\n" + "="*60)
print("TEST 5: Multiple Patient Queries")
print("="*60)
queries = [
    ("001", "What is the patient's history?"),
    ("002", "List all test results"),
    ("003", "What treatments?"),
]

for patient_id, message in queries:
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"patient_id": patient_id, "message": message},
            timeout=30
        )
        status = "✓" if response.status_code == 200 else "✗"
        reply = response.json().get('reply', 'Error')[:100]
        print(f"{status} Patient {patient_id}: {reply}...")
    except Exception as e:
        print(f"✗ Patient {patient_id}: {str(e)[:50]}")

print("\n" + "="*60)
print("✓ Testing Complete!")
print("="*60)
print("\nNext steps:")
print("1. Check if all tests passed (✓)")
print("2. If tests fail, check backend logs")
print("3. Ensure sample data was created: python create_sample_data.py")
print("4. Try frontend at: http://127.0.0.1:5173")
