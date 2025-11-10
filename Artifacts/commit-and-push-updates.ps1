# Script to Commit and Push README Updates to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Commit and Push README Updates" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repos = @(
    @{
        Name = "cipher"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\cipher"
        RepoName = "cipher-threat-tracker"
    },
    @{
        Name = "foresight"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\foresight"
        RepoName = "foresight-crime-prediction"
    },
    @{
        Name = "guardian"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\guardian"
        RepoName = "guardian-fraud-analytics"
    }
)

$successCount = 0
$failCount = 0

foreach ($repo in $repos) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Processing: $($repo.Name)" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    if (-not (Test-Path $repo.Path)) {
        Write-Host "  [SKIP] Path not found: $($repo.Path)" -ForegroundColor Yellow
        $failCount++
        continue
    }
    
    Push-Location $repo.Path
    
    # Check for changes
    $status = git status --short README.md
    if ($status) {
        Write-Host "  [FOUND] Changes detected in README.md" -ForegroundColor Yellow
        
        # Stage README.md
        Write-Host "  Staging README.md..." -ForegroundColor Cyan
        git add README.md 2>&1 | Out-Null
        
        # Commit
        Write-Host "  Committing changes..." -ForegroundColor Cyan
        $commitMessage = "Update README: Fix broken links and demo site references"
        git commit -m $commitMessage 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [PASS] Changes committed" -ForegroundColor Green
            
            # Push
            Write-Host "  Pushing to GitHub..." -ForegroundColor Cyan
            git push 2>&1 | Out-Null
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  [PASS] Successfully pushed to GitHub!" -ForegroundColor Green
                Write-Host "  Repository: https://github.com/reichert-sentinel-ai/$($repo.RepoName)" -ForegroundColor Cyan
                $successCount++
            } else {
                Write-Host "  [FAIL] Failed to push to GitHub" -ForegroundColor Red
                $failCount++
            }
        } else {
            Write-Host "  [FAIL] Failed to commit changes" -ForegroundColor Red
            $failCount++
        }
    } else {
        Write-Host "  [SKIP] No changes to commit" -ForegroundColor Yellow
    }
    
    Pop-Location
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Successful: $successCount" -ForegroundColor Green
Write-Host "Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($successCount -eq 3) {
    Write-Host "[SUCCESS] All README updates pushed to GitHub!" -ForegroundColor Green
} elseif ($successCount -gt 0) {
    Write-Host "[PARTIAL] Some updates pushed. Check failures above." -ForegroundColor Yellow
} else {
    Write-Host "[INFO] No changes to push or all pushes failed." -ForegroundColor Yellow
}

Write-Host ""

