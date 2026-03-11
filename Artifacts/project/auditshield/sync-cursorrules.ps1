# Sync .cursorrules + Phase2-to-Hardening-Sprint-Checklist.md to all four portfolio repo roots
# Run from auditshield root. Keeps Engineering Standards identical across repos.
# Usage: .\sync-cursorrules.ps1
#
# Targets: starguard-desktop, starguard-mobile (nested under auditshield), sovereignshield (sibling under Projects/)
# Assumes Projects/ is four levels up from this script (auditshield -> project -> Artifacts -> workspace -> Projects).

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

# Walk up four levels to reach Projects/ (parent of workspace)
$p1 = Split-Path $root -Parent
$p2 = Split-Path $p1 -Parent
$p3 = Split-Path $p2 -Parent
$projectsRoot = Split-Path $p3 -Parent

$files = @(".cursorrules", "Phase2-to-Hardening-Sprint-Checklist.md")
$nestedDests = @("starguard-desktop", "starguard-mobile")
$sovereignshieldRoot = Join-Path $projectsRoot "sovereignshield"

foreach ($file in $files) {
    $source = Join-Path $root $file
    if (-not (Test-Path $source)) {
        Write-Warning "Skipping $file - not found at $source"
        continue
    }

    # Sync to nested repos (starguard-desktop, starguard-mobile under auditshield)
    foreach ($destName in $nestedDests) {
        $destDir = Join-Path $root $destName
        if (-not (Test-Path $destDir)) {
            Write-Warning "Skipping $destName - directory not found"
            continue
        }
        $dest = Join-Path $destDir $file
        Copy-Item $source $dest -Force
        Write-Host "Synced $file -> $destName/" -ForegroundColor Green
    }

    # Sync to sovereignshield (sibling repo under Projects/)
    if (Test-Path $sovereignshieldRoot) {
        $dest = Join-Path $sovereignshieldRoot $file
        Copy-Item $source $dest -Force
        Write-Host "Synced $file -> sovereignshield/" -ForegroundColor Green
    } else {
        Write-Warning "Skipping sovereignshield - directory not found at $sovereignshieldRoot"
    }
}

Write-Host ""
Write-Host "Sync complete. All four portfolio repos now have identical .cursorrules and Phase2-to-Hardening-Sprint-Checklist.md." -ForegroundColor Cyan
Write-Host ""
Write-Host "SovereignShield git init reminder (if needed):" -ForegroundColor Yellow
Write-Host "  cd $sovereignshieldRoot"
Write-Host "  git init"
Write-Host "  git add ."
Write-Host "  git commit -m 'Initial commit'"
Write-Host ""
