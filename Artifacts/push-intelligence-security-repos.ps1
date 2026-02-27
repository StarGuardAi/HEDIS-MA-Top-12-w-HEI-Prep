# PowerShell Script to Push Intelligence-Security Repositories to GitHub
# This script helps create and push the three Intelligence-Security repositories to GitHub

param(
    [switch]$CheckOnly,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$intelligenceSecurityPath = "C:\Users\reich\Projects\intelligence-security\repos"

# Color output functions
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Error { Write-Host $args -ForegroundColor Red }

Write-Info "=========================================="
Write-Info "Intelligence-Security Repositories Push"
Write-Info "=========================================="
Write-Host ""

# Check if intelligence-security path exists
if (-not (Test-Path $intelligenceSecurityPath)) {
    Write-Error "Error: Intelligence-Security path not found: $intelligenceSecurityPath"
    Write-Info "Please verify the path and try again."
    exit 1
}

# Repositories to check/push
$repos = @(
    @{
        Name = "cipher"
        GitHubRepo = "cipher-threat-tracker"
        GitHubOrg = "reichert-sentinel-ai"
        Path = Join-Path $intelligenceSecurityPath "cipher"
    },
    @{
        Name = "foresight"
        GitHubRepo = "foresight-crime-prediction"
        GitHubOrg = "reichert-sentinel-ai"
        Path = Join-Path $intelligenceSecurityPath "foresight"
    },
    @{
        Name = "guardian"
        GitHubRepo = "guardian-fraud-analytics"
        GitHubOrg = "reichert-sentinel-ai"
        Path = Join-Path $intelligenceSecurityPath "guardian"
    }
)

Write-Info "Checking repository status..."
Write-Host ""

$results = @()

foreach ($repo in $repos) {
    Write-Info "----------------------------------------"
    Write-Info "Repository: $($repo.Name)"
    Write-Info "GitHub: $($repo.GitHubOrg)/$($repo.GitHubRepo)"
    Write-Info "----------------------------------------"
    
    $status = @{
        Name = $repo.Name
        GitHubRepo = $repo.GitHubRepo
        LocalPathExists = $false
        IsGitRepo = $false
        HasRemote = $false
        RemoteURL = $null
        BranchName = $null
        HasUncommittedChanges = $false
        HasUnpushedCommits = $false
        GitHubExists = $false
    }
    
    # Check if local path exists
    if (Test-Path $repo.Path) {
        $status.LocalPathExists = $true
        Write-Success "✓ Local path exists"
        
        # Check if it's a git repository
        Push-Location $repo.Path
        try {
            $gitDir = git rev-parse --git-dir 2>$null
            if ($gitDir) {
                $status.IsGitRepo = $true
                Write-Success "✓ Is a git repository"
                
                # Check remote
                $remote = git remote get-url origin 2>$null
                if ($remote) {
                    $status.HasRemote = $true
                    $status.RemoteURL = $remote
                    Write-Success "✓ Has remote configured: $remote"
                } else {
                    Write-Warning "⚠ No remote configured"
                }
                
                # Get current branch
                $branch = git branch --show-current 2>$null
                if ($branch) {
                    $status.BranchName = $branch
                    Write-Info "  Current branch: $branch"
                }
                
                # Check for uncommitted changes
                $changes = git status --porcelain 2>$null
                if ($changes) {
                    $status.HasUncommittedChanges = $true
                    Write-Warning "⚠ Has uncommitted changes"
                    if (-not $DryRun -and -not $CheckOnly) {
                        Write-Warning "  Consider committing changes before pushing"
                    }
                } else {
                    Write-Success "✓ No uncommitted changes"
                }
                
                # Check for unpushed commits (if remote exists)
                if ($status.HasRemote) {
                    git fetch origin 2>$null | Out-Null
                    $ahead = git rev-list --count HEAD...origin/$branch 2>$null
                    if ($ahead -and [int]$ahead -gt 0) {
                        $status.HasUnpushedCommits = $true
                        Write-Warning "⚠ Has $ahead unpushed commit(s)"
                    } else {
                        Write-Success "✓ All commits are pushed"
                    }
                }
            } else {
                Write-Warning "⚠ Not a git repository"
            }
        } finally {
            Pop-Location
        }
    } else {
        Write-Error "✗ Local path does not exist: $($repo.Path)"
    }
    
    # Check if GitHub repository exists
    $githubUrl = "https://github.com/$($repo.GitHubOrg)/$($repo.GitHubRepo)"
    try {
        $response = Invoke-WebRequest -Uri $githubUrl -Method Head -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $status.GitHubExists = $true
            Write-Success "✓ GitHub repository exists"
        }
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -eq 404) {
            Write-Warning "⚠ GitHub repository does not exist (404)"
            Write-Info "  URL: $githubUrl"
        } else {
            Write-Warning "⚠ Could not verify GitHub repository status"
        }
    }
    
    $results += $status
    Write-Host ""
}

# Summary
Write-Info "=========================================="
Write-Info "Summary"
Write-Info "=========================================="
Write-Host ""

foreach ($result in $results) {
    Write-Info "$($result.Name):"
    Write-Host "  Local: $(if ($result.LocalPathExists) { '✓' } else { '✗' })"
    Write-Host "  Git: $(if ($result.IsGitRepo) { '✓' } else { '✗' })"
    Write-Host "  Remote: $(if ($result.HasRemote) { '✓' } else { '✗' })"
    Write-Host "  GitHub: $(if ($result.GitHubExists) { '✓ EXISTS' } else { '✗ NOT FOUND' })"
    Write-Host "  Uncommitted: $(if ($result.HasUncommittedChanges) { '⚠ YES' } else { '✓ NO' })"
    Write-Host "  Unpushed: $(if ($result.HasUnpushedCommits) { '⚠ YES' } else { '✓ NO' })"
    Write-Host ""
}

# Action items
Write-Info "=========================================="
Write-Info "Action Items"
Write-Info "=========================================="
Write-Host ""

$needsGitHubCreation = $results | Where-Object { -not $_.GitHubExists }
$needsPush = $results | Where-Object { $_.IsGitRepo -and $_.HasRemote -and -not $_.GitHubExists }
$hasUncommitted = $results | Where-Object { $_.HasUncommittedChanges }

if ($needsGitHubCreation.Count -gt 0) {
    Write-Warning "Repositories that need to be created on GitHub:"
    foreach ($repo in $needsGitHubCreation) {
        Write-Info "  - $($repo.GitHubRepo)"
        Write-Info "    URL: https://github.com/reichert-sentinel-ai/$($repo.GitHubRepo)"
        Write-Info "    Steps:"
        Write-Info "      1. Go to https://github.com/organizations/reichert-sentinel-ai/repositories/new"
        Write-Info "      2. Repository name: $($repo.GitHubRepo)"
        Write-Info "      3. Set visibility to Public"
        Write-Info "      4. Do NOT initialize with README (we'll push existing code)"
        Write-Info "      5. Click 'Create repository'"
        Write-Host ""
    }
}

if ($hasUncommitted.Count -gt 0) {
    Write-Warning "Repositories with uncommitted changes:"
    foreach ($repo in $hasUncommitted) {
        Write-Info "  - $($repo.Name)"
        Write-Info "    Consider committing changes before pushing"
        Write-Host ""
    }
}

if ($needsPush.Count -gt 0 -and -not $CheckOnly -and -not $DryRun) {
    Write-Info "Repositories ready to push:"
    foreach ($repo in $needsPush) {
        Write-Info "  - $($repo.Name)"
    }
    Write-Host ""
    
    $response = Read-Host "Do you want to push these repositories now? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        foreach ($repo in $needsPush) {
            $repoInfo = $repos | Where-Object { $_.Name -eq $repo.Name } | Select-Object -First 1
            Write-Info ""
            Write-Info "Pushing $($repo.Name)..."
            Push-Location $repoInfo.Path
            try {
                $branch = $repo.BranchName
                if (-not $branch) {
                    $branch = "main"
                }
                
                Write-Info "  Branch: $branch"
                Write-Info "  Remote: $($repo.RemoteURL)"
                
                # Try to push
                git push -u origin $branch 2>&1 | ForEach-Object {
                    if ($_ -match "error" -or $_ -match "fatal") {
                        Write-Error "  $_"
                    } else {
                        Write-Info "  $_"
                    }
                }
                
                Write-Success "✓ Push completed for $($repo.Name)"
            } catch {
                Write-Error "✗ Error pushing $($repo.Name): $_"
            } finally {
                Pop-Location
            }
        }
    }
} elseif ($DryRun) {
    Write-Info "DRY RUN MODE: No changes will be made"
    Write-Info "Remove -DryRun flag to actually push repositories"
}

Write-Host ""
Write-Info "=========================================="
Write-Info "Next Steps"
Write-Info "=========================================="
Write-Host ""
Write-Info "1. Create missing GitHub repositories (see Action Items above)"
Write-Info "2. Run this script again without -CheckOnly to push repositories"
Write-Info "3. Verify repositories are accessible at:"
foreach ($repo in $repos) {
    $org = $repo.GitHubOrg
    $repoName = $repo.GitHubRepo
    $url = "https://github.com/$org/$repoName"
    Write-Info ('   - ' + $url)
}
Write-Host ""

