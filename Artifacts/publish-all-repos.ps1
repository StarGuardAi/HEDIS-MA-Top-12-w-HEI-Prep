# PowerShell Script to Create and Publish All Intelligence-Security Repositories
# This script creates repositories on GitHub and pushes local code

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Publishing Intelligence-Security Repos" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repos = @(
    @{
        Name = "cipher"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\cipher"
        RepoName = "cipher-threat-tracker"
        Description = "Cyber Threat Attribution & Analysis Platform - Zero-day detection, IOC tracking, and threat attribution using autoencoders and MITRE ATT&CK framework"
        GitHubUrl = "https://github.com/reichert-sentinel-ai/cipher-threat-tracker"
    },
    @{
        Name = "foresight"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\foresight"
        RepoName = "foresight-crime-prediction"
        Description = "Predictive Crime Intelligence Platform - Crime forecasting, hotspot detection, and patrol optimization using Prophet and DBSCAN"
        GitHubUrl = "https://github.com/reichert-sentinel-ai/foresight-crime-prediction"
    },
    @{
        Name = "guardian"
        Path = "C:\Users\reich\Projects\intelligence-security\repos\guardian"
        RepoName = "guardian-fraud-analytics"
        Description = "AI-Powered Fraud Detection System - Real-time fraud detection with XGBoost and Graph Neural Networks"
        GitHubUrl = "https://github.com/reichert-sentinel-ai/guardian-fraud-analytics"
    }
)

$successCount = 0
$failCount = 0

foreach ($repo in $repos) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Processing: $($repo.Name) -> $($repo.RepoName)" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    if (-not (Test-Path $repo.Path)) {
        Write-Host "ERROR: Path does not exist: $($repo.Path)" -ForegroundColor Red
        $failCount++
        continue
    }
    
    Push-Location $repo.Path
    
    # Check if repository already exists on GitHub
    Write-Host "Checking if repository exists on GitHub..." -ForegroundColor Yellow
    $repoExists = $false
    $checkResult = gh repo view "reichert-sentinel-ai/$($repo.RepoName)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Repository already exists on GitHub" -ForegroundColor Green
        $repoExists = $true
    } else {
        Write-Host "Repository does not exist yet, will create it" -ForegroundColor Yellow
    }
    
    # Create repository if it doesn't exist
    if (-not $repoExists) {
        Write-Host ""
        Write-Host "Creating repository on GitHub..." -ForegroundColor Cyan
        $createResult = gh repo create "reichert-sentinel-ai/$($repo.RepoName)" --public --description $repo.Description 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Repository created successfully!" -ForegroundColor Green
        } else {
            Write-Host "ERROR: Failed to create repository" -ForegroundColor Red
            Write-Host "Error: $createResult" -ForegroundColor Red
            $failCount++
            Pop-Location
            continue
        }
    }
    
    # Check git status
    Write-Host ""
    Write-Host "Checking git status..." -ForegroundColor Cyan
    $uncommitted = git status --short
    if ($uncommitted) {
        $uncommittedCount = ($uncommitted | Measure-Object -Line).Lines
        Write-Host "Found $uncommittedCount uncommitted changes" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Committing changes..." -ForegroundColor Cyan
        git add . 2>&1 | Out-Null
        $commitMessage = "Initial commit: $($repo.RepoName)"
        git commit -m $commitMessage 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Changes committed" -ForegroundColor Green
        } else {
            Write-Host "No changes to commit or commit failed" -ForegroundColor Yellow
        }
    } else {
        Write-Host "No uncommitted changes" -ForegroundColor Green
    }
    
    # Check current branch
    $currentBranch = git branch --show-current
    if ([string]::IsNullOrWhiteSpace($currentBranch)) {
        Write-Host "Creating main branch..." -ForegroundColor Yellow
        git checkout -b main 2>&1 | Out-Null
        $currentBranch = "main"
    }
    Write-Host "Current branch: $currentBranch" -ForegroundColor Cyan
    
    # Set remote if not already set
    $remoteUrl = git remote get-url origin 2>&1
    $expectedRemote = "https://github.com/reichert-sentinel-ai/$($repo.RepoName).git"
    if ($remoteUrl -notlike "*$($repo.RepoName)*") {
        if ($LASTEXITCODE -eq 0 -and $remoteUrl) {
            Write-Host "Updating remote URL..." -ForegroundColor Yellow
            git remote set-url origin $expectedRemote 2>&1 | Out-Null
        } else {
            Write-Host "Adding remote..." -ForegroundColor Yellow
            git remote add origin $expectedRemote 2>&1 | Out-Null
        }
    }
    
    # Push to GitHub
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
    $pushOutput = git push -u origin $currentBranch 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
        Write-Host "Repository URL: $($repo.GitHubUrl)" -ForegroundColor Green
        $successCount++
    } else {
        # Try pushing to main if current branch failed
        if ($currentBranch -ne "main") {
            Write-Host "Attempting to push to main branch..." -ForegroundColor Yellow
            git checkout -b main 2>&1 | Out-Null
            $pushOutput = git push -u origin main 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
                Write-Host "Repository URL: $($repo.GitHubUrl)" -ForegroundColor Green
                $successCount++
            } else {
                Write-Host "ERROR: Failed to push to GitHub" -ForegroundColor Red
                Write-Host "Error: $pushOutput" -ForegroundColor Red
                $failCount++
            }
        } else {
            Write-Host "ERROR: Failed to push to GitHub" -ForegroundColor Red
            Write-Host "Error: $pushOutput" -ForegroundColor Red
            $failCount++
        }
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
    Write-Host "All repositories published successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repository URLs:" -ForegroundColor Cyan
    foreach ($repo in $repos) {
        Write-Host "  - $($repo.RepoName): $($repo.GitHubUrl)" -ForegroundColor Cyan
    }
    Write-Host ""
    Write-Host "Verify at: https://github.com/reichert-sentinel-ai" -ForegroundColor Cyan
} else {
    Write-Host "Some repositories failed to publish. Please check errors above." -ForegroundColor Yellow
}
