#Requires -Version 5.1
<#
.SYNOPSIS
  Push StarGuard Desktop subtree to its Hugging Face Space (same monorepo pattern as AuditShield).

.USAGE
  From monorepo root:
    .\deploy_hf_starguard_desktop.ps1

.NOTES
  Space: https://huggingface.co/spaces/rreichert/starguard-desktop
  Prefix: Artifacts/project/auditshield/starguard-desktop
  If HF rejects the push (binaries under subtree), trim tracked binaries or use git-xet per HF docs.
#>
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Prefix = 'Artifacts/project/auditshield/starguard-desktop'
$RemoteName = 'hf-desktop'
$RemoteUrl = 'https://huggingface.co/spaces/rreichert/starguard-desktop'
$SplitBranch = 'hf-starguard-desktop-space-only'

$remotes = @(git remote)
if ($remotes -notcontains $RemoteName) {
    Write-Host "Adding git remote $RemoteName -> $RemoteUrl"
    git remote add $RemoteName $RemoteUrl
}

Write-Host "==> Subtree split: $Prefix -> $SplitBranch"
git subtree split --prefix=$Prefix -b $SplitBranch
if ($LASTEXITCODE -ne 0) { throw "subtree split failed" }

Write-Host "==> Push $SplitBranch -> ${RemoteName}:main (force)"
git push $RemoteName "${SplitBranch}:main" --force
if ($LASTEXITCODE -ne 0) { throw "git push failed" }

Write-Host ""
Write-Host "Done. Monitor build: https://huggingface.co/spaces/rreichert/starguard-desktop"
