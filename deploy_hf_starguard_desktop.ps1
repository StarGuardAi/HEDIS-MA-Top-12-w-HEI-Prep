#Requires -Version 5.1
<#
.SYNOPSIS
  Push StarGuard Desktop to its Hugging Face Space from the submodule repo (no subtree split).

.DESCRIPTION
  Artifacts/project/auditshield/starguard-desktop is a separate git repo (submodule), not part of
  the AuditShield subtree. This script cds into that directory and runs git push to the HF remote.

.USAGE
  From monorepo root:
    .\deploy_hf_starguard_desktop.ps1

  Commit and push your changes from inside the submodule first (or from the monorepo after
  updating the submodule pointer).

.NOTES
  Space: https://huggingface.co/spaces/rreichert/starguard-desktop
  Submodule: Artifacts/project/auditshield/starguard-desktop
  Expected HF remote names (first match wins): hf, hf-desktop, space
#>
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$SubPath = Join-Path $Root 'Artifacts/project/auditshield/starguard-desktop'
$DefaultHfUrl = 'https://huggingface.co/spaces/rreichert/starguard-desktop'

if (-not (Test-Path $SubPath)) {
    throw "Submodule path not found: $SubPath"
}
$gitDir = Join-Path $SubPath '.git'
if (-not (Test-Path $gitDir)) {
    throw "Not a git repo (missing .git): $SubPath"
}

Push-Location $SubPath
try {
    $branch = (git branch --show-current).Trim()
    if ($branch -ne 'main') {
        Write-Warning "Current branch is '$branch', not 'main'. Pushing it to HF main anyway (HEAD:main)."
    }

    $remotes = @(git remote)
    $hfRemote = $null
    foreach ($r in @('hf', 'hf-desktop', 'space')) {
        if ($remotes -contains $r) {
            $hfRemote = $r
            break
        }
    }
    if (-not $hfRemote) {
        Write-Host "Adding remote hf -> $DefaultHfUrl"
        git remote add hf $DefaultHfUrl
        $hfRemote = 'hf'
    }

    Write-Host "==> Push submodule $SubPath -> ${hfRemote}:main (from branch $branch)"
    git push $hfRemote HEAD:main --force
    if ($LASTEXITCODE -ne 0) { throw "git push failed" }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "Done. Monitor build: https://huggingface.co/spaces/rreichert/starguard-desktop"
