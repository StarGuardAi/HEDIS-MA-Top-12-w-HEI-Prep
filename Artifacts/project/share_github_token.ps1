# Share GitHub Token from Secure Storage
# This script helps you retrieve and share your stored GitHub token

Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "GITHUB TOKEN SHARING TOOL" -ForegroundColor Cyan
Write-Host ("="*60) -ForegroundColor Cyan

# Retrieve token from secure storage
try {
    $token = Get-Secret -Name GITHUB_TOKEN -Vault LocalSecrets -AsPlainText
    if (-not $token) {
        Write-Host "`n[ERROR] Token not found in secure storage" -ForegroundColor Red
        Write-Host "  Run setup_github_token.ps1 first to store your token" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "`nToken retrieved successfully!" -ForegroundColor Green
    Write-Host "`nChoose how to share:" -ForegroundColor Cyan
    Write-Host "  1. Copy to clipboard" -ForegroundColor Yellow
    Write-Host "  2. Display in terminal (you can copy manually)" -ForegroundColor Yellow
    Write-Host "  3. Save to temporary file" -ForegroundColor Yellow
    Write-Host "  4. Copy as PowerShell variable assignment" -ForegroundColor Yellow
    Write-Host "  5. Copy as curl/API header format" -ForegroundColor Yellow
    
    $choice = Read-Host "`nEnter choice (1-5)"
    
    switch ($choice) {
        "1" {
            Set-Clipboard -Value $token
            Write-Host "`n[OK] Token copied to clipboard!" -ForegroundColor Green
            Write-Host "  Token preview: $($token.Substring(0, [Math]::Min(20, $token.Length)))..." -ForegroundColor Gray
        }
        "2" {
            Write-Host "`nYour GitHub token:" -ForegroundColor Cyan
            Write-Host $token -ForegroundColor White
            Write-Host "`n[OK] Token displayed above - copy it manually" -ForegroundColor Green
        }
        "3" {
            $tempFile = Join-Path $env:TEMP "github_token_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
            Set-Content -Path $tempFile -Value $token -NoNewline
            Write-Host "`n[OK] Token saved to temporary file:" -ForegroundColor Green
            Write-Host "  $tempFile" -ForegroundColor Gray
            Write-Host "`n  IMPORTANT: Delete this file after sharing!" -ForegroundColor Yellow
            Write-Host "  To open: notepad `"$tempFile`"" -ForegroundColor Gray
        }
        "4" {
            $psVar = '$token = "' + $token + '"'
            Set-Clipboard -Value $psVar
            Write-Host "`n[OK] PowerShell variable copied to clipboard!" -ForegroundColor Green
            Write-Host "  Format: `$token = `"...`"" -ForegroundColor Gray
        }
        "5" {
            $curlHeader = "Authorization: token $token"
            Set-Clipboard -Value $curlHeader
            Write-Host "`n[OK] Authorization header copied to clipboard!" -ForegroundColor Green
            Write-Host "  Format: Authorization: token <your-token>" -ForegroundColor Gray
        }
        default {
            Write-Host "`n[ERROR] Invalid choice" -ForegroundColor Red
            exit 1
        }
    }
    
    Write-Host "`nSecurity reminder:" -ForegroundColor Yellow
    Write-Host "  - Only share tokens through secure channels" -ForegroundColor Gray
    Write-Host "  - Revoke and recreate tokens if accidentally exposed" -ForegroundColor Gray
    Write-Host "  - Use fine-grained tokens with minimal permissions" -ForegroundColor Gray
    
} catch {
    Write-Host "`n[ERROR] Failed to retrieve token: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Make sure SecretManagement modules are installed and vault is registered" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

