# Fix Performance Dashboard Order - Clear Cache and Restart
# Run this script to clear Streamlit cache and restart the app

Write-Host "=== PERFORMANCE DASHBOARD ORDER FIX ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Verify file exists
Write-Host "Step 1: Verifying file rename..." -ForegroundColor Yellow
$perfFile = Get-ChildItem "pages\z_Performance_Dashboard.py" -ErrorAction SilentlyContinue
if ($perfFile) {
    Write-Host "  ✓ z_Performance_Dashboard.py found" -ForegroundColor Green
} else {
    Write-Host "  ✗ ERROR: z_Performance_Dashboard.py NOT FOUND" -ForegroundColor Red
    Write-Host "  Please check that the file was renamed correctly." -ForegroundColor Yellow
    exit 1
}

# Step 2: Stop Streamlit processes
Write-Host ""
Write-Host "Step 2: Stopping Streamlit processes..." -ForegroundColor Yellow
$streamlitProcs = Get-Process | Where-Object {$_.ProcessName -like "*streamlit*" -or $_.CommandLine -like "*streamlit*"} -ErrorAction SilentlyContinue
if ($streamlitProcs) {
    $streamlitProcs | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "  ✓ Streamlit processes stopped" -ForegroundColor Green
} else {
    Write-Host "  ℹ No Streamlit processes found (may already be stopped)" -ForegroundColor Gray
}

# Step 3: Clear Streamlit cache
Write-Host ""
Write-Host "Step 3: Clearing Streamlit cache..." -ForegroundColor Yellow
$cachePath = "$env:USERPROFILE\.streamlit\cache"
if (Test-Path $cachePath) {
    try {
        Remove-Item -Path $cachePath -Recurse -Force -ErrorAction Stop
        Write-Host "  ✓ Cache cleared: $cachePath" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ Could not clear cache: $_" -ForegroundColor Yellow
        Write-Host "  You may need to manually delete: $cachePath" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ℹ Cache directory not found (may be empty)" -ForegroundColor Gray
}

# Step 4: Clear Streamlit cache using command
Write-Host ""
Write-Host "Step 4: Running streamlit cache clear..." -ForegroundColor Yellow
try {
    streamlit cache clear 2>&1 | Out-Null
    Write-Host "  ✓ Streamlit cache cleared via command" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Could not run streamlit cache clear (may not be in PATH)" -ForegroundColor Yellow
}

# Step 5: Instructions
Write-Host ""
Write-Host "=== NEXT STEPS ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Close ALL browser tabs with localhost:8502" -ForegroundColor White
Write-Host "2. Open a NEW incognito/private window:" -ForegroundColor White
Write-Host "   - Chrome: Ctrl+Shift+N" -ForegroundColor Gray
Write-Host "   - Firefox: Ctrl+Shift+P" -ForegroundColor Gray
Write-Host "   - Edge: Ctrl+Shift+N" -ForegroundColor Gray
Write-Host "3. Restart Streamlit:" -ForegroundColor White
Write-Host "   streamlit run app.py --server.port 8502" -ForegroundColor Green
Write-Host "4. Navigate to: http://localhost:8502" -ForegroundColor White
Write-Host "5. Check sidebar - Performance Dashboard should be at the BOTTOM" -ForegroundColor White
Write-Host ""
Write-Host "=== VERIFICATION ===" -ForegroundColor Cyan
Write-Host "Expected sidebar order (last 3 items):" -ForegroundColor Yellow
Write-Host "  ..." -ForegroundColor Gray
Write-Host "  ⚖️ Health Equity Index" -ForegroundColor White
Write-Host "  ⚡ Performance Dashboard  ← Should be HERE (BOTTOM)" -ForegroundColor Green
Write-Host ""

# Optional: Auto-restart Streamlit
$restart = Read-Host "Do you want to restart Streamlit now? (Y/N)"
if ($restart -eq "Y" -or $restart -eq "y") {
    Write-Host ""
    Write-Host "Starting Streamlit..." -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
    Write-Host ""
    streamlit run app.py --server.port 8502
}

