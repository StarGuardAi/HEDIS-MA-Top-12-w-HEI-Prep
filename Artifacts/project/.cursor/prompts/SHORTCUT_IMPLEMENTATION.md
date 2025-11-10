# Speed Shortcuts Implementation Guide

## What These Shortcuts Do

These shortcuts are **custom prompt patterns** that tell Cursor AI to:
1. Use specific models (fast vs deep)
2. Focus on specific review types
3. Target specific code sections
4. Batch operations efficiently

## Implementation Status

### ✅ Created Files
- ✅ `.cursor/prompts/speed-shortcuts.md` - Full guide with examples
- ✅ `.cursor/prompts/QUICK_REFERENCE.md` - One-page reference card
- ✅ `.cursor/prompts/SHORTCUT_IMPLEMENTATION.md` - This file
- ✅ Updated `.cursorrules` with shortcuts section

### ⚠️ How These Work (Important)

**These are NOT built-in Cursor commands.** They are **pattern templates** you type as natural prompts.

## Usage Examples

### Pattern: `/quick-review [file]`
**What you type:**
```
/quick-review src/data/feature_engineering.py

Run security and HIPAA reviews only, show failures:
- Check for PHI exposure
- Check for hardcoded credentials
- Check for SQL injection
- Check for proper logging (no member IDs)
- Show only failures and critical issues
```

**What it does:**
- Focuses on Security + HIPAA only
- Ignores detailed performance checks
- Shows only failures (not passing checks)
- Uses Sonnet 3.5 for speed (~12 seconds)

### Pattern: `/full-review [file]`
**What you type:**
```
/full-review src/data/feature_engineering.py

Run comprehensive code review:
- Security: PHI, credentials, SQL injection
- HIPAA: Compliance, de-identification, audit logging
- Performance: Vectorization, iterrows(), query optimization
- Clinical Logic: HEDIS specs, ICD-10 validation, age calculations
- Data Quality: Nulls, types, outliers
- Documentation: Docstrings, comments, healthcare context
```

**What it does:**
- Runs all review types
- Shows comprehensive report with all checks
- Uses Sonnet 3.5 (~28 seconds)

### Pattern: `/safe-commit`
**What you type:**
```
/safe-commit

Before committing, run PHI scanner and review all changed files:

1. Scan all Python files for PHI patterns (member_id, SSN, DOB, names)
2. For each changed file, run quick-review (security + HIPAA)
3. Provide summary of all issues found
4. List files ready to commit vs files needing fixes
```

**What it does:**
- Scans entire project for PHI patterns
- Reviews all modified files
- Provides commit readiness summary
- Takes ~45 seconds

### Pattern: `FAST - [question]`
**What you type:**
```
FAST - explain the calculate_age() function

Keep response concise, maximum 3 sentences.
Focus on what it does and why.
```

**What it does:**
- Explicitly uses Sonnet 3.5
- Forces brief, actionable responses
- Skips detailed explanations

### Pattern: `DEEP - [question]`
**What you type:**
```
DEEP - design a temporal validation strategy for HEDIS GSD prediction

Consider:
- Train/test split methodology for time-series healthcare data
- Handling of data drift in 5-year span
- Integration with HEDIS measurement year requirements
- Ensuring no data leakage from future to past
```

**What it does:**
- Uses Claude Sonnet 4.5 for deeper reasoning
- Provides comprehensive analysis
- Considers multiple angles and edge cases

## Integrating into Your Workflow

### Option 1: Use as Prompts (Recommended)
Simply type these patterns in Cursor chat when needed. No setup required.

### Option 2: Create Custom Snippets
In VS Code/Cursor, you can create code snippets for these patterns:

1. Open Cursor Settings
2. Search for "snippets"
3. Create Python JSON snippets file
4. Add snippet mappings:

```json
{
  "Quick Review": {
    "prefix": "qr",
    "body": [
      "/quick-review ${1:filename}",
      "",
      "Run security and HIPAA reviews only, show failures:",
      "- Check for PHI exposure",
      "- Check for hardcoded credentials", 
      "- Check for SQL injection",
      "- Check for proper logging (no member IDs)",
      "- Show only failures and critical issues"
    ]
  },
  "Full Review": {
    "prefix": "fr",
    "body": [
      "/full-review ${1:filename}",
      "",
      "Run comprehensive code review:",
      "- Security: PHI, credentials, SQL injection",
      "- HIPAA: Compliance, de-identification, audit logging",
      "- Performance: Vectorization, iterrows(), query optimization",
      "- Clinical Logic: HEDIS specs, ICD-10 validation, age calculations",
      "- Data Quality: Nulls, types, outliers",
      "- Documentation: Docstrings, comments, healthcare context"
    ]
  }
}
```

Then type `qr` or `fr` + Tab to expand.

### Option 3: Print Reference Card
Print `QUICK_REFERENCE.md` and keep it on your desk.

## Testing Your Shortcuts

### Test Quick Review
1. Create a test file with a PHI issue:
```python
# test_review.py
import logging

def process_member(member_id):
    logger.info(f"Processing member {member_id}")  # PHI exposure!
    return "done"
```
2. Run: `/quick-review test_review.py`
3. Should catch the PHI issue

### Test Full Review
1. Use the same test file
2. Run: `/full-review test_review.py`
3. Should catch PHI + provide performance suggestions

### Test Safe Commit
1. Make a change to a file
2. Run: `/safe-commit`
3. Should show commit readiness

## Troubleshooting

### "Command not recognized"
These aren't actual commands. Just type the full prompt pattern as natural language. Cursor AI understands the intent.

### "Doesn't follow the pattern"
Be explicit. Include "Run security and HIPAA reviews only" or "comprehensive code review" to guide behavior.

### "Still too slow"
- Use `FAST -` prefix explicitly
- Check you're loading minimal context
- Verify Sonnet 3.5 is selected in Cursor settings

### "Missing some reviews"
The shortcuts are focused. For everything, use `/full-review`.

## Next Steps

1. **Try one today:** Start with `/quick-review` on a recent file
2. **Add to your routine:** Use `/safe-commit` before git commits
3. **Customize:** Add your own patterns to `speed-shortcuts.md`
4. **Share:** These shortcuts work for any healthcare ML project

## Custom Shortcuts

Want to add your own? Pattern is:
```
/PATTERN-NAME [args]

[Explicit instructions for what to do]
[Include what to focus on]
[Include what to skip]
[Include model preference]
```

Example:
```
/phi-check [file]

Scan this file for PHI exposure only:
- Look for member_id, patient_id, subscriber_id in logs or prints
- Check for SSN patterns
- Check for DOB/date_of_birth in logs
- Show line numbers and suggested fixes
Use Sonnet 3.5 for speed.
```

## 🛡️ Guardian Fraud Detection System Rules

### Core Principles (Apply to All Projects)

When using shortcuts, also follow these Guardian rules:

**Sequential Execution Only**
- NEVER suggest running multiple complex tasks simultaneously
- ALWAYS complete one task fully before starting the next
- Each chat/script should have ONE clear objective
- Wait for explicit user confirmation before proceeding to next step

**Task Sizing**
- Break large tasks (>2 hours) into smaller chunks (30 min - 1 hour each)
- Each chunk should have a single, testable deliverable
- Complete in under 1 hour when possible

**Synthetic Data First**
- For demonstration/portfolio projects, ALWAYS prefer synthetic/sample data
- Default to 10K-100K records for rapid iteration
- Only use large datasets (>1M records) if explicitly requested

**Quick vs Full Mode**
- **Quick Mode (Default):** 10K-100K samples, <15 min training
- **Full Mode (Optional):** 1M+ samples, 1-4 hour runtime, only if explicitly requested

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
If user asks about parallel execution, ALWAYS recommend waiting and explain the specific conflict or risk.

**Exception: Independent Tasks Only**
- Only allow parallel execution if tasks use different files/resources and no shared state.

See `.cursorrules` for complete Guardian Fraud Detection System rules.

## 📋 Sprint Template

When using shortcuts in sprints, follow the sprint template structure:

### Sprint Template Elements
- **Prerequisites:** Verify previous sprint, check git status, ensure dependencies installed
- **Objective:** Define one clear sentence describing sprint goal
- **Deliverables:** List all files to create/modify with paths
- **Implementation Steps:** Add step-by-step instructions with test commands and expected output
- **Success Criteria:** Create clear checklist before proceeding
- **STOP Marker:** Do not proceed to next sprint until all criteria met

### Integration with Shortcuts
- Use `/quick-review` after each file in implementation steps
- Use `/safe-commit` before marking success criteria complete
- Use `FAST -` prefix for quick checks during implementation
- Use `DEEP -` prefix for complex design decisions in objective

**Template Location:** `.cursor/prompts/SPRINT_TEMPLATE.md`

## Questions?

See `speed-shortcuts.md` for full examples.
See `QUICK_REFERENCE.md` for one-page quick reference.
See `SPRINT_TEMPLATE.md` for sprint structure.


