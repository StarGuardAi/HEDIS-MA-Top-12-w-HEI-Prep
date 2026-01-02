# 🚨 EMERGENCY START GUIDE

## You're Getting "Connection Refused" - Here's the Fix

### ✅ SOLUTION: Start the Server First!

The error means **no server is running**. You MUST start Streamlit before opening the browser.

## 🎯 Step-by-Step (Do This Now)

### Step 1: Open PowerShell
- Press `Windows Key + X`
- Select "Windows PowerShell" or "Terminal"

### Step 2: Navigate to Dashboard Folder
Copy and paste this EXACT command:

```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
```

Press Enter

### Step 3: Start the Server
Copy and paste this command:

```powershell
streamlit run app.py
```

Press Enter

### Step 4: WAIT for This Message
You should see:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.100:8501
```

### Step 5: Open Browser
- Browser should open automatically
- OR manually go to: **http://localhost:8501**

## ⚠️ CRITICAL: Keep Terminal Open!

**DO NOT CLOSE THE TERMINAL WINDOW!**

- ✅ Terminal open = App works
- ❌ Terminal closed = Connection refused

## 🎯 Even Easier: Use the Batch File

1. **Open File Explorer**
2. **Navigate to**: `C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard`
3. **Double-click**: `START_NOW.bat`
4. **Wait** for server to start
5. **Browser opens automatically**

## 🔍 Verify It's Working

You'll know it's working when:
- ✅ Terminal shows "Local URL: http://localhost:8501"
- ✅ Browser opens (or you can open it manually)
- ✅ You see the HEDIS Portfolio Optimizer page
- ✅ No "connection refused" error

## 🐛 If Still Not Working

### Check 1: Is Streamlit Installed?
```powershell
streamlit --version
```

If error, install:
```powershell
pip install streamlit
```

### Check 2: Are You in the Right Folder?
```powershell
dir app.py
```

Should show: `app.py` file exists

### Check 3: Try Different Port
```powershell
streamlit run app.py --server.port 8502
```

Then go to: http://localhost:8502

## 📱 For Android Access

1. **Start with network access:**
   ```powershell
   streamlit run app.py --server.address 0.0.0.0
   ```

2. **Find your IP:**
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

3. **On Android**: `http://YOUR_IP:8501`

## ✅ Quick Copy-Paste Commands

**Full sequence (copy all at once):**
```powershell
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
streamlit run app.py
```

Then wait for the URL and open it in your browser!

---

**Remember**: The server MUST be running in a terminal window. If you close the terminal, the app stops working!

