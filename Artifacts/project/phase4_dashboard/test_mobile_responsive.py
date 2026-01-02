"""
Quick Mobile Responsiveness Test
Run this to verify mobile CSS is properly applied
"""
import streamlit as st

st.set_page_config(
    page_title="Mobile Responsiveness Test",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import sidebar styling
from utils.sidebar_styling import apply_sidebar_styling
apply_sidebar_styling()

st.title("📱 Mobile Responsiveness Test")
st.markdown("""
### Test Checklist

Use Chrome DevTools (F12 → Ctrl+Shift+M) to test mobile view:

#### Sidebar Tests:
- [ ] Sidebar collapses on mobile (< 768px)
- [ ] ">" button visible in top-left
- [ ] Tapping ">" opens sidebar
- [ ] App Home frame visible at top of sidebar
- [ ] Navigation items appear below frame
- [ ] Frame fits mobile width (no overflow)
- [ ] Text is readable (white on purple)
- [ ] Touch targets are at least 44px tall
- [ ] Links are clickable
- [ ] Sidebar closes when tapping outside or ">" again

#### App Home Frame Tests:
- [ ] Frame is visible when sidebar opens
- [ ] Frame width fits mobile screen (100%)
- [ ] Text "App Home" is readable
- [ ] Subtitle "Return to Dashboard" is visible
- [ ] Link is clickable (navigates to home)
- [ ] Touch feedback works (highlight on tap)

#### Navigation Links Tests:
- [ ] All page links visible below App Home frame
- [ ] Links are white text on purple background
- [ ] Each link is at least 44px tall (touch-friendly)
- [ ] Links have proper spacing between them
- [ ] Links navigate to correct pages
- [ ] Active page is highlighted

#### Responsive Breakpoints:
- [ ] Desktop (> 1024px): Sidebar always visible
- [ ] Tablet (768px - 1024px): Sidebar can collapse
- [ ] Mobile (< 768px): Sidebar collapsed by default

---

### Quick Test Steps:

1. **Open Chrome DevTools:**
   - Press `F12` or `Ctrl+Shift+I`

2. **Toggle Device Mode:**
   - Press `Ctrl+Shift+M`
   - Select "iPhone 12 Pro" or "Pixel 5"

3. **Navigate to ROI by Measure:**
   - Click "📊 ROI by Measure" in sidebar

4. **Test Sidebar:**
   - Look for ">" button (top-left)
   - Click to open sidebar
   - Verify App Home frame at top
   - Verify navigation items below

5. **Test Navigation:**
   - Click "App Home" → Should navigate
   - Click any page link → Should navigate

---

### Expected CSS Classes:

- `.custom-sidebar-home` - App Home frame container
- `.custom-sidebar-subtitle` - Subtitle text
- `[data-testid="stSidebar"]` - Streamlit sidebar element
- `[data-testid="stPageLink-NavLink"]` - Navigation links

---

### Mobile CSS Media Queries:

```css
@media (max-width: 768px) {
    /* Mobile-specific styles */
}

@media (min-width: 769px) and (max-width: 1024px) {
    /* Tablet-specific styles */
}
```

---

### Troubleshooting:

**Sidebar doesn't collapse:**
- Check browser width < 768px
- Verify `initial_sidebar_state` in page config

**App Home frame not visible:**
- Check CSS is loading (inspect element)
- Verify `.custom-sidebar-home` class exists

**Text not readable:**
- Verify `color: #FFFFFF !important;` is applied
- Check font-size is at least 14px

**Touch targets too small:**
- Verify `min-height: 44px` is applied
- Check padding provides adequate touch area
""")

st.divider()

st.markdown("### Current Viewport")
st.info("""
**To test mobile responsiveness:**
1. Open Chrome DevTools (F12)
2. Press Ctrl+Shift+M to toggle device mode
3. Select a mobile device (iPhone 12 Pro, Pixel 5, etc.)
4. Navigate to "📊 ROI by Measure" page
5. Test sidebar toggle and navigation
""")

# Show current viewport info (if available via JavaScript)
st.markdown("""
<script>
// Display viewport info
document.addEventListener('DOMContentLoaded', function() {
    const info = document.createElement('div');
    info.innerHTML = `
        <strong>Viewport Width:</strong> <span id="viewport-width">${window.innerWidth}px</span><br>
        <strong>Viewport Height:</strong> <span id="viewport-height">${window.innerHeight}px</span><br>
        <strong>Device Type:</strong> <span id="device-type">${window.innerWidth < 768 ? 'Mobile' : window.innerWidth < 1024 ? 'Tablet' : 'Desktop'}</span>
    `;
    info.style.padding = '1rem';
    info.style.backgroundColor = '#f0f0f0';
    info.style.borderRadius = '6px';
    info.style.marginTop = '1rem';
    document.body.appendChild(info);
    
    // Update on resize
    window.addEventListener('resize', function() {
        document.getElementById('viewport-width').textContent = window.innerWidth + 'px';
        document.getElementById('viewport-height').textContent = window.innerHeight + 'px';
        document.getElementById('device-type').textContent = 
            window.innerWidth < 768 ? 'Mobile' : window.innerWidth < 1024 ? 'Tablet' : 'Desktop';
    });
});
</script>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📱 Mobile Test")
st.sidebar.info("""
**Test Steps:**
1. Open DevTools (F12)
2. Toggle device mode (Ctrl+Shift+M)
3. Select mobile device
4. Test sidebar toggle
5. Verify App Home frame
""")







