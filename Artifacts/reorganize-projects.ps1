# Project Reorganization Script
# Separates HEDIS project from Intelligence-Security projects
# Author: Automated reorganization
# Date: 2024

<#
.SYNOPSIS
    Reorganizes project structure by separating HEDIS and Intelligence-Security projects.

.DESCRIPTION
    This script:
    1. Creates a new directory for Intelligence-Security projects
    2. Moves intelligence-security related files from HEDIS project
    3. Organizes the three repos (cipher, foresight, guardian) into the new location
    4. Creates a backup of the original structure
    5. Generates a reorganization report

.NOTES
    Run this script from the HEDIS project root directory.
    Ensure you have administrator privileges if needed.
#>

param(
    [string]$ProjectsPath = "C:\Users\reich\Projects",
    [string]$HedisProject = "HEDIS-MA-Top-12-w-HEI-Prep",
    [string]$IntelligenceProject = "intelligence-security",
    [switch]$DryRun = $false,
    [switch]$CreateBackup = $true
)

# Color output functions
function Write-Info { param([string]$Message) Write-Host $Message -ForegroundColor Cyan }
function Write-Success { param([string]$Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param([string]$Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param([string]$Message) Write-Host $Message -ForegroundColor Red }

# Set paths
$HedisPath = Join-Path $ProjectsPath $HedisProject
$IntelligencePath = Join-Path $ProjectsPath $IntelligenceProject
$BackupPath = Join-Path $ProjectsPath "${HedisProject}_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# Validate HEDIS project exists
if (-not (Test-Path $HedisPath)) {
    Write-Error -Message "HEDIS project path not found: $HedisPath"
    exit 1
}

Write-Info -Message "=========================================="
Write-Info -Message "Project Reorganization Script"
Write-Info -Message "=========================================="
Write-Info -Message "HEDIS Project: $HedisPath"
Write-Info -Message "Intelligence Project: $IntelligencePath"
Write-Info -Message "Dry Run: $DryRun"
Write-Info -Message "Create Backup: $CreateBackup"
Write-Info -Message ""

# Define files and directories to move to Intelligence-Security project
$ItemsToMove = @(
    # Repository directories
    @{ Source = "project\repo-cipher"; Target = "repos\cipher"; Type = "Directory" },
    @{ Source = "project\repo-foresight"; Target = "repos\foresight"; Type = "Directory" },
    @{ Source = "project\repo-guardian"; Target = "repos\guardian"; Type = "Directory" },
    
    # Configuration files
    @{ Source = "repo_configs"; Target = "repo_configs"; Type = "Directory" },
    @{ Source = "org_config.json"; Target = "org_config.json"; Type = "File" },
    
    # Documentation files
    @{ Source = "SENTINEL_SETUP_README.md"; Target = "README.md"; Type = "File" },
    @{ Source = "SECURITY_REPOS_COMPLETION_SUMMARY.md"; Target = "docs\SECURITY_REPOS_COMPLETION_SUMMARY.md"; Type = "File" },
    @{ Source = "ARCHITECTURE_SPECS.md"; Target = "docs\ARCHITECTURE_SPECS.md"; Type = "File" },
    @{ Source = "FEATURE_SPECIFICATIONS.md"; Target = "docs\FEATURE_SPECIFICATIONS.md"; Type = "File" },
    @{ Source = "DATA_ACQUISITION_GUIDE.md"; Target = "docs\DATA_ACQUISITION_GUIDE.md"; Type = "File" },
    @{ Source = "SETUP_GUIDE.md"; Target = "docs\SETUP_GUIDE.md"; Type = "File" },
    @{ Source = "CANVA_PORTFOLIO_GUIDE.md"; Target = "docs\CANVA_PORTFOLIO_GUIDE.md"; Type = "File" },
    @{ Source = "VISUALIZATION_EXPORT_GUIDE.md"; Target = "docs\VISUALIZATION_EXPORT_GUIDE.md"; Type = "File" },
    
    # Test scripts
    @{ Source = "test_ioc_quick.ps1"; Target = "scripts\test_ioc_quick.ps1"; Type = "File" },
    @{ Source = "test_ioc_search.ps1"; Target = "scripts\test_ioc_search.ps1"; Type = "File" },
    
    # Chat segmentation documents (related to security repos)
    @{ Source = "CHAT_SEGMENTATION_PLAN.md"; Target = "docs\CHAT_SEGMENTATION_PLAN.md"; Type = "File" },
    @{ Source = "CHAT_SEGMENTATION_COMPLETE.md"; Target = "docs\CHAT_SEGMENTATION_COMPLETE.md"; Type = "File" },
    @{ Source = "CHAT_SEGMENTATION_EXECUTIVE_SUMMARY.md"; Target = "docs\CHAT_SEGMENTATION_EXECUTIVE_SUMMARY.md"; Type = "File" },
    @{ Source = "CHAT_SEGMENTATION_README.md"; Target = "docs\CHAT_SEGMENTATION_README.md"; Type = "File" },
    @{ Source = "CHAT_SEGMENTATION_TASK_COMPLETE.md"; Target = "docs\CHAT_SEGMENTATION_TASK_COMPLETE.md"; Type = "File" },
    @{ Source = "MULTI_CHAT_SEGMENTATION_PLAN.md"; Target = "docs\MULTI_CHAT_SEGMENTATION_PLAN.md"; Type = "File" },
    @{ Source = "SEGMENTATION_DOCUMENTS_INDEX.md"; Target = "docs\SEGMENTATION_DOCUMENTS_INDEX.md"; Type = "File" },
    @{ Source = "SEGMENTATION_UPDATES_SUMMARY.md"; Target = "docs\SEGMENTATION_UPDATES_SUMMARY.md"; Type = "File" },
    
    # Sprint documents related to security repos
    @{ Source = "SPRINT_C2_FIXES.md"; Target = "docs\sprints\SPRINT_C2_FIXES.md"; Type = "File" },
    @{ Source = "SPRINT_C2_TEST_RESULTS.md"; Target = "docs\sprints\SPRINT_C2_TEST_RESULTS.md"; Type = "File" },
    @{ Source = "SPRINT_C2_TESTING_GUIDE.md"; Target = "docs\sprints\SPRINT_C2_TESTING_GUIDE.md"; Type = "File" },
    @{ Source = "SPRINT_C3_MITRE_ATTACK_COMPLETE.md"; Target = "docs\sprints\SPRINT_C3_MITRE_ATTACK_COMPLETE.md"; Type = "File" }
)

# Function to create directory structure
function New-DirectoryStructure {
    param([string]$Path)
    
    $directories = @(
        "repos",
        "docs",
        "docs\sprints",
        "scripts"
    )
    
    foreach ($dir in $directories) {
        $fullPath = Join-Path $Path $dir
        if (-not (Test-Path $fullPath)) {
            if (-not $DryRun) {
                New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
                Write-Success -Message "Created directory: $fullPath"
            } else {
                Write-Info -Message "[DRY RUN] Would create directory: $fullPath"
            }
        }
    }
}

# Function to move item
function Move-ProjectItem {
    param(
        [string]$SourcePath,
        [string]$TargetPath,
        [string]$Type
    )
    
    $sourceFull = Join-Path $HedisPath $SourcePath
    $targetFull = Join-Path $IntelligencePath $TargetPath
    
    if (-not (Test-Path $sourceFull)) {
        Write-Warning -Message "Source not found: $sourceFull"
        return $false
    }
    
    # Create target directory if needed
    $targetDir = Split-Path $targetFull -Parent
    if (-not (Test-Path $targetDir)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
    }
    
    if (-not $DryRun) {
        try {
            Move-Item -Path $sourceFull -Destination $targetFull -Force
            Write-Success -Message "Moved: $SourcePath -> $TargetPath"
            return $true
        } catch {
            Write-Error -Message "Failed to move $SourcePath : $_"
            return $false
        }
    } else {
        Write-Info -Message "[DRY RUN] Would move: $SourcePath -> $TargetPath"
        return $true
    }
}

# Main execution
Write-Info -Message "Step 1: Creating backup..."
if ($CreateBackup -and -not $DryRun) {
    Write-Info -Message "Creating backup at: $BackupPath (this may take a few minutes for large repositories)..."
    try {
        # Copy only the items that will be moved (for a lighter backup)
        $null = New-Item -ItemType Directory -Path $BackupPath -Force
        $itemCount = 0
        foreach ($item in $ItemsToMove) {
            $itemCount++
            $sourceFull = Join-Path $HedisPath $item.Source
            if (Test-Path $sourceFull) {
                Write-Info -Message "  Backing up item $itemCount/$($ItemsToMove.Count): $($item.Source)"
                $targetDir = Join-Path $BackupPath (Split-Path $item.Source -Parent)
                if (-not (Test-Path $targetDir)) {
                    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                }
                Copy-Item -Path $sourceFull -Destination (Join-Path $BackupPath $item.Source) -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
        Write-Success -Message "Backup created successfully"
    } catch {
        Write-Warning -Message "Backup creation failed: $_"
        Write-Warning -Message "Continuing without backup (files are in Git repositories)..."
    }
} elseif ($DryRun) {
    Write-Info -Message "[DRY RUN] Would create backup at: $BackupPath"
}

Write-Info -Message ""
Write-Info -Message "Step 2: Creating Intelligence-Security project structure..."
if (-not $DryRun) {
    if (-not (Test-Path $IntelligencePath)) {
        New-Item -ItemType Directory -Path $IntelligencePath -Force | Out-Null
        Write-Success -Message "Created Intelligence-Security project directory"
    } else {
        Write-Warning -Message "Intelligence-Security project directory already exists"
    }
} else {
    Write-Info -Message "[DRY RUN] Would create: $IntelligencePath"
}

New-DirectoryStructure -Path $IntelligencePath

Write-Info -Message ""
Write-Info -Message "Step 3: Moving files and directories..."
$movedCount = 0
$failedCount = 0

foreach ($item in $ItemsToMove) {
    if (Move-ProjectItem -SourcePath $item.Source -TargetPath $item.Target -Type $item.Type) {
        $movedCount++
    } else {
        $failedCount++
    }
}

Write-Info -Message ""
Write-Info -Message "=========================================="
Write-Info -Message "Reorganization Summary"
Write-Info -Message "=========================================="
Write-Info -Message "Items moved successfully: $movedCount"
if ($failedCount -gt 0) {
    Write-Warning -Message "Items failed: $failedCount"
}
if ($CreateBackup) {
    Write-Info -Message "Backup location: $BackupPath"
}
Write-Info -Message ""

# Create reorganization report
$reportPath = Join-Path $IntelligencePath "REORGANIZATION_REPORT.md"
if (-not $DryRun) {
    $status = if ($DryRun) { 'Dry Run' } else { 'Completed' }
    $report = @"
# Project Reorganization Report

**Date**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
**Status**: $status

## Summary

- **HEDIS Project**: $HedisPath
- **Intelligence-Security Project**: $IntelligencePath
- **Items Moved**: $movedCount
- **Items Failed**: $failedCount

## Moved Items

$(($ItemsToMove | ForEach-Object { "- $($_.Source) -> $($_.Target)" }) -join "`n")

## Next Steps

1. Review the new Intelligence-Security project structure
2. Update any hardcoded paths in configuration files
3. Verify Git repositories are working correctly
4. Update documentation references

## Backup Location

$(if ($CreateBackup) { "Backup created at: $BackupPath" } else { "No backup was created" })
"@
    Set-Content -Path $reportPath -Value $report
    Write-Success -Message "Reorganization report created: $reportPath"
}

Write-Info -Message ""
if ($DryRun) {
    Write-Success -Message "Reorganization dry run completed!"
} else {
    Write-Success -Message "Reorganization completed!"
}
Write-Info -Message "Please review the changes before proceeding."

