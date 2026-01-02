# How to Stop and Restart Streamlit

## 🛑 Method 1: Stop in Terminal (Easiest)

### If Streamlit is running in a terminal window:

1. **Click on the terminal window** where Streamlit is running
2. **Press `Ctrl + C`** (hold Ctrl, press C)
3. Wait for it to stop (you'll see "Shutting down...")
4. **Restart** by running:
   ```bash
   streamlit run app.py --server.port 8502
   ```

---

## 🛑 Method 2: Stop All Streamlit Processes

### If you can't find the terminal window:

1. **Open PowerShell or Command Prompt**
2. **Run this command**:
   ```powershell
   taskkill /F /IM streamlit.exe
   ```
3. **Restart** by navigating to the dashboard folder and running:
   ```powershell
   cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
   streamlit run app.py --server.port 8502
   ```

---

## 🚀 Method 3: Use the Batch Script (Easiest!)

### Just double-click a batch file:

**Option A: Restart on Port 8502**
- Double-click: `restart_8502.bat`
- Located in: `phase4_dashboard/restart_8502.bat`

**Option B: Clear Cache and Restart**
- Double-click: `CLEAR_CACHE_AND_RESTART.bat`
- This will clear cache AND restart

**Option C: Simple Start**
- Double-click: `START_STREAMLIT_NOW.bat`
- Starts on port 8502

---

## 📍 Where to Find the Terminal

### If Streamlit is running in background:

1. **Check Taskbar** - Look for a minimized terminal window
2. **Check System Tray** - Some terminals minimize there
3. **Task Manager**:
   - Press `Ctrl + Shift + Esc`
   - Look for "Python" or "Streamlit" processes
   - Right-click → "End Task"

---

## 🔄 Quick Restart Steps

### Fastest Method:

1. **Stop**: Press `Ctrl + C` in terminal (or use `taskkill /F /IM streamlit.exe`)
2. **Navigate**: 
   ```powershell
   cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
   ```
3. **Start**:
   ```powershell
   streamlit run app.py --server.port 8502
   ```

---

## 🎯 After Restart

1. **Wait 5-10 seconds** for Streamlit to start
2. **Open browser** to: http://localhost:8502
3. **Hard refresh** (Ctrl + Shift + R) to clear cache
4. **Check sidebar** - mobile pages should be gone!

---

## 💡 Pro Tip

**Keep a terminal window open** while using Streamlit:
- You can see errors/logs
- Easy to stop with Ctrl+C
- Can restart quickly

---

**Location of batch files:**
- `C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard\`









