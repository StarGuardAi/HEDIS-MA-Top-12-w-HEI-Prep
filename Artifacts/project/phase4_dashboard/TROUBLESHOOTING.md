# Troubleshooting: Connection Refused

## 🔴 Error: "localhost refused to connect" / ERR_CONNECTION_REFUSED

This means Streamlit isn't running. Let's fix it!

## ✅ Quick Fix Steps

### Step 1: Verify You're in the Right Directory

```bash
# Navigate to the dashboard directory
cd Artifacts/project/phase4_dashboard

# Verify you're in the right place (should see app.py)
dir  # Windows
# or
ls   # Mac/Linux
```

### Step 2: Check Streamlit is Installed

```bash
# Check if Streamlit is installed
streamlit --version

# If not installed, install it:
pip install streamlit
```

### Step 3: Start the Server

**Option A: New Architecture**
```bash
streamlit run app_new.py
```

**Option B: Full Version (Recommended)**
```bash
streamlit run app.py
```

**Option C: Using Python Module**
```bash
python -m streamlit run app.py
```

### Step 4: Wait for Server to Start

You should see output like:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.100:8501
```

**Important**: The server must be running in the terminal. Don't close the terminal window!

## 🔍 Common Issues & Solutions

### Issue 1: Port 8501 Already in Use

**Error**: `Port 8501 is already in use`

**Solution**:
```bash
# Use a different port
streamlit run app.py --server.port 8502

# Then access: http://localhost:8502
```

### Issue 2: Module Not Found Errors

**Error**: `ModuleNotFoundError: No module named 'config'`

**Solution**:
```bash
# Make sure you're in the right directory
cd Artifacts/project/phase4_dashboard

# Install all dependencies
pip install -r requirements.txt

# Try again
streamlit run app.py
```

### Issue 3: Python Path Issues

**Error**: `python: command not found` or `streamlit: command not found`

**Solution**:
```bash
# Try python3 instead of python
python3 -m streamlit run app.py

# Or use full path
C:\Python\python.exe -m streamlit run app.py
```

### Issue 4: Firewall Blocking

**Error**: Can't access from Android/other devices

**Solution**:
```bash
# Run with network access enabled
streamlit run app.py --server.address 0.0.0.0

# This allows access from other devices on your network
```

### Issue 5: Wrong Directory

**Error**: `FileNotFoundError: app.py`

**Solution**:
```bash
# Check current directory
pwd  # Mac/Linux
cd   # Windows

# Navigate to correct directory
cd Artifacts/project/phase4_dashboard

# Verify app.py exists
ls app.py  # Mac/Linux
dir app.py # Windows
```

## 🚀 Step-by-Step Startup Guide

### Windows

1. **Open PowerShell or Command Prompt**

2. **Navigate to project:**
   ```powershell
   cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
   ```

3. **Start Streamlit:**
   ```powershell
   streamlit run app.py
   ```

4. **Wait for output:**
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```

5. **Open browser:**
   - Browser should auto-open
   - Or manually go to: http://localhost:8501

### Mac/Linux

1. **Open Terminal**

2. **Navigate to project:**
   ```bash
   cd ~/Projects/HEDIS-MA-Top-12-w-HEI-Prep/Artifacts/project/phase4_dashboard
   ```

3. **Start Streamlit:**
   ```bash
   streamlit run app.py
   ```

4. **Wait for output and open browser**

## 🎯 Verification Checklist

Before accessing the site, verify:

- [ ] Terminal/PowerShell is open
- [ ] You're in `phase4_dashboard` directory
- [ ] Streamlit command ran successfully
- [ ] You see "Local URL: http://localhost:8501" in terminal
- [ ] Terminal window is still open (don't close it!)
- [ ] No error messages in terminal

## 🔧 Alternative: Use Batch Script (Windows)

If you have `run_dashboard.bat`:

```bash
# Double-click run_dashboard.bat
# Or run from command line:
run_dashboard.bat
```

## 📱 Accessing from Android

Once server is running:

1. **Find your PC's IP:**
   ```bash
   # Windows
   ipconfig
   # Look for "IPv4 Address" (e.g., 192.168.1.100)
   ```

2. **Start with network access:**
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```

3. **On Android browser:**
   - Go to: `http://YOUR_PC_IP:8501`
   - Example: `http://192.168.1.100:8501`

## ⚠️ Important Notes

1. **Keep Terminal Open**: Don't close the terminal window while using the app
2. **Stop Server**: Press `Ctrl+C` in terminal to stop the server
3. **Port Conflicts**: If 8501 is busy, use `--server.port 8502`
4. **Network Access**: Use `--server.address 0.0.0.0` for Android access

## 🐛 Still Not Working?

### Check Streamlit Installation

```bash
# Verify installation
pip show streamlit

# Reinstall if needed
pip install --upgrade streamlit
```

### Check Python Version

```bash
# Should be 3.8 or higher
python --version

# Or
python3 --version
```

### Check Dependencies

```bash
# Install all requirements
pip install -r requirements.txt

# Verify key packages
pip show pandas plotly streamlit
```

### Try Minimal Test

```bash
# Create a simple test file
echo "import streamlit as st; st.write('Hello World')" > test.py

# Run it
streamlit run test.py

# If this works, the issue is with app.py, not Streamlit
```

## 📞 Quick Reference

**Start Server:**
```bash
cd Artifacts/project/phase4_dashboard
streamlit run app.py
```

**Start with Network Access:**
```bash
streamlit run app.py --server.address 0.0.0.0
```

**Start on Different Port:**
```bash
streamlit run app.py --server.port 8502
```

**Stop Server:**
- Press `Ctrl+C` in the terminal

---

**Most Common Issue**: Forgetting to start the server! Make sure `streamlit run app.py` is running in a terminal window.

