"""
Add common components (JavaScript fix, sidebar styling, imports) to all pages
"""
import os
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Common components template (inserted after header HTML)
COMMON_COMPONENTS = '''
import sys
from pathlib import Path

# Fix Python path for Streamlit pages - ensure utils can be imported
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import pandas as pd
import numpy as np
from datetime import datetime

# Core imports
from utils.database import execute_query
from utils.data_helpers import show_data_availability_warning, get_data_date_range, format_date_display
from utils.plan_context import get_plan_context, get_plan_size_scenarios

# UI component imports with error handling
try:
    from src.ui.compact_components import compact_metric_card, compact_insight_box
except ImportError:
    # Define fallback functions
    def compact_metric_card(*args, **kwargs):
        return ""
    def compact_insight_box(*args, **kwargs):
        return ""

try:
    from utils.sidebar_styling import apply_sidebar_styling
except ImportError:
    def apply_sidebar_styling():
        pass

try:
    from utils.page_components_FIXED import add_page_footer
    # add_mobile_ready_badge removed - badge no longer needed
except ImportError:
    def add_page_footer():
        st.markdown("---")
        st.markdown("**HEDIS Portfolio Optimizer | StarGuard AI**")
    # def add_mobile_ready_badge():
    #     st.markdown("---")
    #     st.markdown("📱 Mobile Version Ready")

# ============================================================================
# ADDITIONAL JAVASCRIPT FIX FOR PERFORMANCE DASHBOARD EMOJI
# ============================================================================
st.markdown("""
<script>
// Fix Performance Dashboard emoji rendering - Enhanced version
(function() {
    'use strict';
    
    function fixPerformanceDashboardEmoji() {
        // Find all sidebar links
        const sidebarLinks = document.querySelectorAll('[data-testid="stSidebarNav"] a');
        
        sidebarLinks.forEach(link => {
            const href = link.getAttribute('href') || '';
            const text = (link.textContent || link.innerText || '').trim();
            
            // Check if this is the Performance Dashboard link (by href - most reliable)
            const isPerformanceDashboard = (
                href.includes('Performance_Dashboard') ||
                href.includes('Performance-Dashboard') ||
                href.toLowerCase().includes('performance') && href.toLowerCase().includes('dashboard')
            );
            
            // Also check by text as backup
            const textMatches = (
                text === 'Performance Dashboard' ||
                text.includes('Performance Dashboard') ||
                text.match(/Performance\\s*Dashboard/i)
            );
            
            const hasEmoji = text.includes('⚡') || text.includes('\\u26A1') || link.innerHTML.includes('⚡');
            
            // If it's Performance Dashboard but missing emoji, add it
            if ((isPerformanceDashboard || textMatches) && !hasEmoji) {
                // Method 1: Clear and rebuild the entire link content
                const originalHTML = link.innerHTML;
                
                // Try to preserve any icons/spans but update text
                if (link.querySelector('span, div')) {
                    // Has child elements - update them
                    const children = link.querySelectorAll('span, div, p');
                    children.forEach(child => {
                        const childText = (child.textContent || child.innerText || '').trim();
                        if (childText === 'Performance Dashboard' || childText.includes('Performance Dashboard')) {
                            child.textContent = '⚡ Performance Dashboard';
                            child.innerText = '⚡ Performance Dashboard';
                        }
                    });
                } else {
                    // No children - replace entire content
                    link.textContent = '⚡ Performance Dashboard';
                    link.innerText = '⚡ Performance Dashboard';
                }
                
                // Method 2: Use innerHTML as backup
                if (!link.textContent.includes('⚡')) {
                    link.innerHTML = '⚡ Performance Dashboard';
                }
                
                // Method 3: Create a new text node
                const newText = document.createTextNode('⚡ Performance Dashboard');
                if (link.childNodes.length === 0 || !link.textContent.includes('⚡')) {
                    link.innerHTML = '';
                    link.appendChild(newText);
                }
                
                // Force proper font rendering
                link.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI Emoji", "Segoe UI", sans-serif';
                link.style.whiteSpace = 'normal';
                
                // Add data attribute to mark as fixed
                link.setAttribute('data-emoji-fixed', 'true');
            }
        });
    }
    
    // Run immediately
    fixPerformanceDashboardEmoji();
    
    // Run on DOM changes (Streamlit reruns)
    const observer = new MutationObserver(function() {
        fixPerformanceDashboardEmoji();
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        characterData: true
    });
    
    // Also run after delays to catch late-rendering elements
    setTimeout(fixPerformanceDashboardEmoji, 50);
    setTimeout(fixPerformanceDashboardEmoji, 100);
    setTimeout(fixPerformanceDashboardEmoji, 300);
    setTimeout(fixPerformanceDashboardEmoji, 500);
    setTimeout(fixPerformanceDashboardEmoji, 1000);
    setTimeout(fixPerformanceDashboardEmoji, 2000);
    setTimeout(fixPerformanceDashboardEmoji, 3000);
    
    // Periodic check as backup (every 2 seconds)
    setInterval(fixPerformanceDashboardEmoji, 2000);
    
    // Also run when page becomes visible (user switches tabs back)
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            setTimeout(fixPerformanceDashboardEmoji, 100);
        }
    });
})();

// ====================================================================
// FORCE DATE INPUT VISIBILITY - DARK TEXT ON WHITE BACKGROUND
// ====================================================================
function forceDateInputVisibility() {
    // Find all date inputs in sidebar
    const sidebarDateInputs = document.querySelectorAll('[data-testid="stSidebar"] [data-testid="stDateInput"] input, [data-testid="stSidebar"] .stDateInput input');
    
    sidebarDateInputs.forEach(input => {
        // Force dark text on white background
        input.style.color = '#1f2937';
        input.style.setProperty('color', '#1f2937', 'important');
        input.style.setProperty('-webkit-text-fill-color', '#1f2937', 'important');
        input.style.backgroundColor = 'white';
        input.style.setProperty('background-color', 'white', 'important');
        
        // Also target parent containers
        const parent = input.closest('[data-testid="stDateInput"]') || input.closest('.stDateInput');
        if (parent) {
            // Make container background white
            parent.style.backgroundColor = 'white';
            parent.style.setProperty('background-color', 'white', 'important');
            
            // Find BaseWeb input wrapper
            const baseWebInput = parent.querySelector('[data-baseweb="input"]');
            if (baseWebInput) {
                baseWebInput.style.backgroundColor = 'white';
                baseWebInput.style.setProperty('background-color', 'white', 'important');
                
                const baseWebInputField = baseWebInput.querySelector('input');
                if (baseWebInputField) {
                    baseWebInputField.style.color = '#1f2937';
                    baseWebInputField.style.setProperty('color', '#1f2937', 'important');
                    baseWebInputField.style.setProperty('-webkit-text-fill-color', '#1f2937', 'important');
                    baseWebInputField.style.backgroundColor = 'white';
                }
            }
            
            // Keep labels white
            const labels = parent.querySelectorAll('label');
            labels.forEach(label => {
                label.style.color = '#ffffff';
                label.style.setProperty('color', '#ffffff', 'important');
            });
        }
    });
    
    // Fix captions (days selected)
    const captions = document.querySelectorAll('[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p, [data-testid="stSidebar"] .stCaption p');
    captions.forEach(caption => {
        caption.style.color = '#ffffff';
        caption.style.setProperty('color', '#ffffff', 'important');
    });
}

// Run immediately and on delays
forceDateInputVisibility();
setTimeout(forceDateInputVisibility, 100);
setTimeout(forceDateInputVisibility, 500);
setTimeout(forceDateInputVisibility, 1000);
setTimeout(forceDateInputVisibility, 2000);

// Watch for new date inputs being added
const dateInputObserver = new MutationObserver(function() {
    forceDateInputVisibility();
});

dateInputObserver.observe(document.body, {
    childList: true,
    subtree: true
});

// Also run periodically
setInterval(forceDateInputVisibility, 2000);
</script>
""", unsafe_allow_html=True)

# Purple Sidebar Theme + White Text Everywhere
st.markdown("""
<style>
/* ========== PURPLE SIDEBAR THEME ========== */
/* Match the StarGuard AI header purple gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

/* ========== ALL SIDEBAR TEXT WHITE ========== */
/* Force ALL text in sidebar to be white */
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] button {
    color: #FFFFFF !important;
}

/* Sidebar date input fields - white text for dates */
[data-testid="stSidebar"] .stDateInput input,
[data-testid="stSidebar"] .stDateInput input[type="text"],
[data-testid="stSidebar"] .stDateInput input[type="date"],
[data-testid="stSidebar"] .stDateInput div[data-baseweb="input"] input,
[data-testid="stSidebar"] .stDateInput div[data-baseweb="input"] input::placeholder,
[data-testid="stSidebar"] .stDateInput div[data-baseweb="input"] > div input,
[data-testid="stSidebar"] [data-testid="stDateInput"] input,
[data-testid="stSidebar"] [data-testid="stDateInput"] input[type="text"],
[data-testid="stSidebar"] [data-testid="stDateInput"] div input {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Date input value text - ensure it's visible */
[data-testid="stSidebar"] .stDateInput input::value,
[data-testid="stSidebar"] .stDateInput input::-webkit-input-placeholder,
[data-testid="stSidebar"] .stDateInput input::-moz-placeholder,
[data-testid="stSidebar"] .stDateInput input:-ms-input-placeholder {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

/* ========== FORCE DATE INPUT VISIBILITY IN SIDEBAR ========== */

/* Date input container in sidebar */
[data-testid="stSidebar"] [data-testid="stDateInput"] {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-radius: 5px !important;
    padding: 2px !important;
}

/* Date input label - make it white on purple sidebar */
[data-testid="stSidebar"] [data-testid="stDateInput"] label {
    color: white !important;
    font-weight: 500 !important;
}

/* The actual date input field - dark text on white background */
[data-testid="stSidebar"] [data-testid="stDateInput"] input {
    color: #1f2937 !important;
    background-color: white !important;
    border: 1px solid #d1d5db !important;
    border-radius: 4px !important;
    padding: 0.5rem !important;
    font-size: 0.9rem !important;
    -webkit-text-fill-color: #1f2937 !important;
}

/* Date input box wrapper */
[data-testid="stSidebar"] [data-testid="stDateInput"] > div > div {
    background-color: white !important;
}

/* Ensure the date text is dark and visible */
[data-testid="stSidebar"] [data-testid="stDateInput"] [data-baseweb="input"] {
    background-color: white !important;
}

[data-testid="stSidebar"] [data-testid="stDateInput"] [data-baseweb="input"] input {
    color: #1f2937 !important;
    -webkit-text-fill-color: #1f2937 !important;
}

/* Date picker button/icon */
[data-testid="stSidebar"] [data-testid="stDateInput"] button {
    color: #4A3D6F !important;
    background-color: white !important;
}

/* Calendar icon */
[data-testid="stSidebar"] [data-testid="stDateInput"] svg {
    fill: #4A3D6F !important;
    color: #4A3D6F !important;
}

/* Make the "91 days selected" caption visible */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: white !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: white !important;
    font-size: 0.85rem !important;
}

/* Section header "📅 Date Range" styling */
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .sidebar-section-header {
    color: white !important;
    font-size: 1rem !important;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
}

/* Alternative: Target BaseWeb date input specifically */
[data-testid="stSidebar"] [data-baseweb="base-input"] {
    background-color: white !important;
}

[data-testid="stSidebar"] [data-baseweb="base-input"] input {
    color: #1f2937 !important;
    -webkit-text-fill-color: #1f2937 !important;
}

/* Fix any transparent backgrounds */
[data-testid="stSidebar"] .stDateInput > div {
    background-color: white !important;
    border-radius: 5px !important;
}

[data-testid="stSidebar"] .stDateInput input {
    color: #1f2937 !important;
    background-color: white !important;
    -webkit-text-fill-color: #1f2937 !important;
}

/* Date input labels stay white */
[data-testid="stSidebar"] .stDateInput label,
[data-testid="stSidebar"] [data-testid="stDateInput"] label {
    color: #FFFFFF !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}

/* Date input container children - labels white, inputs dark */
[data-testid="stSidebar"] .stDateInput span:not(input),
[data-testid="stSidebar"] .stDateInput div:not([data-baseweb="input"]):not(input),
[data-testid="stSidebar"] .stDateInput p {
    color: #FFFFFF !important;
}

/* ========== ENSURE DATE RANGE LABELS ARE VISIBLE ========== */
/* Force all paragraphs in sidebar to be white (covers custom date labels) */
[data-testid="stSidebar"] p {
    color: #FFFFFF !important;
}

/* Specifically target custom date labels */
[data-testid="stSidebar"] p[style*="Start Date"],
[data-testid="stSidebar"] p[style*="End Date"] {
    color: #FFFFFF !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

/* ========== WHITE "HOME" LABEL ========== */
[data-testid="stSidebarNav"] ul li:first-child a {
    font-size: 0 !important;
    background: rgba(255, 255, 255, 0.2) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    margin-bottom: 0rem !important;
}

[data-testid="stSidebarNav"] ul li:first-child a::before {
    content: "🏠 Home" !important;
    font-size: 1.1rem !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    display: block !important;
    -webkit-text-fill-color: #FFFFFF !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
}

/* All sidebar navigation links white */
[data-testid="stSidebarNav"] a {
    color: #FFFFFF !important;
}

[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a div,
[data-testid="stSidebarNav"] a p {
    color: #FFFFFF !important;
}

/* CSS Backup: Add emoji via ::before for Performance Dashboard links */
[data-testid="stSidebarNav"] a[href*="Performance_Dashboard"]::before {
    content: "⚡ " !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI Emoji", "Apple Color Emoji", sans-serif !important;
    display: inline !important;
}

/* Success/Info boxes in sidebar - white text */
[data-testid="stSidebar"] [data-testid="stSuccess"],
[data-testid="stSidebar"] [data-testid="stInfo"] {
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}

[data-testid="stSidebar"] [data-testid="stSuccess"] *,
[data-testid="stSidebar"] [data-testid="stInfo"] * {
    color: #FFFFFF !important;
}

/* View less/more links - white */
[data-testid="stSidebar"] button {
    color: #FFFFFF !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
}

/* ========== SIDEBAR SEPARATOR STYLING - SUBTLE GREEN GRADIENT ========== */
/* Sidebar separator styling - subtle green gradient (thicker for visibility) */
[data-testid="stSidebar"] hr {
    border: none !important;
    height: 4px !important;
    margin: 1rem 0 !important;
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(74, 222, 128, 0.8) 50%,
        transparent 100%
    ) !important;
}

</style>
""", unsafe_allow_html=True)

# Apply sidebar styling FIRST (purple gradient matching StarGuard AI header)
apply_sidebar_styling()

# Sidebar content (matching app.py pattern)
with st.sidebar:
    st.markdown("<p style='color: white; font-size: 1rem; font-weight: 600;'>🎛️ Filters</p>", unsafe_allow_html=True)
    
    # Membership Size Control
    st.markdown("### 👥 Plan Membership Size")
    membership_size = st.slider(
        "Membership Size",
        min_value=5000,
        max_value=200000,
        value=st.session_state.get('membership_size', 10000),
        step=5000,
        key="membership_slider",
        help="Adjust to scale calculations for different plan sizes"
    )
    st.session_state.membership_size = membership_size
    st.caption(f"📊 Scaling calculations to {membership_size:,} members")
    
    st.markdown("---")
    
    # Date Range Filters
    st.markdown("<h3 style='color: white; margin: 1rem 0 0.5rem 0;'>📅 Date Range</h3>", unsafe_allow_html=True)
    
    date_col1, date_col2 = st.columns(2, gap="small")
    
    with date_col1:
        # Explicitly show Start Date label
        st.markdown("<p style='color: white; font-size: 0.9rem; font-weight: 500; margin-bottom: 0.25rem;'>Start Date</p>", unsafe_allow_html=True)
        start_date_sidebar = st.date_input(
            "Start Date",
            value=st.session_state.get('sidebar_start_date', datetime(2024, 10, 1)),
            key="sidebar_start_date",
            format="MM/DD/YYYY",
            label_visibility="collapsed"  # Hide default label, we use custom above
        )
    
    with date_col2:
        # Explicitly show End Date label
        st.markdown("<p style='color: white; font-size: 0.9rem; font-weight: 500; margin-bottom: 0.25rem;'>End Date</p>", unsafe_allow_html=True)
        end_date_sidebar = st.date_input(
            "End Date",
            value=st.session_state.get('sidebar_end_date', datetime(2024, 12, 31)),
            key="sidebar_end_date",
            format="MM/DD/YYYY",
            label_visibility="collapsed"  # Hide default label, we use custom above
        )
    
    if start_date_sidebar <= end_date_sidebar:
        days = (end_date_sidebar - start_date_sidebar).days
        st.markdown(f"<p style='color: white; font-size: 0.85rem; margin-top: 0.5rem;'>📆 {days} days selected</p>", unsafe_allow_html=True)
    else:
        st.error("⚠️ Start date must be before end date")
    
    st.markdown("---")
    
    # Database Status
    try:
        from utils.database import get_connection
        conn, count = get_connection()
        if conn:
            st.success(f"✅ Database Connected ({count:,} records)")
        else:
            st.warning("⚠️ Database connection issue")
    except Exception as e:
        st.warning("⚠️ Database status unavailable")
    
    st.markdown("---")
    
    # Sidebar footer content (matching app.py)
    st.markdown("**Built by:** Robert Reichert")
    st.markdown("**Version:** 4.0")
    
    st.markdown("---")
    
    # Secure AI Architect box - moved to bottom
    st.sidebar.markdown("""
    <style>
    #secure-ai-box, #secure-ai-box * { color: #000 !important; }
    </style>
    <div id='secure-ai-box' style='background: #e8f5e9; padding: 12px; border-radius: 12px; margin: 16px auto; text-align: center; border: 2px solid #4caf50; max-width: 280px;'>
        <div style='color: #000 !important; font-weight: 700; font-size: 1.1rem; margin-bottom: 8px;'><font color='#000000'>🔒 Secure AI Architect</font></div>
        <div style='color: #000 !important; font-size: 0.85rem; line-height: 1.5;'><font color='#000000'>Healthcare AI insights without data exposure. On-premises intelligence delivering 2.8-4.1x ROI and full HIPAA compliance.</font></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Rounded rectangle Mobile Optimized badge at END of sidebar (hidden on mobile)
    st.sidebar.markdown("""
    <style>
    @media (max-width: 768px) {
        .mobile-optimized-badge { display: none !important; }
    }
    </style>
    <div class='mobile-optimized-badge' style='background: linear-gradient(135deg, #10B981 0%, #059669 100%); border-radius: 50px; padding: 10px 24px; text-align: center; margin: 24px auto; color: white; font-weight: 700; font-size: 1rem; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4); border: 3px solid rgba(255, 255, 255, 0.5); max-width: 220px; display: inline-block;'>
        📱 Mobile Optimized
    </div>
    """, unsafe_allow_html=True)

# Get membership size from session state (set by sidebar slider)
membership_size = st.session_state.get('membership_size', 10000)
BASELINE_MEMBERS = 10000
scale_factor = membership_size / BASELINE_MEMBERS

# Get date range from sidebar (widgets automatically update session state)
start_date = st.session_state.get('sidebar_start_date', datetime(2024, 10, 1))
end_date = st.session_state.get('sidebar_end_date', datetime(2024, 12, 31))
'''

def add_common_components(file_path):
    """Add common components to a page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if common components already exist
        if 'fixPerformanceDashboardEmoji' in content and 'apply_sidebar_styling' in content:
            return False, "Already has common components"
        
        # Find where to insert (after header HTML)
        header_marker = '</div>\n""", unsafe_allow_html=True)'
        header_end = content.find(header_marker)
        
        if header_end == -1:
            return False, "Header HTML not found"
        
        # Insert position is after the header closing
        insert_pos = header_end + len(header_marker)
        
        # Insert common components
        new_content = content[:insert_pos] + COMMON_COMPONENTS + content[insert_pos:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Added common components"
            
    except Exception as e:
        return None, str(e)

def main():
    """Process all page files"""
    pages_dir = Path(__file__).parent / 'pages'
    
    if not pages_dir.exists():
        print(f"Error: {pages_dir} does not exist")
        return
    
    print("Adding common components to all pages...")
    print("=" * 60)
    
    # Exclude already complete files
    excluded_files = ['1_📊_ROI_by_Measure.py', '2_💰_Cost_Per_Closure.py']
    
    page_files = sorted([
        f for f in pages_dir.glob('*.py') 
        if f.name != '__init__.py' and f.name not in excluded_files
    ])
    
    stats = {
        'added': 0,
        'skipped': 0,
        'errors': 0
    }
    
    for page_file in page_files:
        result, info = add_common_components(page_file)
        
        if result is True:
            print(f"[ADDED] {page_file.name}")
            stats['added'] += 1
        elif result is False:
            print(f"[SKIP] {page_file.name} - {info}")
            stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_file.name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  Added: {stats['added']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total: {len(page_files)} files")

if __name__ == '__main__':
    main()

