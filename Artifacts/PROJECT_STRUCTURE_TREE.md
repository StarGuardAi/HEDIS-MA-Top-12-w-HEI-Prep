# Project Structure Tree Diagram

## Current Structure (Before Reorganization)

```
C:\Users\reich\Projects\
└── HEDIS-MA-Top-12-w-HEI-Prep\
    ├── data\
    │   └── processed\
    ├── docs\
    │   └── architecture-decisions\
    ├── project\
    │   ├── repo-cipher\              ⚠️ [MOVE] Intelligence-Security
    │   │   ├── src\
    │   │   ├── frontend\
    │   │   ├── docs\
    │   │   └── ...
    │   ├── repo-foresight\           ⚠️ [MOVE] Intelligence-Security
    │   │   ├── src\
    │   │   ├── frontend\
    │   │   ├── docs\
    │   │   └── ...
    │   ├── repo-guardian\            ⚠️ [MOVE] Intelligence-Security
    │   │   ├── src\
    │   │   ├── frontend\
    │   │   ├── docs\
    │   │   └── ...
    │   └── ... (HEDIS project files)
    ├── repo_configs\                 ⚠️ [MOVE] Intelligence-Security
    │   ├── cipher.json
    │   ├── foresight.json
    │   └── guardian.json
    ├── SENTINEL_SETUP_README.md      ⚠️ [MOVE] Intelligence-Security
    ├── ARCHITECTURE_SPECS.md         ⚠️ [MOVE] Intelligence-Security
    ├── FEATURE_SPECIFICATIONS.md     ⚠️ [MOVE] Intelligence-Security
    ├── DATA_ACQUISITION_GUIDE.md     ⚠️ [MOVE] Intelligence-Security
    ├── SETUP_GUIDE.md                ⚠️ [MOVE] Intelligence-Security
    ├── SECURITY_REPOS_COMPLETION_SUMMARY.md  ⚠️ [MOVE] Intelligence-Security
    ├── test_ioc_quick.ps1            ⚠️ [MOVE] Intelligence-Security
    ├── test_ioc_search.ps1           ⚠️ [MOVE] Intelligence-Security
    ├── CHAT_SEGMENTATION_*.md        ⚠️ [MOVE] Intelligence-Security
    ├── SPRINT_C2_*.md                ⚠️ [MOVE] Intelligence-Security
    ├── SPRINT_C3_*.md                ⚠️ [MOVE] Intelligence-Security
    ├── README.md                     ✓ [KEEP] HEDIS
    ├── CHAT_*.md                     ✓ [KEEP] HEDIS
    ├── PHASE_*.md                    ✓ [KEEP] HEDIS
    └── ... (other HEDIS files)
```

**Problem**: Intelligence-Security repositories are nested 2 levels deep (`project/repo-*`), making them awkward to access.

---

## Proposed Structure (After Reorganization)

```
C:\Users\reich\Projects\
│
├── HEDIS-MA-Top-12-w-HEI-Prep\          ✓ HEDIS Project (Cleaned)
│   ├── data\
│   │   └── processed\
│   ├── docs\
│   │   └── architecture-decisions\
│   ├── project\                         ✓ HEDIS project files only
│   │   ├── src\
│   │   ├── models\
│   │   ├── streamlit_app.py
│   │   └── ... (HEDIS-specific files)
│   ├── scripts\
│   │   ├── create_demo_data.py
│   │   ├── generate_synthetic_data.py
│   │   └── ... (HEDIS scripts)
│   ├── github\
│   ├── linkedin\
│   ├── resume\
│   ├── README.md                        ✓ HEDIS
│   ├── CHAT_*.md                        ✓ HEDIS chat logs
│   ├── PHASE_*.md                       ✓ HEDIS phase docs
│   └── ... (HEDIS-related files only)
│
└── intelligence-security\                ✓ NEW: Intelligence-Security Project
    │
    ├── README.md                         (renamed from SENTINEL_SETUP_README.md)
    ├── org_config.json
    │
    ├── repo_configs\
    │   ├── cipher.json
    │   ├── foresight.json
    │   └── guardian.json
    │
    ├── repos\                            ✓ Better organization (1 level, not 2)
    │   │
    │   ├── cipher\                       (from project/repo-cipher)
    │   │   ├── src\
    │   │   │   ├── api\
    │   │   │   └── ...
    │   │   ├── frontend\
    │   │   │   ├── src\
    │   │   │   └── ...
    │   │   ├── docs\
    │   │   ├── data\
    │   │   ├── scripts\
    │   │   ├── tests\
    │   │   ├── README.md
    │   │   ├── requirements.txt
    │   │   └── ...
    │   │
    │   ├── foresight\                    (from project/repo-foresight)
    │   │   ├── src\
    │   │   │   ├── api\
    │   │   │   └── ...
    │   │   ├── frontend\
    │   │   │   ├── src\
    │   │   │   └── ...
    │   │   ├── docs\
    │   │   ├── data\
    │   │   ├── scripts\
    │   │   ├── tests\
    │   │   ├── README.md
    │   │   ├── requirements.txt
    │   │   └── ...
    │   │
    │   └── guardian\                     (from project/repo-guardian)
    │       ├── src\
    │       │   ├── api\
    │       │   └── ...
    │       ├── frontend\
    │       │   ├── src\
    │       │   └── ...
    │       ├── docs\
    │       ├── data\
    │       ├── scripts\
    │       ├── tests\
    │       ├── README.md
    │       ├── requirements.txt
    │       └── ...
    │
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
    │
    └── scripts\
        ├── test_ioc_quick.ps1
        └── test_ioc_search.ps1
```

---

## Key Improvements

### ✅ Before vs After

| Aspect | Before | After |
|--------|--------|-------|
| **Intelligence-Security Location** | `project/repo-*` (2 levels deep) | `repos/*` (1 level deep) |
| **Project Separation** | Mixed in HEDIS directory | Separate directory |
| **Navigation** | Awkward nested structure | Clean, flat structure |
| **Organization** | Unclear file ownership | Clear project boundaries |
| **Development** | Coupled with HEDIS | Independent projects |

### 📊 File Movement Summary

- **Repositories**: 3 major repos moved from 2 levels deep to 1 level
- **Configuration Files**: 2 items (directory + file)
- **Documentation**: ~15 files organized into logical structure
- **Scripts**: 2 test scripts moved to dedicated scripts directory

### 🎯 Benefits

1. **Clear Separation**: HEDIS and Intelligence-Security projects are distinct
2. **Better Access**: Repos are easier to access (1 level vs 2 levels)
3. **Logical Organization**: Related files grouped together
4. **Independent Development**: Each project can be developed separately
5. **Easier Maintenance**: Clear structure makes maintenance simpler

---

## Legend

- ✓ = Keep in current location
- ⚠️ = Move to new location
- [MOVE] = Needs to be moved
- [KEEP] = Stays in place


