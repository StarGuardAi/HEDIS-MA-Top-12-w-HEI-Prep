# Project Reorganization - Quick Start Guide

## 🚀 Quick Execution

### Step 1: Review the Plan
```powershell
# Open and review the reorganization plan
notepad PROJECT_REORGANIZATION_PLAN.md

# View the tree diagram
notepad PROJECT_STRUCTURE_TREE.txt
```

### Step 2: Run Dry Run (Test First!)
```powershell
# Test the reorganization without making changes
.\reorganize-projects.ps1 -DryRun
```

### Step 3: Execute Reorganization
```powershell
# Run the actual reorganization (creates backup automatically)
.\reorganize-projects.ps1
```

### Step 4: Verify Results
```powershell
# Check the new Intelligence-Security project
Get-ChildItem "C:\Users\reich\Projects\intelligence-security" -Recurse -Depth 2

# Check the cleaned HEDIS project
Get-ChildItem "C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project" -Depth 1
```

## 📋 What Gets Moved

### Repositories (3)
- `project/repo-cipher` → `intelligence-security/repos/cipher`
- `project/repo-foresight` → `intelligence-security/repos/foresight`
- `project/repo-guardian` → `intelligence-security/repos/guardian`

### Configuration (2 items)
- `repo_configs/` → `intelligence-security/repo_configs/`
- `org_config.json` → `intelligence-security/org_config.json`

### Documentation (~15 files)
- Sentinel/Intelligence-Security related docs → `intelligence-security/docs/`
- Chat segmentation docs → `intelligence-security/docs/`
- Sprint docs → `intelligence-security/docs/sprints/`

### Scripts (2)
- `test_ioc_*.ps1` → `intelligence-security/scripts/`

## ⚠️ Important Notes

1. **Backup is automatic**: A timestamped backup is created before moving files
2. **Git repos preserved**: Git repositories in the moved directories will continue to work
3. **Dry run first**: Always test with `-DryRun` before executing
4. **Review paths**: After reorganization, check for any hardcoded paths in config files

## 🔍 Post-Reorganization Checklist

- [ ] Verify all three repos moved correctly
- [ ] Check Git repositories still work
- [ ] Update any hardcoded paths in configuration files
- [ ] Test scripts in new location
- [ ] Verify documentation links
- [ ] Review backup location
- [ ] Clean up empty directories (if any)

## 📁 Backup Location

Backups are stored at:
```
C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep_backup_YYYYMMDD_HHMMSS\
```

## 🆘 Troubleshooting

### Script won't run
- Ensure you're running PowerShell as Administrator (if needed)
- Check execution policy: `Get-ExecutionPolicy`
- If needed: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Files not found
- Verify you're running from the HEDIS project root directory
- Check that all source files exist before running

### Git issues
- Git repositories should work after moving, but verify remote URLs
- Check `.git` folders weren't corrupted during move

## 📞 Need Help?

1. Review `PROJECT_REORGANIZATION_PLAN.md` for detailed information
2. Check `PROJECT_STRUCTURE_TREE.txt` for visual structure
3. Review the reorganization report: `intelligence-security/REORGANIZATION_REPORT.md`


