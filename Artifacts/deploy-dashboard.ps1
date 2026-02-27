# Dashboard Deployment Script
# Quick deployment helper for Streamlit Cloud

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  HEDIS Dashboard Deployment Helper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Streamlit is installed
Write-Host "Step 1: Checking Streamlit installation..." -ForegroundColor Yellow
try {
    $streamlitVersion = python -c "import streamlit; print(streamlit.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Streamlit installed: $streamlitVersion" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Streamlit not found. Installing..." -ForegroundColor Red
        pip install streamlit
    }
} catch {
    Write-Host "  ✗ Error checking Streamlit" -ForegroundColor Red
    Write-Host "  Install with: pip install streamlit" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 2: Testing dashboard locally..." -ForegroundColor Yellow
$dashboardPath = "project\streamlit_app.py"
if (Test-Path $dashboardPath) {
    Write-Host "  ✓ Dashboard file found: $dashboardPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "  To test locally, run:" -ForegroundColor Cyan
    Write-Host "    cd project" -ForegroundColor White
    Write-Host "    streamlit run streamlit_app.py" -ForegroundColor White
    Write-Host ""
    $test = Read-Host "  Test dashboard now? (y/n)"
    if ($test -eq "y" -or $test -eq "Y") {
        Write-Host "  Starting Streamlit..." -ForegroundColor Yellow
        Set-Location project
        streamlit run streamlit_app.py
    }
} else {
    Write-Host "  ✗ Dashboard file not found: $dashboardPath" -ForegroundColor Red
}

Write-Host ""
Write-Host "Step 3: Deployment Instructions" -ForegroundColor Yellow
Write-Host ""
Write-Host "To deploy to Streamlit Cloud:" -ForegroundColor Cyan
Write-Host "  1. Go to: https://share.streamlit.io/" -ForegroundColor White
Write-Host "  2. Sign in with GitHub" -ForegroundColor White
Write-Host "  3. Click 'New app'" -ForegroundColor White
Write-Host "  4. Configure:" -ForegroundColor White
Write-Host "     - Repository: bobareichert/HEDIS-MA-Top-12-w-HEI-Prep" -ForegroundColor Gray
Write-Host "     - Branch: main" -ForegroundColor Gray
Write-Host "     - Main file: project/streamlit_app.py" -ForegroundColor Gray
Write-Host "  5. Click 'Deploy'" -ForegroundColor White
Write-Host "  6. Wait 3-5 minutes for deployment" -ForegroundColor White
Write-Host "  7. Copy the URL and share!" -ForegroundColor White
Write-Host ""

Write-Host "Step 4: Verify GitHub Repository" -ForegroundColor Yellow
$gitStatus = git status 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Git repository found" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Make sure your code is pushed to GitHub:" -ForegroundColor Cyan
    Write-Host "    git add ." -ForegroundColor White
    Write-Host "    git commit -m 'Ready for dashboard deployment'" -ForegroundColor White
    Write-Host "    git push origin main" -ForegroundColor White
} else {
    Write-Host "  ⚠ Git not found or not in a repository" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  1. Test dashboard locally (if not done)" -ForegroundColor White
Write-Host "  2. Push code to GitHub" -ForegroundColor White
Write-Host "  3. Deploy to Streamlit Cloud" -ForegroundColor White
Write-Host "  4. Share dashboard URL" -ForegroundColor White
Write-Host ""
Write-Host "  See DASHBOARD_PUBLICATION_PLAN.md for detailed instructions" -ForegroundColor Gray
Write-Host ""

