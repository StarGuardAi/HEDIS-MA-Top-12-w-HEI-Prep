# PowerShell Script to Push Intelligence-Security Repositories to GitHub
# This script helps push the three repositories to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Intelligence-Security Repositories Push" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repos = @(
    @{
        Name = "cipher"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\cipher"
        Remote = "https://github.com/reichert-sentinel-ai/cipher-threat-tracker.git"
        GitHubUrl = "https://github.com/reichert-sentinel-ai/cipher-threat-tracker"
    },
    @{
        Name = "foresight"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\foresight"
        Remote = "https://github.com/reichert-sentinel-ai/foresight-crime-prediction.git"
        GitHubUrl = "https://github.com/reichert-sentinel-ai/foresight-crime-prediction"
    },
    @{
        Name = "guardian"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\guardian"
        Remote = "https://github.com/reichert-sentinel-ai/guardian-fraud-analytics.git"
        GitHubUrl = "https://github.com/reichert-sentinel-ai/guardian-fraud-analytics"
    }
)

Write-Host "IMPORTANT: Before running this script:" -ForegroundColor Yellow
Write-Host "1. Create the repositories on GitHub first:" -ForegroundColor Yellow
Write-Host "   - Go to https://github.com/reichert-sentinel-ai" -ForegroundColor Yellow
Write-Host "   - Click 'New repository' for each:" -ForegroundColor Yellow
Write-Host "     * cipher-threat-tracker" -ForegroundColor Yellow
Write-Host "     * foresight-crime-prediction" -ForegroundColor Yellow
Write-Host "     * guardian-fraud-analytics" -ForegroundColor Yellow
Write-Host "2. Make sure repositories are PUBLIC" -ForegroundColor Yellow
Write-Host "3. Do NOT initialize with README, .gitignore, or license" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to continue (or Ctrl+C to cancel)..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

foreach ($repo in $repos) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Processing: $($repo.Name)" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    if (-not (Test-Path $repo.Path)) {
        Write-Host "ERROR: Path does not exist: $($repo.Path)" -ForegroundColor Red
        continue
    }
    
    Push-Location $repo.Path
    
    # Check if it's a git repository
    if (-not (Test-Path ".git")) {
        Write-Host "WARNING: Not a git repository. Initializing..." -ForegroundColor Yellow
        git init
        git remote add origin $repo.Remote
    } else {
        Write-Host "✓ Git repository found" -ForegroundColor Green
        
        # Check remote
        $remote = git remote get-url origin 2>$null
        if ($remote -ne $repo.Remote) {
            Write-Host "Updating remote URL..." -ForegroundColor Yellow
            git remote set-url origin $repo.Remote
        }
        Write-Host "✓ Remote configured: $($repo.Remote)" -ForegroundColor Green
    }
    
    # Check for uncommitted changes
    $status = git status --short
    if ($status) {
        Write-Host "WARNING: Uncommitted changes found:" -ForegroundColor Yellow
        git status --short
        Write-Host ""
        $commit = Read-Host "Do you want to commit these changes? (y/n)"
        if ($commit -eq "y" -or $commit -eq "Y") {
            $message = Read-Host "Enter commit message (or press Enter for default)"
            if ([string]::IsNullOrWhiteSpace($message)) {
                $message = "Initial commit: Push $($repo.Name) to GitHub"
            }
            git add .
            git commit -m $message
            Write-Host "✓ Changes committed" -ForegroundColor Green
        }
    }
    
    # Check current branch
    $currentBranch = git branch --show-current
    if ([string]::IsNullOrWhiteSpace($currentBranch)) {
        Write-Host "No branch found. Creating 'main' branch..." -ForegroundColor Yellow
        git checkout -b main
        $currentBranch = "main"
    }
    Write-Host "✓ Current branch: $currentBranch" -ForegroundColor Green
    
    # Check if repository exists on GitHub
    Write-Host ""
    Write-Host "Checking if repository exists on GitHub..." -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri $repo.GitHubUrl -Method Head -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "✓ Repository exists on GitHub" -ForegroundColor Green
        }
    } catch {
        Write-Host "⚠ Repository does not exist on GitHub yet!" -ForegroundColor Yellow
        Write-Host "   Please create it at: $($repo.GitHubUrl)" -ForegroundColor Yellow
        Write-Host "   Then press any key to continue..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
    
    # Push to GitHub
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
    try {
        # Try to push to main first, fallback to master
        $pushSuccess = $false
        try {
            git push -u origin $currentBranch 2>&1 | Out-String
            $pushSuccess = $true
            Write-Host "✓ Successfully pushed to GitHub!" -ForegroundColor Green
        } catch {
            # If main doesn't work, try master
            if ($currentBranch -ne "master") {
                Write-Host "Trying to push to 'master' branch..." -ForegroundColor Yellow
                git checkout -b master 2>$null
                git push -u origin master 2>&1 | Out-String
                $pushSuccess = $true
                Write-Host "✓ Successfully pushed to GitHub!" -ForegroundColor Green
            }
        }
        
        if (-not $pushSuccess) {
            throw "Push failed"
        }
        
        Write-Host ""
        Write-Host "Repository URL: $($repo.GitHubUrl)" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to push to GitHub" -ForegroundColor Red
        Write-Host "Error details: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Troubleshooting:" -ForegroundColor Yellow
        Write-Host "1. Make sure the repository exists on GitHub" -ForegroundColor Yellow
        Write-Host "2. Check your GitHub authentication (git credential)" -ForegroundColor Yellow
        Write-Host "3. Verify you have write access to the repository" -ForegroundColor Yellow
    }
    
    Pop-Location
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Verify repositories are public and accessible" -ForegroundColor Green
Write-Host "2. Check that all files are pushed correctly" -ForegroundColor Green
Write-Host "3. Update documentation with correct GitHub URLs" -ForegroundColor Green
Write-Host ""
Write-Host "Repository URLs:" -ForegroundColor Cyan
foreach ($repo in $repos) {
    Write-Host "  - $($repo.Name): $($repo.GitHubUrl)" -ForegroundColor Cyan
}
Write-Host ""

