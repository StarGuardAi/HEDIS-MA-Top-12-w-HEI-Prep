# push-all-repos.ps1
# Initialize and push all 3 repos to GitHub

$ErrorActionPreference = 'Stop'
$projectRoot = "C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep"

function Setup-Repo {
    param(
        [string]$RepoDir,
        [string]$RepoName,
        [string]$CommitMessage
    )
    
    Write-Host "[INFO] Setting up $RepoName..."
    
    $fullPath = Join-Path $projectRoot $RepoDir
    
    if (-not (Test-Path $fullPath)) {
        Write-Host "[ERROR] Directory does not exist: $fullPath"
        return
    }
    
    Push-Location $fullPath
    
    # Initialize git
    git init
    git add .
    git commit -m $CommitMessage
    git branch -M main
    
    # Set remote and push
    git remote add origin "https://github.com/reichert-sentinel-ai/$RepoName.git"
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] $RepoName pushed to GitHub"
    } else {
        Write-Host "[ERROR] Failed to push $RepoName"
    }
    
    Pop-Location
}

# Setup Guardian
Setup-Repo -RepoDir "repo-guardian" -RepoName "guardian-fraud-analytics" -CommitMessage "Initial commit: Guardian fraud detection system"

# Setup Foresight
Setup-Repo -RepoDir "repo-foresight" -RepoName "foresight-crime-prediction" -CommitMessage "Initial commit: Foresight crime prediction platform"

# Setup Cipher
Setup-Repo -RepoDir "repo-cipher" -RepoName "cipher-threat-tracker" -CommitMessage "Initial commit: Cipher threat tracker"

Write-Host "[OK] All repos set up and pushed to GitHub"

