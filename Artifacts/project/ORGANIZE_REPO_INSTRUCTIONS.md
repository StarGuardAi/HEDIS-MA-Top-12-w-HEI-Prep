# Organize Repository Files - Instructions

## Goal
Move all files to a subfolder except `README.md`, keeping the root directory clean.

## Option 1: PowerShell Script (Recommended)

### Step 1: Run the Script
```powershell
# Dry run first (preview changes)
.\organize-repo-files.ps1 -TargetFolder "project" -DryRun

# If preview looks good, run for real
.\organize-repo-files.ps1 -TargetFolder "project"
```

**Custom folder name:**
```powershell
.\organize-repo-files.ps1 -TargetFolder "hedis-portfolio"
```

### Step 2: Review Changes
```powershell
git status
```

### Step 3: Commit and Push
```powershell
git add .
git commit -m "Organize files: move all to project/"
git push origin main
```

---

## Option 2: Batch File (Simple)

```batch
.\organize-repo-files.bat
```

Then commit and push:
```batch
git add .
git commit -m "Organize files: move all to project/"
git push origin main
```

---

## Option 3: Manual Git Commands

If you prefer to do it manually with git:

### Create folder and move files
```powershell
# Create target folder
mkdir project

# Move all files except README.md and .git
# PowerShell
Get-ChildItem -Force | Where-Object { $_.Name -ne "README.md" -and $_.Name -ne ".git" } | Move-Item -Destination "project\"

# Or using git mv (preserves history better)
git mv alembic project/
git mv data project/
git mv docs project/
git mv src project/
git mv tests project/
# ... continue for all files/folders except README.md and .git
```

### Using git mv preserves file history better

---

## Folder Structure After Organization

```
HEDIS-MA-Top-12-w-HEI-Prep/
├── README.md          ← Visible at root
├── .git/             ← Git repository
├── project/          ← All other files moved here
│   ├── alembic/
│   ├── data/
│   ├── docs/
│   ├── src/
│   ├── tests/
│   ├── scripts/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── ... (all other files)
```

---

## Important Notes

1. **Preserves .git directory:** The `.git` folder stays at root (required)

2. **Keeps README.md visible:** README.md remains at root for GitHub visibility

3. **Preserves file history:** Using `git mv` preserves file history better than regular `move`

4. **Common folder names:**
   - `project/` - Generic
   - `hedis-portfolio/` - Descriptive
   - `src/` - If you want source code at root
   - `portfolio/` - Portfolio-specific

5. **GitHub Pages:** If using GitHub Pages, you may need to update settings if they point to root

---

## Verification

After moving files, verify:

1. **Root directory:**
   ```powershell
   Get-ChildItem -Force | Select-Object Name
   ```
   Should show: `.git`, `README.md`, `project/` (or your target folder)

2. **Target folder:**
   ```powershell
   Get-ChildItem project\ | Select-Object Name
   ```
   Should show all your files/folders

3. **Git status:**
   ```powershell
   git status
   ```
   Should show all files as renamed/moved

---

## Reverting Changes

If you need to undo:

```powershell
git reset --hard HEAD~1
```

Or manually move files back:
```powershell
Get-ChildItem project\ | Move-Item -Destination .
```

---

## Recommended Folder Name

Based on your repository, suggested folder names:
- `project/` - Simple and generic
- `hedis-portfolio/` - Descriptive of content
- `portfolio/` - Short and clear

