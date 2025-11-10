# Cursor Speed Shortcuts - Quick Reference

## Daily Commands (Use These Constantly)

### Starting Work
```
"Read tasks/todo.md lines 1-20 only, show current task"
[Instead of: "Read my todo file"]
```

### Code Reviews (New Batch Style)
```
"/quick-review src/data/feature_engineering.py"
[Runs: security + HIPAA, shows only failures, ~12 sec]

"/full-review src/data/feature_engineering.py"
[Runs: all checks, detailed report, ~28 sec]
```

### Fixing Issues
```
"Fix line 45 only: remove member_id from log"
[Instead of: "Can you help fix the logging issue?"]
```

### Before Committing
```
"/safe-commit"
[Runs: PHI scanner + reviews changed files + summary]
```

## Prompt Patterns for Speed

### ✅ FAST Prompts
- `"Add docstring to calculate_age() only"`
- `"Fix PHI exposure line 45"`
- `"Review src/data/*.py security, failures only"`
- `"FAST - explain this function"` [uses Sonnet 3.5]

### ❌ SLOW Prompts (Avoid)
- `"Can you review my code and let me know if there are issues?"`
- `"I'm working on feature engineering, could you help?"`
- `"Please check everything in my data pipeline"`

## Model Selection
- **Default:** Uses Sonnet 3.5 (fast)
- **When you need depth:** `"DEEP - design temporal validation strategy"`

## Healthcare-Specific Shortcuts

### Quick Reviews
```
"/quick-review [file]" → Security + HIPAA only, show failures
"/full-review [file]"  → All review types, comprehensive
"/safe-commit"         → PHI scan + changed files review
```

### Targeted Fixes
```
"Fix PHI exposure line 45"
"Add HIPAA logging to function X"
"Vectorize line 78-92 for performance"
"Validate ICD-10 codes in load_claims()"
```

### Fast Explanations
```
"FAST - explain this function"
"FAST - what does this HEDIS measure mean?"
"FAST - why is this a violation?"
```

### Deep Analysis
```
"DEEP - design temporal validation strategy"
"DEEP - optimize for 5M member dataset"
"DEEP - create fairness evaluation framework"
```

## Common Workflows

### Morning Start
```
1. "Read tasks/todo.md lines 1-20 only, show current task"
2. "Read Plan.md section on [current phase]"
3. Review plan, then: "Begin implementing [specific subtask]"
```

### After Finishing a File
```
1. "/quick-review [filename]"
2. If issues found: Fix them with targeted prompts
3. Verify: "/quick-review [filename]" again
```

### Before Lunch/Break
```
"/safe-commit"
[Quick check of all changed files before breaking]
```

### End of Day
```
1. "/full-review" on any major changes
2. "Update tasks/todo.md with review summary"
3. "Next: prep tomorrow's task list"
```

## Time-Saving Tips

### Be Specific
❌ `"Fix the bug"`
✅ `"Fix line 45: remove member_id from log"`

### Target Single Functions
❌ `"Review this file"`
✅ `"Review validate_claims() function only"`

### Batch Reviews
❌ Review files one by one
✅ `"/quick-review src/data/*.py"`

### Use Line Numbers
❌ `"There's an issue with the logging"`
✅ `"Fix logging issue line 45"`

## Integration with Main Workflow

These shortcuts work alongside your `.cursorrules` file. The rules provide:
- **Automatic context loading** (HEDIS specs, HIPAA requirements)
- **Default review commands** when you complete files
- **Project-specific terminology** (GSD, MY, PHI, etc.)

The shortcuts give you **faster manual control** for:
- Quick checks
- Targeted fixes
- Rapid iterations

## Customizable Shortcuts

You can add your own shortcuts by creating aliases in `.cursor/prompts/shortcuts-local.md`:

```markdown
# Personal Shortcuts

"/fix-phi [file]" → Same as quick-review but auto-fixes common PHI issues
"/hedis-validate [measure]" → Validates against HEDIS specs
"/performance-profile [file]" → Profiles and suggests optimizations
```

## Pro Tips

1. **Line-specific fixes save 70% time** vs general requests
2. **Batch reviews** handle multiple files at once
3. **FAST prefix** uses Sonnet 3.5 for speed
4. **DEEP prefix** uses Claude for complex problems
5. **Use /safe-commit** before ANY git commit in healthcare

## Quick Reference Card (Print This)

```
START WORK:      "Read tasks/todo.md lines 1-20"
QUICK CHECK:     "/quick-review [file]"
FULL CHECK:      "/full-review [file]"
BEFORE COMMIT:   "/safe-commit"
FAST ANSWER:     "FAST - [question]"
DEEP ANALYSIS:   "DEEP - [question]"
FIX SPECIFIC:    "Fix line X: [issue]"
REVIEW ALL:      "/quick-review src/data/*.py"
```

---

## 🛡️ Guardian Fraud Detection System Rules

### Core Principles (Apply to All Projects)

These rules from the Guardian Fraud Detection System apply to all Cursor AI chats:

**Sequential Execution Only**
- NEVER suggest running multiple complex tasks simultaneously
- ALWAYS complete one task fully before starting the next
- Each chat/script should have ONE clear objective
- Wait for explicit user confirmation before proceeding to next step

**Task Sizing**
- Break large tasks (>2 hours) into smaller chunks (30 min - 1 hour each)
- Each chunk should have a single, testable deliverable
- Complete in under 1 hour when possible
- Not depend on incomplete parallel work

**Synthetic Data First**
- For demonstration/portfolio projects, ALWAYS prefer synthetic/sample data
- Default to 10K-100K records for rapid iteration
- Only use large datasets (>1M records) if explicitly requested
- Optimize for development speed over scale

**Quick vs Full Mode**
- **Quick Mode (Default):** 10K-100K samples, <15 min training, full feature set
- **Full Mode (Optional):** 1M+ samples, 1-4 hour runtime, only if explicitly requested

**No Parallel Long-Running Tasks**
- ❌ NEVER suggest running multiple 30+ minute tasks simultaneously
- ✅ ALWAYS suggest sequential execution with checkpoints

**File Conflict Prevention**
- NEVER modify the same file from multiple processes/sessions
- Check if files are being written by other processes before editing
- Use sequential execution for shared resources

**Ask Before Assuming**
If uncertain about task duration, user's time availability, or quick vs full mode:
**ALWAYS ASK:** "Would you prefer [quick option] or [full option]?"
**DON'T ASSUME:** User wants the longest, most complex version

### ⚠️ Rule: Sequential Execution Only

**Never Suggest Parallel Tasks**

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

**Detection Pattern:**
If user says:
- "Can I run X and Y at the same time?"
- "Should I run this while that's running?"
- "Can I start the next thing?"

**ALWAYS respond with:**
```
⚠️  I recommend waiting for [current task] to complete first.

REASON: [Specific conflict or risk]

SAFE APPROACH:
1. Finish current task
2. Verify success
3. Then start next task

This prevents [specific problem] and ensures clean results.
```

**Exception: Independent Tasks Only**
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

See `.cursorrules` for complete Guardian Fraud Detection System rules (lines 559-836).

---

## 📋 Sprint Template

Every sprint must follow the structured template in `.cursor/prompts/SPRINT_TEMPLATE.md`:

### Key Elements
- **Prerequisites:** Previous sprint verified, git clean, dependencies installed
- **Objective:** One clear sentence
- **Deliverables:** Files to create/modify with paths
- **Implementation Steps:** Step-by-step with test commands and expected output
- **Success Criteria:** Clear checklist
- **STOP Marker:** Do not proceed until all criteria met

### Usage
Before starting any sprint:
1. Copy `SPRINT_TEMPLATE.md` structure
2. Fill in prerequisites checklist
3. Define clear objective (one sentence)
4. List deliverables
5. Add implementation steps with tests
6. Define success criteria
7. Add STOP marker

This ensures sequential execution and proper verification.

---
*Add to Cursor rules with: `.cursorrules` includes this file as a reference*  
*Sprint template: `SPRINT_TEMPLATE.md`*


