#Requires -Version 5.1
<#
.SYNOPSIS
  Push AuditShield-Live subtree to Hugging Face Space (monorepo-safe; avoids HF binary rejection).

.DESCRIPTION
  HF Spaces reject pushes of this full monorepo (tracked PNGs/PDFs/etc.). Only
  Artifacts/project/auditshield is the Space app root. This script runs git subtree split
  and force-pushes that history to the Space main branch.

.USAGE
  From monorepo root:
    .\deploy_hf_auditshield.ps1

  Uses HF username + Access Token when git prompts (https://huggingface.co/settings/tokens).

.NOTES
  Space: https://huggingface.co/spaces/rreichert/auditshield-live
  App:   https://rreichert-auditshield-live.hf.space
#>
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Prefix = 'Artifacts/project/auditshield'
$RemoteName = 'space'
$RemoteUrl = 'https://huggingface.co/spaces/rreichert/auditshield-live'
$SplitBranch = 'hf-auditshield-space-only'

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
Write-Host "Done. Monitor build: https://huggingface.co/spaces/rreichert/auditshield-live"
