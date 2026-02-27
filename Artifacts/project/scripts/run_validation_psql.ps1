# PowerShell script to run full system validation via psql
# Usage: .\run_validation_psql.ps1

$ErrorActionPreference = "Stop"

# Database configuration
$DB_HOST = if ($env:DB_HOST) { $env:DB_HOST } else { "localhost" }
$DB_NAME = if ($env:DB_NAME) { $env:DB_NAME } else { "hedis_portfolio" }
$DB_USER = if ($env:DB_USER) { $env:DB_USER } else { "hedis_api" }
$DB_PASSWORD = if ($env:DB_PASSWORD) { $env:DB_PASSWORD } else { "hedis_password" }
$DB_PORT = if ($env:DB_PORT) { $env:DB_PORT } else { "5432" }

# Paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ValidationScript = Join-Path $ScriptDir "validate_full_system.sql"
$OutputFile = Join-Path $ScriptDir "validation_report.txt"

Write-Host "=" -NoNewline
Write-Host ("=" * 79)
Write-Host "HEDIS STAR RATING PORTFOLIO OPTIMIZER"
Write-Host "FULL SYSTEM VALIDATION SUITE"
Write-Host "=" -NoNewline
Write-Host ("=" * 79)
Write-Host ""

if (-not (Test-Path $ValidationScript)) {
    Write-Host "[ERROR] Validation script not found: $ValidationScript" -ForegroundColor Red
    exit 1
}

Write-Host "[INFO] Running validation via psql..."
Write-Host "[INFO] Output will be saved to: $OutputFile"
Write-Host ""

# Set PGPASSWORD environment variable
$env:PGPASSWORD = $DB_PASSWORD

try {
    # Run psql with the validation script
    $psqlArgs = @(
        "-h", $DB_HOST,
        "-p", $DB_PORT,
        "-U", $DB_USER,
        "-d", $DB_NAME,
        "-f", $ValidationScript
    )
    
    # Execute psql and capture output
    $output = & psql $psqlArgs 2>&1
    
    # Save to file
    $output | Out-File -FilePath $OutputFile -Encoding UTF8
    
    # Display to console
    $output
    
    Write-Host ""
    Write-Host "[OK] Validation complete! Report saved to: $OutputFile" -ForegroundColor Green
    
} catch {
    Write-Host "[ERROR] Failed to run validation: $_" -ForegroundColor Red
    exit 1
} finally {
    # Clear password from environment
    Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
}

