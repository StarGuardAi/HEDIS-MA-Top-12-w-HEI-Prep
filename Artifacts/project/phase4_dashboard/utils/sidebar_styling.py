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
    </style>
    """, unsafe_allow_html=True)

