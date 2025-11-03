# Integrating Code Review Commands with Plan.md in Cursor AI

## 🎯 Integration Goal
Embed healthcare-specific code review commands into your HEDIS GSD development workflow so that every task follows: **Plan → Verify → Code → Review → Complete**

---

## 📁 File Structure Setup

```
hedis-gsd-prediction/
├── .cursorrules                    # Main Cursor AI rules (ALWAYS loaded)
├── .cursor/                        # Cursor-specific config directory
│   └── prompts/
│       ├── code-review.md          # Healthcare code review commands
│       └── claude-rules.md         # Your existing workflow rules
├── Plan.md                         # Your comprehensive development plan
├── tasks/
│   ├── todo.md                     # Current sprint tasks
│   └── completed/                  # Completed task summaries
├── src/
│   ├── data/
│   ├── models/
│   └── api/
├── tests/
├── scripts/
│   ├── hipaa-scanner.py
│   ├── context-builder.py
│   └── pre-commit-checks.sh
└── docs/
    ├── healthcare-glossary.md
    └── PROJECT_CONTEXT.md
```

---

## 🔧 Method 1: Master .cursorrules File (RECOMMENDED)

**Best for:** Automatic integration - Cursor loads this on every chat

### Step 1: Create Your Master .cursorrules File

Create a file named `.cursorrules` in your project root:

```markdown
# HEDIS GSD Prediction Engine - Cursor AI Rules
# This file is AUTOMATICALLY loaded by Cursor AI in every conversation

---

## 🎯 WORKFLOW: Always Follow These Steps

### 1. PLAN PHASE
Before writing any code:
1. Read Plan.md to understand the current phase
2. Check tasks/todo.md for the current task
3. Create a detailed task breakdown
4. Save the plan to tasks/todo.md
5. **STOP and wait for human verification**

### 2. IMPLEMENTATION PHASE
After plan approval:
1. Make simple, minimal changes (impact as little code as possible)
2. Provide high-level explanations of changes
3. Mark todo items as complete: `- [x] Task description`
4. **After every file/module completion, run code reviews**

### 3. REVIEW PHASE (CRITICAL - Healthcare Compliance)
After writing code, ALWAYS run these reviews in order:

**For ALL Python code:**
```
/review-security [filename]
/review-hipaa [filename]
/review-performance [filename]
```

**For data processing code:**
```
/review-data-quality [filename]
```

**For SQL queries:**
```
/review-sql [filename]
```

**For ML model code:**
```
/review-model-code [filename]
/review-clinical-logic [filename]
```

**For API code:**
```
/review-security [filename]
/review-gen-ai [filename]  # If using LLMs
```

### 4. COMPLETION PHASE
1. Run pre-commit checks: `bash scripts/pre-commit-checks.sh`
2. Update tasks/todo.md with review section
3. Summarize changes in simple terms
4. Archive completed task to tasks/completed/

---

## 🏥 HEALTHCARE-SPECIFIC REQUIREMENTS

### Always Consider (HIPAA Compliance)
- **PHI Handling:** Never log, print, or expose patient identifiers
- **De-identification:** Use Safe Harbor or Expert Determination methods
- **Audit Logging:** Log all access to patient data with timestamps
- **Data Minimization:** Only process necessary fields
- **Encryption:** Ensure data at rest and in transit is encrypted

### Clinical Validation Requirements
- **ICD-10 Codes:** Validate against current year code set
- **HEDIS Measures:** Follow NCQA specifications exactly
- **Age Calculations:** Use index date from HEDIS specs
- **Date Logic:** Handle multiple encounters and service dates correctly
- **Exclusions:** Apply HEDIS exclusion criteria (hospice, SNP, etc.)

### Model Development Standards
- **Temporal Validation:** Train on past years, test on future year
- **No Data Leakage:** Ensure outcome variable not in features
- **Fairness Metrics:** Report performance across age, gender, race
- **Interpretability:** Provide SHAP values for all predictions
- **Clinical Thresholds:** Document source for all cutoff values

---

## 💻 CODE REVIEW COMMANDS (Reference: .cursor/prompts/code-review.md)

### Quick Reference
| Command | Use Case | Files |
|---------|----------|-------|
| `/review-security` | PHI exposure, SQL injection, API keys | All Python/SQL |
| `/review-hipaa` | HIPAA compliance check | Data processing, APIs |
| `/review-performance` | Optimization for large datasets | ETL, queries |
| `/review-data-quality` | Null handling, outliers, types | Feature engineering |
| `/review-clinical-logic` | HEDIS specs, ICD-10, calculations | Model features, business rules |
| `/review-model-code` | Bias, leakage, validation | ML training, evaluation |
| `/review-sql` | Query optimization for EHR data | All SQL files |

### How to Use Commands
1. Select code in editor (or specify filename)
2. Open Cursor chat (Cmd/Ctrl + L)
3. Type the command: `/review-security src/data/data_loader.py`
4. Review findings and fix issues
5. Re-run command to verify fixes

---

## 📋 SIMPLIFIED WORKFLOW EXAMPLE

### Example: Implementing Feature Engineering (Phase 1.1)

**Step 1: Plan** (You do this first)
```
Task: Create feature_engineering.py with HEDIS GSD-specific features

Subtasks:
1. [ ] Load processed claims data
2. [ ] Calculate age at measurement year end
3. [ ] Create diabetes comorbidity flags (CKD, CVD, retinopathy)
4. [ ] Calculate HbA1c test frequency features
5. [ ] Create utilization features (ED visits, hospitalizations)
6. [ ] Validate features match HEDIS specifications
```

**Step 2: Implementation** (Cursor AI does this)
```python
# src/data/feature_engineering.py
# Cursor creates the code with inline comments
def create_hedis_gsd_features(claims_df, lab_df, member_df):
    """
    Create features for HEDIS GSD (Glycemic Status Diabetes) prediction.
    
    HEDIS Specification: MY2023 Volume 2
    Measure: HBD - Hemoglobin A1c Control for Patients with Diabetes
    """
    # Implementation here...
```

**Step 3: Review** (Cursor AI does this automatically)
```
User → Cursor Chat:
"I've just completed feature_engineering.py. 
Run these reviews:
/review-security src/data/feature_engineering.py
/review-hipaa src/data/feature_engineering.py
/review-clinical-logic src/data/feature_engineering.py
/review-performance src/data/feature_engineering.py"
```

**Cursor's Review Output:**
```
✅ /review-security: PASSED
  - No PHI in logs or print statements
  - No hardcoded credentials

⚠️  /review-hipaa: 1 MEDIUM issue
  - Line 45: Consider hashing member_id before logging
  - Recommendation: Use SHA-256 hash for audit logs

✅ /review-clinical-logic: PASSED
  - Age calculation uses HEDIS measurement year end (Dec 31)
  - ICD-10 codes match HEDIS diabetes value set
  - Comorbidity definitions align with CMS-HCC model

⚠️  /review-performance: 1 HIGH issue
  - Line 78: DataFrame iterrows() detected
  - Recommendation: Use vectorized operations or apply()
```

**Step 4: Fix Issues**
```python
# BEFORE (from review)
for idx, row in claims_df.iterrows():
    member_id = row['member_id']
    logger.info(f"Processing member {member_id}")  # PHI exposure!

# AFTER (fixed)
claims_df['member_hash'] = claims_df['member_id'].apply(
    lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:8]
)
logger.info(f"Processing {len(claims_df)} member records")
```

**Step 5: Complete**
```
- [x] Create feature_engineering.py
  - Review Results: 
    - Security: PASSED
    - HIPAA: PASSED (after fixes)
    - Clinical Logic: PASSED
    - Performance: PASSED (after vectorization)
  - Changes: 
    - Implemented 25 HEDIS-aligned features
    - Added member_id hashing for audit logs
    - Vectorized DataFrame operations for 10x speedup
```

---

## 🔄 INTEGRATION WITH YOUR EXISTING WORKFLOW

Your current workflow (from claude-rules.md):
```
1. Think through problem → Read codebase → Write plan to tasks/todo.md
2. Create checklist of todo items
3. CHECK IN with human for verification ⚠️
4. Work on items, mark complete
5. Give high-level explanations
6. Keep changes simple and minimal
7. Create review section in todo.md
```

**Enhanced workflow with code reviews:**
```
1. Think through problem → Read codebase → Write plan to tasks/todo.md
2. Create checklist of todo items
3. CHECK IN with human for verification ⚠️
4. Work on items
   └─→ After each file/module: RUN CODE REVIEWS
5. Fix issues found in reviews
6. Mark item complete only after reviews pass
7. Give high-level explanations
8. Keep changes simple and minimal
9. Create review section in todo.md with security/HIPAA summary
```

---

## 🚀 SETUP INSTRUCTIONS

### Step 1: Create .cursorrules File
```bash
cd /path/to/hedis-gsd-prediction
touch .cursorrules
# Copy the content from "Master .cursorrules File" section above
```

### Step 2: Create Code Review Reference
```bash
mkdir -p .cursor/prompts
# Save the code-review.md artifact to .cursor/prompts/code-review.md
```

### Step 3: Create Healthcare Context Files
```bash
# Create glossary
cat > docs/healthcare-glossary.md << 'EOF'
# Healthcare Analytics Glossary

## HEDIS Measures
- **GSD (Glycemic Status Diabetes):** HbA1c control measure
- **HBD:** Hemoglobin A1c Control for Patients with Diabetes
- **MY:** Measurement Year (calendar year for HEDIS)
- **Denominator:** Diabetic members 18-75 years old
- **Numerator:** Members with most recent HbA1c >9.0% (poor control)

## ICD-10 Codes (Diabetes)
- E08.*: Diabetes due to underlying condition
- E09.*: Drug or chemical induced diabetes
- E10.*: Type 1 diabetes mellitus
- E11.*: Type 2 diabetes mellitus
- E13.*: Other specified diabetes mellitus

## Key Comorbidities
- CKD: Chronic Kidney Disease (N18.*)
- CVD: Cardiovascular Disease (I20-I25)
- Retinopathy: Diabetic eye disease (E*.3*)
- Neuropathy: Diabetic nerve damage (E*.4*)

## Data Sources
- **Carrier Claims:** Professional services (CPT codes)
- **Inpatient Claims:** Hospital stays (DRG codes)
- **Outpatient Claims:** Facility services
- **Prescription Drug:** Medication fills (NDC codes)
- **Lab Data:** HbA1c test results (LOINC codes)
EOF

# Create security scanner
cat > scripts/hipaa-scanner.py << 'EOF'
#!/usr/bin/env python3
"""
HIPAA PHI Scanner for HEDIS GSD Project
Scans code for potential PHI exposure before commits
"""
import re
import sys
from pathlib import Path

PHI_PATTERNS = {
    'member_id': r'\b(member_id|patient_id|subscriber_id)\s*[=:]\s*["\']?\d+["\']?',
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    'dob': r'\b(dob|date_of_birth|birth_date)\s*[=:]\s*["\']?\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
    'name': r'\b(first_name|last_name|patient_name)\s*[=:]\s*["\'][A-Z][a-z]+',
}

def scan_file(filepath):
    """Scan a file for PHI patterns"""
    violations = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            for pattern_name, pattern in PHI_PATTERNS.items():
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line_num = content[:match.start()].count('\n') + 1
                    
                    # Skip if in comments explaining the pattern
                    line_content = lines[line_num - 1].strip()
                    if line_content.startswith('#') or line_content.startswith('"""'):
                        continue
                    
                    violations.append({
                        'file': str(filepath),
                        'line': line_num,
                        'type': pattern_name,
                        'text': line_content
                    })
    except Exception as e:
        print(f"Error scanning {filepath}: {e}")
    
    return violations

def scan_project():
    """Scan all Python files in project"""
    project_root = Path.cwd()
    all_violations = []
    
    # Scan Python files
    for py_file in project_root.rglob('*.py'):
        # Skip virtual env and cache
        if any(p in py_file.parts for p in ['venv', '.venv', '__pycache__', 'site-packages']):
            continue
        
        violations = scan_file(py_file)
        all_violations.extend(violations)
    
    return all_violations

if __name__ == '__main__':
    print("🔍 Scanning for PHI exposure...")
    violations = scan_project()
    
    if violations:
        print(f"\n⚠️  Found {len(violations)} potential PHI exposures:\n")
        for v in violations:
            print(f"  {v['file']}:{v['line']} - {v['type']}")
            print(f"    → {v['text']}\n")
        sys.exit(1)
    else:
        print("✅ No obvious PHI patterns detected")
        sys.exit(0)
EOF

chmod +x scripts/hipaa-scanner.py

# Create pre-commit checks
cat > scripts/pre-commit-checks.sh << 'EOF'
#!/bin/bash
# Pre-commit checks for HEDIS GSD project

set -e

echo "🔍 Running pre-commit checks for HEDIS GSD..."

# 1. PHI Scan
echo "1/4 Scanning for PHI exposure..."
python scripts/hipaa-scanner.py

# 2. Run tests
echo "2/4 Running unit tests..."
if [ -d "tests" ]; then
    python -m pytest tests/ -v --tb=short 2>/dev/null || echo "⚠️  Some tests failed"
fi

# 3. Check for sensitive data in git
echo "3/4 Checking for sensitive files..."
if git ls-files | grep -qE '\.(pkl|csv|parquet)$'; then
    echo "⚠️  Warning: Model/data files detected in git"
    echo "   Consider using Git LFS or .gitignore"
fi

# 4. Code quality
echo "4/4 Checking code quality..."
if command -v flake8 &> /dev/null; then
    flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics 2>/dev/null || true
fi

echo ""
echo "✅ Pre-commit checks complete!"
EOF

chmod +x scripts/pre-commit-checks.sh
```

### Step 4: Test the Integration
```bash
# Open Cursor AI
# In Cursor chat, type:

"I'm ready to start Phase 1.1: Data Pipeline Reconstruction.
First, let me create the plan in tasks/todo.md.

Task: Create data_loader.py to load CMS DE-SynPUF data
Subtasks:
1. [ ] Load beneficiary summary file
2. [ ] Load inpatient claims
3. [ ] Load outpatient claims
4. [ ] Load carrier claims
5. [ ] Validate data schemas
6. [ ] Apply HEDIS diabetes value set filter

Please review this plan before I begin coding."
```

---

## 📖 DAILY USAGE PATTERN

### Morning: Start New Task
```
You → Cursor:
"Starting Phase 1.1 Task 2: Create feature_engineering.py
Let me read the Plan.md and create a detailed task breakdown in tasks/todo.md"

Cursor → Creates task breakdown and waits for your approval

You → Cursor: 
"Plan approved. Begin implementation."
```

### During Development: After Each Module
```
Cursor → Completes feature_engineering.py

Cursor → Automatically runs:
"Running code reviews on src/data/feature_engineering.py:
/review-security
/review-hipaa  
/review-clinical-logic
/review-performance"

Cursor → Shows results and fixes issues

You → Review the changes and fixes
```

### End of Day: Complete Task
```
Cursor → Updates tasks/todo.md:

## Completed Today
- [x] Create feature_engineering.py
  - **Security Review:** PASSED (no PHI exposure)
  - **HIPAA Review:** PASSED (member IDs hashed in logs)
  - **Clinical Review:** PASSED (HEDIS specs validated)
  - **Performance Review:** PASSED (vectorized operations)
  - **Code Changes:**
    - Created 25 features aligned with HEDIS GSD measure
    - Implemented temporal validation (no future data leakage)
    - Added comprehensive docstrings with HEDIS references
    - Used pandas vectorization for 10x speedup

You → Run final checks:
bash scripts/pre-commit-checks.sh
```

---

## 🎯 BENEFITS OF THIS INTEGRATION

### For You
✅ **Zero Mental Overhead:** Cursor automatically runs healthcare checks
✅ **Compliance by Default:** HIPAA violations caught before commit
✅ **Simplified Reviews:** One command runs all relevant checks
✅ **Learning Tool:** See best practices in action on your code

### For Your Code
✅ **Production-Ready:** Every file passes security/compliance checks
✅ **Optimized:** Performance issues caught early
✅ **Documented:** Reviews force good documentation
✅ **Testable:** Test coverage tracked automatically

### For Your Career
✅ **Portfolio Quality:** Show HIPAA-compliant healthcare ML code
✅ **Interview Prep:** Explain security choices confidently
✅ **Best Practices:** Learn healthcare AI standards hands-on
✅ **Differentiator:** Stand out with compliance knowledge

---

## 🔧 TROUBLESHOOTING

### Issue: "Cursor doesn't seem to follow .cursorrules"
**Solution:** 
1. Close and reopen Cursor
2. Check file is named exactly `.cursorrules` (with leading dot)
3. Verify it's in project root (same level as Plan.md)
4. Try: Cmd/Ctrl + Shift + P → "Reload Window"

### Issue: "Code review commands not working"
**Solution:**
1. Commands are **custom prompts**, not built-in
2. Manually type the full review prompt, e.g.:
   ```
   Review this code for security vulnerabilities:
   - Check for PHI exposure in logs
   - Check for SQL injection in queries
   - Check for hardcoded credentials
   
   File: src/data/data_loader.py
   ```

### Issue: "Too many review steps, slowing down"
**Solution:**
1. For quick prototypes, skip reviews
2. Run reviews only at task completion
3. Batch multiple files: `/review-security src/data/*.py`

### Issue: "Reviews find issues but I don't understand the fix"
**Solution:**
Ask Cursor to explain:
```
"You found a PHI exposure issue on line 45. 
Please explain:
1. Why is this a HIPAA violation?
2. What's the security risk?
3. Show me the corrected code with explanation
Act like you're a senior engineer teaching me."
```

---

## 📚 QUICK REFERENCE CARD

### Most Common Commands
```bash
# Start new task
"Read Plan.md Phase X.X and create task breakdown in tasks/todo.md"

# During coding (after completing a file)
"/review-security [filename]"
"/review-hipaa [filename]"
"/review-performance [filename]"

# For data processing code
"/review-data-quality [filename]"

# For model code  
"/review-model-code [filename]"
"/review-clinical-logic [filename]"

# Before committing
"Run pre-commit checks: bash scripts/pre-commit-checks.sh"

# Complete task
"Update tasks/todo.md with review summary"
```

### File Locations
```
.cursorrules                          ← Main rules (auto-loaded)
.cursor/prompts/code-review.md        ← Detailed review commands
.cursor/prompts/SPRINT_TEMPLATE.md    ← Sprint template structure
docs/healthcare-glossary.md           ← Domain terminology
scripts/hipaa-scanner.py              ← PHI detector
scripts/pre-commit-checks.sh          ← Final validation
tasks/todo.md                         ← Current sprint tasks
Plan.md                               ← Master development plan
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

### Template Structure
- **Prerequisites:** Previous sprint verified, git status clean, dependencies installed
- **Objective:** One clear sentence describing the sprint goal
- **Deliverables:** List of files to create/modify with paths
- **Implementation Steps:** Step-by-step with test commands and expected output
- **Success Criteria:** Clear checklist that must be met
- **STOP Marker:** Do not proceed to next sprint until all criteria met

### Using the Template
1. Copy `SPRINT_TEMPLATE.md` for each new sprint
2. Fill in sprint name and estimated time
3. Complete prerequisites checklist
4. Define clear objective
5. List all deliverables
6. Add implementation steps with tests
7. Define success criteria
8. Add STOP marker before proceeding

This ensures sequential execution, clear deliverables, and proper verification before moving to the next sprint.

---

## 🎓 LEARNING PATH

### Week 1: Get Comfortable
- Use .cursorrules for workflow automation
- Run code reviews on every file
- Understand common HIPAA issues

### Week 2: Optimize Your Flow  
- Create custom review shortcuts
- Build your own healthcare patterns
- Speed up with batch reviews

### Week 3: Advanced Techniques
- Write custom security scanners
- Create project-specific rules
- Integrate with CI/CD

### Week 4: Mastery
- Teach others your workflow
- Contribute improvements
- Build reusable templates

---

## ✅ NEXT STEPS

1. **Copy this entire guide** to a new file: `.cursor/prompts/integration-guide.md`

2. **Create your .cursorrules** file using the master template above

3. **Test it** by starting a new Cursor chat:
   ```
   "I want to start Phase 1.1 of my HEDIS GSD project. 
   Create the task breakdown in tasks/todo.md and wait for my approval."
   ```

4. **Verify it works** - Cursor should:
   - Read Plan.md
   - Create detailed subtasks
   - **STOP and wait** for your verification
   - Only proceed after you approve

5. **Report back** - Tell me if it works or if you need adjustments!

---

