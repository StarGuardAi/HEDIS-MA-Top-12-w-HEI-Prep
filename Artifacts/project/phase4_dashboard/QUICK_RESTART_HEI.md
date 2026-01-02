# Quick Restart Guide - HEI Page Testing

## 🚀 Fastest Way to Restart on Port 8502

### Option 1: Use the Batch Script (Easiest) ✅

1. **Double-click** this file: `restart_8502.bat`
   - Located in: `phase4_dashboard/restart_8502.bat`
   
2. **Wait for it to start** (takes ~5 seconds)

3. **Open browser** to: **http://localhost:8502**

4. **Look for HEI page** in sidebar: **"⚖️ Health Equity Index"**

---

### Option 2: Manual Commands

**In Command Prompt or PowerShell:**

```bash
# Navigate to dashboard folder
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard

# Stop any running Streamlit (press Ctrl+C if you see it running)

# Start on port 8502
streamlit run app.py --server.port 8502
```

---

## ✅ After Restart - Quick Verification

1. ✅ Browser opens to http://localhost:8502
2. ✅ Dashboard loads (no errors)
3. ✅ Look in sidebar → Find **"⚖️ Health Equity Index"**
4. ✅ Click it → Page loads successfully

---

## 🐛 If Port 8502 is Already in Use

If you get an error that port 8502 is busy:

### Quick Fix - Use Different Port:

```bash
streamlit run app.py --server.port 8503
```

Then access at: **http://localhost:8503**

---

## 📝 What the Script Does

1. ✅ Stops any running Streamlit processes
2. ✅ Waits 2 seconds (clean shutdown)
3. ✅ Changes to correct directory
4. ✅ Checks Streamlit is installed
5. ✅ Starts Streamlit on port 8502
6. ✅ Shows you the URL to access

---

## 🎯 Next Steps After Restart

1. **Open**: http://localhost:8502
2. **Find**: "⚖️ Health Equity Index" in sidebar
3. **Test**: Follow the testing checklist in `HEI_PAGE_TESTING_GUIDE.md`

---

**Ready?** Just double-click `restart_8502.bat`!









