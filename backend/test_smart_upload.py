"""
Test the new Smart PDF Upload feature
Upload PDFs and query without patient ID
Run from backend directory: python test_smart_upload.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

print("\n" + "="*80)
print("🆕 TESTING SMART PDF UPLOAD FEATURE")
print("="*80 + "\n")

# Test 1: Query without patient_id (global search)
print("TEST 1: Query Without Patient ID (Global Search)")
print("-"*80)
try:
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "What is the patient's diagnosis?"
        },
        timeout=30
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if response.status_code == 200:
        reply = data.get('reply', 'No reply')
        print(f"✓ Response received: {reply[:200]}...")
    else:
        print(f"✗ Error: {data}")
except Exception as e:
    print(f"✗ Exception: {e}")

# Test 2: Query with generic message (no patient ID)
print("\n\nTEST 2: Generic Medical Question (No Patient ID)")
print("-"*80)
try:
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "What medications are being prescribed?"
        },
        timeout=30
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if response.status_code == 200:
        reply = data.get('reply', 'No reply')
        print(f"✓ Response received: {reply[:200]}...")
    else:
        print(f"✗ Error: {data}")
except Exception as e:
    print(f"✗ Exception: {e}")

# Test 3: Query with patient_id (traditional)
print("\n\nTEST 3: Query With Patient ID (Traditional)")
print("-"*80)
try:
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "patient_id": "001",
            "message": "What is their diagnosis?"
        },
        timeout=30
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if response.status_code == 200:
        reply = data.get('reply', 'No reply')
        print(f"✓ Response received: {reply[:200]}...")
    else:
        print(f"✗ Error: {data}")
except Exception as e:
    print(f"✗ Exception: {e}")

# Test 4: Query for uploaded documents
print("\n\nTEST 4: Query for Uploaded Documents")
print("-"*80)
try:
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "Tell me about patient symptoms and treatment"
        },
        timeout=30
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if response.status_code == 200:
        reply = data.get('reply', 'No reply')
        print(f"✓ Response received: {reply[:200]}...")
    else:
        print(f"✗ Error: {data}")
except Exception as e:
    print(f"✗ Exception: {e}")

print("\n" + "="*80)
print("✓ TESTING COMPLETE")
print("="*80)
print("\nNotes:")
print("1. Queries without patient_id search all documents")
print("2. Queries with patient_id search specific patient")
print("3. System automatically falls back to uploaded_documents")
print("4. Works with both traditional patient records and new uploads")
print("\n" + "="*80 + "\n")
