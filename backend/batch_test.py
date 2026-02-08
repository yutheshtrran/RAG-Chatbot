"""
Batch testing script for chatbot API
Tests multiple queries and generates a summary report
Run from backend directory: python batch_test.py
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api"

# Define test cases
test_cases = [
    {"patient_id": "001", "message": "What is the patient's diagnosis?"},
    {"patient_id": "001", "message": "List medications"},
    {"patient_id": "001", "message": "What is the medical history?"},
    {"patient_id": "002", "message": "What are the test results?"},
    {"patient_id": "002", "message": "List medications"},
    {"patient_id": "002", "message": "Show patient summary"},
    {"patient_id": "003", "message": "What treatments?"},
    {"patient_id": "003", "message": "What is the diagnosis?"},
    {"patient_id": "004", "message": "Patient overview"},
    {"patient_id": "005", "message": "Recent test results"},
    {"patient_id": "999", "message": "Who is this patient?"},  # Non-existent patient
]

print("\n" + "="*80)
print(f"Batch Testing Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
print(f"\n{'Patient':<10} {'Message':<35} {'Status':<10} {'Time':<10} {'Reply Length':<15}")
print("-"*80)

passed = 0
failed = 0
errors = []
response_times = []

for idx, test in enumerate(test_cases, 1):
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/chat",
            json=test,
            timeout=30
        )
        elapsed = time.time() - start_time
        response_times.append(elapsed)
        
        if response.status_code == 200:
            status = "✓ PASS"
            passed += 1
            reply_length = len(response.json().get("reply", ""))
        else:
            status = "✗ FAIL"
            failed += 1
            reply_length = 0
            errors.append(f"Test {idx}: HTTP {response.status_code}")
        
        print(f"{test['patient_id']:<10} {test['message']:<35} {status:<10} {elapsed:>7.2f}s   {reply_length:>6} chars")
        
    except requests.exceptions.Timeout:
        print(f"{test['patient_id']:<10} {test['message']:<35} ✗ TIMEOUT  >30.00s   0 chars")
        failed += 1
        errors.append(f"Test {idx}: Timeout")
    except requests.exceptions.ConnectionError:
        print(f"{test['patient_id']:<10} {test['message']:<35} ✗ ERROR    0.00s     0 chars")
        failed += 1
        errors.append(f"Test {idx}: Connection failed")
        if idx == 1:  # Only show once
            print("\n❌ ERROR: Cannot connect to backend at http://127.0.0.1:5000")
            print("   Start backend with: python run.py")
            exit(1)
    except Exception as e:
        print(f"{test['patient_id']:<10} {test['message']:<35} ✗ ERROR    0.00s     0 chars")
        failed += 1
        errors.append(f"Test {idx}: {str(e)[:30]}")

# Summary Report
print("\n" + "="*80)
print("SUMMARY REPORT")
print("="*80)
print(f"Total Tests: {len(test_cases)}")
print(f"✓ Passed:    {passed}/{len(test_cases)}")
print(f"✗ Failed:    {failed}/{len(test_cases)}")

if response_times:
    print(f"\nResponse Time Statistics:")
    print(f"  Average:   {sum(response_times)/len(response_times):.2f}s")
    print(f"  Min:       {min(response_times):.2f}s")
    print(f"  Max:       {max(response_times):.2f}s")

success_rate = (passed / len(test_cases)) * 100
print(f"\nSuccess Rate: {success_rate:.1f}%")

if errors:
    print(f"\nErrors ({len(errors)}):")
    for error in errors:
        print(f"  - {error}")

if success_rate == 100:
    print("\n✓ All tests passed! Your chatbot is working correctly!")
elif success_rate >= 80:
    print("\n⚠ Most tests passed. Review errors above.")
else:
    print("\n✗ Many tests failed. Check backend logs and configuration.")

print("\n" + "="*80)
