# PowerShell script to update email and GitHub URLs in all files within the project directory
# Replaces:
#   - reichert99@gmail.com -> reichert.starguardai@gmail.com
#   - https://github.com/bobareichert/hedis-gsd-prediction-engine -> https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep
#   - github.com/bobareichert/hedis-gsd-prediction-engine -> github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep
#   - bobareichert/hedis-gsd-prediction-engine -> StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep
#   - https://github.com/bobareichert -> https://github.com/StarGuardAi (for profile links)

Write-Host "Starting bulk replacement of email and GitHub URLs..." -ForegroundColor Green

$projectPath = "project"
$filesUpdated = 0
$totalReplacements = 0

# Define replacements: old value -> new value
$replacements = @{
    'reichert99@gmail.com' = 'reichert.starguardai@gmail.com'
    'https://github.com/bobareichert/hedis-gsd-prediction-engine' = 'https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep'
    'github.com/bobareichert/hedis-gsd-prediction-engine' = 'github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep'
    'bobareichert/hedis-gsd-prediction-engine' = 'StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep'
    'https://github.com/bobareichert' = 'https://github.com/StarGuardAi'
    'github.com/bobareichert' = 'github.com/StarGuardAi'
}

# Get all files in project directory recursively
$files = Get-ChildItem -Path $projectPath -Recurse -File | Where-Object { 
    $_.Extension -in @('.md', '.py', '.txt', '.json', '.yaml', '.yml', '.bat', '.ps1', '.sh', '.html', '.js', '.ts', '.css')
}

Write-Host "Found $($files.Count) files to process..." -ForegroundColor Cyan

foreach ($file in $files) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -ErrorAction Stop
        $originalContent = $content
        $fileReplacements = 0
        
        # Apply each replacement
        foreach ($oldValue in $replacements.Keys) {
            $newValue = $replacements[$oldValue]
            if ($content -match [regex]::Escape($oldValue)) {
                $matches = ([regex]::Matches($content, [regex]::Escape($oldValue))).Count
                $content = $content -replace [regex]::Escape($oldValue), $newValue
                $fileReplacements += $matches
                $totalReplacements += $matches
            }
        }
        
        # Write back if changes were made
        if ($content -ne $originalContent) {
            Set-Content -Path $file.FullName -Value $content -NoNewline -ErrorAction Stop
            $filesUpdated++
            Write-Host "  [OK] Updated: $($file.FullName) ($fileReplacements replacement(s))" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "  [ERROR] Error processing: $($file.FullName) - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nReplacement complete!" -ForegroundColor Green
Write-Host "  Files updated: $filesUpdated" -ForegroundColor Cyan
Write-Host "  Total replacements: $totalReplacements" -ForegroundColor Cyan

