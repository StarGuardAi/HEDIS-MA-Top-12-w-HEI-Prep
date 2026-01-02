# 📱 Testing on Android Phone - Step-by-Step Guide

## Your Laptop IP Address
**`192.168.1.161`**

---

## Step-by-Step Instructions

### Step 1: Ensure Both Devices Are on Same WiFi
- ✅ Laptop connected to WiFi
- ✅ Android phone connected to **same WiFi network**

### Step 2: Start Dashboard on Laptop
```bash
cd Artifacts/project/phase4_dashboard
restart_8502.bat
```

Wait for message: **"SUCCESS! Streamlit is starting..."**

### Step 3: On Your Android Phone

1. **Open Chrome Browser** (or Firefox/Samsung Internet)

2. **Type this URL in address bar:**
   ```
   http://192.168.1.161:8502
   ```

3. **Press Enter/Go**

4. **Dashboard should load** (may take 5-10 seconds first time)

---

## What to Test on Android

### ✅ Sidebar Test
1. **Look for ">" button** in top-left corner
2. **Tap ">" button** to open sidebar
3. **Verify:**
   - ✅ **App Home frame** appears at top of sidebar
   - ✅ Frame shows "⭐ App Home" with "Return to Dashboard" subtitle
   - ✅ Navigation items appear below frame
   - ✅ Frame fits mobile width (no horizontal scroll)
   - ✅ Text is readable (white on purple gradient)
   - ✅ Touch targets are large enough (easy to tap)

### ✅ Navigation Test
1. **Tap "App Home" link** → Should navigate to home page
2. **Tap any page link** (e.g., "📊 ROI by Measure") → Should navigate
3. **Tap ">" again** → Sidebar should close
4. **Tap outside sidebar** → Should also close

### ✅ Touch Targets Test
- All links should be **easy to tap** (no accidental taps)
- Links should have **visual feedback** when tapped
- **No text overlap** or cut-off text
- **Smooth scrolling** in sidebar if many items

---

## Troubleshooting

### ❌ Can't Connect from Phone

**Problem:** Phone can't reach `http://192.168.1.161:8502`

**Solutions:**
1. **Check WiFi:** Both devices on same network?
2. **Check Firewall:** Windows Firewall may be blocking port 8502
   - Go to Windows Security → Firewall & network protection
   - Allow Streamlit through firewall
3. **Check Streamlit:** Make sure it's running with `--server.address 0.0.0.0`
4. **Try ping:** On phone, try accessing `http://192.168.1.161` (without port)

### ❌ Sidebar Doesn't Open

**Problem:** Tapping ">" doesn't open sidebar

**Solutions:**
1. **Refresh page** (pull down to refresh)
2. **Clear browser cache** on phone
3. **Try different browser** (Chrome, Firefox, Samsung Internet)
4. **Check console:** Open Chrome DevTools on phone (if possible)

### ❌ App Home Frame Not Visible

**Problem:** Sidebar opens but App Home frame not showing

**Solutions:**
1. **Scroll to top** of sidebar
2. **Refresh page**
3. **Check CSS loaded:** Inspect element (if possible)

### ❌ Text Too Small or Unreadable

**Problem:** Text is hard to read on phone

**Solutions:**
1. **Zoom in** on phone browser
2. **Check font size:** Should be at least 14px
3. **Verify contrast:** White text on purple background

---

## Quick Test Checklist

- [ ] Phone and laptop on same WiFi
- [ ] Dashboard running on laptop
- [ ] Can access `http://192.168.1.161:8502` from phone
- [ ] ">" button visible in top-left
- [ ] Tapping ">" opens sidebar
- [ ] App Home frame visible at top
- [ ] Navigation items below frame
- [ ] Frame fits mobile width
- [ ] Text readable
- [ ] Touch targets work
- [ ] Links navigate correctly
- [ ] Sidebar closes properly

---

## Alternative: Use Chrome DevTools on PC

If you can't test on real Android phone, use Chrome DevTools:

1. **Open:** `http://localhost:8502` on PC
2. **Press:** `F12` → `Ctrl+Shift+M`
3. **Select:** "Pixel 5" or "Samsung Galaxy S20"
4. **Test:** Same tests as above

This simulates Android device on your PC.

---

## Your URLs

**On PC (localhost):**
```
http://localhost:8502
```

**On Android Phone (same WiFi):**
```
http://192.168.1.161:8502
```

---

## Security Note

⚠️ **Important:** The dashboard is now accessible from any device on your WiFi network. This is fine for testing, but:
- Don't leave it running unattended
- Stop the server when done testing
- Use `Ctrl+C` in the terminal to stop

---

## Need Help?

If you encounter issues:
1. Check Windows Firewall settings
2. Verify both devices on same WiFi
3. Try accessing from PC first: `http://192.168.1.161:8502`
4. Check Streamlit terminal for error messages







