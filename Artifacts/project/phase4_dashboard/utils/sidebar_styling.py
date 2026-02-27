"""
Sidebar Styling Utility
Shared CSS styling for consistent sidebar appearance across all pages
"""
import streamlit as st


def render_landing_page_link():
    """Render a styled link to the landing page at the top of the sidebar"""
    # Add comprehensive CSS to ensure white text for navigation
    st.markdown("""
    <style>
    /* Navigation section header - white text */
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    
    /* Page link styling - white text (all possible selectors) */
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"],
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] *,
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] span,
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p,
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] div,
    [data-testid="stSidebar"] a[href="/"],
    [data-testid="stSidebar"] a[href*="app.py"] {
        color: #FFFFFF !important;
    }
    
    /* Button text in sidebar - white */
    [data-testid="stSidebar"] button[kind="base"],
    [data-testid="stSidebar"] button[kind="secondary"],
    [data-testid="stSidebar"] button {
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Use markdown link for maximum control over styling
    st.sidebar.markdown("---")
    st.sidebar.markdown('<h3 style="color: #FFFFFF !important; margin-bottom: 0.3rem; font-size: 1.1rem;">🏠 Navigation</h3>', unsafe_allow_html=True)
    
    # Use HTML link for guaranteed white text
    st.sidebar.markdown("""
    <div style="margin-bottom: 0.5rem;">
        <a href="/" style="
            display: block;
            padding: 0.5rem 0.7rem;
            background: rgba(255, 255, 255, 0.1);
            color: #FFFFFF !important;
            text-decoration: none;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.2s ease;
            font-weight: 600;
            font-size: 1rem;
        " onmouseover="this.style.background='rgba(255, 255, 255, 0.2)'; this.style.color='#FFFFFF';" 
           onmouseout="this.style.background='rgba(255, 255, 255, 0.1)'; this.style.color='#FFFFFF';">
            🏠 App Home
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")


def apply_sidebar_styling():
    """Apply the same sidebar styling as the main app landing page"""
    st.markdown("""
    <style>
    /* Sidebar styling - matches StarGuard AI header purple gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #4e2a84 0%, #6f5f96 100%);
        padding-top: 0.8rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    
    /* ========== NAVIGATION CONTAINER - MINIMAL ========== */
    /* Only add background - don't change padding/margins/alignment */
    [data-testid="stSidebarNav"] {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        margin: 4px 8px !important;
    }
    
    /* Home button highlight - match ROI page exactly */
    [data-testid="stSidebarNav"] ul li:first-child a {
        font-size: 0 !important;
        background: rgba(255, 255, 255, 0.2) !important;
        padding: 0.75rem 1rem !important;
        border-radius: 8px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        margin-bottom: 0rem !important;
    }
    
    /* Fix Home button label - hide "app" and show "🏠 Home" - match ROI page */
    [data-testid="stSidebarNav"] ul li:first-child a::before {
        content: "🏠 Home" !important;
        font-size: 1.1rem !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        display: block !important;
        -webkit-text-fill-color: #FFFFFF !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Style "app" link as "Home" in sidebar navigation */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href="/"],
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href="./"],
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href*="app"],
    [data-testid="stSidebar"] nav a[href="/"],
    [data-testid="stSidebar"] nav a[href="./"],
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li:first-child a,
    [data-testid="stSidebar"] nav ul li:first-child a {
        color: #FFFFFF !important;
    }
    
    /* Ensure first navigation item (app.py) is visible and styled */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] > div > ul > li:first-child a,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] > ul > li:first-child a {
        color: #FFFFFF !important;
        display: flex !important;
    }
    
    /* Sidebar navigation "View less" / "View more" button - white text */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button span,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button p,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button div,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button *,
    [data-testid="stSidebar"] nav button,
    [data-testid="stSidebar"] nav button span,
    [data-testid="stSidebar"] nav button p,
    [data-testid="stSidebar"] nav button div,
    [data-testid="stSidebar"] nav button * {
        color: #FFFFFF !important;
    }
    
    /* Specifically target "View 10 more" and "View less" navigation buttons */
    [data-testid="stSidebar"] button[aria-label*="View"],
    [data-testid="stSidebar"] button[aria-label*="view"],
    [data-testid="stSidebar"] button[aria-label*="more"],
    [data-testid="stSidebar"] button[aria-label*="less"],
    [data-testid="stSidebar"] button[aria-label*="More"],
    [data-testid="stSidebar"] button[aria-label*="Less"] {
        color: #FFFFFF !important;
    }
    
    /* Target all text content inside navigation buttons - comprehensive */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button *,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button span,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button p,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button div,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] button label,
    [data-testid="stSidebar"] nav button,
    [data-testid="stSidebar"] nav button *,
    [data-testid="stSidebar"] nav button span,
    [data-testid="stSidebar"] nav button p,
    [data-testid="stSidebar"] nav button div,
    [data-testid="stSidebar"] nav button label {
        color: #FFFFFF !important;
    }
    
    /* Force white text for ALL sidebar buttons and their children */
    [data-testid="stSidebar"] button,
    [data-testid="stSidebar"] button * {
        color: #FFFFFF !important;
    }
    
    /* Sidebar text - white for contrast */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span:not([class*="icon"]),
    [data-testid="stSidebar"] div:not([class*="button"]),
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 500;
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
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    
    /* Date input value text - ensure it's visible */
    [data-testid="stSidebar"] .stDateInput input::value,
    [data-testid="stSidebar"] .stDateInput input::-webkit-input-placeholder,
    [data-testid="stSidebar"] .stDateInput input::-moz-placeholder,
    [data-testid="stSidebar"] .stDateInput input:-ms-input-placeholder {
        color: #ffffff !important;
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
        font-size: 0.9rem !important;
    }
    
    /* Explicitly style custom date labels */
    [data-testid="stSidebar"] p:has-text("Start Date"),
    [data-testid="stSidebar"] p:has-text("End Date") {
        color: white !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
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
        color: #ffffff !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    /* Date input container children - labels white, inputs dark */
    [data-testid="stSidebar"] .stDateInput span:not(input),
    [data-testid="stSidebar"] .stDateInput div:not([data-baseweb="input"]):not(input),
    [data-testid="stSidebar"] .stDateInput p {
        color: #ffffff !important;
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
    
    /* Force white text on all date input elements - comprehensive targeting */
    [data-testid="stSidebar"] .stDateInput input,
    [data-testid="stSidebar"] .stDateInput input[type="text"],
    [data-testid="stSidebar"] .stDateInput input[type="date"],
    [data-testid="stSidebar"] .stDateInput input[readonly],
    [data-testid="stSidebar"] .stDateInput div[data-baseweb="input"] input,
    [data-testid="stSidebar"] .stDateInput div[data-baseweb="input"] > div input,
    [data-testid="stSidebar"] [data-testid="stDateInput"] input,
    [data-testid="stSidebar"] [data-testid="stDateInput"] input[type="text"],
    [data-testid="stSidebar"] [data-testid="stDateInput"] div input,
    [data-testid="stSidebar"] .stDateInput span,
    [data-testid="stSidebar"] .stDateInput div,
    [data-testid="stSidebar"] .stDateInput p {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        fill: #ffffff !important;
    }
    
    /* Sidebar help icon (?) - light font - comprehensive targeting */
    [data-testid="stSidebar"] button[title*="help"],
    [data-testid="stSidebar"] button[title*="Help"],
    [data-testid="stSidebar"] button[aria-label*="help"],
    [data-testid="stSidebar"] button[aria-label*="Help"],
    [data-testid="stSidebar"] .stTooltipIcon,
    [data-testid="stSidebar"] button[data-testid*="help"],
    [data-testid="stSidebar"] button[data-testid*="Help"],
    [data-testid="stSidebar"] button.kind-secondary[aria-label],
    [data-testid="stSidebar"] button[class*="tooltip"],
    [data-testid="stSidebar"] button[class*="help"] {
        color: #b0d4ff !important;
        opacity: 0.7 !important;
        font-weight: 300 !important;
        background-color: transparent !important;
    }
    
    /* Sidebar help icon SVG and text - light color */
    [data-testid="stSidebar"] button[title*="help"] svg,
    [data-testid="stSidebar"] button[title*="Help"] svg,
    [data-testid="stSidebar"] button[aria-label*="help"] svg,
    [data-testid="stSidebar"] button[aria-label*="Help"] svg,
    [data-testid="stSidebar"] .stTooltipIcon svg,
    [data-testid="stSidebar"] button[data-testid*="help"] svg,
    [data-testid="stSidebar"] button[class*="tooltip"] svg {
        color: #b0d4ff !important;
        fill: #b0d4ff !important;
        stroke: #b0d4ff !important;
        opacity: 0.7 !important;
    }
    
    /* Target any small icon button in sidebar that might be help icon */
    [data-testid="stSidebar"] button[style*="width"] svg,
    [data-testid="stSidebar"] button[style*="height"] svg {
        color: #b0d4ff !important;
        fill: #b0d4ff !important;
        stroke: #b0d4ff !important;
        opacity: 0.7 !important;
    }
    
    /* ============================================================
       MOBILE RESPONSIVENESS - Sidebar and App Home Frame
       ============================================================ */
    
    /* Mobile sidebar toggle button - ensure it's visible and touch-friendly */
    @media (max-width: 768px) {
        /* Sidebar toggle button styling */
        button[data-testid="baseButton-header"] {
            min-width: 44px !important;
            min-height: 44px !important;
            padding: 0.5rem !important;
            z-index: 1000 !important;
        }
        
        /* Sidebar overlay on mobile */
        [data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100vh !important;
            z-index: 999 !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
        }
        
        /* App Home frame - mobile responsive */
        .custom-sidebar-home {
            width: 100% !important;
            max-width: 100% !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            padding: 0.5rem !important;
            margin-bottom: 0.5rem !important;
            box-sizing: border-box !important;
        }
        
        /* App Home link - touch-friendly */
        .custom-sidebar-home a {
            min-height: 40px !important;
            padding: 0.5rem 0.7rem !important;
            font-size: 1rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            touch-action: manipulation !important;
            -webkit-tap-highlight-color: rgba(255, 255, 255, 0.2) !important;
        }
        
        /* App Home subtitle - readable on mobile */
        .custom-sidebar-subtitle {
            font-size: 0.7rem !important;
            margin-top: 0.5rem !important;
            padding: 0 0.5rem !important;
        }
        
        /* Navigation links - touch-friendly */
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
            min-height: 40px !important;
            padding: 0.5rem 0.7rem !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.15rem !important;
            touch-action: manipulation !important;
            -webkit-tap-highlight-color: rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Ensure text is readable on mobile */
        [data-testid="stSidebar"] {
            font-size: 14px !important;
            line-height: 1.5 !important;
        }
        
        /* Sidebar headings - readable */
        [data-testid="stSidebar"] h3 {
            font-size: 1rem !important;
            margin-bottom: 0.4rem !important;
            padding: 0 0.7rem !important;
        }
        
        /* Sidebar padding for mobile */
        [data-testid="stSidebar"] > div {
            padding: 0.5rem 0.4rem !important;
        }
        [data-testid="stSidebar"] {
            padding-top: 0.5rem !important;
            padding-left: 0.3rem !important;
            padding-right: 0.3rem !important;
        }
        
        /* Ensure sidebar content doesn't overflow */
        [data-testid="stSidebar"] * {
            max-width: 100% !important;
            word-wrap: break-word !important;
        }
        
        /* Sidebar scrollbar styling for mobile */
        [data-testid="stSidebar"]::-webkit-scrollbar {
            width: 6px !important;
        }
        
        [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3) !important;
            border-radius: 3px !important;
        }
    }
    
    /* Tablet responsiveness (768px - 1024px) */
    @media (min-width: 769px) and (max-width: 1024px) {
        .custom-sidebar-home {
            padding: 0.5rem !important;
        }
        
        .custom-sidebar-home a {
            min-height: 36px !important;
            font-size: 1rem !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
            min-height: 36px !important;
            padding: 0.4rem 0.6rem !important;
        }
    }
    
    /* Ensure App Home frame is always visible and properly styled */
    .custom-sidebar-home {
        position: relative !important;
        z-index: 1 !important;
    }
    
    /* Touch feedback for all interactive elements */
    @media (hover: none) and (pointer: coarse) {
        .custom-sidebar-home a:active,
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:active {
            background: rgba(255, 255, 255, 0.3) !important;
            transform: scale(0.98) !important;
        }
    }
    
    /* ========== CENTER TAB BUTTONS ========== */
    /* Center the entire tab bar */
    [data-testid="stTabs"] > div:first-child {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    
    [data-baseweb="tab-list"] {
        justify-content: center !important;
        margin: 0 auto !important;
    }
    
    [role="tablist"] {
        justify-content: center !important;
        display: flex !important;
        width: 100% !important;
    }
    
    /* Center the tab list container */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        justify-content: center !important;
        display: flex !important;
    }
    
    /* Center individual tabs */
    [data-testid="stTabs"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }
    
    /* Ensure tabs don't stretch full width */
    [data-baseweb="tab-list"] {
        justify-content: center !important;
        width: auto !important;
    }
    
    /* ========== LEFT-ALIGN DATA TABLES ========== */
    /* Table container - left align */
    [data-testid="stDataFrame"] {
        text-align: left !important;
    }
    
    [data-testid="stDataFrame"] table {
        text-align: left !important;
    }
    
    [data-testid="stDataFrame"] th {
        text-align: left !important;
    }
    
    [data-testid="stDataFrame"] td {
        text-align: left !important;
    }
    
    /* Ensure table headers left-aligned */
    [data-testid="stDataFrame"] thead th {
        text-align: left !important;
    }
    
    /* Table body cells left-aligned */
    [data-testid="stDataFrame"] tbody td {
        text-align: left !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # JavaScript to force tab centering and table alignment
    st.markdown("""
    <script>
    // Enhanced function to center tabs with diagnostics
    function fixTabsAndTables() {
        // Find and log all tab-related elements
        const tabSelectors = [
            '[role="tablist"]',
            '[data-baseweb="tab-list"]',
            '.stTabs',
            '[data-testid="stTabs"]',
            '.stTabs > div',
            '.stTabs > div > div',
            '[class*="st-emotion-cache"] [role="tablist"]'
        ];
        
        let foundElements = [];
        
        tabSelectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach((el, i) => {
                if (!foundElements.includes(el)) {
                    foundElements.push(el);
                    console.log(`Found tab element with selector "${selector}":`, el);
                    console.log(`Classes: ${el.className}`);
                    console.log(`Parent classes: ${el.parentElement?.className || 'none'}`);
                    
                    // Apply centering styles
                    el.style.justifyContent = 'center';
                    el.style.display = 'flex';
                    el.style.width = '100%';
                    
                    // Also try setting on parent if it's a flex container
                    if (el.parentElement) {
                        const parent = el.parentElement;
                        const parentStyle = window.getComputedStyle(parent);
                        if (parentStyle.display === 'flex' || parentStyle.display === 'inline-flex') {
                            parent.style.justifyContent = 'center';
                            parent.style.display = 'flex';
                            parent.style.width = '100%';
                        }
                    }
                }
            });
        });
        
        // Specific targeting for tab lists
        const tabLists = document.querySelectorAll('[role="tablist"]');
        tabLists.forEach(tabList => {
            tabList.style.justifyContent = 'center';
            tabList.style.display = 'flex';
            tabList.style.width = '100%';
            tabList.style.marginLeft = 'auto';
            tabList.style.marginRight = 'auto';
        });
        
        // Also target by data-baseweb attribute
        const basewebTabs = document.querySelectorAll('[data-baseweb="tab-list"]');
        basewebTabs.forEach(tabList => {
            tabList.style.justifyContent = 'center';
            tabList.style.display = 'flex';
            tabList.style.width = '100%';
            tabList.style.marginLeft = 'auto';
            tabList.style.marginRight = 'auto';
        });
        
        // Target Streamlit tab containers
        const stTabs = document.querySelectorAll('[data-testid="stTabs"]');
        stTabs.forEach(container => {
            const firstDiv = container.querySelector('> div');
            if (firstDiv) {
                firstDiv.style.justifyContent = 'center';
                firstDiv.style.display = 'flex';
                firstDiv.style.width = '100%';
            }
        });
        
        // Left-align all table cells
        const tableCells = document.querySelectorAll('[data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th');
        tableCells.forEach(cell => {
            cell.style.textAlign = 'left';
        });
        
        if (foundElements.length > 0) {
            console.log(`✅ Applied centering to ${foundElements.length} tab element(s)`);
        }
    }
    
    // Run on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixTabsAndTables);
    } else {
        fixTabsAndTables();
    }
    
    // Run again after short delays (Streamlit renders async)
    setTimeout(fixTabsAndTables, 100);
    setTimeout(fixTabsAndTables, 500);
    setTimeout(fixTabsAndTables, 1000);
    setTimeout(fixTabsAndTables, 2000);
    setTimeout(fixTabsAndTables, 3000);
    
    // Run when DOM changes (for tab switches and dynamic content)
    const observer = new MutationObserver(() => {
        setTimeout(fixTabsAndTables, 100);
    });
    observer.observe(document.body, { 
        childList: true, 
        subtree: true,
        attributes: true,
        attributeFilter: ['class', 'style']
    });
    
    // Also run when page becomes visible
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            setTimeout(fixTabsAndTables, 100);
        }
    });
    </script>
    """, unsafe_allow_html=True)

