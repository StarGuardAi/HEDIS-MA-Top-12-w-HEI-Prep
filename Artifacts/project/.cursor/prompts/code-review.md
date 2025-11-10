# Healthcare Code Review Commands for Cursor

Use these review prompts after completing a file/module. Run them in Cursor chat by pasting the command and specifying the file path.

## Quick Reference
| Command | Purpose | Target Files |
|---|---|---|
| /review-security [file] | Check PHI exposure, secrets, injections | Python, SQL, API |
| /review-hipaa [file] | HIPAA compliance and PHI handling | Data processing, APIs |
| /review-performance [file] | Performance for large datasets | ETL, queries, data pipelines |
| /review-data-quality [file] | Schema, nulls, outliers, types | Feature engineering |
| /review-model-code [file] | Leakage, validation, bias | ML training/eval |
| /review-clinical-logic [file] | HEDIS specs, ICD-10 logic | Features, business rules |
| /review-sql [file] | SQL correctness and optimization | SQL files |

## How to Use
1. Select the code or specify a filename.
2. Paste one or more commands in Cursor chat.
3. Fix any findings and rerun until PASS.

## Example
```
/review-security src/data/feature_engineering.py
/review-hipaa src/data/feature_engineering.py
/review-clinical-logic src/data/feature_engineering.py
/review-performance src/data/feature_engineering.py
```

## Notes
- Never log raw identifiers (member_id, name, DOB). Hash when necessary.
- Validate age using HEDIS measurement year end (Dec 31).
- Avoid iterrows(); prefer vectorization.
- Document clinical assumptions with citations to HEDIS Volume 2.

---

## 🛡️ Guardian Fraud Detection System Rules

### Core Principles (Apply to All Projects)

When using code reviews, also follow these Guardian rules:

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
- **Quick Mode (Default):** 10K-100K samples, <15 min training, full feature set
- **Full Mode (Optional):** 1M+ samples, 1-4 hour runtime, only if explicitly requested

See `.cursorrules` for complete Guardian Fraud Detection System rules.

---

## ⚠️ Rule: Sequential Execution Only

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

---

## 📋 Sprint Template

When using code reviews in sprints, follow the sprint template structure:

### Sprint Integration
- **Prerequisites:** Verify previous sprint, check git status, ensure dependencies installed
- **Implementation Steps:** Add code reviews after each file creation/modification
- **Success Criteria:** All code reviews must pass before marking sprint complete
- **STOP Marker:** Do not proceed to next sprint until all reviews pass

### Using Reviews in Sprints
1. After each file/module: Run appropriate code reviews (`/review-security`, `/review-hipaa`, etc.)
2. Before marking success criteria: Run `/safe-commit` to verify all reviews pass
3. Document review results in sprint deliverables section

**Template Location:** `.cursor/prompts/SPRINT_TEMPLATE.md`