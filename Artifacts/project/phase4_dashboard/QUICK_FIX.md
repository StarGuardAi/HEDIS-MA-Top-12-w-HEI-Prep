# 🚨 QUICK FIX: ModuleNotFoundError

## The Error You're Seeing

```
ModuleNotFoundError: No module named 'streamlit_extras'
```

## ✅ Solution: Install Missing Package

### Option 1: Quick Install (Recommended)

Open PowerShell and run:

```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
python -m pip install streamlit-extras
```

### Option 2: Install All Dependencies

```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
python -m pip install -r requirements.txt
```

### Option 3: Use Batch Script

Double-click: `INSTALL_DEPENDENCIES.bat`

## 🔄 After Installing

1. **Restart the Streamlit server:**
   - Stop current server (Ctrl+C in terminal)
   - Start again: `streamlit run app.py`

2. **Refresh browser:**
   - Go to: http://localhost:8502
   - Should work now!

## ✅ Verification

Check if installed:

```powershell
python -c "import streamlit_extras.metric_cards; print('SUCCESS!')"
```

If you see "SUCCESS!", the package is installed correctly.

## 🎯 Complete Fix Sequence

```powershell
# 1. Navigate to folder
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard

# 2. Install package
python -m pip install streamlit-extras

# 3. Verify installation
python -c "import streamlit_extras.metric_cards; print('OK')"

# 4. Start server
streamlit run app.py

# 5. Open browser to http://localhost:8501
```

## ⚠️ Note

I've updated the code to handle missing `streamlit-extras` gracefully, but it's better to install it for full functionality.

---

**After installing, restart the Streamlit server for changes to take effect!**

