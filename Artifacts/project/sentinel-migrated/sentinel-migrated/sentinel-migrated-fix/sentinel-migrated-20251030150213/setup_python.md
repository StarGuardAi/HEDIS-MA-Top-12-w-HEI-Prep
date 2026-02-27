# Python Setup Guide for Criminal Intelligence Database GSD Prediction Engine

## Current Status
Python stub executables found but not properly installed.

## Recommended Setup: Install Python from Python.org

### Step 1: Download Python
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12 (latest stable version)
3. Run the installer

### Step 2: Installation Settings (CRITICAL)
✅ **CHECK "Add Python to PATH"** - This is essential!
✅ Select "Install for all users" (recommended)
✅ Select "Install pip"
✅ Select "Add Python to environment variables"

### Step 3: Verify Installation
Open a NEW PowerShell window and run:
```powershell
python --version
pip --version
```

You should see version numbers like:
```
Python 3.11.x
pip 23.x.x
```

### Step 4: Install Project Dependencies
```powershell
cd C:\Users\reich\Projects\hedis-gsd-prediction-engine
pip install -r requirements.txt
```

## Alternative: Anaconda/Miniconda (Data Science Focused)

### If you prefer Anaconda:
1. Download from https://www.anaconda.com/download
2. Install Anaconda
3. Open Anaconda Prompt
4. Navigate to project:
   ```
   cd C:\Users\reich\Projects\hedis-gsd-prediction-engine
   ```
5. Create environment:
   ```
   conda create -n hedis-gsd python=3.11
   conda activate hedis-gsd
   pip install -r requirements.txt
   ```

## Quick Fix: Remove Microsoft Store Stub

To prevent confusion, disable the Microsoft Store stub:
1. Open Windows Settings
2. Go to Apps > Advanced app settings > App execution aliases
3. Turn OFF "App Installer" for python.exe and python3.exe

## After Python Installation

### Run Milestone Tracker
```powershell
python milestone_tracker.py
```

### Run Portfolio Optimizer
```powershell
python scripts/canva_portfolio_optimizer.py
```

### Run Verification Scripts
```powershell
python scripts/verify-success-criteria.py
python scripts/verify-testing.py
python scripts/verify-iteration.py
```

## Troubleshooting

### If "python" still not found after installation:
1. Close ALL PowerShell/Command Prompt windows
2. Open a NEW PowerShell window
3. Try again

### If PATH not set correctly:
Add Python to PATH manually:
1. Search "Environment Variables" in Windows
2. Edit "Path" in System Variables
3. Add: `C:\Python311\` and `C:\Python311\Scripts\`
4. Click OK and restart PowerShell

### Verify Python Location
```powershell
where.exe python
```

Should show something like:
```
C:\Python311\python.exe
```

## Next Steps After Python Setup

1. ✅ Install Python with PATH enabled
2. ✅ Verify installation
3. ✅ Install project dependencies
4. ✅ Run milestone tracker
5. ✅ Update Canva portfolio with milestone progress
6. ✅ Run verification scripts

## Quick Start Commands (After Setup)

```powershell
# Navigate to project
cd C:\Users\reich\Projects\hedis-gsd-prediction-engine

# Install dependencies
pip install -r requirements.txt

# Run milestone tracker
python milestone_tracker.py

# Optimize Canva portfolio
python scripts/canva_portfolio_optimizer.py

# Update portfolio with milestone
python scripts/milestone_portfolio_updater.py

# Run verification checks
python scripts/verify-iteration.py
```

## Contact for Support
If you encounter issues, the setup scripts are ready to run once Python is installed correctly.


---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
