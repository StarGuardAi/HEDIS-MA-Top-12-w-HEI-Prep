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

  Uses a temporary git worktree so an unclean monorepo working tree does not block checkout.

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

$existingSplit = git branch --list $SplitBranch
if ($existingSplit) {
    git branch -D $SplitBranch
}

Write-Host "==> Subtree split: $Prefix -> $SplitBranch"
git subtree split --prefix=$Prefix -b $SplitBranch
if ($LASTEXITCODE -ne 0) { throw "subtree split failed" }

$wt = Join-Path $env:TEMP ("hf-platform-hub-deploy-" + [Guid]::NewGuid().ToString("N").Substring(0, 12))
try {
    Write-Host "==> Worktree (avoids checkout conflicts): $wt"
    git worktree add $wt $SplitBranch
    if ($LASTEXITCODE -ne 0) { throw "git worktree add failed" }

    Push-Location $wt
    try {
        if (Test-Path -LiteralPath "LinkedIn_Avatar_300PX.png") {
            Write-Host "==> Remove avatar PNG from Space branch (HF binary policy)"
            git rm -f "LinkedIn_Avatar_300PX.png"
            git commit -m "chore(hf): omit avatar PNG; app uses GitHub raw / AVATAR_URL"
            if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
        }

        Write-Host "==> Push to ${RemoteName}:main (force)"
        git push $RemoteName "HEAD:main" --force
        if ($LASTEXITCODE -ne 0) { throw "git push failed" }
    }
    finally {
        Pop-Location
    }
}
finally {
    Set-Location $Root
    git worktree remove $wt --force 2>$null | Out-Null
    if (Test-Path -LiteralPath $wt) {
        Remove-Item -LiteralPath $wt -Recurse -Force -ErrorAction SilentlyContinue
    }
    $still = git branch --list $SplitBranch
    if ($still) {
        git branch -D $SplitBranch
    }
}

Write-Host ""
Write-Host "Done. Monitor build: https://huggingface.co/spaces/rreichert/reichert-platform-hub"
