# Quick Reorganization Script (No Backup)
# For when you want to skip the backup step

param(
    [string]$ProjectsPath = "C:\Users\reich\Projects",
    [string]$HedisProject = "HEDIS-MA-Top-12-w-HEI-Prep",
    [string]$IntelligenceProject = "intelligence-security"
)

# Color output functions
function Write-Info { param([string]$Message) Write-Host $Message -ForegroundColor Cyan }
function Write-Success { param([string]$Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param([string]$Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param([string]$Message) Write-Host $Message -ForegroundColor Red }

# Set paths
$HedisPath = Join-Path $ProjectsPath $HedisProject
$IntelligencePath = Join-Path $ProjectsPath $IntelligenceProject

Write-Info -Message "=========================================="
Write-Info -Message "Quick Reorganization (No Backup)"
Write-Info -Message "=========================================="
Write-Info -Message "HEDIS Project: $HedisPath"
Write-Info -Message "Intelligence Project: $IntelligencePath"
Write-Warning -Message "Note: Backup is skipped. Files are in Git repositories."
Write-Info -Message ""

# Define files and directories to move
$ItemsToMove = @(
    @{ Source = "project\repo-cipher"; Target = "repos\cipher"; Type = "Directory" },
    @{ Source = "project\repo-foresight"; Target = "repos\foresight"; Type = "Directory" },
    @{ Source = "project\repo-guardian"; Target = "repos\guardian"; Type = "Directory" },
    @{ Source = "repo_configs"; Target = "repo_configs"; Type = "Directory" },
    @{ Source = "org_config.json"; Target = "org_config.json"; Type = "File" },
    @{ Source = "SENTINEL_SETUP_README.md"; Target = "README.md"; Type = "File" },
    @{ Source = "SECURITY_REPOS_COMPLETION_SUMMARY.md"; Target = "docs\SECURITY_REPOS_COMPLETION_SUMMARY.md"; Type = "File" },
    @{ Source = "ARCHITECTURE_SPECS.md"; Target = "docs\ARCHITECTURE_SPECS.md"; Type = "File" },
    @{ Source = "FEATURE_SPECIFICATIONS.md"; Target = "docs\FEATURE_SPECIFICATIONS.md"; Type = "File" },
    @{ Source = "DATA_ACQUISITION_GUIDE.md"; Target = "docs\DATA_ACQUISITION_GUIDE.md"; Type = "File" },
    @{ Source = "SETUP_GUIDE.md"; Target = "docs\SETUP_GUIDE.md"; Type = "File" },
    @{ Source = "CANVA_PORTFOLIO_GUIDE.md"; Target = "docs\CANVA_PORTFOLIO_GUIDE.md"; Type = "File" },
    @{ Source = "VISUALIZATION_EXPORT_GUIDE.md"; Target = "docs\VISUALIZATION_EXPORT_GUIDE.md"; Type = "File" },
    @{ Source = "test_ioc_quick.ps1"; Target = "scripts\test_ioc_quick.ps1"; Type = "File" },
    @{ Source = "test_ioc_search.ps1"; Target = "scripts\test_ioc_search.ps1"; Type = "File" },
    @{ Source = "CHAT_SEGMENTATION_PLAN.md"; Target = "docs\CHAT_SEGMENTATION_PLAN.md"; Type = "File" },
    @{ Source = "CHAT_SEGMENTATION_COMPLETE.md"; Target = "docs\CHAT_SEGMENTATION_COMPLETE.md"; Type = "File" },
    @{ Source = "CHAT_SEGMENTATION_EXECUTIVE_SUMMARY.md"; Target = "docs\CHAT_SEGMENTATION_EXECUTIVE_SUMMARY.md"; Type = "File" },
    @{ Source = "CHAT_SEGMENTATION_README.md"; Target = "docs\CHAT_SEGMENTATION_README.md"; Type = "File" },
    @{ Source = "CHAT_SEGMENTATION_TASK_COMPLETE.md"; Target = "docs\CHAT_SEGMENTATION_TASK_COMPLETE.md"; Type = "File" },
    @{ Source = "MULTI_CHAT_SEGMENTATION_PLAN.md"; Target = "docs\MULTI_CHAT_SEGMENTATION_PLAN.md"; Type = "File" },
    @{ Source = "SEGMENTATION_DOCUMENTS_INDEX.md"; Target = "docs\SEGMENTATION_DOCUMENTS_INDEX.md"; Type = "File" },
    @{ Source = "SEGMENTATION_UPDATES_SUMMARY.md"; Target = "docs\SEGMENTATION_UPDATES_SUMMARY.md"; Type = "File" },
    @{ Source = "SPRINT_C2_FIXES.md"; Target = "docs\sprints\SPRINT_C2_FIXES.md"; Type = "File" },
    @{ Source = "SPRINT_C2_TEST_RESULTS.md"; Target = "docs\sprints\SPRINT_C2_TEST_RESULTS.md"; Type = "File" },
    @{ Source = "SPRINT_C2_TESTING_GUIDE.md"; Target = "docs\sprints\SPRINT_C2_TESTING_GUIDE.md"; Type = "File" },
    @{ Source = "SPRINT_C3_MITRE_ATTACK_COMPLETE.md"; Target = "docs\sprints\SPRINT_C3_MITRE_ATTACK_COMPLETE.md"; Type = "File" }
)

# Create directory structure
Write-Info -Message "Creating Intelligence-Security project structure..."
if (-not (Test-Path $IntelligencePath)) {
    New-Item -ItemType Directory -Path $IntelligencePath -Force | Out-Null
    Write-Success -Message "Created: $IntelligencePath"
}

$directories = @("repos", "docs", "docs\sprints", "scripts")
foreach ($dir in $directories) {
    $fullPath = Join-Path $IntelligencePath $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Success -Message "Created: $fullPath"
    }
}

# Move items
Write-Info -Message ""
Write-Info -Message "Moving files and directories..."
$movedCount = 0
$failedCount = 0

foreach ($item in $ItemsToMove) {
    $sourceFull = Join-Path $HedisPath $item.Source
    $targetFull = Join-Path $IntelligencePath $item.Target
    
    if (-not (Test-Path $sourceFull)) {
        Write-Warning -Message "Source not found: $($item.Source)"
        $failedCount++
        continue
    }
    
    # Create target directory if needed
    $targetDir = Split-Path $targetFull -Parent
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
    
    try {
        Move-Item -Path $sourceFull -Destination $targetFull -Force
        Write-Success -Message "Moved: $($item.Source) -> $($item.Target)"
        $movedCount++
    } catch {
        Write-Error -Message "Failed to move $($item.Source): $_"
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
Write-Info -Message ""
Write-Success -Message "Reorganization completed!"
Write-Info -Message "Please verify the new structure at: $IntelligencePath"


