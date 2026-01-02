# Mobile Access Troubleshooting

## Issue: Page shows grey placeholders but doesn't load content

### Solution 1: Check Streamlit is running with network access

**Stop current Streamlit** (Ctrl+C), then restart with:

```powershell
cd Artifacts\project\phase4_dashboard
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

Or use the batch file:
```powershell
.\run_mobile.bat
```

### Solution 2: Check Windows Firewall

1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Find Python or add a new rule for port 8501
4. Allow both Private and Public networks

### Solution 3: Test with simple page first

Try the test page:
```
http://192.168.1.161:8501/_mobile_test
```

If this works, the issue is with the main pages.

### Solution 4: Check browser console

On Android:
1. Open Chrome
2. Go to chrome://inspect
3. Connect your device
4. Check for JavaScript errors

### Solution 5: Verify network connectivity

From Android, try:
```
http://192.168.1.161:8501/_health
```

Or ping test:
```
ping 192.168.1.161
```

### Solution 6: Try different port

If 8501 is blocked, try:
```powershell
streamlit run app.py --server.address=0.0.0.0 --server.port=8502
```

Then use: `http://192.168.1.161:8502/_mobile_view`

### Solution 7: Check Streamlit terminal

Look for errors when accessing from Android:
- Connection refused = Firewall issue
- 404 errors = Page not found
- WebSocket errors = Network configuration issue









