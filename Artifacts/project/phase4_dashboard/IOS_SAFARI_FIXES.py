"""
iOS Safari Compatibility Fixes
Apply these fixes to resolve iOS Safari issues

CRITICAL FIXES - Apply in order:
1. Fix session state clearing
2. Fix mobile redirect logic  
3. Standardize sidebar state
4. Remove CSS :has() selectors
5. Optimize MutationObserver
"""

# ============================================================================
# FIX 1: Session State Clearing (app.py:1101-1103)
# ============================================================================
# REPLACE THIS:
"""
if 'initialized' not in st.session_state:
    st.session_state.clear()
    st.session_state.initialized = True
"""

# WITH THIS:
def initialize_session_state_safely():
    """Initialize session state without clearing navigation state"""
    if 'initialized' not in st.session_state:
        # Preserve critical navigation state
        preserved_keys = ['mobile_redirected', 'initialized']
        preserved_state = {
            k: st.session_state.get(k) 
            for k in preserved_keys 
            if k in st.session_state
        }
        
        # Clear only non-critical state
        keys_to_clear = [
            k for k in st.session_state.keys() 
            if k not in preserved_keys
        ]
        for key in keys_to_clear:
            del st.session_state[key]
        
        # Restore preserved state
        st.session_state.update(preserved_state)
        st.session_state.initialized = True

# Usage in app.py:
# initialize_session_state_safely()


# ============================================================================
# FIX 2: Mobile Redirect Logic (app.py:743-817)
# ============================================================================
# REPLACE JavaScript redirect with Python-based redirect

def handle_mobile_redirect():
    """Handle mobile redirect server-side for better iOS Safari compatibility"""
    import streamlit as st
    
    # Initialize redirect state
    if 'mobile_redirected' not in st.session_state:
        st.session_state.mobile_redirected = False
    
    # Detect mobile using request headers (server-side)
    user_agent = ""
    try:
        # Try to get user agent from request headers
        if hasattr(st, 'request_headers'):
            user_agent = st.request_headers.get('User-Agent', '').lower()
        elif hasattr(st, 'server') and hasattr(st.server, 'request'):
            user_agent = st.server.request.headers.get('User-Agent', '').lower()
    except:
        pass
    
    is_mobile = any(x in user_agent for x in ['iphone', 'ipad', 'ipod', 'mobile'])
    
    # Check if we're on a sub-page
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        if ctx:
            current_page = getattr(ctx, 'current_page_name', None)
            is_sub_page = current_page and current_page != 'app' and current_page != 'app.py'
            
            if is_mobile and is_sub_page and not st.session_state.mobile_redirected:
                st.session_state.mobile_redirected = True
                # Use switch_page if available (Streamlit 1.28+)
                try:
                    st.switch_page("app.py")
                except:
                    # Fallback: Use JavaScript redirect with better handling
                    st.markdown("""
                    <script>
                    if (window.location.pathname !== '/' && 
                        window.location.pathname !== '/app' &&
                        !window.location.hash.includes('mobile-redirected')) {
                        window.location.hash = '#mobile-redirected';
                        window.location.replace('/');
                    }
                    </script>
                    """, unsafe_allow_html=True)
    except Exception as e:
        # Fallback to JavaScript if server-side detection fails
        pass

# Usage in app.py (after st.set_page_config, before sidebar):
# handle_mobile_redirect()


# ============================================================================
# FIX 3: Improved Mobile Detection JavaScript (app.py:743-817)
# ============================================================================
# REPLACE existing mobile detection script with this improved version

IMPROVED_MOBILE_DETECTION_SCRIPT = """
<script>
(function() {
    'use strict';
    
    // More reliable mobile detection for iOS Safari
    const isMobile = window.innerWidth <= 768 || 
                     /iPhone|iPad|iPod|Android/i.test(navigator.userAgent) ||
                     (window.matchMedia && window.matchMedia("(max-width: 768px)").matches);
    
    if (!isMobile) return; // Exit early if not mobile
    
    // Hide sidebar function - optimized for iOS Safari
    function hideSidebar() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.style.display = 'none';
            sidebar.style.visibility = 'hidden';
            sidebar.style.opacity = '0';
            sidebar.setAttribute('aria-hidden', 'true');
        }
        
        // Hide sidebar toggle button
        const buttons = document.querySelectorAll('button[aria-label]');
        buttons.forEach(btn => {
            const label = (btn.getAttribute('aria-label') || '').toLowerCase();
            if (label.includes('sidebar') || label.includes('menu')) {
                btn.style.display = 'none';
            }
        });
    }
    
    // Hide sidebar immediately
    hideSidebar();
    
    // Use requestAnimationFrame for better iOS Safari performance
    function scheduleHideSidebar() {
        requestAnimationFrame(hideSidebar);
    }
    
    // Hide on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', scheduleHideSidebar);
    } else {
        scheduleHideSidebar();
    }
    
    // Optimized MutationObserver - only watch sidebar container
    const sidebarContainer = document.querySelector('[data-testid="stSidebar"]');
    if (sidebarContainer) {
        const observer = new MutationObserver(function(mutations) {
            // Only hide if sidebar becomes visible
            if (sidebarContainer.style.display !== 'none') {
                hideSidebar();
            }
        });
        
        observer.observe(sidebarContainer, {
            childList: true,
            attributes: true,
            attributeFilter: ['style', 'class'],
            subtree: false  // Don't watch entire subtree
        });
    }
    
    // Handle redirect - use replace instead of href for iOS Safari
    const currentPath = window.location.pathname;
    const isOnSubPage = currentPath.includes('/pages/') || 
                       (currentPath !== '/' && currentPath !== '/app' && currentPath !== '/app.py');
    
    // Use localStorage instead of sessionStorage (more reliable in iOS Safari)
    const redirectKey = 'streamlit_mobile_redirect_done';
    const hasRedirected = localStorage.getItem(redirectKey);
    
    if (isOnSubPage && !hasRedirected) {
        localStorage.setItem(redirectKey, 'true');
        // Use replace to avoid back button issues
        setTimeout(() => {
            window.location.replace('/');
        }, 50);  // Reduced delay for faster redirect
    }
    
    // Clean up redirect flag when leaving app
    window.addEventListener('beforeunload', function() {
        if (window.location.pathname === '/' || window.location.pathname === '/app') {
            localStorage.removeItem(redirectKey);
        }
    });
    
    // Handle resize events - debounced for performance
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth <= 768) {
                hideSidebar();
            }
        }, 250);
    });
    
    // Handle orientation change (iOS Safari specific)
    window.addEventListener('orientationchange', function() {
        setTimeout(hideSidebar, 100);
    });
})();
</script>
"""

# Usage in app.py:
# st.markdown(IMPROVED_MOBILE_DETECTION_SCRIPT, unsafe_allow_html=True)


# ============================================================================
# FIX 4: Standardize Sidebar State
# ============================================================================
# In app.py, change:
# initial_sidebar_state="collapsed"
# TO:
# initial_sidebar_state="auto"

# In all page files, change:
# initial_sidebar_state="expanded"  
# TO:
# initial_sidebar_state="auto"


# ============================================================================
# FIX 5: Remove CSS :has() Selectors
# ============================================================================
# REPLACE CSS like this:
"""
[data-testid="column"]:has([data-testid="stMetricContainer"]) {
    display: flex !important;
}
"""

# WITH JavaScript-based class addition:
CSS_WITHOUT_HAS = """
<style>
.metric-column {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

/* Remove all :has() selectors and use classes instead */
</style>
"""

JAVASCRIPT_FOR_METRIC_COLUMNS = """
<script>
(function() {
    // Add metric-column class to columns containing metrics
    function addMetricColumnClass() {
        const columns = document.querySelectorAll('[data-testid="column"]');
        columns.forEach(col => {
            const hasMetric = col.querySelector('[data-testid="stMetric"], [data-testid="stMetricContainer"]');
            if (hasMetric) {
                col.classList.add('metric-column');
            }
        });
    }
    
    // Run on load and when DOM changes
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addMetricColumnClass);
    } else {
        addMetricColumnClass();
    }
    
    // Watch for dynamically added metrics
    const observer = new MutationObserver(addMetricColumnClass);
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
})();
</script>
"""


# ============================================================================
# FIX 6: WebSocket Reconnection Handler
# ============================================================================
WEBSOCKET_RECONNECTION_SCRIPT = """
<script>
(function() {
    'use strict';
    
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 3;
    const reconnectDelay = 2000;
    
    function checkWebSocketConnection() {
        // Check if Streamlit is connected
        // Look for connection indicators or errors
        const errorElements = document.querySelectorAll('[data-testid="stException"], .stException');
        const hasErrors = errorElements.length > 0;
        
        // Check if page is responsive
        const isPageResponsive = document.body && document.body.children.length > 0;
        
        if (hasErrors || !isPageResponsive) {
            if (reconnectAttempts < maxReconnectAttempts) {
                reconnectAttempts++;
                console.log(`WebSocket issue detected, attempt ${reconnectAttempts}/${maxReconnectAttempts}`);
                
                setTimeout(() => {
                    // Try to reconnect by reloading
                    window.location.reload();
                }, reconnectDelay);
            }
        } else {
            reconnectAttempts = 0; // Reset on successful connection
        }
    }
    
    // Check connection periodically (less frequent for iOS Safari)
    setInterval(checkWebSocketConnection, 10000); // Every 10 seconds
    
    // Also check when page becomes visible (iOS Safari specific)
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            setTimeout(checkWebSocketConnection, 500);
        }
    });
    
    // Check on focus (iOS Safari may suspend connections)
    window.addEventListener('focus', function() {
        setTimeout(checkWebSocketConnection, 500);
    });
})();
</script>
"""


# ============================================================================
# FIX 7: iOS Safari Viewport Height Fix
# ============================================================================
VIEWPORT_HEIGHT_FIX = """
<script>
(function() {
    'use strict';
    
    function setViewportHeight() {
        // iOS Safari address bar causes vh issues
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    
    // Set initially
    setViewportHeight();
    
    // Update on resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(setViewportHeight, 100);
    });
    
    // Update on orientation change (iOS Safari specific)
    window.addEventListener('orientationchange', function() {
        setTimeout(setViewportHeight, 200);
    });
    
    // Update on scroll (address bar may hide/show)
    let scrollTimer;
    window.addEventListener('scroll', function() {
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(setViewportHeight, 150);
    });
})();
</script>

<style>
/* Use CSS variable instead of vh */
.block-container {
    min-height: calc(var(--vh, 1vh) * 100) !important;
}
</style>
"""


# ============================================================================
# CONFIG FILE: .streamlit/config.toml
# ============================================================================
STREAMLIT_CONFIG_TOML = """
# Streamlit Configuration for iOS Safari Compatibility
[server]
# Disable CORS for local network access
enableCORS = false
# Disable XSRF protection for local development
enableXsrfProtection = false
# Port configuration
port = 8502
address = "0.0.0.0"
# Increase timeout for slow connections
runOnSave = true
runOnSaveTimeout = 2.0

[browser]
# Disable usage stats collection
gatherUsageStats = false
# Server address (use your local IP)
serverAddress = "192.168.1.161"
serverPort = 8502

[theme]
# Optional: Set theme for better mobile experience
primaryColor = "#4A3D6F"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
"""


# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================
"""
To apply these fixes:

1. Copy initialize_session_state_safely() to app.py and replace the clearing logic
2. Copy handle_mobile_redirect() to app.py and call it after st.set_page_config()
3. Replace the mobile detection script with IMPROVED_MOBILE_DETECTION_SCRIPT
4. Change all initial_sidebar_state to "auto"
5. Remove :has() CSS selectors and use JavaScript class addition instead
6. Add WEBSOCKET_RECONNECTION_SCRIPT to app.py
7. Add VIEWPORT_HEIGHT_FIX to app.py
8. Create .streamlit/config.toml with STREAMLIT_CONFIG_TOML content

Test on iOS Safari after each fix to verify improvement.
"""




