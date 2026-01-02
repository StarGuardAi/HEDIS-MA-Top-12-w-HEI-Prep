# Mobile Testing URLs

## Your Local IP Address
**192.168.1.161**

## Quick Start

### Option 1: Run Mobile View Directly (Recommended)
```bash
streamlit run pages/mobile_view.py --server.address=0.0.0.0 --server.port=8501
```

Or use the batch file:
```bash
run_mobile_test.bat
```

### Option 2: Run Main App (Desktop + Mobile)
```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

## URLs for Your Android Phone

### Mobile-Optimized View (Recommended)
```
http://192.168.1.161:8501/mobile_view
```

### Main Dashboard (Desktop View)
```
http://192.168.1.161:8501
```

## Important Notes

1. **Same WiFi Network Required**
   - Your phone and computer must be on the same WiFi network
   - Check your phone's WiFi settings to confirm

2. **Firewall Settings**
   - Windows Firewall may block the connection
   - If you can't connect, allow Streamlit through Windows Firewall:
     - Windows Security → Firewall & network protection
     - Allow an app through firewall
     - Add Python/Streamlit to allowed apps

3. **Port 8501**
   - Default Streamlit port is 8501
   - If port is in use, Streamlit will try 8502, 8503, etc.
   - Check the terminal output for the actual port number

4. **Testing Steps**
   ```
   1. Run: streamlit run pages/mobile_view.py --server.address=0.0.0.0
   2. Note the URL shown in terminal (should include 192.168.1.161:8501)
   3. On your phone, open browser (Chrome, Firefox, etc.)
   4. Enter: http://192.168.1.161:8501/mobile_view
   5. Test all views and features
   ```

## Troubleshooting

### Can't Connect from Phone?
1. **Check IP Address:**
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" under your active network adapter

2. **Check Firewall:**
   - Temporarily disable Windows Firewall to test
   - If it works, re-enable and add exception

3. **Check Network:**
   - Ensure phone and computer are on same WiFi
   - Try pinging from phone (if you have a network tool)

4. **Try Different Port:**
   ```bash
   streamlit run pages/mobile_view.py --server.address=0.0.0.0 --server.port=8502
   ```

### Streamlit Shows Wrong IP?
- The terminal will show the actual URL
- Use that URL instead of the one above
- Format: `http://[IP_ADDRESS]:[PORT]/mobile_view`

## Mobile Views to Test

1. **📊 Dashboard** - Main overview with metrics
2. **🎯 Top Opportunities** - Priority opportunities
3. **📈 Measure Deep-Dive** - Detailed measure analysis
4. **👥 Member Lists** - Member-level data
5. **💰 ROI Analysis** - ROI metrics and projections
6. **🔒 Secure Query** - AI chatbot interface
7. **⚙️ Settings** - App settings

## Quick Test Commands

```bash
# Test mobile view
cd Artifacts\project\phase4_dashboard
streamlit run pages/mobile_view.py --server.address=0.0.0.0

# Test main app
streamlit run app.py --server.address=0.0.0.0

# Run quick import test first
python test_mobile_quick.py
```

---

**Your IP:** 192.168.1.161  
**Default Port:** 8501  
**Mobile URL:** http://192.168.1.161:8501/mobile_view

