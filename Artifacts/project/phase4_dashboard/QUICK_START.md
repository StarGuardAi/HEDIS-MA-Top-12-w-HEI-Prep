# Quick Start Guide

## Easiest Way: Double-Click Batch File

Simply double-click `run_app.bat` in the `phase4_dashboard` folder. This will:
- Activate the conda environment (hedis_py311)
- Start the Streamlit app
- Keep the window open when done

---

## For Future Sessions (Manual Method)

Every time you want to work on this app:

### 1. Open Anaconda Prompt (not regular PowerShell)

### 2. Activate environment:
```bash
conda activate hedis_py311
```

### 3. Navigate to project:
```bash
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
```

### 4. Run app:
```bash
streamlit run app.py
```

---

## Alternative: Using Current Python 3.13 Setup

If you haven't installed conda yet, you can use your current Python 3.13.9 setup:

### Navigate to project:
```bash
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
```

### Run app:
```bash
streamlit run app.py
```

---

## Notes

- **Conda Environment**: Requires Anaconda or Miniconda to be installed first
- **Python 3.13**: Current setup works with Python 3.13.9 and includes compatibility fixes
- **Streamlit Version**: 1.39.0 (installed and working)
