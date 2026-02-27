# Setup GitHub Token Secure Storage
# This script sets up PowerShell SecretManagement and stores your GitHub token securely

Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "GITHUB TOKEN SECURE STORAGE SETUP" -ForegroundColor Cyan
Write-Host ("="*60) -ForegroundColor Cyan

# Step 1: Install modules if needed
Write-Host "`n[1/4] Checking/Installing SecretManagement modules..." -ForegroundColor Yellow
try {
    if (-not (Get-Module -ListAvailable -Name Microsoft.PowerShell.SecretManagement)) {
        Write-Host "  Installing SecretManagement..." -ForegroundColor Gray
        Install-Module Microsoft.PowerShell.SecretManagement -Scope CurrentUser -Force -AllowClobber
    }
    if (-not (Get-Module -ListAvailable -Name Microsoft.PowerShell.SecretStore)) {
        Write-Host "  Installing SecretStore..." -ForegroundColor Gray
        Install-Module Microsoft.PowerShell.SecretStore -Scope CurrentUser -Force -AllowClobber
    }
    Write-Host "  [OK] Modules ready" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Failed to install modules: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 2: Register vault
Write-Host "`n[2/4] Registering SecretStore vault..." -ForegroundColor Yellow
try {
    $vaults = Get-SecretVault
    if ($vaults.Name -contains "LocalSecrets") {
        Write-Host "  [OK] Vault already registered" -ForegroundColor Green
    } else {
        Write-Host "  Registering vault (you'll need to create a vault password)..." -ForegroundColor Gray
        Register-SecretVault -Name LocalSecrets -ModuleName Microsoft.PowerShell.SecretStore -DefaultVault
        Write-Host "  [OK] Vault registered" -ForegroundColor Green
    }
} catch {
    Write-Host "  [ERROR] Failed to register vault: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 3: Get token from user
Write-Host "`n[3/4] Storing GitHub token..." -ForegroundColor Yellow
$existingToken = $null
try {
    $existingToken = Get-Secret -Name GITHUB_TOKEN -Vault LocalSecrets -AsPlainText -ErrorAction SilentlyContinue
    if ($existingToken) {
        Write-Host "  [!] Token already exists in vault" -ForegroundColor Yellow
        $overwrite = Read-Host "  Overwrite existing token? (yes/no)"
        if ($overwrite -notmatch "^[Yy]") {
            Write-Host "  Keeping existing token" -ForegroundColor Green
            Write-Host "`n[OK] Setup complete! Token stored securely." -ForegroundColor Green
            exit 0
        }
    }
} catch {
    # Token doesn't exist, which is fine
}

Write-Host "`n  Enter your GitHub Personal Access Token" -ForegroundColor Cyan
Write-Host "  (Get one from: https://github.com/settings/tokens)" -ForegroundColor Gray
Write-Host "`n  IMPORTANT: If you shared your token earlier, create a NEW one!" -ForegroundColor Yellow
$token = Read-Host "  Token" -AsSecureString

# Convert secure string to plain text for storage
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
$plainToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

try {
    Set-Secret -Name GITHUB_TOKEN -Secret $plainToken -Vault LocalSecrets
    Write-Host "  [OK] Token stored securely in vault" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Failed to store token: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 4: Update check_github_status.ps1 to use stored token
Write-Host "`n[4/4] Updating check_github_status.ps1 to use stored token..." -ForegroundColor Yellow
$scriptPath = Join-Path $PSScriptRoot "check_github_status.ps1"
if (Test-Path $scriptPath) {
    $scriptContent = Get-Content $scriptPath -Raw
    
    # Add function to retrieve token from vault at the top of script
    $tokenFunction = @'

# Function to retrieve GitHub token from secure storage
function Get-GitHubToken {
    try {
        if (Get-Module -ListAvailable -Name Microsoft.PowerShell.SecretManagement) {
            Import-Module Microsoft.PowerShell.SecretManagement -ErrorAction SilentlyContinue
            $vault = Get-SecretVault -Name LocalSecrets -ErrorAction SilentlyContinue
            if ($vault) {
                return Get-Secret -Name GITHUB_TOKEN -Vault LocalSecrets -AsPlainText -ErrorAction SilentlyContinue
            }
        }
        return $null
    } catch {
        return $null
    }
}

'@
    
    # Check if function already exists
    if ($scriptContent -notmatch "function Get-GitHubToken") {
        # Insert after param block
        $scriptContent = $scriptContent -replace "(param\([^)]+\))", "`$1`n`n$tokenFunction"
        Set-Content -Path $scriptPath -Value $scriptContent -Encoding UTF8
        Write-Host "  [OK] Script updated to use secure token storage" -ForegroundColor Green
    } else {
        Write-Host "  [OK] Script already configured for secure storage" -ForegroundColor Green
    }
} else {
    Write-Host "  [!] Script not found, skipping update" -ForegroundColor Yellow
}

# Summary
Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "SETUP COMPLETE" -ForegroundColor Cyan
Write-Host ("="*60) -ForegroundColor Cyan
Write-Host "`nYour GitHub token is now stored securely!" -ForegroundColor Green
Write-Host "`nTo use it in scripts, add this at the beginning:" -ForegroundColor Cyan
Write-Host @'
    $token = Get-Secret -Name GITHUB_TOKEN -Vault LocalSecrets -AsPlainText
    $headers = @{
        "Accept" = "application/vnd.github.v3+json"
        "Authorization" = "token $token"
    }
'@ -ForegroundColor Gray

Write-Host "`nTo retrieve token manually:" -ForegroundColor Cyan
Write-Host '  Get-Secret -Name GITHUB_TOKEN -Vault LocalSecrets -AsPlainText' -ForegroundColor Gray

Write-Host "`nTo remove token:" -ForegroundColor Cyan
Write-Host '  Remove-Secret -Name GITHUB_TOKEN -Vault LocalSecrets' -ForegroundColor Gray
Write-Host ""


