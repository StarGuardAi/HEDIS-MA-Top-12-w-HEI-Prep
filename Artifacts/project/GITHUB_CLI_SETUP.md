# GitHub CLI Setup for Milestone Automation

## 🎯 Goal
Enable automated posting of Milestones 1, 2, and 3 to GitHub

---

## 📋 Step-by-Step Setup

### **Option A: If GitHub CLI is Already Installed**

1. **Find the installation location:**
   - Check: `C:\Program Files\GitHub CLI\`
   - Or: `C:\Program Files (x86)\GitHub CLI\`
   - Or search: Windows Start → "gh" → Right-click → "Open file location"

2. **Add to PATH:**
   ```powershell
   # Replace with your actual GitHub CLI path
   $ghPath = "C:\Program Files\GitHub CLI\bin"
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$ghPath", "User")
   ```

3. **Restart PowerShell** (close and reopen)

4. **Verify installation:**
   ```powershell
   gh --version
   ```

---

### **Option B: Fresh Installation (Recommended)**

1. **Download GitHub CLI:**
   - Visit: https://cli.github.com/
   - Download Windows installer (.msi)
   - Run installer (it will automatically add to PATH)

2. **Verify installation:**
   ```powershell
   gh --version
   # Should show: gh version 2.x.x
   ```

---

## 🔐 Step 2: Authenticate GitHub CLI

Once `gh` is in your PATH:

```powershell
# Authenticate with GitHub
gh auth login
```

**Follow the prompts:**
1. Choose: **GitHub.com**
2. Protocol: **HTTPS**
3. Authentication: **Login with a web browser** (easiest)
4. Copy the one-time code shown
5. Press Enter to open browser
6. Paste code and authorize

**Verify authentication:**
```powershell
gh auth status
```

---

## 🚀 Step 3: Enable Automation for Milestones 1, 2, 3

### **Quick Start - Publish All Milestones**

```batch
# Publish Milestone 1
publish_github.bat
> Enter milestone number: 1

# Publish Milestone 2
publish_github.bat
> Enter milestone number: 2

# Publish Milestone 3 (when completed)
publish_github.bat
> Enter milestone number: 3
```

### **Or Use Master Script (All Platforms)**

```batch
# Publishes to GitHub + generates LinkedIn content + creates resume
publish_all.bat
> Enter milestone number: 1
```

---

## 📋 What the Automation Does

### **For Each Milestone:**

1. ✅ **Updates README.md**
   - Adds milestone status badges
   - Updates completion dates
   - Shows deliverables

2. ✅ **Creates GitHub Release**
   - Tag: `v1.0.0`, `v2.0.0`, `v3.0.0`
   - Title: "Milestone 1: Foundation & Data Pipeline"
   - Release notes with:
     - Technical details
     - Performance metrics
     - Success criteria

3. ✅ **Commits Changes**
   - Professional commit messages
   - Ready to push

4. ✅ **Updates Milestone Tracker**
   - Sets publishing status to "published"
   - Updates timestamps in `milestones.json`

---

## 🎯 Complete Workflow Example

### **Publishing Milestone 1:**

```powershell
# Step 1: Run automation
publish_github.bat
> Enter milestone number: 1

# Output:
# ✅ Badges added to README.md
# ✅ README.md updated with milestone status
# ✅ GitHub release created: v1.0.0
# ✅ Changes committed: "docs: Update for Milestone 1"

# Step 2: Push to GitHub
git push origin main

# Step 3: Verify on GitHub
# - Check: https://github.com/YOUR_USERNAME/hedis-gsd-prediction-engine/releases
# - Should see: "v1.0.0 - Milestone 1: Foundation & Data Pipeline"
```

---

## 🔍 Testing Before Publishing

### **Dry Run (See What Would Happen)**

```powershell
# Test without making changes
python scripts/publish_to_github.py --milestone 1 --all --dry-run
```

### **Manual Control (Step-by-Step)**

```powershell
# 1. Just update README
python scripts/publish_to_github.py --milestone 1 --update-readme

# 2. Add badges
python scripts/publish_to_github.py --milestone 1 --add-badges

# 3. Create release (requires gh CLI)
python scripts/publish_to_github.py --milestone 1 --create-release

# 4. Commit changes
python scripts/publish_to_github.py --milestone 1 --commit
```

---

## ✅ Success Checklist

Before publishing each milestone, verify:

- [ ] GitHub CLI is installed and in PATH
- [ ] GitHub CLI is authenticated (`gh auth status`)
- [ ] Milestone is marked as "completed" in `milestones.json`
- [ ] You're in the project directory
- [ ] You have permissions to create releases on the repo

---

## 🎨 What Gets Published

### **Milestone 1: Foundation & Data Pipeline**
- **Tag:** v1.0.0
- **Highlights:**
  - 150,000+ claims processed
  - 24,935 diabetic members
  - 25+ HEDIS-compliant features
  - 100% HIPAA compliant
  - 91% AUC-ROC achieved

### **Milestone 2: Model Development & Validation**
- **Tag:** v2.0.0
- **Highlights:**
  - AUC-ROC: 0.91
  - Sensitivity: 0.87
  - SHAP analysis implemented
  - Temporal validation complete
  - Bias analysis across demographics

### **Milestone 3: API Development & Testing**
- **Tag:** v3.0.0
- **To be published when completed**
- **Highlights:**
  - FastAPI application
  - REST endpoints
  - API documentation
  - Integration tests

---

## 🚨 Troubleshooting

### **Issue: "gh not recognized"**
**Solution:** Add GitHub CLI to PATH (see Option A or B above)

### **Issue: "gh auth login failed"**
**Solution:** 
1. Try: `gh auth logout`
2. Then: `gh auth login` (choose web browser method)

### **Issue: "Release already exists"**
**Solution:** 
- Releases are created only once per milestone
- To update: Delete release on GitHub, then re-run

### **Issue: "No milestone data found"**
**Solution:** 
- Check `milestones.json` exists
- Verify milestone ID is valid (1-6)
- Ensure milestone status is "completed"

---

## 📞 Quick Reference

### **Commands:**
```powershell
# Check GitHub CLI
gh --version
gh auth status

# Publish milestone
publish_github.bat
publish_all.bat

# Dry run
python scripts/publish_to_github.py --milestone 1 --all --dry-run

# Push to GitHub
git push origin main
```

### **Files Modified:**
- `README.md` (badges, milestone status)
- `milestones.json` (publishing status)
- `reports/release_notes_milestone_X.md` (release notes)

### **GitHub Releases Created:**
- v1.0.0 - Milestone 1
- v2.0.0 - Milestone 2
- v3.0.0 - Milestone 3 (when completed)

---

## ✨ Next Steps

1. **Complete GitHub CLI setup** (follow Option A or B)
2. **Authenticate:** `gh auth login`
3. **Test dry run:** `python scripts/publish_to_github.py --milestone 1 --all --dry-run`
4. **Publish Milestone 1:** `publish_github.bat` → Enter `1`
5. **Publish Milestone 2:** `publish_github.bat` → Enter `2`
6. **Push to GitHub:** `git push origin main`
7. **Verify releases:** Check GitHub repository releases page

---

**Time to Complete:** 5-10 minutes  
**One-time Setup:** GitHub CLI installation + authentication  
**Per Milestone:** 2 minutes (automated)

**Ready to automate your milestone publishing!** 🚀

