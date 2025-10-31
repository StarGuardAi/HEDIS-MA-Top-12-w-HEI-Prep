# GitHub Status Checker
param(
    [Parameter(Mandatory=$false)]
    [string]$GitHubToken
)

# Function to retrieve GitHub token from secure storage
function Get-GitHubTokenFromVault {
    try {
        if (Get-Module -ListAvailable -Name Microsoft.PowerShell.SecretManagement) {
            Import-Module Microsoft.PowerShell.SecretManagement -ErrorAction SilentlyContinue
            $vault = Get-SecretVault -Name LocalSecrets -ErrorAction SilentlyContinue
            if ($vault) {
                return Get-Secret -Name GITHUB_TOKEN -Vault LocalSecrets -AsPlainText -ErrorAction SilentlyContinue
            }
        }
        return $null
    } catch {
        return $null
    }
}

Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "GITHUB ACCOUNT & ORGANIZATION STATUS CHECK" -ForegroundColor Cyan
Write-Host ("="*60) -ForegroundColor Cyan

# Try to get token from parameter, environment variable, or secure storage
if (-not $GitHubToken) {
    $GitHubToken = $env:GITHUB_TOKEN
}
if (-not $GitHubToken) {
    Write-Host "`nChecking secure storage for token..." -ForegroundColor Gray
    $GitHubToken = Get-GitHubTokenFromVault
    if ($GitHubToken) {
        Write-Host "  [OK] Token retrieved from secure storage" -ForegroundColor Green
    }
}

if ($GitHubToken) {
    $headers = @{
        "Accept" = "application/vnd.github.v3+json"
        "Authorization" = "token $GitHubToken"
    }
    
    # Check user info
    Write-Host "`n[1/4] Checking Personal Account..." -ForegroundColor Yellow
    try {
        $user = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
        Write-Host "  [OK] Username: $($user.login)" -ForegroundColor Green
        Write-Host "  [OK] Name: $($user.name)" -ForegroundColor Green
        Write-Host "  [OK] Email: $($user.email)" -ForegroundColor Green
        Write-Host "  [OK] Profile: $($user.html_url)" -ForegroundColor Green
    } catch {
        Write-Host "  [ERROR] Could not fetch user info: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Check organizations
    Write-Host "`n[2/4] Checking Organizations..." -ForegroundColor Yellow
    try {
        $orgs = Invoke-RestMethod -Uri "https://api.github.com/user/orgs" -Headers $headers
        
        if ($orgs.Count -eq 0) {
            Write-Host "  [!] No organizations found" -ForegroundColor Yellow
        } else {
            $orgs | ForEach-Object {
                Write-Host "  [OK] $($_.login)" -ForegroundColor Green
                Write-Host "     URL: $($_.html_url)" -ForegroundColor Gray
            }
        }
    } catch {
        Write-Host "  [ERROR] Could not fetch organizations: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Check for specific organizations
    Write-Host "`n[3/4] Checking Expected Organizations..." -ForegroundColor Yellow
    $expectedOrgs = @("StarGuardAI", "sentinel-analytics")
    
    foreach ($orgName in $expectedOrgs) {
        try {
            $org = Invoke-RestMethod -Uri "https://api.github.com/orgs/$orgName" -Headers $headers
            Write-Host "  [OK] ${orgName} EXISTS" -ForegroundColor Green
            Write-Host "     Name: $($org.name)" -ForegroundColor Gray
            Write-Host "     URL: $($org.html_url)" -ForegroundColor Gray
            
            # Check repositories in org
            $repos = Invoke-RestMethod -Uri "https://api.github.com/orgs/$orgName/repos" -Headers $headers
            Write-Host "     Repositories: $($repos.Count)" -ForegroundColor Gray
        } catch {
            if ($_.Exception.Response.StatusCode -eq 404) {
                Write-Host "  [X] ${orgName} NOT FOUND (needs to be created)" -ForegroundColor Red
            } else {
                Write-Host "  [!] ${orgName}: $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }
    }
    
    # List personal repositories
    Write-Host "`n[4/4] Checking Personal Repositories..." -ForegroundColor Yellow
    try {
        $repos = Invoke-RestMethod -Uri "https://api.github.com/user/repos?per_page=100" -Headers $headers
        Write-Host "  [OK] Total personal repositories: $($repos.Count)" -ForegroundColor Green
        
        Write-Host "`n  Recent repositories:" -ForegroundColor Cyan
        $repos | Select-Object -First 10 | ForEach-Object {
            Write-Host "    - $($_.name) ($($_.html_url))" -ForegroundColor Gray
        }
    } catch {
        Write-Host "  [ERROR] Could not fetch repositories: $($_.Exception.Message)" -ForegroundColor Red
    }
    
} else {
    Write-Host "`n[!] No GitHub token provided. Using web URLs only." -ForegroundColor Yellow
    Write-Host "`nTo use API features, run:" -ForegroundColor Cyan
    Write-Host '  .\check_github_status.ps1 -GitHubToken "your_token_here"' -ForegroundColor Gray
    
    Write-Host "`n[Manual Check URLs]" -ForegroundColor Yellow
    Write-Host "  Personal Account: https://github.com/bobareichert" -ForegroundColor Cyan
    Write-Host "  Settings: https://github.com/settings/admin" -ForegroundColor Cyan
    Write-Host "  Organizations: https://github.com/settings/organizations" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  StarGuardAI Org: https://github.com/StarGuardAI" -ForegroundColor Cyan
    Write-Host "  sentinel-analytics Org: https://github.com/sentinel-analytics" -ForegroundColor Cyan
}

Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "RECOMMENDATIONS" -ForegroundColor Cyan
Write-Host ("="*60) -ForegroundColor Cyan

Write-Host "`n1. Verify your username is correct"
Write-Host "2. Ensure both organizations exist"
Write-Host "3. Check organization memberships"
Write-Host "4. Verify repository locations"
Write-Host ""

