# Quick Stop & Start Streamlit Guide

## 🛑 How to Stop Streamlit

### Method 1: In Terminal Window (Easiest)
If you see the terminal where Streamlit is running:
- **Press `Ctrl + C`**
- Wait for "Shutting down..." message

### Method 2: Kill Process
Open PowerShell/Command Prompt and run:
```powershell
taskkill /F /IM streamlit.exe
```

### Method 3: Kill by Port (Most Reliable)
```powershell
netstat -ano | findstr :8502
# Note the PID number, then:
taskkill /F /PID <PID_NUMBER>
```

---

## 🚀 How to Start Streamlit

### Easiest: Double-Click Batch File
- **`restart_8502.bat`** - Stops and restarts on port 8502
- **`STOP_AND_RESTART.bat`** - Simple stop and restart

### Manual Start:
```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
streamlit run app.py --server.port 8502
```

---

## 📍 File Locations

All batch files are in:
```
C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard\
```

**Available batch files:**
- `restart_8502.bat` - Full restart with port checking
- `STOP_AND_RESTART.bat` - Simple stop/start
- `START_STREAMLIT_NOW.bat` - Just start (assumes nothing running)

---

## ⚡ Quick Reference

**Stop**: `Ctrl + C` in terminal OR `taskkill /F /IM streamlit.exe`  
**Start**: `streamlit run app.py --server.port 8502`  
**Easiest**: Double-click `restart_8502.bat`

---

## 🎯 After Restart

1. Wait 5-10 seconds
2. Open: http://localhost:8502
3. Hard refresh: `Ctrl + Shift + R`
4. Check sidebar - mobile pages should be gone!









