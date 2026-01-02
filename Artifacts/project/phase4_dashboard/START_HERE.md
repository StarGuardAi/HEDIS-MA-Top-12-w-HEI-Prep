# 🚀 START HERE: How to Launch the Application

## ⚠️ The Error You're Seeing

**"localhost refused to connect"** means **Streamlit isn't running yet**.

You need to **start the server first** before opening the browser!

## ✅ Solution: Start the Server

### Method 1: Using Batch Script (Easiest - Windows)

1. **Double-click** `run_dashboard.bat` in the `phase4_dashboard` folder
2. **Wait** for the terminal window to show:
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```
3. **Browser should auto-open**, or manually go to: http://localhost:8501

### Method 2: Using Command Line

1. **Open PowerShell or Command Prompt**

2. **Navigate to the dashboard folder:**
   ```powershell
   cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
   ```

3. **Start Streamlit:**
   ```powershell
   streamlit run app.py
   ```

4. **Wait for this message:**
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   Network URL: http://192.168.1.100:8501
   ```

5. **Open your browser** to: http://localhost:8501

### Method 3: Using Python Module

```powershell
cd Artifacts\project\phase4_dashboard
python -m streamlit run app.py
```

## 🔴 Important: Keep Terminal Open!

**DO NOT close the terminal window!** The server must keep running.

- ✅ **Keep terminal open** = App works
- ❌ **Close terminal** = Connection refused error

To stop the server: Press `Ctrl+C` in the terminal

## 📱 For Android Access

1. **Start server with network access:**
   ```powershell
   streamlit run app.py --server.address 0.0.0.0
   ```

2. **Find your PC's IP:**
   ```powershell
   ipconfig
   # Look for "IPv4 Address" (e.g., 192.168.1.100)
   ```

3. **On Android browser:**
   - Go to: `http://YOUR_PC_IP:8501`
   - Example: `http://192.168.1.100:8501`

## 🎯 Quick Test

Try this to verify everything works:

```powershell
# Navigate to dashboard folder
cd Artifacts\project\phase4_dashboard

# Start server
streamlit run app.py

# Wait for "Local URL: http://localhost:8501"
# Then open browser to that URL
```

## ✅ Success Indicators

You'll know it's working when:

1. ✅ Terminal shows: "You can now view your Streamlit app..."
2. ✅ Browser opens automatically (or you can open manually)
3. ✅ Page loads without "connection refused" error
4. ✅ You see the HEDIS Portfolio Optimizer interface

## 🐛 Still Having Issues?

See `TROUBLESHOOTING.md` for detailed solutions.

---

**Remember**: The server must be running in a terminal window for the app to work!

