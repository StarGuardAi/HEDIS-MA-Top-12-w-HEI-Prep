# PHASE 2 — Google Sheets Setup Script
# Run this AFTER downloading your service account JSON from GCP (Step 2)
# Replace $key with the actual path to your downloaded file

$key = "C:\Users\reich\Downloads\starguard-personal-1fb01168bd9a.json"

if (-not (Test-Path $key)) {
    Write-Host "ERROR: Key file not found at: $key" -ForegroundColor Red
    Write-Host "Download the JSON key from GCP Console first (Step 2), then update `$key above." -ForegroundColor Yellow
    exit 1
}

$base = "C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\auditshield"

Copy-Item $key "$base\service_account.json" -Force
Copy-Item $key "$base\starguard-desktop\service_account.json" -Force
Copy-Item $key "$base\starguard-mobile\Artifacts\app\service_account.json" -Force

Write-Host "SUCCESS: service_account.json copied to all 3 app folders." -ForegroundColor Green

# Show client_email for Step 5 (sharing sheets)
$json = Get-Content $key | ConvertFrom-Json
Write-Host "`nShare these 3 sheets with this email as Editor:" -ForegroundColor Cyan
Write-Host $json.client_email -ForegroundColor White
Write-Host "`nSheets to create: AuditShield_RADV_Audit_Trail | StarGuard_HEDIS_Gap_Tracker | StarGuard_Star_Rating_Cache" -ForegroundColor Gray
