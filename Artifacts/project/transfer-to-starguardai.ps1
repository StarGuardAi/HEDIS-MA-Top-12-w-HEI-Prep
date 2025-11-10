# transfer-to-starguardai.ps1
# Transfer repository from reichert-science-intelligence to StarGuardAi organization

$ErrorActionPreference = 'Stop'

Write-Host "[INFO] Transferring repository to StarGuardAi organization..."

# Check GitHub CLI authentication
Write-Host "[INFO] Checking GitHub CLI authentication..."
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] GitHub CLI not authenticated. Please run: gh auth login"
    exit 1
}

Write-Host "[OK] GitHub CLI authenticated"

# Transfer the repository
Write-Host "[INFO] Transferring reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep to StarGuardAi..."
gh repo transfer reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep StarGuardAi --yes

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Repository transferred successfully!"
    Write-Host "[INFO] New URL: https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep"
    
    # Update local remote URL
    Write-Host "[INFO] Updating local git remote URL..."
    git remote set-url origin https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep.git
    Write-Host "[OK] Local remote URL updated"
} else {
    Write-Host "[ERROR] Transfer failed. Check error message above."
    exit 1
}

Write-Host "[OK] Transfer complete!"

