# ⚡ Cursor Speed Shortcuts - Desk Reference

## 🎯 The Big 3 (Use Daily)

| Pattern | What It Does | When To Use |
|---------|-------------|-------------|
| **`/quick-review [file]`** | Security + HIPAA check, ~12s | After finishing any file |
| **`/full-review [file]`** | All checks, detailed, ~28s | Before major commits |
| **`/safe-commit`** | PHI scan + review all, ~45s | Before EVERY commit |

---

## 📝 What To Type (Copy & Paste)

### After Finishing a File
```
/quick-review src/data/feature_engineering.py

Run security and HIPAA reviews only, show failures:
- Check for PHI exposure
- Check for hardcoded credentials
- Check for SQL injection
- Show only failures and critical issues
```

### Before Committing
```
/safe-commit

Before committing, run PHI scanner and review all changed files:
1. Scan all Python files for PHI patterns
2. For each changed file, run quick-review
3. Provide summary of all issues found
4. List files ready to commit vs files needing fixes
```

### Need a Quick Answer
```
FAST - explain calculate_age() function

Keep response concise, maximum 3 sentences.
```

### Need Deep Thinking
```
DEEP - design temporal validation strategy

Consider train/test split, data drift, HEDIS requirements, no leakage.
```

---

## 🏥 Healthcare-Specific

### Fix PHI Exposure
```
Fix line 45 only: remove member_id from log
```

### Add HIPAA Logging
```
Add HIPAA logging to validate_claims() function
```

### Review Security Issues Only
```
Review src/data/*.py security, failures only
```

---

## ⏱️ Timing Guide

| Task | Old Way | New Way | Time Saved |
|------|---------|---------|------------|
| Review a file | Read whole file, manually check | `/quick-review file` | 85% faster |
| Before commit | Manual checklist | `/safe-commit` | 60% faster |
| Quick question | Long explanation | `FAST - question` | 70% faster |
| Targeted fix | "Fix the bug" | `Fix line X: issue` | 75% faster |

---

## 💡 Pro Tips

1. **Always specify line numbers** when fixing issues
2. **Use `/quick-review`** for daily development
3. **Use `/full-review`** only for major milestones
4. **Always `/safe-commit`** before git operations
5. **Batch reviews:** `/quick-review src/data/*.py`

---

## ❌ DON'T

- ❌ "Can you review my code?"
- ❌ "I need help with feature engineering"
- ❌ Review files one at a time
- ❌ Skip `/safe-commit` before pushing

---

## ✅ DO

- ✅ "Fix line 45: remove member_id from log"
- ✅ "Add docstring to calculate_age() only"
- ✅ Use batch reviews: `/quick-review src/data/*.py`
- ✅ Always run `/safe-commit` before commits

---

## 🚀 Morning Routine

```
1. "Read tasks/todo.md lines 1-20, show current task"
2. Start coding
3. After each file: "/quick-review [filename]"
4. Before break: "/safe-commit"
```

---

## 🛡️ Guardian Project Rules (Quick Reference)

### ⚠️ Always Remember
- **One task at a time** - Complete fully before starting next
- **30 min - 1 hour chunks** - Break large tasks into smaller pieces
- **Quick mode first** - Default to 10K-100K samples, <15 min training
- **Ask before assuming** - If uncertain about duration or mode, ask user

### ❌ Never Do
- Run multiple complex tasks simultaneously
- Create 10+ files without testing
- Start new task before previous one verified
- Assume user wants longest, most complex version

### ✅ Always Do
- Sequential execution with checkpoints
- Test after each file created
- Provide quick alternatives
- Clear success criteria before starting

## ⚠️ Rule: Sequential Execution Only

### Never Suggest Parallel Tasks

**❌ BAD:**
```
Run these in separate terminals:
Terminal 1: python train_model.py
Terminal 2: python run_enhancements.py
```

**✅ GOOD:**
```
Step-by-step:

**Step 1:** Train model (15 min)
python train_model.py

⏸️  PAUSE: Verify success

**Step 2:** Run enhancements (30 min)
python run_enhancements.py
```

### If User Asks About Parallel Execution

**Always respond:**
```
⚠️  I recommend waiting for [current task] to complete first.

REASON: [Specific conflict or risk]
SAFE APPROACH:
1. Finish current task
2. Verify success
3. Then start next task
```

### Exception: Independent Tasks Only

Only allow parallel if:
- Different files
- Different resources (CPU vs network)
- No shared state
- Both read-only

---

## 📋 Sprint Template Reference

Before starting any sprint, use the sprint template:
- Check prerequisites (previous sprint verified, git clean)
- Define clear objective (one sentence)
- List deliverables (files to create/modify)
- Add implementation steps with tests
- Define success criteria
- Add STOP marker before proceeding

**Template:** `.cursor/prompts/SPRINT_TEMPLATE.md`

---

**Remember:** These are prompt patterns, not built-in commands. Type them naturally in Cursor chat.

Full guide: `speed-shortcuts.md`  
Quick ref: `QUICK_REFERENCE.md`  
Guardian Rules: See `.cursorrules` for complete rules  
Sprint Template: `SPRINT_TEMPLATE.md`


