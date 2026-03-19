#Requires -Version 5.1
<#
.SYNOPSIS
  Push SovereignShield app subtree to its Hugging Face Space (monorepo-safe).

.USAGE
  From monorepo root:
    .\deploy_hf_sovereignshield.ps1

.NOTES
  Space (mobile): https://huggingface.co/spaces/rreichert/sovereignshield-mobile
  Prefix:        Artifacts/project/sovereignshield
  Remote name matches common local alias hf-sovereignshield-mobile.
#>
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Prefix = 'Artifacts/project/sovereignshield'
$RemoteName = 'hf-sovereignshield-mobile'
$RemoteUrl = 'https://huggingface.co/spaces/rreichert/sovereignshield-mobile'
$SplitBranch = 'hf-sovereignshield-space-only'

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
Write-Host "Done. Monitor build: https://huggingface.co/spaces/rreichert/sovereignshield-mobile"
