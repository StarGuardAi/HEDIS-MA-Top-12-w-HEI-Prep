# GitHub Repository Setup Guide

## Quick Start

This guide will help you create and push the Intelligence-Security repositories to GitHub.

## Prerequisites

1. ✅ GitHub organization exists: `reichert-sentinel-ai`
2. ✅ Local repositories exist with git remotes configured
3. ✅ You have push access to the organization

## Step-by-Step Instructions

### Option 1: Automated Script (Recommended)

1. **Check repository status**:
   ```powershell
   .\push-intelligence-security-repos.ps1 -CheckOnly
   ```

2. **Create GitHub repositories** (if needed):
   - Follow the instructions provided by the script
   - Or use the manual steps below

3. **Push repositories**:
   ```powershell
   .\push-intelligence-security-repos.ps1
   ```

### Option 2: Manual Setup

#### Step 1: Create GitHub Repositories

For each repository (cipher, foresight, guardian):

1. Go to: https://github.com/organizations/reichert-sentinel-ai/repositories/new

2. **Repository Settings**:
   - **Repository name**: 
     - `cipher-threat-tracker`
     - `foresight-crime-prediction`
     - `guardian-fraud-analytics`
   - **Visibility**: ✅ **Public** (so external visitors can access)
   - **Initialize repository**: ❌ **Leave unchecked** (we'll push existing code)
   - **Add .gitignore**: ❌ Leave as None
   - **Choose a license**: Optional (MIT recommended)

3. Click **"Create repository"**

#### Step 2: Push Local Code

For each repository:

```powershell
# Navigate to repository
cd "C:\Users\reich\Projects\intelligence-security\repos\cipher"

# Verify remote
git remote -v

# Check current branch
git branch --show-current

# Push to GitHub (replace 'main' with your branch name if different)
git push -u origin main
```

Repeat for:
- `foresight`
- `guardian`

#### Step 3: Verify

Check that repositories are accessible:
- https://github.com/reichert-sentinel-ai/cipher-threat-tracker
- https://github.com/reichert-sentinel-ai/foresight-crime-prediction
- https://github.com/reichert-sentinel-ai/guardian-fraud-analytics

## Troubleshooting

### Issue: "Repository not found" when pushing

**Solution**: Make sure you've created the repository on GitHub first (Step 1).

### Issue: "Permission denied"

**Solution**: 
1. Verify you have push access to the organization
2. Check your GitHub authentication: `gh auth status`
3. If using HTTPS, you may need a Personal Access Token

### Issue: "Remote origin already exists"

**Solution**: This is normal. The remote is already configured. Just push:
```powershell
git push -u origin main
```

### Issue: Uncommitted changes

**Solution**: Commit changes before pushing:
```powershell
git add .
git commit -m "Update before pushing to GitHub"
git push -u origin main
```

## What to Verify After Pushing

✅ Repositories are public and accessible  
✅ README.md files are visible  
✅ Code is pushed correctly  
✅ Links in documentation work  
✅ External visitors can access repositories  

## Next Steps

After repositories are published:

1. ✅ Verify all documentation links work
2. ✅ Test repository accessibility from external browsers
3. ✅ Update any broken links in documentation
4. ✅ Consider adding repository descriptions and topics
5. ✅ Enable GitHub Pages if needed for documentation

## Quick Commands Reference

```powershell
# Check repository status
.\push-intelligence-security-repos.ps1 -CheckOnly

# Dry run (see what would happen)
.\push-intelligence-security-repos.ps1 -DryRun

# Push repositories (interactive)
.\push-intelligence-security-repos.ps1

# Manual push (for one repository)
cd "C:\Users\reich\Projects\intelligence-security\repos\cipher"
git push -u origin main
```

---

**Need Help?** Check the testing results in `INTELLIGENCE_SECURITY_TEST_RESULTS.md`

