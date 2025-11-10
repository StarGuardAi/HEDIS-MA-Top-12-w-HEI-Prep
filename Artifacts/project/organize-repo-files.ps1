# organize-repo-files.ps1
# Move all files to a folder except README.md
# This keeps the root directory clean with only README.md visible

param(
    [string]$TargetFolder = "project",
    [switch]$DryRun = $false
)

$ErrorActionPreference = 'Stop'

Write-Host "[INFO] Organizing repository files..."
Write-Host "[INFO] Target folder: $TargetFolder"

if ($DryRun) {
    Write-Host "[DRY-RUN] Would create folder: $TargetFolder"
} else {
    # Create target folder if it doesn't exist
    if (-not (Test-Path $TargetFolder)) {
        New-Item -ItemType Directory -Path $TargetFolder -Force | Out-Null
        Write-Host "[OK] Created folder: $TargetFolder"
    }
}

# Files and folders to move (excluding README.md and .git)
$itemsToMove = Get-ChildItem -Path . -Force | Where-Object {
    $_.Name -ne "README.md" -and 
    $_.Name -ne ".git" -and 
    $_.Name -ne $TargetFolder -and
    $_.Name -ne ".github" -or $_.Name -eq ".github" -and (Test-Path ".github")
}

if ($DryRun) {
    Write-Host "[DRY-RUN] Would move the following items:"
    foreach ($item in $itemsToMove) {
        Write-Host "  - $($item.Name) -> $TargetFolder/$($item.Name)"
    }
} else {
    Write-Host "[INFO] Moving files and folders..."
    $movedCount = 0
    
    foreach ($item in $itemsToMove) {
        $destination = Join-Path $TargetFolder $item.Name
        
        if (Test-Path $destination) {
            Write-Host "[WARN] Skipping $($item.Name) - already exists in target"
            continue
        }
        
        try {
            Move-Item -Path $item.FullName -Destination $destination -Force
            Write-Host "  [OK] Moved: $($item.Name)"
            $movedCount++
        } catch {
            Write-Host "  [ERROR] Failed to move $($item.Name): $_"
        }
    }
    
    Write-Host "[OK] Moved $movedCount items to $TargetFolder"
    Write-Host ""
    Write-Host "[INFO] Repository organized!"
    Write-Host "[INFO] Root directory now contains:"
    Write-Host "  - README.md (visible at root)"
    Write-Host "  - $TargetFolder/ (contains all other files)"
    Write-Host ""
    Write-Host "[INFO] Next steps:"
    Write-Host "  1. Review changes: git status"
    Write-Host "  2. Stage changes: git add ."
    Write-Host "  3. Commit: git commit -m 'Organize files: move all to $TargetFolder/'"
    Write-Host "  4. Push: git push origin main"
}

