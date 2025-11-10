# PowerShell script to update KPIs
# Usage: .\scripts\update-kpis.ps1

Write-Host "📊 Updating Key Performance Indicators..." -ForegroundColor Cyan

# Check if Python is available
try {
    python --version | Out-Null
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Install dependencies if needed
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install requests pyyaml --quiet

# Run the KPI generator
Write-Host "🔄 Generating KPIs..." -ForegroundColor Yellow
python scripts/generate-kpis.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ KPI update complete!" -ForegroundColor Green
} else {
    Write-Host "❌ KPI update failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

