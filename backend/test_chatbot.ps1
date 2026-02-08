# PowerShell Testing Script for RAG Chatbot
# Run from backend directory: .\test_chatbot.ps1

$baseUrl = "http://127.0.0.1:5000/api"
$passed = 0
$failed = 0

function Write-Header {
    param([string]$text)
    Write-Host "`n" + ("="*70) -ForegroundColor Cyan
    Write-Host $text -ForegroundColor Cyan
    Write-Host ("="*70) -ForegroundColor Cyan
}

function Test-ChatAPI {
    param(
        [string]$patientId,
        [string]$message,
        [string]$testName
    )
    
    Write-Host "`n🧪 Testing: $testName" -ForegroundColor Yellow
    
    try {
        $body = @{
            patient_id = $patientId
            message = $message
        } | ConvertTo-Json
        
        $response = Invoke-WebRequest -Uri "$baseUrl/chat" `
            -Method POST `
            -Headers @{"Content-Type"="application/json"} `
            -Body $body `
            -TimeoutSec 30 `
            -ErrorAction Stop
        
        $data = $response.Content | ConvertFrom-Json
        
        Write-Host "✓ Status: $($response.StatusCode)" -ForegroundColor Green
        Write-Host "✓ Reply: $($data.reply.Substring(0, [Math]::Min(200, $data.reply.Length)))..." -ForegroundColor Green
        
        if ($data.sources) {
            Write-Host "✓ Sources: $($data.sources -join ', ')" -ForegroundColor Green
        }
        
        return $true
    }
    catch {
        Write-Host "✗ Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main Testing
Clear-Host
Write-Host "`n🚀 RAG Chatbot API Testing" -ForegroundColor Magenta
Write-Host "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray

# Test 1: Health Check
Write-Header "TEST 1: Health Check"
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/health" -Method GET -TimeoutSec 10
    Write-Host "✓ Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "✓ Backend is running!" -ForegroundColor Green
    $passed++
}
catch {
    Write-Host "✗ Backend not responding at $baseUrl" -ForegroundColor Red
    Write-Host "❌ Start backend with: python run.py" -ForegroundColor Red
    exit 1
}

# Test 2: Patient 001 - Diagnosis
Write-Header "TEST 2: Patient 001 - Diagnosis"
if (Test-ChatAPI -patientId "001" -message "What is the patient's diagnosis?" -testName "Patient 001 Diagnosis") {
    $passed++
} else {
    $failed++
}

# Test 3: Patient 002 - Medications
Write-Header "TEST 3: Patient 002 - Medications"
if (Test-ChatAPI -patientId "002" -message "What medications is the patient on?" -testName "Patient 002 Medications") {
    $passed++
} else {
    $failed++
}

# Test 4: Patient 003 - Treatments
Write-Header "TEST 4: Patient 003 - Treatments"
if (Test-ChatAPI -patientId "003" -message "What treatments have been applied?" -testName "Patient 003 Treatments") {
    $passed++
} else {
    $failed++
}

# Test 5: Invalid Patient
Write-Header "TEST 5: Error Handling - Invalid Patient"
Write-Host "`n🧪 Testing: Invalid Patient ID" -ForegroundColor Yellow
try {
    $body = @{
        patient_id = "999"
        message = "Who is this patient?"
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "$baseUrl/chat" `
        -Method POST `
        -Headers @{"Content-Type"="application/json"} `
        -Body $body `
        -TimeoutSec 10 `
        -ErrorAction Stop
    
    Write-Host "✓ Response received: $($response.StatusCode)" -ForegroundColor Green
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Response: $($data | ConvertTo-Json -Depth 1)" -ForegroundColor Gray
    $passed++
}
catch {
    Write-Host "Note: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Summary
Write-Header "SUMMARY"
Write-Host "✓ Passed: $passed tests" -ForegroundColor Green
Write-Host "✗ Failed: $failed tests" -ForegroundColor $(If ($failed -gt 0) {'Red'} else {'Green'})
Write-Host "`nSuccess Rate: $(([int](($passed / ($passed + $failed + 3)) * 100)))%" -ForegroundColor Cyan

Write-Host "`n📝 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Ensure sample data exists: python create_sample_data.py" -ForegroundColor Gray
Write-Host "  2. Start frontend: cd frontend && npm run dev" -ForegroundColor Gray
Write-Host "  3. Open in browser: http://127.0.0.1:5173" -ForegroundColor Gray

Write-Host "`n" + ("="*70) -ForegroundColor Cyan
