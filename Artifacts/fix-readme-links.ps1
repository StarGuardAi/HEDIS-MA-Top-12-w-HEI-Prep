# Script to Fix Broken Links in README Files
# Updates demo site, ROI calculator, and community/status site references

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fix README Broken Links" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repos = @(
    @{
        Name = "cipher"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\cipher\README.md"
        RepoName = "cipher-threat-tracker"
    },
    @{
        Name = "foresight"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\foresight\README.md"
        RepoName = "foresight-crime-prediction"
    },
    @{
        Name = "guardian"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\guardian\README.md"
        RepoName = "guardian-fraud-analytics"
    }
)

$changesMade = 0

foreach ($repo in $repos) {
    Write-Host ""
    Write-Host "Processing: $($repo.Name)" -ForegroundColor Cyan
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    
    if (-not (Test-Path $repo.Path)) {
        Write-Host "  [SKIP] README.md not found: $($repo.Path)" -ForegroundColor Yellow
        continue
    }
    
    $content = Get-Content $repo.Path -Raw
    $originalContent = $content
    
    # Fix 1: Update "Try Before You Clone" section
    # Replace demo site links with setup instructions
    if ($content -match '(?s)## 🚀 Try Before You Clone.*?---') {
        $tryBeforeSection = $matches[0]
        
        # Create replacement section
        $newTryBeforeSection = @"
## 🚀 Quick Start

**Local Setup:**
- Clone the repository and follow the installation instructions below
- All features are available when running locally
- See [Quick Start](#quick-start) section for setup instructions

**Demo:**
- Interactive demo coming soon
- For now, please use the local setup instructions to run the project

---
"@
        
        $content = $content -replace [regex]::Escape($tryBeforeSection), $newTryBeforeSection
        Write-Host "  [FIX] Updated 'Try Before You Clone' section" -ForegroundColor Green
        $changesMade++
    }
    
    # Fix 2: Remove or update ROI calculator links
    $roiPattern = '\[Calculate your ROI[^\]]*\]\(https://roi\.sentinel-analytics\.dev/[^\)]+\)'
    if ($content -match $roiPattern) {
        $content = $content -replace $roiPattern, '*ROI Calculator: Coming soon*'
        Write-Host "  [FIX] Updated ROI calculator links" -ForegroundColor Green
        $changesMade++
    }
    
    # Fix 3: Remove or update community dashboard links
    $communityPattern = '\[View Community Dashboard[^\]]*\]\(https://community\.sentinel-analytics\.dev\)'
    if ($content -match $communityPattern) {
        $content = $content -replace $communityPattern, '*Community Dashboard: Coming soon*'
        Write-Host "  [FIX] Updated community dashboard links" -ForegroundColor Green
        $changesMade++
    }
    
    # Fix 4: Remove or update status page links
    $statusPattern = '\*\*Live Status:\*\*\s*\[status\.sentinel-analytics\.dev\]\(https://status\.sentinel-analytics\.dev\)'
    if ($content -match $statusPattern) {
        $content = $content -replace $statusPattern, '**Status:** *Coming soon*'
        Write-Host "  [FIX] Updated status page links" -ForegroundColor Green
        $changesMade++
    }
    
    # Fix 5: Remove status subscribe links
    $subscribePattern = '\[Subscribe to Status Updates[^\]]*\]\(https://status\.sentinel-analytics\.dev/subscribe\)'
    if ($content -match $subscribePattern) {
        $content = $content -replace $subscribePattern, ''
        Write-Host "  [FIX] Removed status subscribe links" -ForegroundColor Green
        $changesMade++
    }
    
    # Fix 6: Update localhost links to be clearer (optional - keep these as they're for local dev)
    # We'll leave localhost links as they're expected for local development
    
    # Save if changes were made
    if ($content -ne $originalContent) {
        # Create backup
        $backupPath = "$($repo.Path).backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item $repo.Path $backupPath
        Write-Host "  [BACKUP] Created backup: $(Split-Path $backupPath -Leaf)" -ForegroundColor Cyan
        
        # Save updated content
        Set-Content -Path $repo.Path -Value $content -NoNewline
        Write-Host "  [SAVE] README.md updated" -ForegroundColor Green
    } else {
        Write-Host "  [SKIP] No changes needed" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Changes made: $changesMade" -ForegroundColor $(if ($changesMade -gt 0) { "Green" } else { "Yellow" })
Write-Host ""

if ($changesMade -gt 0) {
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Review the changes in each README.md file" -ForegroundColor Yellow
    Write-Host "2. Commit and push changes to GitHub" -ForegroundColor Yellow
    Write-Host "3. Run validation script again to verify" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To commit changes:" -ForegroundColor Cyan
    Write-Host "  cd C:\Users\reich\Projects\intelligence-security\repos\[repo-name]" -ForegroundColor White
    Write-Host "  git add README.md" -ForegroundColor White
    Write-Host "  git commit -m 'Update README: Fix broken links and demo site references'" -ForegroundColor White
    Write-Host "  git push" -ForegroundColor White
} else {
    Write-Host "No changes were needed. All links are already updated." -ForegroundColor Green
}

