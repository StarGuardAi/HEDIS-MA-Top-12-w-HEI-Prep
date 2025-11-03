# Cursor Speed Shortcuts - Quick Reference

## ⚡ Most Used Commands

| Command | Purpose | Time |
|---------|---------|------|
| `"/quick-review [file]"` | Security + HIPAA, failures only | ~12s |
| `"/full-review [file]"` | All checks, detailed | ~28s |
| `"/safe-commit"` | PHI scan + review changed files | ~45s |

## 🎯 Smart Prompt Patterns

### FAST Prompts (Sonnet 3.5)
```
"FAST - explain this function"
"FAST - what HEDIS violation is this?"
"FAST - review line 45 for PHI"
```

### DEEP Prompts (Claude Sonnet 4.5)
```
"DEEP - design temporal validation"
"DEEP - optimize for 5M members"
"DEEP - fairness framework"
```

### Targeted Fixes
```
"Fix line 45: remove member_id from log"
"Add HIPAA logging to validate_claims()"
"Vectorize lines 78-92"
```

## 📋 Daily Workflows

### Morning Start
```
"Read tasks/todo.md lines 1-20, show current task"
```

### After File
```
"/quick-review [filename]" → fix if issues → verify again
```

### Before Commit
```
"/safe-commit"
```

## 🏥 Healthcare Shortcuts

| Shortcut | Action |
|----------|--------|
| `"Fix PHI exposure line X"` | Quick HIPAA fix |
| `"Add HIPAA logging to [func]"` | Add compliance logging |
| `"Validate ICD-10 codes in [file]"` | Check clinical codes |
| `"Review [file] security, failures only"` | Quick security pass |

## ✅ DO vs ❌ DON'T

### ✅ Fast
- `"Fix line 45: remove member_id"`
- `"Review src/data/*.py security, failures only"`
- `"FAST - explain calculate_age()"`

### ❌ Slow
- `"Can you review my code?"`
- `"Help with feature engineering"`
- `"Check all my files"`

## 🚀 Pro Tips

1. **Line numbers** save 70% time
2. **Batch reviews**: `"/quick-review src/data/*.py"`
3. **FAST** = Sonnet 3.5 speed
4. **DEEP** = Claude Sonnet 4.5 depth
5. **Always** `/safe-commit` in healthcare

## 🛡️ Guardian Project Rules (Apply to All Projects)

### Core Principles
- **Sequential Execution Only** - Never run multiple complex tasks simultaneously
- **Task Sizing** - Break large tasks (>2 hours) into 30 min - 1 hour chunks
- **Synthetic Data First** - Default to 10K-100K records for rapid iteration
- **File Conflict Prevention** - Never modify same file from multiple processes

### Quick vs Full Mode
- **Quick Mode (Default):** 10K-100K samples, <15 min training
- **Full Mode (Optional):** 1M+ samples, 1-4 hour runtime, only if explicitly requested

### Task Execution Rules
```
❌ DON'T: Run train_large_model.py (2hr) + run_enhancements.py (1hr) simultaneously
✅ DO: Sequential with checkpoints
  1. Run train_quick_model.py (15 min)
  2. Test and verify
  3. Run enhancement (30 min)
  4. Test and verify
```

### Before Starting Any Task
- Check previous task completed and verified
- All files from previous task committed to git
- No long-running processes active
- Dependencies installed and tested

### Ask Before Assuming
If uncertain about task duration, user's time availability, or quick vs full mode:
**ALWAYS ASK:** "Would you prefer [quick option] or [full option]?"

## ⚠️ Rule: Sequential Execution Only

### Never Suggest Parallel Tasks

**❌ BAD Response:**
```
Run these in separate terminals:
Terminal 1: python train_model.py
Terminal 2: python run_enhancements.py
Terminal 3: python generate_reports.py
```

**✅ GOOD Response:**
```
Let's do this step-by-step:

**Step 1:** Train model (15 min)
python train_model.py

⏸️  PAUSE: Verify training succeeded before proceeding

**Step 2:** Run enhancements (30 min)
python run_enhancements.py

⏸️  PAUSE: Verify enhancements succeeded

**Step 3:** Generate reports (10 min)
python generate_reports.py
```

### Detection Pattern

If user asks about parallel execution:
- "Can I run X and Y at the same time?"
- "Should I run this while that's running?"
- "Can I start the next thing?"

**ALWAYS respond:**
```
⚠️  I recommend waiting for [current task] to complete first.

REASON: [Specific conflict or risk]

SAFE APPROACH:
1. Finish current task
2. Verify success
3. Then start next task

This prevents [specific problem] and ensures clean results.
```

### Exception: Independent Tasks Only

Only allow parallel execution if:
1. Tasks use completely different files
2. Tasks use different resources (CPU vs network)
3. No shared state between tasks
4. Both tasks are read-only

**Example of SAFE parallel execution:**
```
✅ SAFE: Can run these together:
Terminal 1: jupyter notebook (interactive exploration)
Terminal 2: git push origin main (network operation)

These don't conflict because:
- No shared files being written
- Different resources (CPU vs network)
- Independent operations
```

## 📋 Sprint Template

Every sprint must follow a structured template:
- **Prerequisites:** Previous sprint verified, git clean, dependencies installed
- **Objective:** One clear sentence
- **Deliverables:** List of files to create/modify
- **Implementation Steps:** Step-by-step with tests and expected output
- **Success Criteria:** Clear checklist before proceeding
- **STOP Marker:** Do not proceed until all criteria met

**Template Location:** `.cursor/prompts/SPRINT_TEMPLATE.md`

---
*Full guide: speed-shortcuts.md*  
*Sprint template: SPRINT_TEMPLATE.md*


