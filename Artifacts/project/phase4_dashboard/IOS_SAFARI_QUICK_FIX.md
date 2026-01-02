# iOS Safari Quick Fix Guide

## Critical Code Changes Required

### 1. Fix Session State Clearing (CRITICAL)

**File:** `app.py`  
**Line:** 1101-1103  
**Current Code:**
```python
if 'initialized' not in st.session_state:
    st.session_state.clear()
    st.session_state.initialized = True
```

**Replace With:**
```python
if 'initialized' not in st.session_state:
    # Preserve navigation state for iOS Safari
    mobile_redirected = st.session_state.get('mobile_redirected', False)
    st.session_state.clear()
    st.session_state.initialized = True
    st.session_state.mobile_redirected = mobile_redirected
```

---

### 2. Fix Mobile Redirect JavaScript (CRITICAL)

**File:** `app.py`  
**Lines:** 743-817  
**Action:** Replace entire mobile detection script block

**Find:**
```javascript
if (isOnSubPage && !sessionStorage.getItem('mobileRedirectDone')) {
    sessionStorage.setItem('mobileRedirectDone', 'true');
    setTimeout(() => {
        window.location.href = '/';
    }, 100);
}
```

**Replace With:**
```javascript
// Use localStorage instead of sessionStorage (more reliable in iOS Safari)
const redirectKey = 'streamlit_mobile_redirect_done';
const hasRedirected = localStorage.getItem(redirectKey);

if (isOnSubPage && !hasRedirected) {
    localStorage.setItem(redirectKey, 'true');
    // Use replace instead of href to avoid back button issues
    setTimeout(() => {
        window.location.replace('/');
    }, 50);
}

// Clean up redirect flag when leaving app
window.addEventListener('beforeunload', function() {
    if (window.location.pathname === '/' || window.location.pathname === '/app') {
        localStorage.removeItem(redirectKey);
    }
});
```

**Also optimize MutationObserver:**
```javascript
// REPLACE THIS (line 785):
observer.observe(document.body, { childList: true, subtree: true });

// WITH THIS:
const sidebarContainer = document.querySelector('[data-testid="stSidebar"]');
if (sidebarContainer) {
    observer.observe(sidebarContainer, {
        childList: true,
        attributes: true,
        attributeFilter: ['style', 'class'],
        subtree: false  // Don't watch entire subtree
    });
}
```

---

### 3. Standardize Sidebar State (HIGH PRIORITY)

**File:** `app.py`  
**Line:** 33  
**Change:**
```python
initial_sidebar_state="collapsed"  # OLD
```
**To:**
```python
initial_sidebar_state="auto"  # NEW
```

**Files to Update:** All page files in `pages/` directory  
**Find:** `initial_sidebar_state="expanded"`  
**Replace:** `initial_sidebar_state="auto"`

**Affected Files:**
- `pages/6_🤖_AI_Executive_Insights.py` (line 29)
- `pages/19_⚖️_Health_Equity_Index.py` (line 30)
- `pages/15_🔄_Gap_Closure_Workflow.py` (line 27)
- `pages/10_📈_Historical_Tracking.py` (line 21)
- `pages/z_Performance_Dashboard.py` (line 20)
- `pages/8_📋_Campaign_Builder.py` (line 21)
- `pages/7_📊_What-If_Scenario_Modeler.py` (line 29)
- `pages/16_🤖_ML_Gap_Closure_Predictions.py` (line 22)
- `pages/14_⭐_Star_Rating_Simulator.py` (line 21)
- `pages/13_📋_Measure_Analysis.py` (line 33)
- `pages/11_💰_ROI_Calculator.py` (line 22)
- `pages/9_🔔_Alert_Center.py` (line 19)

---

### 4. Remove CSS :has() Selectors (MEDIUM PRIORITY)

**File:** `app.py`  
**Lines:** 143, 149, 874  

**Find and Remove:**
```css
[data-testid="column"]:has([data-testid="stMetricContainer"]) {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

[data-testid="column"]:has([data-testid="stMetric"]) {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

.element-container:has([data-testid="stExpander"]) {
    margin-bottom: 0 !important;
}
```

**Replace With:**
```css
.metric-column {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

.expander-container {
    margin-bottom: 0 !important;
}
```

**Add JavaScript (after CSS):**
```javascript
<script>
(function() {
    function addHelperClasses() {
        // Add metric-column class
        document.querySelectorAll('[data-testid="column"]').forEach(col => {
            if (col.querySelector('[data-testid="stMetric"], [data-testid="stMetricContainer"]')) {
                col.classList.add('metric-column');
            }
        });
        
        // Add expander-container class
        document.querySelectorAll('.element-container').forEach(container => {
            if (container.querySelector('[data-testid="stExpander"]')) {
                container.classList.add('expander-container');
            }
        });
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addHelperClasses);
    } else {
        addHelperClasses();
    }
    
    // Watch for dynamically added elements
    const observer = new MutationObserver(addHelperClasses);
    observer.observe(document.body, { childList: true, subtree: true });
})();
</script>
```

---

### 5. Add WebSocket Reconnection Handler (MEDIUM PRIORITY)

**File:** `app.py`  
**Location:** After mobile detection script (around line 818)

**Add:**
```javascript
<script>
(function() {
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 3;
    
    function checkConnection() {
        const hasErrors = document.querySelectorAll('[data-testid="stException"]').length > 0;
        const isResponsive = document.body && document.body.children.length > 0;
        
        if ((hasErrors || !isResponsive) && reconnectAttempts < maxReconnectAttempts) {
            reconnectAttempts++;
            setTimeout(() => window.location.reload(), 2000);
        } else {
            reconnectAttempts = 0;
        }
    }
    
    setInterval(checkConnection, 10000);
    
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            setTimeout(checkConnection, 500);
        }
    });
})();
</script>
```

---

### 6. Add iOS Safari Viewport Fix (LOW PRIORITY)

**File:** `app.py`  
**Location:** In CSS section (around line 40)

**Add to CSS:**
```css
:root {
    --vh: 1vh; /* Fallback */
}
```

**Add JavaScript (after CSS):**
```javascript
<script>
(function() {
    function setViewportHeight() {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    
    setViewportHeight();
    
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(setViewportHeight, 100);
    });
    
    window.addEventListener('orientationchange', function() {
        setTimeout(setViewportHeight, 200);
    });
})();
</script>
```

---

### 7. Create Streamlit Config File (RECOMMENDED)

**File:** `.streamlit/config.toml`  
**Create new file with:**

```toml
[server]
enableCORS = false
enableXsrfProtection = false
port = 8502
address = "0.0.0.0"
runOnSave = true
runOnSaveTimeout = 2.0

[browser]
gatherUsageStats = false
serverAddress = "192.168.1.161"
serverPort = 8502
```

---

## Testing Checklist

After applying fixes, test on iOS Safari:

- [ ] App loads without privacy warning (or acceptable warning)
- [ ] Home page loads correctly (not sidebar)
- [ ] Navigation between pages works
- [ ] Sidebar stays hidden on mobile
- [ ] No redirect loops
- [ ] Page loads in < 3 seconds
- [ ] WebSocket connection stays active
- [ ] No console errors in Safari Web Inspector
- [ ] Orientation changes work correctly
- [ ] Touch interactions work properly

---

## Quick Test Command

After making changes, restart Streamlit:
```bash
# Stop current instance (Ctrl+C)
# Then restart:
streamlit run app.py --server.port 8502
```

Test on iPhone Safari by navigating to: `http://192.168.1.161:8502`

---

## Priority Order

1. **Fix 1** - Session state clearing (CRITICAL - causes slow loading)
2. **Fix 2** - Mobile redirect (CRITICAL - causes navigation issues)
3. **Fix 3** - Sidebar state (HIGH - causes sidebar to show incorrectly)
4. **Fix 4** - CSS :has() (MEDIUM - causes styling issues)
5. **Fix 5** - WebSocket reconnection (MEDIUM - improves reliability)
6. **Fix 6** - Viewport height (LOW - improves UX)
7. **Fix 7** - Config file (RECOMMENDED - improves server behavior)

---

## Notes

- Test each fix individually to identify which resolves specific issues
- iOS Safari may cache aggressively - clear cache between tests
- Use Safari Web Inspector (Settings > Safari > Advanced > Web Inspector) for debugging
- Private browsing mode may have different behavior - test both modes




