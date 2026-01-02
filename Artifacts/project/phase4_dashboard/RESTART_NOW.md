# 🚀 Restart Streamlit Now - Quick Instructions

## ✅ EASIEST: Double-Click the Batch File

**Just double-click this file:**
```
restart_8502.bat
```

It's located in:
```
C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard\restart_8502.bat
```

The script will:
1. ✅ Stop any running Streamlit
2. ✅ Start fresh on port 8502
3. ✅ Show you the URL

---

## 📋 Manual Steps (If You Prefer)

### Step 1: Stop Current Streamlit
If Streamlit is running, press **Ctrl+C** in that terminal window.

OR use this command in a NEW terminal:
```powershell
taskkill /F /IM streamlit.exe
```

### Step 2: Navigate to Dashboard Folder
```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
```

### Step 3: Start Streamlit on Port 8502
```powershell
streamlit run app.py --server.port 8502
```

### Step 4: Open Browser
Go to: **http://localhost:8502**

---

## 🎯 After Restart - Find HEI Page

1. **Look in the sidebar** (left side of the page)
2. **Scroll down** if needed
3. **Find**: **"⚖️ Health Equity Index"**
4. **Click it** → Page loads!

---

## ⚠️ If Port 8502 is Busy

If you get an error that port 8502 is already in use, try:

```powershell
streamlit run app.py --server.port 8503
```

Then go to: **http://localhost:8503**

---

## ✅ Quick Test Checklist

After restart, verify:
- [ ] Browser shows http://localhost:8502
- [ ] Dashboard loads (no errors)
- [ ] Sidebar shows "⚖️ Health Equity Index"
- [ ] Clicking HEI page loads successfully
- [ ] HEI Score gauge displays

---

**Ready?** Just double-click `restart_8502.bat` and wait ~5 seconds! 🚀









