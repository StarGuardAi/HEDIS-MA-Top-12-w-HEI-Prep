# PowerShell script to find psql and run validation
# Searches common PostgreSQL installation locations

$ErrorActionPreference = "Stop"

# Common PostgreSQL installation paths
$psqlPaths = @(
    "C:\Program Files\PostgreSQL\*\bin\psql.exe",
    "C:\Program Files (x86)\PostgreSQL\*\bin\psql.exe",
    "$env:ProgramFiles\PostgreSQL\*\bin\psql.exe",
    "$env:ProgramFiles(x86)\PostgreSQL\*\bin\psql.exe",
    "$env:LOCALAPPDATA\Programs\PostgreSQL\*\bin\psql.exe"
)

# Also check PATH
$psqlInPath = Get-Command psql -ErrorAction SilentlyContinue

if ($psqlInPath) {
    $psqlExe = $psqlInPath.Source
    Write-Host "[OK] Found psql in PATH: $psqlExe" -ForegroundColor Green
} else {
    # Search for psql in common locations
    $found = $false
    foreach ($pattern in $psqlPaths) {
        $matches = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($matches) {
            $psqlExe = $matches.FullName
            Write-Host "[OK] Found psql: $psqlExe" -ForegroundColor Green
            $found = $true
            break
        }
    }
    
    if (-not $found) {
        Write-Host "[ERROR] psql not found. Please:" -ForegroundColor Red
        Write-Host "  1. Install PostgreSQL client tools, OR"
        Write-Host "  2. Add PostgreSQL bin directory to PATH, OR"
        Write-Host "  3. Run: python quick_validation_check.py (for quick validation)"
        exit 1
    }
}

# Database configuration
$DB_HOST = if ($env:DB_HOST) { $env:DB_HOST } else { "localhost" }
$DB_NAME = if ($env:DB_NAME) { $env:DB_NAME } else { "hedis_portfolio" }
$DB_USER = if ($env:DB_USER) { $env:DB_USER } else { "hedis_api" }
$DB_PASSWORD = if ($env:DB_PASSWORD) { $env:DB_PASSWORD } else { "hedis_password" }
$DB_PORT = if ($env:DB_PORT) { $env:DB_PORT } else { "5432" }

# Script paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ValidationScript = Join-Path $ScriptDir "validate_full_system.sql"
$OutputFile = Join-Path $ScriptDir "validation_report.txt"

if (-not (Test-Path $ValidationScript)) {
    Write-Host "[ERROR] Validation script not found: $ValidationScript" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=" -NoNewline
Write-Host ("=" * 79)
Write-Host "Running Full System Validation"
Write-Host "=" -NoNewline
Write-Host ("=" * 79)
Write-Host ""
Write-Host "Database: $DB_NAME on $DB_HOST:$DB_PORT"
Write-Host "Output: $OutputFile"
Write-Host ""
Write-Host "[INFO] This will take 5-7 minutes..."
Write-Host ""

# Set password
$env:PGPASSWORD = $DB_PASSWORD

try {
    # Run psql
    $psqlArgs = @(
        "-h", $DB_HOST,
        "-p", $DB_PORT,
        "-U", $DB_USER,
        "-d", $DB_NAME,
        "-f", $ValidationScript
    )
    
    & $psqlExe $psqlArgs | Out-File -FilePath $OutputFile -Encoding UTF8
    
    Write-Host "[OK] Validation complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Report saved to: $OutputFile"
    Write-Host ""
    Write-Host "First 50 lines of report:"
    Write-Host ("-" * 80)
    Get-Content $OutputFile -TotalCount 50
    
    Write-Host ""
    Write-Host ("-" * 80)
    Write-Host "To view full report:"
    Write-Host "  Get-Content $OutputFile"
    Write-Host "  or"
    Write-Host "  notepad $OutputFile"
    
} catch {
    Write-Host "[ERROR] Validation failed: $_" -ForegroundColor Red
    exit 1
} finally {
    Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
}

