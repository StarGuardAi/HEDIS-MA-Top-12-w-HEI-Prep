# Sync .cursorrules + Phase2-to-Hardening-Sprint-Checklist.md to all three repo roots
# Run from auditshield root. Keeps Engineering Standards identical across repos.
# Usage: .\sync-cursorrules.ps1
#
# If repos are SIBLINGS (e.g. ../starguard-desktop, ../starguard-mobile):
#   Copy-Item .cursorrules ../starguard-desktop/.cursorrules
#   Copy-Item .cursorrules ../starguard-mobile/.cursorrules
#   Copy-Item Phase2-to-Hardening-Sprint-Checklist.md ../starguard-desktop/Phase2-to-Hardening-Sprint-Checklist.md
#   Copy-Item Phase2-to-Hardening-Sprint-Checklist.md ../starguard-mobile/Phase2-to-Hardening-Sprint-Checklist.md

$root = $PSScriptRoot
$files = @(".cursorrules", "Phase2-to-Hardening-Sprint-Checklist.md")
$dests = @("starguard-desktop", "starguard-mobile")

foreach ($file in $files) {
    $source = Join-Path $root $file
    if (-not (Test-Path $source)) {
        Write-Warning "Skipping $file - not found at $source"
        continue
    }
    foreach ($destName in $dests) {
        $dest = Join-Path $root $destName $file
        $destDir = Split-Path $dest -Parent
        if (-not (Test-Path $destDir)) {
            Write-Warning "Skipping $dest - directory not found (use sibling layout?)"
            continue
        }
        Copy-Item $source $dest -Force
        Write-Host "Synced $file -> $destName/"
    }
}

Write-Host "Done. All three repos now have identical .cursorrules and Phase2-to-Hardening-Sprint-Checklist.md."
