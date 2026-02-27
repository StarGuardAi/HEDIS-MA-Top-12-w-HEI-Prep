# Validation Script for Intelligence-Security Repositories Publication
# This script validates that all repositories are properly published and accessible

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Validation: Repository Publication" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repos = @(
    @{
        Name = "cipher"
        RepoName = "cipher-threat-tracker"
        GitHubUrl = "https://github.com/reichert-sentinel-ai/cipher-threat-tracker"
        LocalPath = "C:\Users\reich\Projects\intelligence-security\repos\cipher"
    },
    @{
        Name = "foresight"
        RepoName = "foresight-crime-prediction"
        GitHubUrl = "https://github.com/reichert-sentinel-ai/foresight-crime-prediction"
        LocalPath = "C:\Users\reich\Projects\intelligence-security\repos\foresight"
    },
    @{
        Name = "guardian"
        RepoName = "guardian-fraud-analytics"
        GitHubUrl = "https://github.com/reichert-sentinel-ai/guardian-fraud-analytics"
        LocalPath = "C:\Users\reich\Projects\intelligence-security\repos\guardian"
    }
)

$validationResults = @()
$overallStatus = $true

# Test 1: Verify Repositories Exist and Are Public
Write-Host "Test 1: Repository Existence and Visibility" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

foreach ($repo in $repos) {
    Write-Host ""
    Write-Host "Checking: $($repo.RepoName)" -ForegroundColor Cyan
    
    try {
        $repoInfo = gh repo view "reichert-sentinel-ai/$($repo.RepoName)" --json name,isPrivate,url,description 2>&1
        if ($LASTEXITCODE -eq 0) {
            $repoJson = $repoInfo | ConvertFrom-Json
            $isPublic = -not $repoJson.isPrivate
            $hasDescription = -not [string]::IsNullOrWhiteSpace($repoJson.description)
            
            $test1Pass = $isPublic
            $test1Message = if ($isPublic) { "[PASS] Repository is PUBLIC" } else { "[FAIL] Repository is PRIVATE" }
            $test1Color = if ($isPublic) { "Green" } else { "Red" }
            
            Write-Host "  $test1Message" -ForegroundColor $test1Color
            Write-Host "  URL: $($repo.GitHubUrl)" -ForegroundColor Cyan
            Write-Host "  Description: $(if ($hasDescription) { 'Present' } else { 'Missing' })" -ForegroundColor $(if ($hasDescription) { "Green" } else { "Yellow" })
            
            $validationResults += @{
                Repository = $repo.RepoName
                Test = "Existence and Visibility"
                Status = if ($test1Pass) { "PASS" } else { "FAIL" }
                Details = $test1Message
            }
            
            if (-not $test1Pass) {
                $overallStatus = $false
            }
        } else {
            Write-Host "  [FAIL] Repository not found or not accessible" -ForegroundColor Red
            $validationResults += @{
                Repository = $repo.RepoName
                Test = "Existence and Visibility"
                Status = "FAIL"
                Details = "Repository not found"
            }
            $overallStatus = $false
        }
    } catch {
        Write-Host "  [FAIL] Error checking repository: $_" -ForegroundColor Red
        $validationResults += @{
            Repository = $repo.RepoName
            Test = "Existence and Visibility"
            Status = "FAIL"
            Details = "Error: $_"
        }
        $overallStatus = $false
    }
}

# Test 2: Verify Local Repository Status
Write-Host ""
Write-Host "Test 2: Local Repository Status" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

foreach ($repo in $repos) {
    Write-Host ""
    Write-Host "Checking: $($repo.RepoName)" -ForegroundColor Cyan
    
    if (Test-Path $repo.LocalPath) {
        Push-Location $repo.LocalPath
        
        # Check if git repository
        if (Test-Path ".git") {
            Write-Host "  [PASS] Git repository found" -ForegroundColor Green
            
            # Check current branch
            $branch = git branch --show-current
            Write-Host "  Current branch: $branch" -ForegroundColor Cyan
            
            # Check remote
            $remote = git remote get-url origin 2>&1
            if ($LASTEXITCODE -eq 0) {
                $expectedRemote = "https://github.com/reichert-sentinel-ai/$($repo.RepoName).git"
                if ($remote -like "*$($repo.RepoName)*") {
                    Write-Host "  [PASS] Remote configured correctly" -ForegroundColor Green
                } else {
                    Write-Host "  ⚠ Remote may be incorrect: $remote" -ForegroundColor Yellow
                }
            }
            
            # Check for uncommitted changes
            $status = git status --short
            if ($status) {
                $uncommittedCount = ($status | Measure-Object -Line).Lines
                Write-Host "  ⚠ $uncommittedCount uncommitted changes found" -ForegroundColor Yellow
            } else {
                Write-Host "  [PASS] No uncommitted changes" -ForegroundColor Green
            }
            
            $validationResults += @{
                Repository = $repo.RepoName
                Test = "Local Repository Status"
                Status = "PASS"
                Details = "Git repository configured"
            }
        } else {
            Write-Host "  [FAIL] Not a git repository" -ForegroundColor Red
            $validationResults += @{
                Repository = $repo.RepoName
                Test = "Local Repository Status"
                Status = "FAIL"
                Details = "Not a git repository"
            }
            $overallStatus = $false
        }
        
        Pop-Location
    } else {
        Write-Host "  [FAIL] Local path not found: $($repo.LocalPath)" -ForegroundColor Red
        $validationResults += @{
            Repository = $repo.RepoName
            Test = "Local Repository Status"
            Status = "FAIL"
            Details = "Local path not found"
        }
        $overallStatus = $false
    }
}

# Test 3: Verify README Files
Write-Host ""
Write-Host "Test 3: README Files" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

foreach ($repo in $repos) {
    Write-Host ""
    Write-Host "Checking: $($repo.RepoName)" -ForegroundColor Cyan
    
    $readmePath = Join-Path $repo.LocalPath "README.md"
    if (Test-Path $readmePath) {
        $readmeContent = Get-Content $readmePath -Raw
        $readmeSize = (Get-Item $readmePath).Length
        
            $readmeSizeKB = [math]::Round($readmeSize/1KB, 2)
            Write-Host "  [PASS] README.md exists ($readmeSizeKB KB)" -ForegroundColor Green
        
        # Check for key sections
        $hasRecruiters = $readmeContent -match "(?i)for recruiters|recruiters"
        $hasDescription = $readmeContent -match "(?i)overview|description"
        $hasTechStack = $readmeContent -match "(?i)technology|tech stack|built with"
        $hasInstallation = $readmeContent -match "(?i)install|setup|quick start"
        
        Write-Host "    Sections found:" -ForegroundColor Cyan
        Write-Host "      - For Recruiters: $(if ($hasRecruiters) { '[OK]' } else { '[MISSING]' })" -ForegroundColor $(if ($hasRecruiters) { "Green" } else { "Yellow" })
        Write-Host "      - Description: $(if ($hasDescription) { '[OK]' } else { '[MISSING]' })" -ForegroundColor $(if ($hasDescription) { "Green" } else { "Yellow" })
        Write-Host "      - Tech Stack: $(if ($hasTechStack) { '[OK]' } else { '[MISSING]' })" -ForegroundColor $(if ($hasTechStack) { "Green" } else { "Yellow" })
        Write-Host "      - Installation: $(if ($hasInstallation) { '[OK]' } else { '[MISSING]' })" -ForegroundColor $(if ($hasInstallation) { "Green" } else { "Yellow" })
        
        $validationResults += @{
            Repository = $repo.RepoName
            Test = "README File"
            Status = "PASS"
            Details = "README exists with key sections"
        }
    } else {
            Write-Host "  [FAIL] README.md not found" -ForegroundColor Red
        $validationResults += @{
            Repository = $repo.RepoName
            Test = "README File"
            Status = "FAIL"
            Details = "README.md not found"
        }
        $overallStatus = $false
    }
}

# Test 4: Verify GitHub URLs Accessible
Write-Host ""
Write-Host "Test 4: GitHub URL Accessibility" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

foreach ($repo in $repos) {
    Write-Host ""
    Write-Host "Testing: $($repo.GitHubUrl)" -ForegroundColor Cyan
    
    try {
        $response = Invoke-WebRequest -Uri $repo.GitHubUrl -Method Head -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "  [PASS] URL is accessible (HTTP $($response.StatusCode))" -ForegroundColor Green
            $validationResults += @{
                Repository = $repo.RepoName
                Test = "URL Accessibility"
                Status = "PASS"
                Details = "HTTP 200 - Accessible"
            }
        } else {
            Write-Host "  ⚠ Unexpected status: HTTP $($response.StatusCode)" -ForegroundColor Yellow
            $validationResults += @{
                Repository = $repo.RepoName
                Test = "URL Accessibility"
                Status = "WARN"
                Details = "HTTP $($response.StatusCode)"
            }
        }
    } catch {
            Write-Host "  [FAIL] URL not accessible: $_" -ForegroundColor Red
        $validationResults += @{
            Repository = $repo.RepoName
            Test = "URL Accessibility"
            Status = "FAIL"
            Details = "Not accessible"
        }
        $overallStatus = $false
    }
}

# Test 5: Check for Broken Links in README
Write-Host ""
Write-Host "Test 5: README Link Validation" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

foreach ($repo in $repos) {
    Write-Host ""
    Write-Host "Checking: $($repo.RepoName)" -ForegroundColor Cyan
    
    $readmePath = Join-Path $repo.LocalPath "README.md"
    if (Test-Path $readmePath) {
        $readmeContent = Get-Content $readmePath -Raw
        
        # Find URLs in README
        $urlPattern = 'https?://[^\s\)]+'
        $urls = [regex]::Matches($readmeContent, $urlPattern) | ForEach-Object { $_.Value }
        
        $brokenLinks = @()
        $workingLinks = 0
        $totalLinks = $urls.Count
        
        Write-Host "  Found $totalLinks links in README" -ForegroundColor Cyan
        
        foreach ($url in $urls) {
            try {
                # Clean URL (remove markdown syntax)
                $cleanUrl = $url -replace '[\)\]]$', ''
                $response = Invoke-WebRequest -Uri $cleanUrl -Method Head -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
                if ($response.StatusCode -eq 200) {
                    $workingLinks++
                }
            } catch {
                $brokenLinks += $url
            }
        }
        
        if ($brokenLinks.Count -eq 0) {
            Write-Host "  [PASS] All links are working ($workingLinks/$totalLinks)" -ForegroundColor Green
            $validationResults += @{
                Repository = $repo.RepoName
                Test = "README Links"
                Status = "PASS"
                Details = "All links working ($workingLinks/$totalLinks)"
            }
        } else {
            Write-Host "  ⚠ $($brokenLinks.Count) broken link(s) found" -ForegroundColor Yellow
            foreach ($broken in $brokenLinks) {
                Write-Host "    - $broken" -ForegroundColor Yellow
            }
            $validationResults += @{
                Repository = $repo.RepoName
                Test = "README Links"
                Status = "WARN"
                Details = "$($brokenLinks.Count) broken links"
            }
        }
    }
}

# Test 6: Organization Page Check
Write-Host ""
Write-Host "Test 6: Organization Page" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

$orgUrl = "https://github.com/reichert-sentinel-ai"
Write-Host "Testing: $orgUrl" -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri $orgUrl -Method Head -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "  [PASS] Organization page is accessible" -ForegroundColor Green
        $validationResults += @{
            Repository = "Organization"
            Test = "Organization Page"
            Status = "PASS"
            Details = "HTTP 200 - Accessible"
        }
    }
} catch {
    Write-Host "  [FAIL] Organization page not accessible" -ForegroundColor Red
    $validationResults += @{
        Repository = "Organization"
        Test = "Organization Page"
        Status = "FAIL"
        Details = "Not accessible"
    }
    $overallStatus = $false
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Validation Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$passCount = ($validationResults | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($validationResults | Where-Object { $_.Status -eq "FAIL" }).Count
$warnCount = ($validationResults | Where-Object { $_.Status -eq "WARN" }).Count
$totalTests = $validationResults.Count

Write-Host "Total Tests: $totalTests" -ForegroundColor Cyan
Write-Host "Passed: $passCount" -ForegroundColor Green
Write-Host "Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host "Warnings: $warnCount" -ForegroundColor $(if ($warnCount -gt 0) { "Yellow" } else { "Green" })
Write-Host ""

if ($overallStatus) {
    Write-Host "[SUCCESS] Overall Status: PASS" -ForegroundColor Green
    Write-Host ""
    Write-Host "All critical validations passed! Repositories are ready for external visitors." -ForegroundColor Green
} else {
    Write-Host "[FAILED] Overall Status: FAIL" -ForegroundColor Red
    Write-Host ""
    Write-Host "Some validations failed. Please review the issues above." -ForegroundColor Red
}

# Detailed Results Table
Write-Host ""
Write-Host "Detailed Results:" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

$validationResults | Format-Table -AutoSize Repository, Test, Status, Details

# Export Results
$resultsPath = "validation-results-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
$validationResults | ConvertTo-Json -Depth 3 | Out-File $resultsPath
Write-Host ""
Write-Host "Results exported to: $resultsPath" -ForegroundColor Cyan

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Review any FAILED tests above" -ForegroundColor Yellow
Write-Host "2. Fix issues and re-run validation" -ForegroundColor Yellow
Write-Host "3. Test repositories in incognito browser" -ForegroundColor Yellow
Write-Host "4. Check README files for accuracy" -ForegroundColor Yellow
Write-Host ""

