# PromptAgro Backend Test Script for Windows PowerShell

Write-Host "🚀 Testing PromptAgro Backend..." -ForegroundColor Green

# Test 1: Health Check
Write-Host "`n1. Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8001/api/health" -Method GET
    Write-Host "✅ Health Check: $($healthResponse.status)" -ForegroundColor Green
    Write-Host "   Services: $($healthResponse.services | ConvertTo-Json -Compress)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Health Check Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Sample Design
Write-Host "`n2. Testing Sample Design Endpoint..." -ForegroundColor Yellow
try {
    $sampleResponse = Invoke-RestMethod -Uri "http://localhost:8001/api/sample-design" -Method GET
    Write-Host "✅ Sample Design: Success" -ForegroundColor Green
    Write-Host "   Design ID: $($sampleResponse.data.designId)" -ForegroundColor Gray
    Write-Host "   Concepts: $($sampleResponse.data.concepts.Count) concepts generated" -ForegroundColor Gray
} catch {
    Write-Host "❌ Sample Design Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: File Upload Test (without actual file)
Write-Host "`n3. Testing File Upload Validation..." -ForegroundColor Yellow
try {
    # This should fail gracefully since we're not sending a file
    $uploadResponse = Invoke-RestMethod -Uri "http://localhost:8001/api/test-upload" -Method POST -ContentType "multipart/form-data"
} catch {
    # Check the response for proper error handling
    if ($_.Exception.Response.StatusCode -eq 400) {
        Write-Host "✅ Upload Validation: Working correctly (400 Bad Request expected without file)" -ForegroundColor Green
        Write-Host "   This confirms the endpoint validates file uploads properly" -ForegroundColor Gray
    } elseif ($_.Exception.Response.StatusCode -eq 422) {
        Write-Host "✅ Upload Validation: Working correctly (422 Unprocessable Entity)" -ForegroundColor Green
        Write-Host "   This confirms the endpoint validates file uploads properly" -ForegroundColor Gray
    } else {
        Write-Host "❌ Upload Test Unexpected Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test 4: API Documentation
Write-Host "`n4. Testing API Documentation..." -ForegroundColor Yellow
try {
    $docsResponse = Invoke-WebRequest -Uri "http://localhost:8001/docs" -Method GET
    if ($docsResponse.StatusCode -eq 200) {
        Write-Host "✅ API Docs: Available at http://localhost:8001/docs" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ API Docs Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 Backend Testing Complete!" -ForegroundColor Green
Write-Host "Visit http://localhost:8001/docs for interactive API testing" -ForegroundColor Cyan
