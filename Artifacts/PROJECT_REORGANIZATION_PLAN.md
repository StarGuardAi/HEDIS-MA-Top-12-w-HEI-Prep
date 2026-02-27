# Project Reorganization Plan

## Overview

This document outlines the reorganization plan to separate the HEDIS project from the Intelligence-Security projects into distinct directories.

## Current Structure Problems

1. **Intelligence-Security repos are nested 2 levels deep**: `project/repo-*` within HEDIS project
2. **Mixed concerns**: HEDIS and Intelligence-Security files are intermingled
3. **Unclear organization**: Difficult to identify which files belong to which project

## Proposed Structure

### Target Directory Layout

```
C:\Users\reich\Projects\
├── HEDIS-MA-Top-12-w-HEI-Prep\          # HEDIS project (cleaned)
│   ├── data\
│   ├── docs\
│   ├── scripts\
│   ├── project\                          # HEDIS-specific project files only
│   ├── README.md
│   └── ... (HEDIS-related files)
│
└── intelligence-security\                 # NEW: Intelligence-Security project
    ├── README.md                          # (from SENTINEL_SETUP_README.md)
    ├── org_config.json
    ├── repo_configs\
    │   ├── cipher.json
    │   ├── foresight.json
    │   └── guardian.json
    ├── repos\                             # NEW: Better organization
    │   ├── cipher\                        # (from project/repo-cipher)
    │   ├── foresight\                     # (from project/repo-foresight)
    │   └── guardian\                      # (from project/repo-guardian)
    ├── docs\
    │   ├── ARCHITECTURE_SPECS.md
    │   ├── FEATURE_SPECIFICATIONS.md
    │   ├── DATA_ACQUISITION_GUIDE.md
    │   ├── SETUP_GUIDE.md
    │   ├── CANVA_PORTFOLIO_GUIDE.md
    │   ├── VISUALIZATION_EXPORT_GUIDE.md
    │   ├── SECURITY_REPOS_COMPLETION_SUMMARY.md
    │   ├── CHAT_SEGMENTATION_PLAN.md
    │   ├── CHAT_SEGMENTATION_COMPLETE.md
    │   ├── CHAT_SEGMENTATION_EXECUTIVE_SUMMARY.md
    │   ├── CHAT_SEGMENTATION_README.md
    │   ├── CHAT_SEGMENTATION_TASK_COMPLETE.md
    │   ├── MULTI_CHAT_SEGMENTATION_PLAN.md
    │   ├── SEGMENTATION_DOCUMENTS_INDEX.md
    │   ├── SEGMENTATION_UPDATES_SUMMARY.md
    │   └── sprints\
    │       ├── SPRINT_C2_FIXES.md
    │       ├── SPRINT_C2_TEST_RESULTS.md
    │       ├── SPRINT_C2_TESTING_GUIDE.md
    │       └── SPRINT_C3_MITRE_ATTACK_COMPLETE.md
    └── scripts\
        ├── test_ioc_quick.ps1
        └── test_ioc_search.ps1
```

## Files to Move

### Repository Directories
- `project/repo-cipher` → `intelligence-security/repos/cipher`
- `project/repo-foresight` → `intelligence-security/repos/foresight`
- `project/repo-guardian` → `intelligence-security/repos/guardian`

### Configuration Files
- `repo_configs/` → `intelligence-security/repo_configs/`
- `org_config.json` → `intelligence-security/org_config.json`

### Documentation Files
- `SENTINEL_SETUP_README.md` → `intelligence-security/README.md`
- `ARCHITECTURE_SPECS.md` → `intelligence-security/docs/ARCHITECTURE_SPECS.md`
- `FEATURE_SPECIFICATIONS.md` → `intelligence-security/docs/FEATURE_SPECIFICATIONS.md`
- `DATA_ACQUISITION_GUIDE.md` → `intelligence-security/docs/DATA_ACQUISITION_GUIDE.md`
- `SETUP_GUIDE.md` → `intelligence-security/docs/SETUP_GUIDE.md`
- `CANVA_PORTFOLIO_GUIDE.md` → `intelligence-security/docs/CANVA_PORTFOLIO_GUIDE.md`
- `VISUALIZATION_EXPORT_GUIDE.md` → `intelligence-security/docs/VISUALIZATION_EXPORT_GUIDE.md`
- `SECURITY_REPOS_COMPLETION_SUMMARY.md` → `intelligence-security/docs/SECURITY_REPOS_COMPLETION_SUMMARY.md`

### Chat Segmentation Documents
- `CHAT_SEGMENTATION_*.md` → `intelligence-security/docs/`
- `MULTI_CHAT_SEGMENTATION_PLAN.md` → `intelligence-security/docs/`
- `SEGMENTATION_*.md` → `intelligence-security/docs/`

### Sprint Documents
- `SPRINT_C2_*.md` → `intelligence-security/docs/sprints/`
- `SPRINT_C3_*.md` → `intelligence-security/docs/sprints/`

### Test Scripts
- `test_ioc_quick.ps1` → `intelligence-security/scripts/`
- `test_ioc_search.ps1` → `intelligence-security/scripts/`

## Files to Keep in HEDIS Project

All HEDIS-specific files remain:
- `data/` (HEDIS datasets)
- `docs/` (HEDIS documentation)
- `scripts/` (HEDIS scripts)
- `project/` (HEDIS-specific project files, excluding repo-*)
- All `CHAT_*.md` files related to HEDIS
- All `PHASE_*.md` files
- `README.md` (HEDIS-specific)
- All other HEDIS-related files

## Execution Steps

### Option 1: Automated Script (Recommended)

1. **Review the plan**: Read this document and verify the file list
2. **Run dry run**: `.\reorganize-projects.ps1 -DryRun`
3. **Review output**: Check what will be moved
4. **Execute**: `.\reorganize-projects.ps1`
5. **Verify**: Check both project directories
6. **Update paths**: Update any hardcoded paths in configuration files
7. **Test Git repos**: Verify Git repositories still work correctly

### Option 2: Manual Execution

1. Create `C:\Users\reich\Projects\intelligence-security\`
2. Create subdirectories: `repos/`, `docs/`, `docs/sprints/`, `scripts/`
3. Move files according to the mapping above
4. Verify all files moved correctly

## Post-Reorganization Tasks

### 1. Update Configuration Files
- Check `org_config.json` for any hardcoded paths
- Update paths in `repo_configs/*.json` if needed
- Review environment variables in `.env` files

### 2. Update Git Repositories
- Verify Git repos in `repos/cipher`, `repos/foresight`, `repos/guardian` still work
- Check for any `.git` folder issues
- Update any remote URLs if needed

### 3. Update Documentation
- Update README.md files with new paths
- Fix any broken links in documentation
- Update any path references in markdown files

### 4. Update Scripts
- Check PowerShell scripts for hardcoded paths
- Update any path references in Python scripts
- Verify test scripts still work

### 5. Cleanup
- Remove empty directories from HEDIS project
- Review and remove any duplicate files
- Archive backup if reorganization is successful

## Benefits

1. **Clear Separation**: HEDIS and Intelligence-Security projects are now distinct
2. **Better Organization**: Intelligence-Security repos are at the same level (not nested 2 deep)
3. **Easier Navigation**: Clear directory structure for each project
4. **Independent Development**: Each project can be developed independently
5. **Better Git Management**: Separate Git repositories for each project

## Rollback Plan

If issues occur:
1. Restore from backup: `C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep_backup_YYYYMMDD_HHMMSS\`
2. Delete the new `intelligence-security` directory
3. Review what went wrong and adjust plan

## Safety Measures

- **Dry Run**: Always test with `-DryRun` first
- **Backup**: Automatic backup of moved files
- **Verification**: Script verifies each move operation
- **Report**: Detailed report generated after reorganization


