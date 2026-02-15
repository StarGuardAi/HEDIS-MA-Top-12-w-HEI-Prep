"""
HEDIS Portfolio Optimizer - Reusable Page Components (FIXED VERSION)
====================================================================

This is the CORRECTED version that fixes:
1. Header spacing (reduces gap between header and title)
2. Header visibility (ensures header is fully visible at top)
3. Mobile badge (creates proper circular badge in sidebar)

Author: Robert Reichert
Version: 1.1 (FIXED)
Date: January 2026
"""

import streamlit as st


def apply_header_spacing():
    """
    Apply AGGRESSIVE header spacing reduction to eliminate gaps.
    
    This FIXED version:
    - Forces zero padding at the top
    - Removes ALL extra spacing between header and content
    - Ensures header is fully visible
    
    Usage:
        Call this immediately after st.set_page_config() on every page:
        
        ```python
        st.set_page_config(page_title="My Page", layout="wide")
        apply_header_spacing()  # ← Add this line
        ```
    """
    st.markdown("""
    <style>
    /* ========== AGGRESSIVE HEADER SPACING FIX ========== */
    
    /* FORCE zero padding at top - most aggressive setting */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 100% !important;
        margin-top: 0 !important;
    }
    
    /* Remove ALL top margins from main container */
    .main > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Target the main section element directly */
    section.main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Remove space from stApp container */
    .stApp {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Force first vertical block to have zero margin */
    div[data-testid="stVerticalBlock"]:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
        gap: 0 !important;
    }
    
    /* ZERO margins on all headers */
    h1, h2, h3, h4, h5, h6 {
        margin-top: 0rem !important;
        margin-bottom: 0.3rem !important;
        padding-top: 0 !important;
    }
    
    /* Reduce paragraph spacing */
    p {
        margin-top: 0 !important;
        margin-bottom: 0.3rem !important;
    }
    
    /* Minimize vertical block gaps */
    div[data-testid="stVerticalBlock"] {
        gap: 0.1rem !important;
    }
    
    /* Markdown container tight spacing */
    .stMarkdown {
        margin-bottom: 0.2rem !important;
        margin-top: 0 !important;
    }
    
    /* Element container tight spacing */
    .element-container {
        margin-top: 0 !important;
        margin-bottom: 0.2rem !important;
    }
    
    /* Metric spacing */
    div[data-testid="stMetric"] {
        padding: 0.2rem !important;
        margin: 0 !important;
    }
    
    /* Force header container to top */
    .header-container {
        margin-top: 0 !important;
        padding-top: 0.5rem !important;
    }
    
    /* ========== MOBILE ADJUSTMENTS ========== */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 0 !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        
        .main > div:first-child {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        h1 {
            margin-top: 0.2rem !important;
            font-size: 1.5rem !important;
            line-height: 1.3;
            text-align: center !important;
        }
        
        h2 {
            margin-top: 0.3rem !important;
            font-size: 1.25rem !important;
            text-align: center !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
            text-align: center !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# def add_mobile_ready_badge():
#     """
#     Add a "Mobile Version Ready" badge to the sidebar.
#     
#     FIXED VERSION: Creates a proper circular/pill badge with:
#     - Green gradient background
#     - White bold text
#     - Mobile emoji
#     - Proper centering
#     
#     Usage:
#         Call this inside your sidebar context:
#         
#         ```python
#         with st.sidebar:
#             st.title("Filters")
#             # ... other sidebar content ...
#             add_mobile_ready_badge()  # ← Add at end of sidebar
#         ```
#     """
#     # Use st.markdown instead of direct HTML to ensure proper rendering
#     st.markdown("---")  # Separator before badge
#     
#     st.markdown("""
#     <div style='
#         background: linear-gradient(135deg, #10B981 0%, #059669 100%);
#         border-radius: 50px;
#         padding: 14px 24px;
#         text-align: center;
#         margin: 24px auto;
#         color: white;
#         font-weight: 700;
#         font-size: 1rem;
#         box-shadow: 0 4px 8px rgba(16, 185, 129, 0.35);
#         border: 2px solid rgba(255, 255, 255, 0.4);
#         max-width: 220px;
#         letter-spacing: 0.3px;
#     '>
#         📱 Mobile Version Ready
#     </div>
#     """, unsafe_allow_html=True)


def add_page_footer():
    """
    Add the standard HEDIS Portfolio Optimizer footer to the page.
    
    This footer includes:
    - Project name and branding
    - Technology stack information
    - Project timeline (10/01/2025 - 12/31/2025)
    - Security and compliance messaging
    - Demo project disclaimer
    - Copyright notice
    
    Usage:
        Call this at the very end of your page, after all content:
        
        ```python
        # ... all your page content ...
        
        # Footer should be last thing on page
        add_page_footer()
        ```
    """
    st.markdown("---")
    st.markdown("""
    <div style='
        text-align: center;
        color: #666;
        font-size: 0.85rem;
        line-height: 1.8;
        padding: 2rem 1rem 1rem 1rem;
        border-top: 2px solid #e0e0e0;
        margin-top: 3rem;
    '>
        <p style='font-weight: 700; font-size: 1rem; color: #4A3D6F; margin-bottom: 0.5rem;'>
            HEDIS Portfolio Optimizer | StarGuard AI
        </p>
        <p style='margin-bottom: 0.5rem;'>
            Built with Streamlit, Plotly, PostgreSQL | 10/01/2025 - 12/31/2025
        </p>
        <p style='margin-bottom: 0.5rem; color: #2d7d32; font-weight: 600;'>
            🔒 <strong>Secure AI Architect</strong> | Enabling LLM insights from PHI without API exposure.
        </p>
        <p style='margin-bottom: 0.5rem;'>
            On-premises HIPAA-compliant AI: 2.8-4.1x ROI, $148M+ impact.
        </p>
        <p style='margin-bottom: 0.5rem; font-weight: 600;'>
            Zero PHI Transmission | On-Premises | Compliance-First
        </p>
        <p style='margin-bottom: 0.5rem; color: #d32f2f; font-weight: 600;'>
            ⚠️ <strong>Demo Project:</strong> Synthetic data only. Not production data.
        </p>
        <p style='margin-top: 1rem; color: #999; font-size: 0.8rem;'>
            © 2024-2026 Robert Reichert | StarGuard AI™
        </p>
    </div>
    
    <style>
    /* Mobile footer adjustments */
    @media (max-width: 768px) {
        div[style*="text-align: center"] {
            padding: 1rem 0.5rem !important;
            font-size: 0.75rem !important;
        }
        
        div[style*="text-align: center"] p {
            line-height: 1.6 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def apply_purple_sidebar():
    """
    Apply the purple gradient sidebar theme with white text.
    
    This function ensures all sidebar elements have:
    - Purple gradient background (#4A3D6F to #6F5F96)
    - White text color for all elements
    - Proper styling for navigation items
    
    Usage:
        Call this after st.set_page_config() if the page doesn't
        inherit the sidebar styling from app.py:
        
        ```python
        st.set_page_config(page_title="My Page", layout="wide")
        apply_purple_sidebar()  # ← Add this line if sidebar isn't purple
        apply_header_spacing()
        ```
    """
    st.markdown("""
    <style>
    /* ========== PURPLE SIDEBAR THEME ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
    }
    
    /* ========== ALL SIDEBAR TEXT WHITE ========== */
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
    
    /* Sidebar navigation links */
    [data-testid="stSidebarNav"] a {
        color: #FFFFFF !important;
    }
    
    /* Mobile sidebar */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
        }
        
        [data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def fix_header_visibility():
    """
    EMERGENCY FIX: Force header to be fully visible at the top of the page.
    
    Use this if the header is cut off or partially hidden.
    Call this AFTER apply_header_spacing() for maximum effect.
    
    Usage:
        ```python
        st.set_page_config(page_title="My Page", layout="wide")
        apply_header_spacing()
        fix_header_visibility()  # ← Add this to fix cut-off header
        ```
    """
    st.markdown("""
    <style>
    /* ========== EMERGENCY HEADER VISIBILITY FIX ========== */
    
    /* Force Streamlit app container to start at very top */
    .stApp {
        padding-top: 0 !important;
        margin-top: 0 !important;
        position: relative !important;
        top: 0 !important;
    }
    
    /* Force main section to start at top */
    section.main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Ensure header container is visible */
    .header-container {
        position: relative !important;
        top: 0 !important;
        margin-top: 0 !important;
        padding-top: 0.8rem !important;
        z-index: 100 !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Force first element to have no margin */
    .main > div:first-child > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Override any Streamlit defaults */
    div[data-testid="block-container"] {
        padding-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# DEBUGGING HELPER
# ============================================================================

def debug_spacing():
    """
    Show visual debugging information for spacing issues.
    
    Usage:
        Add this temporarily to see what's causing spacing problems:
        
        ```python
        from utils.page_components import debug_spacing
        debug_spacing()
        ```
    """
    st.markdown("""
    <style>
    /* Visual debugging - shows borders around containers */
    .block-container {
        border: 3px solid red !important;
    }
    
    .main {
        border: 3px solid blue !important;
    }
    
    .header-container {
        border: 3px solid green !important;
    }
    
    section.main {
        border: 3px solid orange !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.warning("🔧 DEBUG MODE: Borders show container boundaries (red=block, blue=main, green=header, orange=section)")

