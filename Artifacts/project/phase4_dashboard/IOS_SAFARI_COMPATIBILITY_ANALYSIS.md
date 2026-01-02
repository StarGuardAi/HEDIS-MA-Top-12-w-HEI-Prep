# iOS Safari Compatibility Analysis & Fixes

## Executive Summary

Your Streamlit app has several iOS Safari-specific compatibility issues causing:
1. **Privacy warnings** on HTTP connections
2. **Very slow loading** due to session state clearing and JavaScript execution
3. **Sidebar loading instead of home page** due to redirect logic issues
4. **Navigation failures** caused by redirect loops and sessionStorage problems

---

## Critical Issues Identified

### 1. Session State Management Issues

#### **Issue 1.1: Aggressive Session State Clearing**
**Location:** `app.py:1101-1103`

```python
if 'initialized' not in st.session_state:
    st.session_state.clear()  # ⚠️ PROBLEM: Clears ALL session state
    st.session_state.initialized = True
```

**Problem:** 
- iOS Safari may reload pages more frequently, causing repeated clearing
- This resets all user interactions and navigation state
- Causes slow loading as data must be regenerated

**Fix:** Only clear specific keys, not entire session state:
```python
if 'initialized' not in st.session_state:
    # Only clear problematic keys, preserve navigation state
    keys_to_clear = [k for k in st.session_state.keys() 
                     if k not in ['mobile_redirected', 'initialized']]
    for key in keys_to_clear:
        del st.session_state[key]
    st.session_state.initialized = True
```

---

#### **Issue 1.2: Mobile Redirect State Not Persisting**
**Location:** `app.py:740-741`

```python
if 'mobile_redirected' not in st.session_state:
    st.session_state.mobile_redirected = False
```

**Problem:**
- Session state is cleared on initialization, losing redirect state
- iOS Safari may not properly persist session state between page loads
- Causes redirect loops

**Fix:** Use a more persistent approach:
```python
# Initialize mobile redirect state BEFORE clearing session
if 'mobile_redirected' not in st.session_state:
    st.session_state.mobile_redirected = False

# Then in the clearing logic, preserve this key
if 'initialized' not in st.session_state:
    mobile_redirected = st.session_state.get('mobile_redirected', False)
    st.session_state.clear()
    st.session_state.initialized = True
    st.session_state.mobile_redirected = mobile_redirected
```

---

### 2. Page Navigation Problems

#### **Issue 2.1: JavaScript Redirect Using sessionStorage**
**Location:** `app.py:793-798`

```javascript
if (isOnSubPage && !sessionStorage.getItem('mobileRedirectDone')) {
    sessionStorage.setItem('mobileRedirectDone', 'true');
    setTimeout(() => {
        window.location.href = '/';
    }, 100);
}
```

**Problems:**
- iOS Safari has strict `sessionStorage` policies and may block it
- `window.location.href = '/'` causes full page reload, losing WebSocket connection
- Redirect happens AFTER page loads, causing sidebar flash
- `sessionStorage` may not persist properly in iOS Safari private browsing

**Fix:** Use Streamlit's built-in navigation instead:
```python
# In app.py, replace JavaScript redirect with Python logic
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

# Detect mobile and redirect BEFORE rendering sidebar
if 'mobile_redirected' not in st.session_state:
    st.session_state.mobile_redirected = False

# Check if we're on a sub-page and should redirect
ctx = get_script_run_ctx()
if ctx:
    current_page = ctx.current_page_name
    is_sub_page = current_page and current_page != 'app'
    
    # Detect mobile using user agent (server-side)
    user_agent = st.request_headers.get('User-Agent', '')
    is_mobile = any(x in user_agent.lower() for x in ['iphone', 'ipad', 'ipod', 'mobile'])
    
    if is_mobile and is_sub_page and not st.session_state.mobile_redirected:
        st.session_state.mobile_redirected = True
        st.switch_page("app.py")  # Navigate to home page
```

**Alternative Fix (if switch_page not available):**
```javascript
// Use localStorage instead of sessionStorage (more persistent)
// Check URL hash to prevent loops
if (isOnSubPage && window.location.hash !== '#mobile-redirected') {
    window.location.hash = '#mobile-redirected';
    window.location.replace('/');  // Use replace instead of href
}
```

---

#### **Issue 2.2: Inconsistent initial_sidebar_state**
**Location:** Multiple files

**Problem:**
- `app.py:33` uses `initial_sidebar_state="collapsed"`
- Many page files use `initial_sidebar_state="expanded"`
- iOS Safari may cache sidebar state inconsistently
- Causes sidebar to appear when it shouldn't

**Fix:** Standardize sidebar state:
```python
# In app.py - use "auto" for better mobile compatibility
st.set_page_config(
    page_title="HEDIS Portfolio Optimizer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="auto"  # Let Streamlit decide based on screen size
)
```

**Update all page files** to use `initial_sidebar_state="auto"` instead of `"expanded"`.

---

### 3. WebSocket Connection Handling

#### **Issue 3.1: HTTP Connection Privacy Warning**
**Location:** Server configuration (not in code)

**Problem:**
- iOS Safari shows privacy warning for HTTP connections
- WebSocket connections over HTTP (`ws://`) are blocked or degraded
- Causes slow loading and connection failures

**Fix:** 
1. **Immediate:** Add Streamlit config to handle HTTP better:
   ```toml
   # .streamlit/config.toml
   [server]
   enableCORS = false
   enableXsrfProtection = false
   port = 8502
   address = "0.0.0.0"
   
   [browser]
   gatherUsageStats = false
   ```

2. **Best Practice:** Use HTTPS with self-signed certificate:
   ```bash
   # Generate self-signed certificate
   openssl req -x509 -newkey rsa:4096 -nodes \
     -keyout key.pem -out cert.pem -days 365 \
     -subj "/CN=192.168.1.161"
   
   # Run Streamlit with HTTPS
   streamlit run app.py --server.sslCertFile=cert.pem --server.sslKeyFile=key.pem
   ```

3. **iOS Safari:** User must accept certificate warning once, then it works normally

---

#### **Issue 3.2: WebSocket Reconnection Issues**
**Location:** Streamlit runtime (not directly in code)

**Problem:**
- iOS Safari aggressively suspends WebSocket connections
- Page reloads break WebSocket connections
- No automatic reconnection handling

**Fix:** Add WebSocket reconnection handling:
```javascript
// Add to app.py after mobile detection script
st.markdown("""
<script>
(function() {
    // WebSocket reconnection for iOS Safari
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;
    
    function checkWebSocket() {
        // Check if Streamlit WebSocket is connected
        const wsIndicator = document.querySelector('[data-testid="stWebSocketStatus"]');
        if (!wsIndicator || wsIndicator.textContent.includes('disconnected')) {
            if (reconnectAttempts < maxReconnectAttempts) {
                reconnectAttempts++;
                console.log('WebSocket disconnected, attempting reconnect...');
                // Trigger Streamlit rerun to reconnect
                window.location.reload();
            }
        } else {
            reconnectAttempts = 0;
        }
    }
    
    // Check WebSocket status periodically
    setInterval(checkWebSocket, 5000);
    
    // Also check on page visibility change (iOS Safari specific)
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            checkWebSocket();
        }
    });
})();
</script>
""", unsafe_allow_html=True)
```

---

### 4. CSS/JavaScript Incompatibilities

#### **Issue 4.1: MutationObserver Performance**
**Location:** `app.py:784-786`

```javascript
const observer = new MutationObserver(hideSidebar);
observer.observe(document.body, { childList: true, subtree: true });
```

**Problem:**
- MutationObserver with `subtree: true` watches entire DOM
- iOS Safari has performance issues with frequent DOM mutations
- Causes slow rendering and high CPU usage

**Fix:** Use more targeted observation:
```javascript
// Only observe sidebar container, not entire body
const sidebarContainer = document.querySelector('[data-testid="stSidebar"]');
if (sidebarContainer) {
    const observer = new MutationObserver(function(mutations) {
        hideSidebar(); // Only run when sidebar changes
    });
    observer.observe(sidebarContainer, { 
        childList: true, 
        attributes: true,
        attributeFilter: ['style', 'class']
    });
}
```

---

#### **Issue 4.2: CSS Viewport Units**
**Location:** Multiple CSS blocks in `app.py`

**Problem:**
- iOS Safari has known issues with `vh` units (address bar causes recalculation)
- `@viewport` rule may not be supported

**Fix:** Use JavaScript to set viewport height:
```javascript
// Fix viewport height for iOS Safari
function setViewportHeight() {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}
setViewportHeight();
window.addEventListener('resize', setViewportHeight);
window.addEventListener('orientationchange', setViewportHeight);

// Then use var(--vh) in CSS instead of vh
```

---

#### **Issue 4.3: CSS :has() Selector**
**Location:** `app.py:143, 149, 874`

```css
[data-testid="column"]:has([data-testid="stMetricContainer"]) {
    display: flex !important;
}
```

**Problem:**
- `:has()` selector not supported in iOS Safari < 15.4
- Causes styles to not apply

**Fix:** Use JavaScript fallback or remove `:has()`:
```css
/* Remove :has() and use class-based approach */
.metric-column {
    display: flex !important;
    justify-content: center !important;
}
```

```python
# In Python, add class when rendering metrics
st.markdown('<div class="metric-column">', unsafe_allow_html=True)
# ... render metric ...
st.markdown('</div>', unsafe_allow_html=True)
```

---

### 5. st.set_page_config() Issues

#### **Issue 5.1: Multiple st.set_page_config() Calls**
**Location:** `src/ui/layout.py:10`

**Problem:**
- `st.set_page_config()` can only be called once per app
- Multiple calls cause errors in iOS Safari

**Fix:** Ensure `st.set_page_config()` is only called in `app.py`:
```python
# In src/ui/layout.py, remove st.set_page_config() call
# It should only be in app.py
```

---

#### **Issue 5.2: Page Config After Other Streamlit Commands**
**Location:** Check all page files

**Problem:**
- `st.set_page_config()` must be FIRST Streamlit command
- iOS Safari is stricter about this

**Fix:** Verify all page files have `st.set_page_config()` as first command:
```python
# CORRECT ORDER:
import streamlit as st
st.set_page_config(...)  # MUST BE FIRST
# Then other imports and code
```

---

## Recommended Fix Priority

### **Priority 1: Critical (Fix Immediately)**
1. ✅ Fix session state clearing (Issue 1.1)
2. ✅ Fix mobile redirect logic (Issue 2.1)
3. ✅ Standardize sidebar state (Issue 2.2)
4. ✅ Remove `:has()` CSS selector (Issue 4.3)

### **Priority 2: High (Fix Soon)**
5. ✅ Fix MutationObserver performance (Issue 4.1)
6. ✅ Add WebSocket reconnection (Issue 3.2)
7. ✅ Fix viewport height issues (Issue 4.2)

### **Priority 3: Medium (Consider)**
8. ⚠️ Set up HTTPS (Issue 3.1)
9. ⚠️ Review all `st.set_page_config()` calls (Issue 5.1, 5.2)

---

## Testing Checklist

After applying fixes, test on iOS Safari:

- [ ] App loads without privacy warning (or warning is acceptable)
- [ ] Home page loads correctly (not sidebar)
- [ ] Navigation between pages works
- [ ] Sidebar stays hidden on mobile
- [ ] No redirect loops
- [ ] Page loads in < 3 seconds
- [ ] WebSocket connection stays active
- [ ] No console errors in Safari Web Inspector

---

## Additional iOS Safari Considerations

1. **Touch Events:** Ensure all interactive elements have adequate touch targets (min 44x44px)
2. **Scroll Behavior:** iOS Safari has momentum scrolling - test scroll performance
3. **Keyboard:** Test form inputs - iOS keyboard may cover inputs
4. **Orientation Changes:** Test portrait/landscape rotation
5. **Private Browsing:** Test in private mode - sessionStorage/localStorage may be restricted

---

## Quick Fix Summary

**Immediate actions:**
1. Update `app.py:1101-1103` to preserve navigation state
2. Replace JavaScript redirect with Python `st.switch_page()` or better redirect logic
3. Change all `initial_sidebar_state="expanded"` to `"auto"`
4. Remove or replace `:has()` CSS selectors
5. Optimize MutationObserver to only watch sidebar

**Configuration:**
1. Create `.streamlit/config.toml` with server settings
2. Consider HTTPS setup for production use

---

## Code Locations Reference

| Issue | File | Line(s) | Severity |
|-------|------|---------|----------|
| Session state clearing | `app.py` | 1101-1103 | Critical |
| Mobile redirect JS | `app.py` | 793-798 | Critical |
| Sidebar state | `app.py` | 33 | High |
| Sidebar state (pages) | `pages/*.py` | Various | High |
| MutationObserver | `app.py` | 784-786 | Medium |
| CSS :has() | `app.py` | 143, 149, 874 | Medium |
| Multiple page_config | `src/ui/layout.py` | 10 | Medium |




