#Requires -Version 5.1
<#
.SYNOPSIS
  Push platform-hub subtree to Hugging Face Space (monorepo-safe).

.DESCRIPTION
  Hugging Face Hub rejects raw binary files in git unless Git Xet is installed
  (see https://huggingface.co/docs/hub/xet ). This script splits platform-hub/,
  removes LinkedIn_Avatar_300PX.png on the split branch only, then force-pushes.
  app.py loads the avatar from local PNG if present, else AVATAR_URL or the
  default GitHub raw URL.

  Alternative: install Git-Xet (winget install HuggingFace.Git-Xet), run
  `git xet install`, then you can push the PNG with:
    git subtree push --prefix platform-hub hf-platform-hub main

.USAGE
  From monorepo root (commit platform-hub changes first — subtree uses commits):
    .\deploy_hf_platform_hub.ps1

  Uses HF username + Access Token when git prompts (https://huggingface.co/settings/tokens).

.NOTES
  Space: https://huggingface.co/spaces/rreichert/reichert-platform-hub
#>
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Prefix = 'platform-hub'
$RemoteName = 'hf-platform-hub'
$RemoteUrl = 'https://huggingface.co/spaces/rreichert/reichert-platform-hub'
$SplitBranch = 'hf-platform-hub-space-only'

$remotes = @(git remote)
if ($remotes -notcontains $RemoteName) {
    Write-Host "Adding git remote $RemoteName -> $RemoteUrl"
    git remote add $RemoteName $RemoteUrl
}

git branch -D $SplitBranch 2>$null | Out-Null

Write-Host "==> Subtree split: $Prefix -> $SplitBranch"
git subtree split --prefix=$Prefix -b $SplitBranch
if ($LASTEXITCODE -ne 0) { throw "subtree split failed" }

$goBack = git branch --show-current
git checkout $SplitBranch
if ($LASTEXITCODE -ne 0) { throw "checkout $SplitBranch failed" }

if (Test-Path -LiteralPath "LinkedIn_Avatar_300PX.png") {
    Write-Host "==> Remove avatar PNG from Space branch (HF binary policy)"
    git rm -f "LinkedIn_Avatar_300PX.png"
    git commit -m "chore(hf): omit avatar PNG; app uses GitHub raw / AVATAR_URL"
    if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
}

Write-Host "==> Push $SplitBranch -> ${RemoteName}:main (force)"
git push $RemoteName "${SplitBranch}:main" --force
if ($LASTEXITCODE -ne 0) { throw "git push failed" }

Write-Host "==> Back to $goBack and drop split branch"
git checkout $goBack
if ($LASTEXITCODE -ne 0) { git checkout main }
git branch -D $SplitBranch

Write-Host ""
Write-Host "Done. Monitor build: https://huggingface.co/spaces/rreichert/reichert-platform-hub"
