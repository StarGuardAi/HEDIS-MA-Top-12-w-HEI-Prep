# How to Launch the HEDIS Portfolio Optimizer

## Option 1: Anaconda Prompt (Recommended)

1. **Open Anaconda Prompt** (search for "Anaconda Prompt" in Windows Start menu)

2. **Navigate to project directory:**
   ```bash
   cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
   ```

3. **Activate your conda environment** (if you have one):
   ```bash
   conda activate your_env_name
   ```
   Or if using base environment:
   ```bash
   conda activate base
   ```

4. **Launch Streamlit on port 8504:**
   ```bash
   streamlit run app.py --server.port 8504
   ```

5. **Access the dashboard:**
   - The terminal will show: "You can now view your Streamlit app in your browser."
   - Open: **http://localhost:8504**
   - Or click the URL shown in the terminal

---

## Option 2: Regular Command Prompt / PowerShell

If you don't have Anaconda, but have Python and dependencies installed:

1. **Open Command Prompt or PowerShell**

2. **Navigate to project directory:**
   ```bash
   cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
   ```

3. **Activate virtual environment** (if you have one):
   ```bash
   venv_311\Scripts\activate
   ```
   Or if using a different venv:
   ```bash
   .\venv\Scripts\activate
   ```

4. **Launch Streamlit:**
   ```bash
   streamlit run app.py --server.port 8504
   ```

---

## Option 3: Using Python Directly

1. **Open Anaconda Prompt**

2. **Navigate and activate environment:**
   ```bash
   cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
   conda activate your_env_name
   ```

3. **Run with Python module:**
   ```bash
   python -m streamlit run app.py --server.port 8504
   ```

---

## Troubleshooting

### If you see "streamlit: command not found":
- Make sure your conda environment is activated
- Install streamlit: `pip install streamlit` or `conda install streamlit`

### If you see import errors:
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're in the correct conda environment

### If port 8504 is already in use:
- Use a different port: `streamlit run app.py --server.port 8505`
- Or kill the process using port 8504

### If the page doesn't load:
- Try `http://127.0.0.1:8504` instead of `localhost:8504`
- Check browser console (F12) for errors
- Make sure no firewall is blocking the connection

---

## Quick Start (Copy-Paste)

**For Anaconda Prompt:**
```bash
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
conda activate base
streamlit run app.py --server.port 8504
```

**Then open:** http://localhost:8504

---

## What to Expect

When Streamlit starts successfully, you'll see:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8504
Network URL: http://192.168.x.x:8504
```

The dashboard should load with:
- Sidebar with filters
- Main content area with tabs
- **New Tab 5: "🔒 Secure Query Interface"**
- Value proposition in sidebar and footer










