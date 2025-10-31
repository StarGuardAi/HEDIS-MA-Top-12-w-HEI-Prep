# organize-content.ps1
# Organizes sentinel-migrated content into 3 project directories

$ErrorActionPreference = 'Stop'
$source = ".\sentinel-migrated"
$guardian = ".\repo-guardian"
$foresight = ".\repo-foresight"
$cipher = ".\repo-cipher"

Write-Host "[INFO] Starting content organization..."

# Create project directories
Write-Host "[INFO] Creating project directories..."
New-Item -ItemType Directory -Path $guardian -Force | Out-Null
New-Item -ItemType Directory -Path $foresight -Force | Out-Null
New-Item -ItemType Directory -Path $cipher -Force | Out-Null

# Copy shared infrastructure to all repos
Write-Host "[INFO] Copying shared infrastructure..."
$sharedDirs = @("src", "tests", "scripts", ".github", "alembic", "models")
foreach ($dir in $sharedDirs) {
    $srcPath = Join-Path $source $dir
    if (Test-Path $srcPath) {
        Copy-Item -Path $srcPath -Destination (Join-Path $guardian $dir) -Recurse -Force -ErrorAction SilentlyContinue
        Copy-Item -Path $srcPath -Destination (Join-Path $foresight $dir) -Recurse -Force -ErrorAction SilentlyContinue
        Copy-Item -Path $srcPath -Destination (Join-Path $cipher $dir) -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  [OK] Copied $dir"
    }
}

# Copy shared config files
Write-Host "[INFO] Copying shared config files..."
$configFiles = @("requirements.txt", "Dockerfile", "docker-compose.yml", ".gitignore", "LICENSE", "setup.py", "alembic.ini")
foreach ($file in $configFiles) {
    $srcPath = Join-Path $source $file
    if (Test-Path $srcPath) {
        Copy-Item -Path $srcPath -Destination (Join-Path $guardian $file) -Force -ErrorAction SilentlyContinue
        Copy-Item -Path $srcPath -Destination (Join-Path $foresight $file) -Force -ErrorAction SilentlyContinue
        Copy-Item -Path $srcPath -Destination (Join-Path $cipher $file) -Force -ErrorAction SilentlyContinue
    }
}

# Copy org-contact-info.md to all repos
if (Test-Path (Join-Path $source "org-contact-info.md")) {
    Copy-Item -Path (Join-Path $source "org-contact-info.md") -Destination (Join-Path $guardian "org-contact-info.md") -Force
    Copy-Item -Path (Join-Path $source "org-contact-info.md") -Destination (Join-Path $foresight "org-contact-info.md") -Force
    Copy-Item -Path (Join-Path $source "org-contact-info.md") -Destination (Join-Path $cipher "org-contact-info.md") -Force
    Write-Host "  [OK] Copied org-contact-info.md"
}

# Copy docs directory (shared documentation)
$docsPath = Join-Path $source "docs"
if (Test-Path $docsPath) {
    Copy-Item -Path $docsPath -Destination (Join-Path $guardian "docs") -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item -Path $docsPath -Destination (Join-Path $foresight "docs") -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item -Path $docsPath -Destination (Join-Path $cipher "docs") -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Copied docs directory"
}

Write-Host "[OK] Content organized into project directories"

