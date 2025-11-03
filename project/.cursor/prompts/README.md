# Cursor AI Prompts for HEDIS GSD Project

This directory contains prompts, shortcuts, and workflow guides optimized for healthcare ML development in Cursor AI.

## 📚 Available Resources

### 1. 🎯 Speed Shortcuts
**File:** `speed-shortcuts.md`  
**Purpose:** Complete guide to fast development workflows  
**Best For:** Learning all shortcuts and patterns

### 2. ⚡ Quick Reference Card
**File:** `QUICK_REFERENCE.md`  
**Purpose:** One-page cheat sheet for daily use  
**Best For:** Printing and keeping on your desk

### 3. 🖥️ Desk Quick Start
**File:** `DESK_QUICK_START.md`  
**Purpose:** Visual guide with copy-paste examples  
**Best For:** Quick lookup while coding

### 4. 🔧 Implementation Guide
**File:** `SHORTCUT_IMPLEMENTATION.md`  
**Purpose:** How the shortcuts actually work  
**Best For:** Understanding the mechanics, troubleshooting

### 5. 🏥 Code Review Commands
**File:** `code-review.md`  
**Purpose:** Detailed review command reference  
**Best For:** Understanding review types and when to use them

### 6. 🔗 Integration Guide
**File:** `integration-guide.md`  
**Purpose:** How to integrate everything into your workflow  
**Best For:** New team members, setting up the environment

### 7. 📋 Sprint Template
**File:** `SPRINT_TEMPLATE.md`  
**Purpose:** Structured template for all sprint documentation  
**Best For:** Creating new sprints with clear prerequisites, deliverables, and success criteria

## 🚀 Quick Start

### For New Users
1. Read `DESK_QUICK_START.md` first (5 min)
2. Try `/quick-review` on your next file
3. Use `QUICK_REFERENCE.md` as daily reference
4. Deep dive into `speed-shortcuts.md` when ready

### For Daily Development
1. Keep `QUICK_REFERENCE.md` open
2. Use `/quick-review [file]` after each file
3. Use `/safe-commit` before commits
4. Reference `code-review.md` for review types

### For Troubleshooting
1. Check `SHORTCUT_IMPLEMENTATION.md` for mechanics
2. Verify `.cursorrules` is properly configured
3. Review `integration-guide.md` for setup issues

## 🎯 The Main Commands

### Daily Use (The Big 3)
```
/quick-review [file]    → Fast security/HIPAA check (~12s)
/full-review [file]     → Comprehensive review (~28s)
/safe-commit            → PHI scan + review all (~45s)
```

### Fast vs Deep
```
FAST - [question]       → Sonnet 3.5, concise answer
DEEP - [question]       → Claude Sonnet 4.5, detailed analysis
```

### Targeted Fixes
```
Fix line 45: issue
Add docstring to calculate_age()
Review src/data/*.py security, failures only
```

## 📖 Reading Order

### Beginner Path
1. `DESK_QUICK_START.md` (5 min)
2. `QUICK_REFERENCE.md` (2 min)
3. Start using `/quick-review`
4. Read `speed-shortcuts.md` sections as needed

### Intermediate Path
1. Read `speed-shortcuts.md` fully (15 min)
2. Study `code-review.md` (10 min)
3. Practice all shortcuts for one week
4. Customize patterns to your workflow

### Advanced Path
1. Read `SHORTCUT_IMPLEMENTATION.md` (10 min)
2. Read `integration-guide.md` fully (20 min)
3. Create custom shortcuts
4. Integrate with CI/CD pipelines

## 🔗 Integration

These prompts work together with:
- `.cursorrules` - Main workflow rules (auto-loaded)
- `Plan.md` - Development roadmap
- `tasks/todo.md` - Current sprint tasks
- `docs/healthcare-glossary.md` - Domain terminology
- `scripts/hipaa-scanner.py` - PHI detector
- `scripts/pre-commit-checks.sh` - Final validation

## 🛡️ Guardian Fraud Detection System Rules

### Core Principles (Apply to All Projects)
These rules from the Guardian Fraud Detection System apply to all Cursor AI chats:

**Sequential Execution Only**
- NEVER suggest running multiple complex tasks simultaneously
- ALWAYS complete one task fully before starting the next
- Each chat/script should have ONE clear objective
- Wait for explicit user confirmation before proceeding

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

## 🆘 Quick Help

### "Which file should I read?"
- **Daily reference:** `QUICK_REFERENCE.md`
- **Learning shortcuts:** `speed-shortcuts.md`
- **Copy-paste examples:** `DESK_QUICK_START.md`
- **Troubleshooting:** `SHORTCUT_IMPLEMENTATION.md`
- **Starting a sprint:** `SPRINT_TEMPLATE.md`

### "How do I use this?"
Type the patterns naturally in Cursor chat. They're not built-in commands, they're prompt templates that guide Cursor AI's behavior.

### "Where's the .cursorrules file?"
It's in `project/.cursorrules` (project root, not in this prompts directory).

### "Nothing is working!"
1. Check `.cursorrules` exists and is loaded
2. Verify you're typing full prompts (not just `/quick-review`)
3. Read `SHORTCUT_IMPLEMENTATION.md` troubleshooting section

## 📝 Contributing

Have a better shortcut idea? Add it to `speed-shortcuts.md` under "Customizable Shortcuts" section.

Found a pattern that saves time? Add it to `SHORTCUT_IMPLEMENTATION.md` examples.

## 🔄 Updates

Last updated: 2025-01-27  
Cursor AI version: Latest  
Tested on: HEDIS GSD Prediction Engine

## 📧 Support

See main project README.md for project structure and setup.

For Cursor AI specific questions, check:
- Cursor docs: https://cursor.sh/docs
- GitHub issues: [your repo]/issues

---

**Remember:** These shortcuts are about **speed through specificity**. The more specific you are in your prompts, the faster Cursor AI can help you.

**Start with:** `DESK_QUICK_START.md` → Then use `QUICK_REFERENCE.md` daily → Deep dive as needed.


