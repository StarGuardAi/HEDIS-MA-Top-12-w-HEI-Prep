"""
HEDIS Portfolio Optimizer
Main Application File

CRITICAL: st.set_page_config() MUST be first Streamlit command!
"""

# ============================================================================
# Python 3.13 compatibility fix for Streamlit widgets
# ============================================================================
import sys
import os

if sys.version_info >= (3, 13):
    import warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning'

# ============================================================================
# 1. IMPORTS
# ============================================================================
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="HEDIS Portfolio Optimizer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="auto"  # Auto: Let Streamlit decide based on screen size (iOS Safari optimized)
)

# ============================================================================
# RESPONSIVE DESIGN SYSTEM - Desktop & Mobile Formatting
# ============================================================================
st.markdown("""
<style>
/* ========== VIEWPORT & BASE SETTINGS ========== */
@viewport {
    width: device-width;
    initial-scale: 1.0;
}

/* ========== DESKTOP STYLES (default, 769px+) ========== */
/* Enhanced Desktop Layout System */
.header-container {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%);
    padding: 0.5rem 0.75rem 0.6rem 0.75rem;
    border-radius: 6px;
    margin-top: -1rem !important;
    margin-bottom: 0.1rem;
    text-align: center;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    box-shadow: 0 4px 12px rgba(74, 61, 111, 0.25);
    max-width: 100%;
}

.header-title {
    color: white !important;
    font-weight: 700;
    font-size: 1.25rem;
    margin-bottom: 0.4rem;
    display: block !important;
    line-height: 1.5;
    letter-spacing: 0.3px;
}

.header-subtitle {
    color: #E8D4FF !important;
    font-size: 0.9rem;
    font-style: italic;
    display: block !important;
    line-height: 1.4;
    opacity: 0.95;
}

/* Desktop Container - Optimized for wide screens */
div.block-container {
    padding-top: 0rem !important;
    padding-left: 4rem !important;
    padding-right: 4rem !important;
    padding-bottom: 0.5rem !important;
    max-width: 1600px !important;
    margin: 0 auto !important;
}

/* Zero-top enforcement - Headers flush to top */
.main > div:first-child {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Desktop Typography Hierarchy - CENTER ALIGNED */
h1 {
    margin-top: 0.2rem !important;
    margin-bottom: 0.15rem !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
    color: #1f2937 !important;
    text-align: center !important;
}

h2 {
    margin-top: 0.15rem !important;
    margin-bottom: 0.1rem !important;
    font-size: 1.75rem !important;
    font-weight: 600 !important;
    line-height: 1.3 !important;
    color: #374151 !important;
    text-align: center !important;
}

h3 {
    margin-top: 0.1rem !important;
    margin-bottom: 0.1rem !important;
    font-size: 1.35rem !important;
    font-weight: 600 !important;
    color: #4b5563 !important;
    text-align: center !important;
}

h4, h5, h6 {
    text-align: center !important;
}

/* Center align all markdown headers */
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4,
div[data-testid="stMarkdownContainer"] h5,
div[data-testid="stMarkdownContainer"] h6 {
    text-align: center !important;
}

/* Desktop Grid System - Better column layouts */
[data-testid="column"] {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* Center align columns containing metrics */
/* FIX 4: Replaced :has() with class-based approach for iOS Safari < 15.4 compatibility */
.metric-column {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

/* Desktop Cards & Containers */
.element-container {
    padding: 0 !important;
    margin-bottom: 0 !important;
    text-align: left !important;
}

/* Desktop Metrics - Larger, more prominent - CENTER ALIGNED */
[data-testid="stMetric"] {
    text-align: center !important;
}

[data-testid="stMetricValue"] {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    text-align: center !important;
}

[data-testid="stMetricLabel"] {
    font-size: 1rem !important;
    font-weight: 500 !important;
    text-align: center !important;
}

[data-testid="stMetricDelta"] {
    text-align: center !important;
}

/* Center align metric containers */
[data-testid="metric-container"],
[data-testid="stMetricContainer"] {
    text-align: center !important;
    margin: 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Ensure all metric container children are centered */
[data-testid="metric-container"] > *,
[data-testid="stMetricContainer"] > * {
    text-align: center !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Center align custom metric cards */
.compact-metric-card,
.kpi-card {
    text-align: center !important;
}

.compact-metric-title,
.kpi-title {
    text-align: center !important;
}

.compact-metric-value,
.kpi-value {
    text-align: center !important;
}

.compact-metric-subtitle,
.kpi-subtitle {
    text-align: center !important;
}

/* Desktop Tables - Better spacing */
.stDataFrame {
    margin-top: 1rem !important;
    margin-bottom: 1rem !important;
}

/* Desktop Buttons - Better sizing */
button[kind="primary"],
button[kind="secondary"] {
    padding: 0.6rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    margin-right: 0.5rem !important;
    margin-bottom: 0.5rem !important;
}

/* Desktop Sidebar - Wider for better navigation */
[data-testid="stSidebar"] {
    min-width: 300px !important;
    padding: 1.5rem 1rem !important;
}

/* Desktop Expanders - Better spacing */
[data-testid="stExpander"] {
    margin-bottom: 1rem !important;
}

/* Desktop Selectboxes & Inputs - Better sizing */
.stSelectbox,
.stTextInput,
.stNumberInput {
    margin-bottom: 1rem !important;
}

/* Desktop Charts - Better spacing */
.plotly {
    margin-top: 1rem !important;
    margin-bottom: 1rem !important;
}

/* Desktop Spacing Utilities */
.desktop-spacing-sm { margin-bottom: 0.5rem !important; }
.desktop-spacing-md { margin-bottom: 1rem !important; }
.desktop-spacing-lg { margin-bottom: 1.5rem !important; }
.desktop-spacing-xl { margin-bottom: 2rem !important; }

/* ========== MOBILE STYLES (max-width: 768px) ========== */
@media (max-width: 768px) {
    .header-container {
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(74, 61, 111, 0.15);
    }
    
    .header-title {
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
        line-height: 1.3;
        font-weight: 600;
    }
    
    .header-subtitle {
        font-size: 0.65rem;
        line-height: 1.2;
    }
    
    /* Mobile spacing - tighter */
    div.block-container {
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    h1 {
        margin-top: 0.5rem !important;
        font-size: 1.5rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h2 {
        margin-top: 0.75rem !important;
        font-size: 1.25rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h4, h5, h6 {
        text-align: center !important;
    }
    
    /* Center align markdown headers on mobile */
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4,
    div[data-testid="stMarkdownContainer"] h5,
    div[data-testid="stMarkdownContainer"] h6 {
        text-align: center !important;
    }
    
    /* Center align metrics on mobile */
    [data-testid="stMetric"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"],
    [data-testid="metric-container"],
    .compact-metric-card,
    .kpi-card {
        text-align: center !important;
    }
    
    /* Center align Streamlit app header title on mobile */
    header[data-testid="stHeader"],
    .stAppHeader,
    .st-emotion-cache-ttupiz {
        text-align: center !important;
    }
    
    header[data-testid="stHeader"] *,
    .stAppHeader *,
    .st-emotion-cache-ttupiz * {
        text-align: center !important;
    }
    
    /* Mobile sidebar adjustments */
    [data-testid="stSidebar"] {
        min-width: 240px !important;
    }
    
    /* Hide Home button on mobile - redundant with sidebar nav */
    [data-testid="stSidebar"] .home-button-desktop {
        display: none !important;
    }
    
    /* Hide the hr separator after Home button on mobile */
    /* FIX 4: Replaced :has() with class-based approach for iOS Safari < 15.4 compatibility */
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"].has-home-button hr,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] hr[style*="margin: 1rem 0"] {
        display: none !important;
    }
    
    /* Mobile tables - horizontal scroll */
    .stDataFrame {
        overflow-x: auto !important;
    }
    
    /* Mobile columns - stack vertically */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
    
    /* Mobile buttons - full width */
    button[kind="primary"],
    button[kind="secondary"] {
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Mobile metrics - smaller */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
    }
    
    /* Mobile tabs - stack vertically to eliminate horizontal scrolling */
    [data-testid="stTabs"] {
        overflow-x: visible !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: column !important;
        width: 100% !important;
        gap: 0.5rem !important;
        overflow-x: visible !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        text-align: left !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    /* Wrap Plotly chart titles on mobile */
    .js-plotly-plot .gtitle,
    .plotly .gtitle,
    .js-plotly-plot .xtitle,
    .plotly .xtitle {
        word-wrap: break-word !important;
        white-space: normal !important;
        max-width: 100% !important;
        overflow-wrap: break-word !important;
        hyphens: auto !important;
    }
    
    /* Ensure chart titles wrap */
    .js-plotly-plot .gtitle text,
    .plotly .gtitle text {
        word-wrap: break-word !important;
        white-space: normal !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        width: 100% !important;
    }
}

/* ========== TABLET STYLES (769px - 1024px) ========== */
@media (min-width: 769px) and (max-width: 1024px) {
    .header-container {
        padding: 0.7rem 1rem;
    }
    
    .header-title {
        font-size: 1rem;
    }
    
    .header-subtitle {
        font-size: 0.75rem;
    }
    
    div.block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    h1 {
        font-size: 1.75rem !important;
    }
}

/* ========== LARGE DESKTOP (1025px+) ========== */
@media (min-width: 1025px) {
    div.block-container {
        max-width: 1600px !important;
        margin: 0 auto !important;
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }
    
    .header-container {
        padding: 1.2rem 2.5rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    .header-title {
        font-size: 1.4rem;
    }
    
    .header-subtitle {
        font-size: 1rem;
    }
    
    h1 {
        font-size: 2.75rem !important;
    }
    
    h2 {
        font-size: 2rem !important;
    }
}

/* ========== ULTRA-WIDE DESKTOP (1440px+) ========== */
@media (min-width: 1440px) {
    div.block-container {
        max-width: 1800px !important;
        padding-left: 6rem !important;
        padding-right: 6rem !important;
    }
    
    [data-testid="stSidebar"] {
        min-width: 320px !important;
    }
}

/* ========== KPI SECTION STYLING ========== */
/* Target the specific vertical block container class */
div.stVerticalBlock.st-emotion-cache-e9yaxd.e1f1d6gn2 {
    justify-content: center !important;
    align-items: center !important;
    gap: 0px !important;
    text-align: left !important;
}

/* Target KPI section wrapper and all nested containers */
.kpi-section-wrapper,
.kpi-section-wrapper div.stVerticalBlock {
    justify-content: center !important;
    align-items: center !important;
    gap: 0px !important;
    text-align: left !important;
}

/* Reduce vertical white space - target element containers in KPI section */
.kpi-section-wrapper .element-container {
    margin-bottom: 0.5rem !important;
    padding-bottom: 0 !important;
}

/* Reduce spacing in columns within KPI section */
.kpi-section-wrapper [data-testid="column"] {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}

/* Target plotly containers to reduce spacing */
.kpi-section-wrapper .plotly-container {
    margin-bottom: 0.5rem !important;
}

/* Reduce margin on h4 heading in KPI section */
.kpi-section-wrapper h4 {
    margin-bottom: 0.5rem !important;
    margin-top: 0.5rem !important;
}

/* ========== PRINT STYLES ========== */
@media print {
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    .header-container {
        page-break-after: avoid;
    }
}
</style>
""", unsafe_allow_html=True)

# Responsive Header - Adapts to Desktop/Mobile
st.markdown("""
<div class="header-container">
    <div class="header-title">⭐ StarGuard AI | Turning Data Into Stars</div>
    <div class="header-subtitle">Powered by Predictive Analytics & Machine Learning</div>
</div>
""", unsafe_allow_html=True)

# ========== AGGRESSIVE SPACING REDUCTION ==========
# MATCHED TO INTERVENTION PERFORMANCE ANALYSIS PAGE (Perfect Spacing Template)
st.markdown("""
<style>
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

div[data-testid="stVerticalBlock"] > div:first-child {
    margin-bottom: 0 !important;
}

h1, h2, h3, h4, h5, h6 {
    margin-top: 0.25rem !important;
    margin-bottom: 0.5rem !important;
    padding-top: 0 !important;
}

p {
    margin-top: 0 !important;
    margin-bottom: 0.5rem !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.25rem !important;
}

section.main > div {
    padding-top: 0.5rem !important;
}

.stMarkdown {
    margin-bottom: 0.25rem !important;
}

div[data-testid="stMetric"] {
    padding: 0.25rem !important;
}
</style>
""", unsafe_allow_html=True)

# Rest of your page content starts here
# ... etc

# ============================================================================
# 2. PAGE CONFIG (already set above - no duplicate needed)
# ============================================================================
# Mobile device detection handled via JavaScript below

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

/* ========== WHITE "HOME" LABEL ========== */
[data-testid="stSidebarNav"] ul li:first-child a {
    font-size: 0 !important;
    background: rgba(255, 255, 255, 0.2) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    margin-bottom: 0.5rem !important;
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

/* "Mobile Optimized" badge - white text */
[data-testid="stSidebar"] .element-container div[data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
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
    
    /* Hide "Mobile Optimized" message on mobile */
    [data-testid="stSidebar"] [data-testid="stSuccess"]:has-text("Mobile Optimized"),
    [data-testid="stSidebar"] [data-testid="stSuccess"]:has-text("📱 Mobile Optimized") {
        display: none !important;
    }
    
    /* Alternative: Hide all sidebar success messages containing Mobile Optimized text */
    [data-testid="stSidebar"] [data-testid="stSuccess"] {
        display: none !important;
    }
}

/* Desktop: Show "Mobile Optimized" message */
@media (min-width: 769px) {
    [data-testid="stSidebar"] [data-testid="stSuccess"] {
        display: block !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Mobile detection and redirect - Force mobile to home page with collapsed sidebar
# Use session state to prevent redirect loops
if 'mobile_redirected' not in st.session_state:
    st.session_state.mobile_redirected = False

st.markdown("""
<script>
(function() {
    'use strict';
    
    // Detect mobile device - multiple methods for reliability
    const isMobile = window.innerWidth <= 768 || 
                     /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
                     (window.matchMedia && window.matchMedia("(max-width: 768px)").matches);
    
    // Detect iOS specifically for optimized handling
    const isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);
    
    if (isMobile) {
        // ====================================================================
        // FIX 2: Redirect check BEFORE sidebar operations (prevents flash)
        // ====================================================================
        const currentPath = window.location.pathname;
        const isOnSubPage = currentPath.includes('/pages/') || 
                           (currentPath !== '/' && currentPath !== '/app' && currentPath !== '/app.py');
        
        // Use localStorage instead of sessionStorage (more reliable on iOS Safari)
        const redirectKey = 'streamlit_mobile_redirect_done';
        const redirectTimestampKey = 'streamlit_mobile_redirect_timestamp';
        const hasRedirected = localStorage.getItem(redirectKey);
        
        // iOS-specific: Check redirect timestamp to prevent stale redirects
        let shouldRedirect = false;
        if (isOnSubPage) {
            if (!hasRedirected) {
                shouldRedirect = true;
            } else if (isIOS) {
                // On iOS, check if redirect is recent (within last 5 seconds)
                // This prevents redirect loops while allowing fresh redirects
                const redirectTime = localStorage.getItem(redirectTimestampKey);
                const now = Date.now();
                if (!redirectTime || (now - parseInt(redirectTime)) > 5000) {
                    shouldRedirect = true;
                }
            }
        }
        
        // Perform redirect immediately if needed (before sidebar initialization)
        if (shouldRedirect) {
            // Set redirect flag immediately to prevent loops
            localStorage.setItem(redirectKey, 'true');
            localStorage.setItem(redirectTimestampKey, Date.now().toString());
            
            // Use replace() instead of href to avoid history entry and back button issues
            // This prevents "stuck on home page" navigation problems
            window.location.replace('/');
            
            // Clear redirect flag after successful redirect (iOS-specific cleanup)
            // This ensures fresh redirects work on subsequent visits
            if (isIOS) {
                // On iOS, clear flag after a delay to allow redirect to complete
                setTimeout(function() {
                    // Only clear if we're now on the home page
                    if (window.location.pathname === '/' || window.location.pathname === '/app') {
                        localStorage.removeItem(redirectKey);
                        localStorage.removeItem(redirectTimestampKey);
                    }
                }, 1000);
            }
            
            // Exit early - don't initialize sidebar if redirecting
            return;
        }
        
        // ====================================================================
        // Sidebar hiding (only if not redirecting)
        // ====================================================================
        function hideSidebar() {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                sidebar.style.display = 'none';
                sidebar.style.visibility = 'hidden';
                sidebar.style.opacity = '0';
            }
            
            // Hide sidebar toggle button
            const sidebarToggle = document.querySelector('button[aria-label*="sidebar"], button[aria-label*="menu"]');
            if (sidebarToggle) {
                sidebarToggle.style.display = 'none';
            }
            
            // Also try to find by class
            const toggleButtons = document.querySelectorAll('button');
            toggleButtons.forEach(btn => {
                const ariaLabel = btn.getAttribute('aria-label') || '';
                if (ariaLabel.toLowerCase().includes('sidebar') || ariaLabel.toLowerCase().includes('menu')) {
                    btn.style.display = 'none';
                }
            });
        }
        
        // Hide sidebar immediately
        hideSidebar();
        
        // Also hide after DOM loads
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', hideSidebar);
        }
        
        // ====================================================================
        // FIX 5: Optimized MutationObserver - Performance improvements for iPhone
        // ====================================================================
        const sidebarContainer = document.querySelector('[data-testid="stSidebar"]');
        if (sidebarContainer && !shouldRedirect) {  // Only set up observer if not redirecting
            let observerTimeout;
            let observerDisconnected = false;
            
            const observer = new MutationObserver(function(mutations) {
                // Debounce observer callback (100ms delay) for better performance
                if (observerTimeout) {
                    clearTimeout(observerTimeout);
                }
                
                observerTimeout = setTimeout(function() {
                    // Only hide if sidebar becomes visible
                    if (!observerDisconnected && sidebarContainer && sidebarContainer.style.display !== 'none') {
                        hideSidebar();
                    }
                }, 100); // 100ms debounce delay
            });
            
            // Watch only sidebar container with minimal options (childList only)
            observer.observe(sidebarContainer, {
                childList: true  // Only watch for child node changes (most efficient)
                // Removed attributes and subtree for better performance
            });
            
            // Store observer reference for cleanup
            window.sidebarHideObserver = observer;
            
            // Disconnect observer on page unload or navigation
            window.addEventListener('beforeunload', function() {
                if (observer && !observerDisconnected) {
                    observer.disconnect();
                    observerDisconnected = true;
                    if (observerTimeout) {
                        clearTimeout(observerTimeout);
                    }
                }
            });
            
            // Also disconnect if redirect happens later (safety check)
            window.addEventListener('popstate', function() {
                if (observer && !observerDisconnected) {
                    observer.disconnect();
                    observerDisconnected = true;
                    if (observerTimeout) {
                        clearTimeout(observerTimeout);
                    }
                }
            });
        }
        
        // iOS-specific: Clean up redirect flags when on home page
        if (isIOS) {
            if (currentPath === '/' || currentPath === '/app' || currentPath === '/app.py') {
                // Clear redirect flags when successfully on home page
                localStorage.removeItem(redirectKey);
                localStorage.removeItem(redirectTimestampKey);
            }
            
            // Also clean up on page unload if we're on home page
            window.addEventListener('beforeunload', function() {
                if (window.location.pathname === '/' || window.location.pathname === '/app') {
                    localStorage.removeItem(redirectKey);
                    localStorage.removeItem(redirectTimestampKey);
                }
            });
        }
    }
    
    // Re-check on resize (debounced for performance)
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth <= 768) {
                const sidebar = document.querySelector('[data-testid="stSidebar"]');
                if (sidebar) {
                    sidebar.style.display = 'none';
                }
            }
        }, 250);
    });
    
        // iOS-specific: Handle orientation changes
    if (isIOS) {
        window.addEventListener('orientationchange', function() {
            setTimeout(function() {
                const sidebar = document.querySelector('[data-testid="stSidebar"]');
                if (sidebar && window.innerWidth <= 768) {
                    sidebar.style.display = 'none';
                }
            }, 100);
        });
    }
    
    // ====================================================================
    // FIX 3: Force sidebar closed on iOS Safari after page load
    // ====================================================================
    if (isIOS) {
        function forceSidebarClosed() {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                // Force sidebar closed on iOS
                sidebar.style.display = 'none';
                sidebar.style.visibility = 'hidden';
                sidebar.style.opacity = '0';
                
                // Also try to collapse via Streamlit's internal API
                const sidebarButton = document.querySelector('button[data-testid="baseButton-header"]');
                if (sidebarButton && sidebarButton.getAttribute('aria-label')?.toLowerCase().includes('sidebar')) {
                    // Sidebar is open, close it
                    const isOpen = sidebar.style.display !== 'none' || 
                                   window.getComputedStyle(sidebar).display !== 'none';
                    if (isOpen) {
                        sidebarButton.click();
                    }
                }
            }
        }
        
        // Force closed immediately
        forceSidebarClosed();
        
        // Also force closed after DOM loads
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', forceSidebarClosed);
        }
        
        // Force closed after a short delay (iOS Safari may open it initially)
        setTimeout(forceSidebarClosed, 100);
        setTimeout(forceSidebarClosed, 500);
        
        // ====================================================================
        // FIX 5: Optimized MutationObserver for iOS sidebar forcing
        // ====================================================================
        const sidebarContainer = document.querySelector('[data-testid="stSidebar"]');
        if (sidebarContainer) {
            let sidebarObserverTimeout;
            let sidebarObserverDisconnected = false;
            
            const sidebarObserver = new MutationObserver(function() {
                // Debounce observer callback (100ms delay) for better performance
                if (sidebarObserverTimeout) {
                    clearTimeout(sidebarObserverTimeout);
                }
                
                sidebarObserverTimeout = setTimeout(function() {
                    if (!sidebarObserverDisconnected) {
                        forceSidebarClosed();
                    }
                }, 100); // 100ms debounce delay
            });
            
            // Watch only sidebar container with minimal options (childList only)
            sidebarObserver.observe(sidebarContainer, {
                childList: true  // Only watch for child node changes (most efficient)
                // Removed attributes watching for better performance
            });
            
            // Store observer reference for potential cleanup
            window.sidebarObserver = sidebarObserver;
        }
    }
})();
</script>
""", unsafe_allow_html=True)

# ============================================================================
# FIX 4: CSS :has() Selector Replacement for iOS Safari < 15.4 Compatibility
# ============================================================================
st.markdown("""
<script>
(function() {
    'use strict';
    
    // ====================================================================
    // iOS Version Detection
    // ====================================================================
    function getIOSVersion() {
        const userAgent = navigator.userAgent;
        const match = userAgent.match(/OS (\d+)_(\d+)_?(\d+)?/);
        if (match) {
            return {
                major: parseInt(match[1], 10),
                minor: parseInt(match[2], 10),
                patch: parseInt(match[3] || '0', 10),
                version: parseFloat(match[1] + '.' + match[2])
            };
        }
        return null;
    }
    
    const iosVersion = getIOSVersion();
    const isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);
    const isIOSSafari = isIOS && /Safari/i.test(navigator.userAgent) && !/CriOS|FxiOS|OPiOS/i.test(navigator.userAgent);
    
    // iOS Safari < 15.4 doesn't support :has() selector
    const needsHasFallback = isIOSSafari && (!iosVersion || iosVersion.version < 15.4);
    
    // ====================================================================
    // Feature Detection for :has() Support
    // ====================================================================
    function supportsHasSelector() {
        try {
            // Test if :has() is supported
            document.querySelector(':has(*)');
            return true;
        } catch (e) {
            return false;
        }
    }
    
    const hasSelectorSupported = supportsHasSelector();
    const useJavaScriptFallback = needsHasFallback || !hasSelectorSupported;
    
    // ====================================================================
    // JavaScript Fallback: Add Classes to Elements
    // ====================================================================
    if (useJavaScriptFallback) {
        function addHelperClasses() {
            // 1. Add metric-column class to columns containing metrics
            const columns = document.querySelectorAll('[data-testid="column"]');
            columns.forEach(function(col) {
                const hasMetricContainer = col.querySelector('[data-testid="stMetricContainer"]');
                const hasMetric = col.querySelector('[data-testid="stMetric"]');
                
                if (hasMetricContainer || hasMetric) {
                    col.classList.add('metric-column');
                } else {
                    col.classList.remove('metric-column');
                }
            });
            
            // 2. Add has-home-button class to sidebar containers with home button
            const sidebarContainers = document.querySelectorAll('[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"]');
            sidebarContainers.forEach(function(container) {
                const hasHomeButton = container.querySelector('.home-button-desktop');
                if (hasHomeButton) {
                    container.classList.add('has-home-button');
                } else {
                    container.classList.remove('has-home-button');
                }
            });
            
            // 3. Add has-expander class to element containers with expanders
            const elementContainers = document.querySelectorAll('.element-container');
            elementContainers.forEach(function(container) {
                const hasExpander = container.querySelector('[data-testid="stExpander"]');
                const hasInfo = container.querySelector('.stInfo');
                
                if (hasExpander) {
                    container.classList.add('has-expander');
                } else {
                    container.classList.remove('has-expander');
                }
                
                if (hasInfo) {
                    container.classList.add('has-info');
                } else {
                    container.classList.remove('has-info');
                }
            });
        }
        
        // Run immediately
        addHelperClasses();
        
        // Run on DOM ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', addHelperClasses);
        }
        
        // Watch for dynamically added elements
        const observer = new MutationObserver(function(mutations) {
            let shouldUpdate = false;
            
            mutations.forEach(function(mutation) {
                // Check if new nodes were added
                if (mutation.addedNodes.length > 0) {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) { // Element node
                            // Check if it's a column, sidebar container, or element container
                            if (node.matches && (
                                node.matches('[data-testid="column"]') ||
                                node.matches('[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"]') ||
                                node.matches('.element-container') ||
                                node.querySelector('[data-testid="column"]') ||
                                node.querySelector('[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"]') ||
                                node.querySelector('.element-container')
                            )) {
                                shouldUpdate = true;
                            }
                        }
                    });
                }
                
                // Check if attributes changed (class, data attributes)
                if (mutation.type === 'attributes' && (
                    mutation.attributeName === 'class' ||
                    mutation.attributeName === 'data-testid'
                )) {
                    shouldUpdate = true;
                }
            });
            
            if (shouldUpdate) {
                // Debounce updates for performance
                if (window.hasSelectorUpdateTimeout) {
                    clearTimeout(window.hasSelectorUpdateTimeout);
                }
                window.hasSelectorUpdateTimeout = setTimeout(addHelperClasses, 100);
            }
        });
        
        // Observe document body for changes
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['class', 'data-testid']
        });
        
        // Also run periodically to catch any missed elements (iOS Safari specific)
        if (isIOS) {
            setInterval(addHelperClasses, 2000); // Check every 2 seconds on iOS
        }
        
        // Debug logging (can be removed in production)
        if (isIOS) {
            console.log('iOS Safari detected, using JavaScript fallback for :has() selector');
            if (iosVersion) {
                console.log('iOS Version:', iosVersion.major + '.' + iosVersion.minor);
            }
        }
    } else {
        // Modern browser with :has() support - no fallback needed
        if (isIOS) {
            console.log('iOS Safari 15.4+ detected, :has() selector supported');
        }
    }
})();
</script>
""", unsafe_allow_html=True)

# Improved compact CSS - READABLE fonts, reduced spacing only
# MATCHED TO INTERVENTION PERFORMANCE ANALYSIS PAGE (Perfect Spacing Template)
st.markdown("""
<style>
.main .block-container { 
    padding-top: 1rem !important; 
    padding-bottom: 1rem !important; 
    padding-left: 1rem !important; 
    padding-right: 1rem !important; 
    max-width: 100% !important; 
}

/* Section spacing - REDUCE GAPS between sections */
h1 { 
    font-size: 1.8rem !important; 
    margin-top: 0.8rem !important; 
    margin-bottom: 0.5rem !important; 
    line-height: 1.2 !important; 
}

h2 { 
    font-size: 1.4rem !important; 
    margin-top: 0.6rem !important; 
    margin-bottom: 0.4rem !important; 
    line-height: 1.2 !important; 
}

h3 { 
    font-size: 1.1rem !important; 
    margin-top: 0.5rem !important; 
    margin-bottom: 0.3rem !important; 
    line-height: 1.2 !important; 
}

/* Reduce spacing between elements */
.element-container { margin-bottom: 0.4rem !important; }
.stMarkdown { margin-bottom: 0.4rem !important; }

/* Readable metric fonts */
[data-testid="stMetricValue"] { font-size: 1.6rem !important; }
[data-testid="stMetricLabel"] { font-size: 0.95rem !important; padding-bottom: 0.3rem !important; }
[data-testid="metric-container"] { padding: 0.7rem !important; }

/* Chart and data spacing */
.stPlotlyChart { margin-bottom: 0.6rem !important; }
.stDataFrame { margin-bottom: 0.6rem !important; }

/* Column spacing */
[data-testid="column"] { padding: 0.3rem !important; }

/* Interactive elements */
[data-testid="stExpander"] { margin-bottom: 0.5rem !important; }
[data-testid="stTabs"] { margin-bottom: 0.6rem !important; }
.stTabs [data-baseweb="tab-list"] { gap: 0.3rem !important; }
.stTabs [data-baseweb="tab"] { 
    padding: 0.5rem 1rem !important; 
    font-size: 0.95rem !important; 
}

/* Buttons - keep readable */
.stButton > button { 
    padding: 0.6rem 1.2rem !important; 
    font-size: 0.95rem !important; 
}

/* Form inputs */
.stSelectbox, .stTextInput, .stNumberInput { margin-bottom: 0.4rem !important; }

/* Alerts - keep readable */
.stAlert { 
    padding: 0.7rem !important; 
    margin-bottom: 0.5rem !important; 
    font-size: 0.95rem !important; 
}

/* Reduce gaps between blocks */
div[data-testid="stVerticalBlock"] > div { gap: 0.4rem !important; }

/* Horizontal rules */
hr { margin: 0.6rem 0 !important; }

/* Mobile adjustments - Match Home page formatting */
@media (max-width: 768px) {
    .header-container {
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(74, 61, 111, 0.15);
    }
    
    .header-title {
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
        line-height: 1.3;
        font-weight: 600;
    }
    
    .header-subtitle {
        font-size: 0.65rem;
        line-height: 1.2;
    }
    
    /* Mobile spacing - tighter */
    div.block-container {
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    h1 {
        margin-top: 0.5rem !important;
        font-size: 1.5rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h2 {
        margin-top: 0.75rem !important;
        font-size: 1.25rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h4, h5, h6 {
        text-align: center !important;
    }
    
    /* Center align markdown headers on mobile */
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4,
    div[data-testid="stMarkdownContainer"] h5,
    div[data-testid="stMarkdownContainer"] h6 {
        text-align: center !important;
    }
    
    /* Center align metrics on mobile */
    [data-testid="stMetric"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"],
    [data-testid="metric-container"],
    .compact-metric-card,
    .kpi-card {
        text-align: center !important;
    }
    
    /* Mobile columns - stack vertically */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        padding: 0.2rem !important;
    }
    
    /* Mobile buttons - full width */
    button[kind="primary"],
    button[kind="secondary"] {
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Mobile metrics - smaller */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
    }
    
    /* Mobile tables - horizontal scroll */
    .stDataFrame {
        overflow-x: auto !important;
    }
    
    /* Mobile tabs - stack vertically to eliminate horizontal scrolling */
    [data-testid="stTabs"] {
        overflow-x: visible !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: column !important;
        width: 100% !important;
        gap: 0.5rem !important;
        overflow-x: visible !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
    
    /* Wrap Plotly chart titles on mobile */
    .js-plotly-plot .gtitle,
    .plotly .gtitle,
    .js-plotly-plot .xtitle,
    .plotly .xtitle {
        word-wrap: break-word !important;
        white-space: normal !important;
        max-width: 100% !important;
        overflow-wrap: break-word !important;
        hyphens: auto !important;
    }
    
    /* Ensure chart titles wrap */
    .js-plotly-plot .gtitle text,
    .plotly .gtitle text {
        word-wrap: break-word !important;
        white-space: normal !important;
    }
}
    </style>
    """, unsafe_allow_html=True)

# Clear session state on first run (after page config)
# iOS Safari optimized: Preserve navigation state and skip unnecessary clears
if 'initialized' not in st.session_state:
    # Detect iOS Safari to optimize clearing behavior
    is_ios = False
    try:
        # Try to get user agent from request headers
        if hasattr(st, 'request_headers'):
            user_agent = st.request_headers.get('User-Agent', '').lower()
            is_ios = any(x in user_agent for x in ['iphone', 'ipad', 'ipod'])
        elif hasattr(st, 'server') and hasattr(st.server, 'request'):
            user_agent = st.server.request.headers.get('User-Agent', '').lower()
            is_ios = any(x in user_agent for x in ['iphone', 'ipad', 'ipod'])
    except:
        pass
    
    # Store current page before clearing
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        current_page = None
        if ctx:
            current_page = getattr(ctx, 'current_page_name', None)
    except:
        current_page = None
    
    # Preserve navigation keys
    navigation_keys = ['current_page', 'previous_page', 'navigation_history', 'mobile_redirected', 'initialized']
    preserved_state = {}
    
    for key in navigation_keys:
        if key in st.session_state:
            preserved_state[key] = st.session_state[key]
    
    # Store current page if detected
    if current_page:
        preserved_state['current_page'] = current_page
    
    # On iOS Safari, skip aggressive clearing on subsequent loads to prevent slow loading
    # Check preserved_state since we haven't cleared yet, but will check original state
    has_mobile_redirected = 'mobile_redirected' in st.session_state or 'mobile_redirected' in preserved_state
    
    if is_ios and has_mobile_redirected:
        # Only clear non-navigation state, preserve everything else
        keys_to_clear = [
            k for k in st.session_state.keys() 
            if k not in navigation_keys and k != 'current_page'
        ]
        for key in keys_to_clear:
            del st.session_state[key]
    else:
        # Full clear for first load or non-iOS devices
        st.session_state.clear()
    
    # Restore preserved navigation state
    st.session_state.update(preserved_state)
    
    # Ensure initialized flag is set
    st.session_state.initialized = True
    
    # Restore current page immediately after clearing (explicit restore)
    if current_page:
        st.session_state.current_page = current_page
    elif 'current_page' in preserved_state:
        st.session_state.current_page = preserved_state['current_page']
    
    # ====================================================================
    # FIX 3: Standardize sidebar state management for iOS Safari
    # ====================================================================
    # Initialize sidebar state in session state
    if 'sidebar_state' not in st.session_state:
        st.session_state.sidebar_state = 'auto'
    
    # Detect iOS and force sidebar closed on mobile
    if is_ios:
        # On iOS, always force sidebar closed on mobile devices
        st.session_state.sidebar_state = 'collapsed'

# ============================================================================
# NOW safe to import custom modules (after page config)
# ============================================================================

# Optional import for metric card styling
try:
    from streamlit_extras.metric_cards import style_metric_cards
    HAS_STREAMLIT_EXTRAS = True
except ImportError:
    HAS_STREAMLIT_EXTRAS = False
    def style_metric_cards(*args, **kwargs):
        """Fallback if streamlit-extras not available"""
        pass

# Import custom utility modules (NOW safe after page config)
from utils.database import execute_query, show_db_status, get_connection
from utils.queries import get_portfolio_summary_query
from utils.plan_context import get_plan_context, get_plan_size_scenarios, get_industry_benchmarks
from src.utils.formatters import (
    format_date_mmddyyyy, 
    format_date_range, 
    safe_float as safe_float_formatter,  # Rename to avoid conflict
    safe_int as safe_int_formatter,      # Rename to avoid conflict
    safe_percent,
    standardize_measure_names
)
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# ============================================================================
# CONSTANTS - No Streamlit commands
# ============================================================================
ALL_HEDIS_MEASURES = [
    "HbA1c Testing (CDC)",
    "Blood Pressure Control (CBP)",
    "Colorectal Cancer Screening (COL)",
    "Breast Cancer Screening (BCS)",
    "Controlling High Blood Pressure (CBP)",
    "Diabetes Eye Exam (EED)",
    "Diabetes Kidney Disease Monitoring (KED)",
    "Statin Therapy for CVD (SPC)",
    "Follow-Up After ED - Mental Health (FUM)",
    "Antidepressant Medication Management (AMM)",
    "Plan All-Cause Readmissions (PCR)",
    "Medication Adherence - Diabetes (MAD)"
]

PLAN_SIZE_OPTIONS = [
    "Small (< 10K)",
    "Medium (10K - 50K)",
    "Large (50K - 100K)",
    "Very Large (> 100K)"
]

# Note: Additional utilities (safe_percent, format_date_*, standardize_measure_names) 
# are imported from src.utils.formatters as safe_float_formatter, safe_int_formatter

# ============================================================================
# UTILITY FUNCTIONS - No Streamlit commands
# ============================================================================
def safe_float(value, default=0.0):
    """Safely convert to float"""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value, default=0):
    """Safely convert to int"""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# ============================================================================
# FORMATTING FUNCTIONS
# ============================================================================

def format_currency(value, decimals=0):
    """
    Format value as currency with optional decimals
    
    Args:
        value: Numeric value to format
        decimals: Number of decimal places (default 0)
    
    Returns:
        Formatted string like "$1,234" or "$1,234.56"
    """
    if pd.isna(value) or value is None:
        return "$0"
    
    if decimals == 0:
        return f"${value:,.0f}"
    else:
        return f"${value:,.{decimals}f}"

def format_percent(value, decimals=1):
    """
    Format value as percentage
    
    Args:
        value: Numeric value (0-1 for decimal, or 0-100 for percentage)
        decimals: Number of decimal places
    
    Returns:
        Formatted string like "42.5%"
    """
    if pd.isna(value) or value is None:
        return "0.0%"
    
    # Convert to percentage if needed
    if value <= 1.0:
        value = value * 100
    
    return f"{value:.{decimals}f}%"

def format_number(value, decimals=0):
    """
    Format number with thousands separator
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
    
    Returns:
        Formatted string like "1,234" or "1,234.56"
    """
    if pd.isna(value) or value is None:
        return "0"
    
    if decimals == 0:
        return f"{value:,.0f}"
    else:
        return f"{value:,.{decimals}f}"

# ============================================================================
# SYNTHETIC DATA GENERATOR - For demonstration when database is empty
# ============================================================================
def generate_synthetic_portfolio_data():
    """
    Generate realistic synthetic HEDIS portfolio data with all required columns
    for filtering and analysis
    """
    np.random.seed(42)  # Reproducible data
    
    measures = ALL_HEDIS_MEASURES
    plan_sizes = [8000, 15000, 35000, 75000, 150000]  # Actual member counts
    
    data_rows = []
    
    for measure in measures:
        for plan_size in plan_sizes:
            # Calculate baseline metrics per measure
            base_investment = np.random.uniform(12000, 20000)
            base_members = np.random.randint(100, 500)
            base_closures = int(base_members * np.random.uniform(0.35, 0.50))
            
            # Scale by plan size
            scale = plan_size / 10000
            
            row = {
                'measure_name': measure,
                'plan_size': plan_size,
                'plan_size_category': (
                    'Small (< 10K)' if plan_size < 10000 else
                    'Medium (10K - 50K)' if plan_size < 50000 else
                    'Large (50K - 100K)' if plan_size < 100000 else
                    'Very Large (> 100K)'
                ),
                'member_count': int(base_members * scale),
                'total_interventions': int(base_members * scale * 1.2),
                'successful_closures': int(base_closures * scale),
                'predicted_closure_probability': np.random.uniform(0.35, 0.55),
                'investment': base_investment * scale,
                'financial_value': base_investment * scale * np.random.uniform(1.15, 1.40),
                'revenue_impact': base_investment * scale * np.random.uniform(1.20, 1.45),
                'net_benefit': base_investment * scale * np.random.uniform(0.15, 0.45),
                'roi_ratio': np.random.uniform(1.15, 1.40),
                'success_rate': np.random.uniform(35, 50),
                'cost_per_closure': base_investment / base_closures if base_closures > 0 else 0,
                'service_date': pd.Timestamp('2025-10-15')  # Default date in Q4 2025
            }
            
            data_rows.append(row)
    
    return pd.DataFrame(data_rows)


def generate_synthetic_summary(df):
    """
    Generate portfolio summary from detailed data
    
    Args:
        df: DataFrame with detailed measure/plan data
    
    Returns:
        Dict with portfolio summary metrics
    """
    if df.empty:
        return {
            'total_investment': 0,
            'total_closures': 0,
            'revenue_impact': 0,
            'net_benefit': 0,
            'total_interventions': 0,
            'roi_ratio': 0,
            'overall_success_rate': 0,
            'total_members': 0
        }
    
    return {
        'total_investment': df['investment'].sum(),
        'total_closures': df['successful_closures'].sum(),
        'revenue_impact': df['revenue_impact'].sum(),
        'net_benefit': df['net_benefit'].sum(),
        'total_interventions': df['total_interventions'].sum(),
        'roi_ratio': df['revenue_impact'].sum() / df['investment'].sum() if df['investment'].sum() > 0 else 0,
        'overall_success_rate': (df['successful_closures'].sum() / df['total_interventions'].sum() * 100) if df['total_interventions'].sum() > 0 else 0,
        'total_members': df['member_count'].sum()
    }

# ============================================================================
# DATA FILTERING FUNCTION - MUST BE DEFINED BEFORE SIDEBAR
# ============================================================================
def apply_all_filters(data):
    """Apply all active filters to the dataset"""
    filtered = data.copy()
    
    # Apply measure filter
    if st.session_state.filters.get('selected_measures'):
        filtered = filtered[
            filtered['measure_name'].isin(st.session_state.filters['selected_measures'])
        ]
    
    # Apply plan size filter  
    if st.session_state.filters.get('plan_sizes'):
        filtered = filtered[
            filtered['plan_size_category'].isin(st.session_state.filters['plan_sizes'])
        ]
    
    # Apply member count threshold - READ FROM FILTERS DICTIONARY (synced from widget)
    min_members = st.session_state.filters.get('min_members', 0)
    if min_members > 0:
        filtered = filtered[
            filtered['member_count'] >= min_members
        ]
    
    # Apply financial value threshold - READ FROM FILTERS DICTIONARY (synced from widget)
    min_financial = st.session_state.filters.get('min_financial_value', 0)
    if min_financial > 0:
        # Convert K to dollars for comparison
        min_financial_dollars = min_financial * 1000
        filtered = filtered[
            filtered['financial_value'] >= min_financial_dollars
        ]
    
    # Apply closure rate threshold - READ FROM FILTERS DICTIONARY (synced from widget)
    min_closure = st.session_state.filters.get('min_closure_rate', 0)
    if min_closure > 0:
        min_closure_prob = min_closure / 100.0  # Convert % to probability
        filtered = filtered[
            filtered['predicted_closure_probability'] >= min_closure_prob
        ]
    
    return filtered

# ============================================================================
# 3. SESSION STATE INITIALIZATION
# ============================================================================
# Note: Widget keys are initialized in the sidebar (widget-only approach)
# membership_size is now set automatically based on Plan Size filter selection (consolidated)

if 'filters' not in st.session_state:
    st.session_state.filters = {
        'selected_measures': [],
        'plan_sizes': [],
        'min_members': 0,
        'min_financial_value': 0,
        'min_closure_rate': 0,
        'date_range_start': date(2025, 10, 1),
        'date_range_end': date(2025, 12, 31)
    }

# Initialize with all options selected by default
if not st.session_state.filters.get('selected_measures'):
    st.session_state.filters['selected_measures'] = ALL_HEDIS_MEASURES.copy()

if not st.session_state.filters.get('plan_sizes'):
    st.session_state.filters['plan_sizes'] = PLAN_SIZE_OPTIONS.copy()

# Backward compatibility
if 'all_measures' not in st.session_state:
    st.session_state.all_measures = ALL_HEDIS_MEASURES

if 'selected_measures' not in st.session_state:
    st.session_state.selected_measures = st.session_state.filters.get('selected_measures', [])

if 'date_range' not in st.session_state:
    st.session_state.date_range = {
        'start': st.session_state.filters.get('date_range_start', date(2025, 10, 1)),
        'end': st.session_state.filters.get('date_range_end', date(2025, 12, 31))
    }

if 'filters_initialized' not in st.session_state:
    st.session_state.filters_initialized = True
    st.session_state.data_loaded = False

# ============================================================================
# 4. LOAD DATA (BEFORE SIDEBAR!)
# ============================================================================

# Generate synthetic data once and cache it in session state
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = generate_synthetic_portfolio_data()
    st.session_state.data_loaded = True
    
    if len(st.session_state.portfolio_data) == 0:
        st.error("⚠️ Synthetic data generation failed!")
    else:
        # Check measure names
        unique_measures = st.session_state.portfolio_data['measure_name'].unique()
        if len(unique_measures) != len(ALL_HEDIS_MEASURES):
            st.warning(f"⚠️ Expected {len(ALL_HEDIS_MEASURES)} measures, got {len(unique_measures)}")

# Create raw_portfolio_data for use in sidebar and main content
raw_portfolio_data = st.session_state.portfolio_data.copy()

# Sync membership_size from widget for backward compatibility
if 'membership_slider_widget' in st.session_state:
    st.session_state.membership_size = st.session_state.membership_slider_widget
elif 'membership_size' not in st.session_state:
    st.session_state.membership_size = 10000

# Set membership_size and scale_factor for backward compatibility
BASELINE_MEMBERS = 10000
scale_factor = st.session_state.membership_size / BASELINE_MEMBERS

# ============================================================================
# CUSTOM CSS - DESKTOP OPTIMIZED
# ============================================================================
st.markdown("""
<style>
    /* Main page background - professional healthcare theme */
    .stApp {
        background: linear-gradient(to bottom, #f0f4f8 0%, #ffffff 100%);
    }
    
    /* Main content container - desktop padding */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 100%;
    }
    
    /* Typography - desktop optimized */
    h1 {
        font-size: 2.5rem !important;
        color: #0066cc;
        font-weight: 700;
        margin-bottom: 1rem;
        border-bottom: 3px solid #00cc66;
        padding-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 2rem !important;
        color: #0066cc;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.5rem !important;
        color: #0066cc;
        font-weight: 600;
    }
    
    /* Metric cards - enhanced styling */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700;
        color: #0066cc;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1.1rem !important;
        font-weight: 600;
    }
    
    /* Metric card containers - professional polish - CENTER ALIGNED */
    [data-testid="stMetricContainer"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #00cc66;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center !important;
        margin: 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    [data-testid="stMetricContainer"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Ensure all metric content is centered */
    [data-testid="stMetricContainer"] > * {
        text-align: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* Sidebar styling - matches StarGuard AI header purple gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #4e2a84 0%, #6f5f96 100%);
        padding-top: 2rem;
    }
    
    /* Style "app" link as "Home" in sidebar navigation - show it and style it */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href="/"],
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href="./"],
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[href*="app"],
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li:first-child a,
    [data-testid="stSidebar"] nav a[href="/"],
    [data-testid="stSidebar"] nav a[href="./"] {
        color: #FFFFFF !important;
        display: flex !important;
    }
    
    /* Ensure the list item containing the "app" link is visible */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li:first-child,
    [data-testid="stSidebar"] nav ul li:first-child {
        display: list-item !important;
    }
    
    /* Additional targeting for Streamlit's navigation structure */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] > div > ul > li:first-child,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] > ul > li:first-child {
        display: list-item !important;
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
    
    /* Value proposition - dark text on light background (override sidebar white text) */
    [data-testid="stSidebar"] .sidebar-value-proposition,
    [data-testid="stSidebar"] div[style*="background-color: #e8f5e9"],
    [data-testid="stSidebar"] div[style*="background-color:#e8f5e9"] {
        color: #000000 !important;
    }
    
    [data-testid="stSidebar"] .sidebar-value-proposition p,
    [data-testid="stSidebar"] .sidebar-value-proposition span,
    [data-testid="stSidebar"] .sidebar-value-proposition strong,
    [data-testid="stSidebar"] .sidebar-value-proposition div,
    [data-testid="stSidebar"] div[style*="background-color: #e8f5e9"] p,
    [data-testid="stSidebar"] div[style*="background-color: #e8f5e9"] span,
    [data-testid="stSidebar"] div[style*="background-color: #e8f5e9"] strong,
    [data-testid="stSidebar"] div[style*="background-color:#e8f5e9"] p,
    [data-testid="stSidebar"] div[style*="background-color:#e8f5e9"] span,
    [data-testid="stSidebar"] div[style*="background-color:#e8f5e9"] strong {
        color: #000000 !important;
    }
    
    /* Sidebar selectbox and inputs */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stDateInput label {
        color: #ffffff !important;
    }
    
    /* Executive summary expander - expanded by default styling */
    .streamlit-expanderHeader {
        background-color: #e3f2fd;
        border-left: 4px solid #0066cc;
        padding: 1rem;
        border-radius: 8px;
        color: #ffffff !important;
    }
    
    /* Expander header text - make "View less" button visible */
    .streamlit-expanderHeader p,
    .streamlit-expanderHeader span,
    .streamlit-expanderHeader div,
    .streamlit-expanderHeader button,
    .streamlit-expanderHeader label,
    .streamlit-expanderHeader h1,
    .streamlit-expanderHeader h2,
    .streamlit-expanderHeader h3,
    .streamlit-expanderHeader h4,
    .streamlit-expanderHeader h5,
    .streamlit-expanderHeader h6 {
        color: #ffffff !important;
    }
    
    /* Specifically target the "View less" / "View more" text and icon */
    .streamlit-expanderHeader [data-testid="stExpanderToggleIcon"],
    .streamlit-expanderHeader svg,
    .streamlit-expanderHeader path {
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }
    
    /* Target Streamlit's expander toggle button text */
    button[aria-label*="View"],
    button[aria-label*="view"],
    .streamlit-expanderHeader button span {
        color: #ffffff !important;
    }
    
    /* Sidebar navigation "View 10 more" / "View less" button - white text */
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
        color: #ffffff !important;
    }
    
    /* Specifically target "View 10 more" and "View less" navigation buttons */
    [data-testid="stSidebar"] button[aria-label*="View"],
    [data-testid="stSidebar"] button[aria-label*="view"],
    [data-testid="stSidebar"] button[aria-label*="more"],
    [data-testid="stSidebar"] button[aria-label*="less"],
    [data-testid="stSidebar"] button[aria-label*="More"],
    [data-testid="stSidebar"] button[aria-label*="Less"] {
        color: #ffffff !important;
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
        color: #ffffff !important;
    }
    
    /* Force white text for ALL sidebar buttons and their children */
    [data-testid="stSidebar"] button,
    [data-testid="stSidebar"] button * {
        color: #ffffff !important;
    }
    
    /* Info/Success boxes - enhanced */
    .stInfo {
        background-color: #e3f2fd;
        border-left: 4px solid #0066cc;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stSuccess {
        background-color: #e8f5e9;
        border-left: 4px solid #00cc66;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f4f8;
        border-radius: 8px 8px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0066cc;
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #0052a3;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 102, 204, 0.3);
    }
    
    /* Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #e0e0e0;
    }
    
    /* Chart containers */
    .plotly-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Spacing utilities */
    .spacer-small {
        height: 1rem;
    }
    
    .spacer-medium {
        height: 2rem;
    }
    
    .spacer-large {
        height: 3rem;
    }
</style>

<script>
    // Hide "app" label and mobile pages in sidebar navigation
    function hideAppLabel() {
        // Wait for sidebar navigation to load
        const sidebarNav = document.querySelector('[data-testid="stSidebarNav"]');
        if (sidebarNav) {
            // Find and hide links to main app and mobile pages
            const links = sidebarNav.querySelectorAll('a');
            links.forEach(link => {
                const href = link.getAttribute('href') || '';
                const text = link.textContent.trim().toLowerCase();
                
                // Hide app.py links
                if (href === '/' || href === './' || href.includes('app') || text === 'app') {
                    link.style.display = 'none';
                    const parent = link.closest('li');
                    if (parent) parent.style.display = 'none';
                }
                
                // Hide mobile page links - More aggressive matching
                const mobilePatterns = ['mobile', '_mobile', '📱', 'mobile ai', 'mobile roi', 'mobile scenario', 'mobile test', 'mobile view'];
                const textLower = text.toLowerCase();
                const hrefLower = href.toLowerCase();
                
                const isMobile = mobilePatterns.some(pattern => 
                    textLower.includes(pattern.toLowerCase()) || 
                    hrefLower.includes(pattern.toLowerCase())
                );
                
                if (isMobile) {
                    link.style.display = 'none';
                    link.style.visibility = 'hidden';
                    link.style.height = '0';
                    link.style.padding = '0';
                    link.style.margin = '0';
                    const parent = link.closest('li');
                    if (parent) {
                        parent.style.display = 'none';
                        parent.style.visibility = 'hidden';
                        parent.style.height = '0';
                        parent.style.padding = '0';
                        parent.style.margin = '0';
                    }
                    // Also hide parent ul if it becomes empty
                    const parentUl = link.closest('ul');
                    if (parentUl) {
                        const visibleItems = parentUl.querySelectorAll('li:not([style*="display: none"])');
                        if (visibleItems.length === 0) {
                            parentUl.style.display = 'none';
                        }
                    }
                }
            });
            
            // Hide first navigation item (usually the main app)
            const firstItem = sidebarNav.querySelector('ul > li:first-child');
            if (firstItem && firstItem.textContent.trim().toLowerCase() === 'app') {
                firstItem.style.display = 'none';
            }
        }
    }
    
    // Run on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', hideAppLabel);
    } else {
        hideAppLabel();
    }
    
    // Also run after delays to catch dynamically loaded content and mobile links
    setTimeout(hideAppLabel, 500);
    setTimeout(hideAppLabel, 1000);
    setTimeout(hideAppLabel, 2000);
    
    // Periodically check for mobile links (more frequent to catch them early)
    // Only run if not on a mobile page
    if (!window.location.pathname.includes('_mobile_') && !window.location.pathname.includes('mobile')) {
        setInterval(hideAppLabel, 1000); // Check every second
        setInterval(hideAppLabel, 500); // Also check every 500ms for first few seconds
        setTimeout(() => setInterval(hideAppLabel, 2000), 10000); // Then every 2 seconds
    }
    
    // Additional aggressive cleanup - remove any mobile elements from DOM
    function aggressiveMobileCleanup() {
        // Find all navigation items
        const allNavItems = document.querySelectorAll('[data-testid="stSidebarNav"] li, [data-testid="stSidebarNav"] a');
        allNavItems.forEach(item => {
            const text = item.textContent?.toLowerCase() || '';
            const href = item.getAttribute('href')?.toLowerCase() || '';
            if (text.includes('mobile') || href.includes('mobile') || text.includes('_mobile')) {
                item.remove(); // Actually remove from DOM, not just hide
            }
        });
    }
    
    // Run aggressive cleanup after page loads
    setTimeout(aggressiveMobileCleanup, 100);
    setTimeout(aggressiveMobileCleanup, 500);
    setTimeout(aggressiveMobileCleanup, 1000);
    setTimeout(aggressiveMobileCleanup, 2000);
</script>
""", unsafe_allow_html=True)


# ============================================================================
# 5. SIDEBAR (AFTER DATA IS LOADED)
# ============================================================================
# Sliders can now safely access raw_portfolio_data
with st.sidebar:
    st.markdown("## 🔒 Secure Healthcare AI")
    st.markdown("### HEDIS Portfolio Optimizer")
    st.caption("HIPAA-Compliant | Zero PHI Exposure")
    st.markdown("---")
    st.title("🎛️ Filters")
    
    # ====================================================================
    # MEMBERSHIP SIZE CONTROL - REMOVED (CONSOLIDATED WITH PLAN SIZE FILTER)
    # ====================================================================
    # Note: Plan Membership Size is now automatically set based on Plan Size filter selection
    # This eliminates redundancy and simplifies the user experience
    
    # ====================================================================
    # DATE RANGE - Default Q4 2025
    # ====================================================================
    st.markdown("### 📅 Date Range")
    
    # Quick presets
    preset_col1, preset_col2 = st.columns(2, gap="small")
    
    with preset_col1:
        if st.button("Q4 2025", key="preset_q4", use_container_width=True):
            st.session_state.filters['date_range_start'] = date(2025, 10, 1)
            st.session_state.filters['date_range_end'] = date(2025, 12, 31)
            st.rerun()
    
    with preset_col2:
        if st.button("Full Year", key="preset_full_year", use_container_width=True):
            st.session_state.filters['date_range_start'] = date(2025, 1, 1)
            st.session_state.filters['date_range_end'] = date(2025, 12, 31)
            st.rerun()
    
    # Date inputs
    date_col1, date_col2 = st.columns(2, gap="small")
    
    with date_col1:
        start_date = st.date_input(
            "Start Date",
            value=st.session_state.filters['date_range_start'],
            key="start_date_filter",
            format="MM/DD/YYYY"
        )
        st.session_state.filters['date_range_start'] = start_date
    
    with date_col2:
        end_date = st.date_input(
            "End Date",
            value=st.session_state.filters['date_range_end'],
            key="end_date_filter",
            format="MM/DD/YYYY"
        )
        st.session_state.filters['date_range_end'] = end_date
    
    # Display and validate
    if start_date <= end_date:
        days = (end_date - start_date).days
        st.caption(f"📆 {start_date.strftime('%m/%d/%Y')} to {end_date.strftime('%m/%d/%Y')} ({days} days)")
    else:
        st.error("⚠️ Start date must be before end date")
    
    # Update backward compatibility
    st.session_state.date_range = {'start': start_date, 'end': end_date}
    
    st.markdown("---")
    
    # ====================================================================
    # HEDIS MEASURES - All 12 Selected by Default
    # ====================================================================
    st.markdown("### 📋 HEDIS Measures")
    
    # Get measures from session state
    ALL_MEASURES = st.session_state.all_measures
    
    # Quick select buttons
    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button("Select All", key="select_all_measures", use_container_width=True):
            st.session_state.filters['selected_measures'] = ALL_MEASURES.copy()
            st.rerun()
    
    with col2:
        if st.button("Clear All", key="clear_all_measures", use_container_width=True):
            st.session_state.filters['selected_measures'] = []
            st.rerun()
    
    # Multiselect with ALL measures selected by default
    selected_measures = st.multiselect(
        "Choose measures to analyze:",
        options=ALL_MEASURES,
        default=st.session_state.filters['selected_measures'],  # Will be all 12 by default
        key="measures_multiselect",
        help="Select one or more HEDIS measures to include in analysis"
    )
    
    # Update state
    st.session_state.filters['selected_measures'] = selected_measures
    st.session_state.selected_measures = selected_measures  # Backward compatibility
    
    # Show count
    if len(selected_measures) == len(ALL_MEASURES):
        st.success(f"✅ All {len(ALL_MEASURES)} measures selected")
    else:
        st.caption(f"✅ {len(selected_measures)} of {len(ALL_MEASURES)} measures selected")
    
    st.markdown("---")
    
    # ========================================================================
    # PLAN SIZE FILTER (CONSOLIDATED - Also sets scaling membership size)
    # ========================================================================
    st.markdown("### 🏥 Plan Size")
    
    PLAN_SIZE_OPTIONS = [
        "Small (< 10K)",
        "Medium (10K - 50K)",
        "Large (50K - 100K)",
        "Very Large (> 100K)"
    ]
    
    # Map plan size categories to representative membership values for scaling
    PLAN_SIZE_TO_MEMBERSHIP = {
        "Small (< 10K)": 8000,
        "Medium (10K - 50K)": 30000,
        "Large (50K - 100K)": 75000,
        "Very Large (> 100K)": 150000
    }
    
    selected_plan_sizes = st.multiselect(
        "Select plan size categories:",
        options=PLAN_SIZE_OPTIONS,
        default=st.session_state.filters['plan_sizes'] if st.session_state.filters['plan_sizes'] else PLAN_SIZE_OPTIONS.copy(),
        key="plan_size_multiselect",
        help="Filter data by plan size category and set scaling membership size for calculations"
    )
    
    # Update state
    st.session_state.filters['plan_sizes'] = selected_plan_sizes
    
    # CONSOLIDATION: Set membership_size based on selected plan size
    # If a single category is selected, use that value. If multiple, use the first one.
    # If none selected, keep current value or default to 10,000
    if selected_plan_sizes:
        # Use the first selected category to set membership size for scaling
        first_selected = selected_plan_sizes[0]
        st.session_state.membership_size = PLAN_SIZE_TO_MEMBERSHIP.get(first_selected, 10000)
        st.session_state.membership_slider_widget = st.session_state.membership_size
        
        # Show which value is being used for scaling
        if len(selected_plan_sizes) == 1:
            st.caption(f"✅ {len(selected_plan_sizes)} plan size selected | 📊 Scaling to {st.session_state.membership_size:,} members")
        else:
            st.caption(f"✅ {len(selected_plan_sizes)} plan sizes selected | 📊 Scaling to {st.session_state.membership_size:,} members (using first selection)")
    else:
        # No selection - keep current value or set default
        if 'membership_size' not in st.session_state:
            st.session_state.membership_size = 10000
            st.session_state.membership_slider_widget = 10000
        st.caption(f"⚠️ No plan sizes selected - using {st.session_state.membership_size:,} members for scaling")
    
    st.markdown("---")
    
    # ====================================================================
    # THRESHOLD FILTERS - COMPLETE WORKING VERSION
    # ====================================================================
    st.markdown("### 🎯 Threshold Filters")
    
    # Ensure filters dictionary exists
    if 'filters' not in st.session_state:
        st.session_state.filters = {}
    
    # Get data range for closure slider
    try:
        max_closure_pct = int(raw_portfolio_data['predicted_closure_probability'].max() * 100)
        min_closure_pct = int(raw_portfolio_data['predicted_closure_probability'].min() * 100)
    except:
        max_closure_pct = 100
        min_closure_pct = 0
    
    # MIN MEMBERS SLIDER
    min_members_value = st.slider(
        "Minimum Member Count",
        min_value=0,
        max_value=1000,
        value=st.session_state.filters.get('min_members', 0),
        step=25,
        key="threshold_min_members"
    )
    st.session_state.filters['min_members'] = min_members_value
    st.caption(f"🔍 Filtering: ≥ {min_members_value} members")
    
    # MIN FINANCIAL SLIDER
    min_financial_value = st.slider(
        "Minimum Financial Value ($K)",
        min_value=0,
        max_value=500,
        value=st.session_state.filters.get('min_financial_value', 0),
        step=25,
        key="threshold_min_financial"
    )
    st.session_state.filters['min_financial_value'] = min_financial_value
    st.caption(f"🔍 Filtering: ≥ ${min_financial_value}K value")
    
    # MIN CLOSURE RATE SLIDER
    min_closure_value = st.slider(
        "Minimum Predicted Closure Rate (%)",
        min_value=min_closure_pct,
        max_value=max_closure_pct,
        value=min(st.session_state.filters.get('min_closure_rate', min_closure_pct), max_closure_pct),
        step=5,
        key="threshold_min_closure",
        help=f"Range: {min_closure_pct}% - {max_closure_pct}% based on your data"
    )
    st.session_state.filters['min_closure_rate'] = min_closure_value
    
    if max_closure_pct < 100:
        st.caption(f"🔍 Filtering: ≥ {min_closure_value}% (data range: {min_closure_pct}%-{max_closure_pct}%)")
    else:
        st.caption(f"🔍 Filtering: ≥ {min_closure_value}% closure rate")
    
    st.markdown("---")
    
    
    # ============================================================================
    # LIVE FILTER PREVIEW
    # ============================================================================
    st.markdown("---")
    st.markdown("### 📊 Filter Impact")
    
    # Apply all current filters to see what would be returned
    if 'portfolio_data' in st.session_state:
        preview_data = st.session_state.portfolio_data.copy()
    else:
        preview_data = generate_synthetic_portfolio_data()
    
    preview_filtered = apply_all_filters(preview_data)
    
    # Calculate impact metrics
    total_rows = len(preview_data)
    filtered_rows = len(preview_filtered)
    filter_pct = (filtered_rows / total_rows * 100) if total_rows > 0 else 0
    
    # Color-coded display based on filter strictness
    if filter_pct < 25:
        color = "🔴"
        warning = "**Very strict filters** - showing only top opportunities"
    elif filter_pct < 50:
        color = "🟡"
        warning = "**Moderate filters** - good balance"
    elif filter_pct < 75:
        color = "🟢"
        warning = "**Light filters** - broad view"
    else:
        color = "🔵"
        warning = "**Minimal filters** - nearly all data"
    
    st.markdown(f"""
    {color} **{filtered_rows:,}** of **{total_rows:,}** records  
    
    {filter_pct:.1f}% of total portfolio  
    
    {warning}
    
    """)
    
    # Show which filters are active
    active_filters = []
    if st.session_state.filters.get('selected_measures'):
        count = len(st.session_state.filters['selected_measures'])
        active_filters.append(f"✓ {count} HEDIS measures")
    if st.session_state.filters.get('plan_sizes'):
        count = len(st.session_state.filters['plan_sizes'])
        active_filters.append(f"✓ {count} plan sizes")
    if st.session_state.filters.get('min_members', 0) > 0:
        active_filters.append(f"✓ Members ≥ {st.session_state.filters['min_members']}")
    if st.session_state.filters.get('min_financial_value', 0) > 0:
        active_filters.append(f"✓ Value ≥ ${st.session_state.filters['min_financial_value']}K")
    if st.session_state.filters.get('min_closure_rate', 0) > 0:
        active_filters.append(f"✓ Closure ≥ {st.session_state.filters['min_closure_rate']}%")
    
    if active_filters:
        st.markdown("**Active Filters:**")
        for filter_desc in active_filters:
            st.markdown(f"- {filter_desc}")
    else:
        st.info("No filters active - showing all data")
    
    # Quick stats from filtered data
    if not preview_filtered.empty:
        with st.expander("📈 Filtered Data Stats", expanded=False):
            st.markdown("**Summary of Current View:**")
            
            # Calculate key metrics from filtered data
            if 'member_count' in preview_filtered.columns:
                total_members = preview_filtered['member_count'].sum()
            else:
                total_members = 0
            
            if 'predicted_closure_probability' in preview_filtered.columns:
                avg_closure = preview_filtered['predicted_closure_probability'].mean() * 100  # Convert to percentage
            else:
                avg_closure = 0
            
            if 'financial_value' in preview_filtered.columns:
                total_value = preview_filtered['financial_value'].sum()
            else:
                total_value = 0
            
            col1, col2 = st.columns(2, gap="small")
            with col1:
                st.metric("Total Members", f"{total_members:,.0f}")
                st.metric("Avg Closure Rate", f"{avg_closure:.1f}%")
            with col2:
                st.metric("Total Value", format_currency(total_value))
                st.metric("Records", f"{filtered_rows:,}")
            
            # Show measure distribution in filtered data
            if 'measure_name' in preview_filtered.columns:
                measure_counts = preview_filtered['measure_name'].value_counts()
                st.markdown("**Measures in View:**")
                for measure, count in measure_counts.head(5).items():
                    st.markdown(f"- {measure}: {count} records")
    
    st.markdown("---")
    
    # ========================================================================
    # FILTER ACTIONS
    # ========================================================================
    st.markdown("### ⚙️ Actions")
    
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        if st.button("🔄 Reset All", key="reset_filters_btn", use_container_width=True):
            # Reset to defaults
            st.session_state.filters = {
                'selected_measures': st.session_state.all_measures.copy(),
                'plan_sizes': [
                    "Small (< 10K)",
                    "Medium (10K - 50K)",
                    "Large (50K - 100K)",
                    "Very Large (> 100K)"
                ],
                'min_members': 0,
                'min_financial_value': 0,
                'min_closure_rate': 0,
                'date_range_start': date(2025, 10, 1),
                'date_range_end': date(2025, 12, 31)
            }
            st.rerun()
    
    with col2:
        # Count active filters
        active_filters = 0
        if len(selected_measures) < len(ALL_MEASURES):
            active_filters += 1
        if len(selected_plan_sizes) < len(PLAN_SIZE_OPTIONS):
            active_filters += 1
        if st.session_state.filters.get('min_members', 0) > 0:
            active_filters += 1
        if st.session_state.filters.get('min_financial_value', 0) > 0:
            active_filters += 1
        if st.session_state.filters.get('min_closure_rate', 0) > 0:
            active_filters += 1
        
        if active_filters > 0:
            st.info(f"🔍 {active_filters} active")
        else:
            st.success("✓ All data")
    
    st.markdown("---")
    
    # Database status
    show_db_status()
    st.markdown("---")
    
    st.markdown("**Built by:** Robert Reichert")
    st.markdown("**Version:** 4.0")
    
    # Sidebar value proposition - at bottom
    from utils.value_proposition import render_sidebar_value_proposition
    render_sidebar_value_proposition()
    
    # Sidebar footer - must be inside sidebar context
    render_sidebar_footer()

# ============================================================================
# SYNC WIDGET VALUES FOR BACKWARD COMPATIBILITY
# ============================================================================
# Sync membership_size from widget (widget-only approach)
if 'membership_slider_widget' in st.session_state:
    st.session_state.membership_size = st.session_state.membership_slider_widget

# Filter values are now synced immediately in the sidebar after each slider
# No need for duplicate syncing here

# ============================================================================
# 6. MAIN CONTENT
# ============================================================================
# StarGuard AI Header (already rendered above after st.set_page_config)
st.markdown("### Production-Grade Analytics for Medicare Advantage Star Rating Optimization | Zero PHI Exposure | HIPAA-Compliant Architecture")


# ============================================================================
# HERO SECTION - DYNAMIC PORTFOLIO PERFORMANCE OVERVIEW
# ============================================================================

st.markdown("---")
st.markdown("### 📊 Portfolio Performance Overview")

# Load and filter data for hero metrics
if 'portfolio_data' in st.session_state:
    hero_data = st.session_state.portfolio_data.copy()
    hero_filtered = apply_all_filters(hero_data)
else:
    hero_filtered = pd.DataFrame()  # Empty DataFrame if no data available

# Calculate summary from filtered data
if not hero_filtered.empty:
    hero_summary = generate_synthetic_summary(hero_filtered)
    
    # Scale by membership size
    BASELINE_MEMBERS = 10000
    hero_scale_factor = st.session_state.membership_size / BASELINE_MEMBERS
    
    # Extract and scale metrics
    hero_investment = safe_float(hero_summary.get('total_investment', 0)) * hero_scale_factor
    hero_revenue = safe_float(hero_summary.get('revenue_impact', 0)) * hero_scale_factor
    hero_net_benefit = safe_float(hero_summary.get('net_benefit', 0)) * hero_scale_factor
    hero_roi_ratio = safe_float(hero_summary.get('roi_ratio', 1.29))
    hero_roi_percent = (hero_roi_ratio - 1) * 100  # Convert to percentage
    hero_members = int(safe_float(hero_summary.get('total_members', 0)) * hero_scale_factor)
    hero_success_rate = safe_float(hero_summary.get('overall_success_rate', 42.4))
    hero_closures = int(safe_float(hero_summary.get('total_closures', 0)) * hero_scale_factor)
    
    # Calculate Star Rating impact (simplified)
    # Assumption: Every 10% increase in success rate = 0.1 star improvement
    baseline_success = 34.0  # Industry baseline
    success_improvement = hero_success_rate - baseline_success
    star_improvement = (success_improvement / 10) * 0.1
    current_stars = 4.0  # Baseline
    projected_stars = min(5.0, current_stars + star_improvement)
    
    # 4-column metric cards
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        st.metric(
            label="Potential ROI",
            value=f"{hero_roi_percent:.0f}%",
            delta=f"+{format_currency(hero_net_benefit)} annually",
            help=f"Projected return on {format_currency(hero_investment)} investment"
        )
    
    with col2:
        st.metric(
            label="Star Rating Impact",
            value=f"{projected_stars:.1f} ⭐",
            delta=f"+{star_improvement:.1f} stars",
            help="Projected improvement in CMS Star Rating for 2025"
        )
    
    with col3:
        st.metric(
            label="Members Optimized",
            value=f"{hero_members:,}",
            delta=f"{hero_closures:,} closures",
            help=f"Total members in filtered dataset at {st.session_state.membership_size:,} member plan size"
        )
    
    with col4:
        st.metric(
            label="Compliance Rate",
            value=f"{hero_success_rate:.1f}%",
            delta=f"+{hero_success_rate - baseline_success:.1f}%",
            help="Overall HEDIS measure compliance rate vs industry baseline"
        )

else:
    # No data after filtering - show warning
    st.warning("⚠️ No data matches current filters. Showing baseline estimates.")
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        st.metric(label="Potential ROI", value="--", delta="Adjust filters")
    
    with col2:
        st.metric(label="Star Rating Impact", value="--", delta="Adjust filters")
    
    with col3:
        st.metric(label="Members Optimized", value="0", delta="No data")
    
    with col4:
        st.metric(label="Compliance Rate", value="--", delta="Adjust filters")

# Style the metric cards
if HAS_STREAMLIT_EXTRAS:
    style_metric_cards(
        background_color="#ffffff",
        border_left_color="#00cc66",
        border_size_px=4,
        box_shadow=True
    )

st.markdown("---")

# ============================================================================
# REAL-TIME FILTER STATUS BAR
# ============================================================================

# Calculate current filtered dataset
if 'portfolio_data' in st.session_state:
    current_data = st.session_state.portfolio_data.copy()
else:
    current_data = generate_synthetic_portfolio_data()

current_filtered = apply_all_filters(current_data)

# Create status bar
col1, col2, col3, col4, col5 = st.columns(5, gap="small")

with col1:
    st.metric(
        label="📋 Records Shown",
        value=f"{len(current_filtered):,}",
        delta=f"{len(current_filtered) - len(current_data):,}" if len(current_filtered) != len(current_data) else None
    )

with col2:
    # Show unique measures instead of redundant total members
    if not current_filtered.empty and 'measure_name' in current_filtered.columns:
        unique_measures = current_filtered['measure_name'].nunique()
        total_measures = current_data['measure_name'].nunique() if not current_data.empty else 12
        st.metric(
            label="📊 Measures",
            value=f"{unique_measures}",
            delta=f"{total_measures - unique_measures} filtered out" if unique_measures < total_measures else "All measures"
        )
    else:
        st.metric(label="📊 Measures", value="--")

with col3:
    if not current_filtered.empty and 'financial_value' in current_filtered.columns:
        total_value = current_filtered['financial_value'].sum()
        scaled_value = total_value * (st.session_state.membership_size / 10000)
        st.metric(
            label="💰 Total Value",
            value=format_currency(scaled_value),
            delta=None
        )
    else:
        st.metric(label="💰 Total Value", value="$0")

with col4:
    # Plan Size Count
    plan_sizes_selected = st.session_state.filters.get('plan_sizes', [])
    plan_size_count = len(plan_sizes_selected) if plan_sizes_selected else 0
    membership_size = st.session_state.get('membership_size', 10000)
    
    if plan_size_count > 0:
        st.metric(
            label="🏥 Plan Sizes",
            value=f"{plan_size_count}",
            delta=f"Scaling: {membership_size:,} members",
            help=f"Selected plan size categories: {', '.join(plan_sizes_selected[:2])}{'...' if len(plan_sizes_selected) > 2 else ''}"
        )
    else:
        st.metric(
            label="🏥 Plan Sizes",
            value="All",
            delta=f"Scaling: {membership_size:,} members",
            help="No plan size filter applied - showing all plan sizes"
        )

with col5:
    filter_pct = (len(current_filtered) / len(current_data) * 100) if len(current_data) > 0 else 0
    st.metric(
        label="🎯 Filter Efficiency",
        value=f"{filter_pct:.1f}%",
        delta="Active" if filter_pct < 100 else "No filters"
    )

st.markdown("---")

# ============================================================================
# EXECUTIVE SUMMARY PANEL - Compact styling
# ============================================================================
st.markdown("""
<style>
/* Compact expander content styling */
[data-testid="stExpanderDetails"] {
    padding: 0.3rem 0.5rem !important;
}

/* Compact headers inside expander */
[data-testid="stExpanderDetails"] h3 {
    margin-top: 0.2rem !important;
    margin-bottom: 0.2rem !important;
    font-size: 1.1rem !important;
}

/* Compact alerts inside expander */
[data-testid="stExpanderDetails"] [data-testid="stAlert"] {
    padding: 0.4rem 0.5rem !important;
    margin-bottom: 0.2rem !important;
    margin-top: 0.1rem !important;
}

[data-testid="stExpanderDetails"] [data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
    font-size: 0.9rem !important;
    line-height: 1.4 !important;
}

[data-testid="stExpanderDetails"] [data-testid="stAlert"] p {
    margin: 0 !important;
    padding: 0 !important;
}

/* Compact markdown content */
[data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"] {
    margin-bottom: 0.15rem !important;
}

[data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"] p {
    margin: 0.1rem 0 !important;
    line-height: 1.5 !important;
}

[data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"] ul {
    margin: 0.15rem 0 !important;
    padding-left: 1.2rem !important;
}

[data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"] li {
    margin: 0.1rem 0 !important;
    line-height: 1.5 !important;
}

/* Compact horizontal rules */
[data-testid="stExpanderDetails"] hr {
    margin: 0.2rem 0 !important;
    border-width: 1px !important;
}

/* Reduce vertical block spacing inside expander */
[data-testid="stExpanderDetails"] {
    padding-top: 0.3rem !important;
    padding-bottom: 0.3rem !important;
    margin: 0 !important;
}
[data-testid="stExpanderDetails"] [data-testid="stVerticalBlock"] > div {
    gap: 0.1rem !important;
}
[data-testid="stExpanderDetails"] .element-container {
    margin-bottom: 0.1rem !important;
    margin-top: 0.1rem !important;
}
</style>
""", unsafe_allow_html=True)

with st.expander("📋 Executive Summary", expanded=True):
    st.markdown("### Key Insights")
    
    st.info("**🎯 Breakthrough Discovery:** Low-touch digital interventions achieved **46.4%** success rate, outperforming traditional high-touch methods (**42.1%**) at **14x lower cost** per member.")
    
    st.success("**💰 Top Performer:** Blood Pressure Diabetes (BPD) measure achieved **1.38x ROI** with efficient **$72.49** cost per closure through optimized intervention mix.")
    
    st.info("**📈 Financial Impact:** All **12 HEDIS measures** delivered positive ROI (**1.19x - 1.38x**), generating **$66K net benefit** in single quarter with **42.4%** overall success rate.")
    
    st.success("**🚀 Scalability:** Model proven at **10K member scale**, ready to scale to enterprise plans with consistent ROI performance and predictable outcomes.")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Recommended Actions")
    st.markdown('<ol style="text-align: left;"><li><strong>Immediate Priority:</strong> Expand low-touch digital intervention programs across all 12 measures</li><li><strong>Short-term (Q1 2025):</strong> Implement BPD optimization strategy to remaining eligible members</li><li><strong>Medium-term (Q2-Q3 2025):</strong> Scale successful interventions to enterprise plan sizes</li><li><strong>Long-term (2025+):</strong> Establish continuous monitoring and optimization framework</li></ol>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# NAVIGATION TABS
# ============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Portfolio Overview",
    "📈 Measure Deep-Dive",
    "👥 Member Lists",
    "💰 ROI Analysis",
    "🔒 Secure Query Interface"
])

# ============================================================================
# TAB 1: PORTFOLIO OVERVIEW
# ============================================================================
with tab1:
    st.markdown("### Portfolio Overview Dashboard")
    
    # Show active filters
    active_filters = []
    if len(st.session_state.filters.get('selected_measures', [])) < len([
        "Breast Cancer Screening", "Colorectal Cancer Screening", "Blood Pressure Control",
        "Diabetes Care - Eye Exam", "Diabetes Care - Blood Sugar", "Statin Therapy - Cardiovascular Disease",
        "Statin Therapy - Diabetes", "Controlling High Blood Pressure", "Annual Flu Vaccine",
        "Pneumonia Vaccine", "Depression Screening", "Osteoporosis Management"
    ]):
        active_filters.append(f"Measures: {len(st.session_state.filters.get('selected_measures', []))} selected")
    if st.session_state.filters.get('roi_threshold', 0) > 1.0:
        active_filters.append(f"ROI ≥ {st.session_state.filters.get('roi_threshold', 0):.2f}")
    if st.session_state.filters.get('success_rate_threshold', 0) > 0:
        active_filters.append(f"Success Rate ≥ {st.session_state.filters.get('success_rate_threshold', 0)}%")
    
    if active_filters:
        st.info(f"🔍 Active Filters: {', '.join(active_filters)}")
    
    # Check database connection
    conn, count = get_connection()
    if not conn:
        st.error("⚠️ Database connection failed. Please check configuration.")
        st.stop()
    
    # Get plan context
    plan_context = get_plan_context()
    plan_scenarios = get_plan_size_scenarios()
    benchmarks = get_industry_benchmarks()
    
    # ========================================================================
    # LOAD DATA - Use synthetic data if database is empty
    # ========================================================================
    summary_df = pd.DataFrame()  # Initialize empty DataFrame
    use_synthetic = False
    
    try:
        query = get_portfolio_summary_query(
            start_date=st.session_state.filters['date_range_start'].strftime("%Y-%m-%d"),
            end_date=st.session_state.filters['date_range_end'].strftime("%Y-%m-%d")
        )
        summary_df = execute_query(query)
        
        # Check if database returned data
        if summary_df.empty:
            st.warning("⚠️ Database returned no data. Using synthetic demonstration data.")
            use_synthetic = True
        else:
            use_synthetic = False
            # Validate that summary_df has required columns
            if 'measure_name' not in summary_df.columns:
                # Query returned data but missing measure_name column
                use_synthetic = True
                summary_df = pd.DataFrame()
            else:
                summary_df = apply_all_filters(summary_df)
            
    except KeyError as e:
        # Handle missing column errors silently
        missing_col = str(e).replace("'", "")
        use_synthetic = True
        summary_df = pd.DataFrame()
    except Exception as e:
        # Only show error for unexpected errors, not missing columns
        error_msg = str(e)
        if 'measure_name' in error_msg.lower() or isinstance(e, KeyError):
            # Silent fallback for measure_name errors
            use_synthetic = True
            summary_df = pd.DataFrame()
        else:
            # Show warning only for other types of errors
            st.warning(f"⚠️ Database error: {error_msg[:100]}. Using synthetic demonstration data.")
            use_synthetic = True
            summary_df = pd.DataFrame()
    
    # ========================================================================
    # LOAD PORTFOLIO DATA - Use synthetic for demonstration
    # ========================================================================
    
    # Generate synthetic data once and cache it
    if 'portfolio_data' not in st.session_state:
        st.session_state.portfolio_data = generate_synthetic_portfolio_data()
        st.session_state.data_loaded = True
    
    # Get the data
    raw_portfolio_data = st.session_state.portfolio_data.copy()
    
    # ========================================================================
    # LOAD AND FILTER DATA
    # ========================================================================
    
    # Start with raw data
    raw_data = raw_portfolio_data.copy()
    
    # Apply all filters
    filtered_data = apply_all_filters(raw_data)
    
    # Show filter impact
    st.info(f"📊 Analyzing **{len(filtered_data):,}** opportunities from **{len(raw_data):,}** total (filters applied)")
    
    # ========================================================================
    # DIAGNOSTIC OUTPUT
    # ========================================================================
    with st.expander("🔍 Filter Diagnostics", expanded=False):
        col1, col2, col3 = st.columns(3, gap="small")
        
        with col1:
            st.metric("Raw Data Rows", f"{len(raw_data):,}")
        
        with col2:
            st.metric("Filtered Rows", f"{len(filtered_data):,}")
        
        with col3:
            filter_pct = (len(filtered_data) / len(raw_data) * 100) if len(raw_data) > 0 else 0
            st.metric("% Remaining", f"{filter_pct:.1f}%")
        
        # Show active filters
        st.markdown("#### Active Filters:")
        active_filters = []
        
        if len(st.session_state.filters['selected_measures']) < len(ALL_HEDIS_MEASURES):
            active_filters.append(f"✅ Measures: {len(st.session_state.filters['selected_measures'])} of {len(ALL_HEDIS_MEASURES)}")
        
        if len(st.session_state.filters['plan_sizes']) < len(PLAN_SIZE_OPTIONS):
            active_filters.append(f"✅ Plan Sizes: {len(st.session_state.filters['plan_sizes'])} of {len(PLAN_SIZE_OPTIONS)}")
        
        if st.session_state.filters['min_members'] > 0:
            active_filters.append(f"✅ Min Members: ≥ {st.session_state.filters['min_members']}")
        
        if st.session_state.filters['min_financial_value'] > 0:
            active_filters.append(f"✅ Min Financial: ≥ ${st.session_state.filters['min_financial_value']}K")
        
        if st.session_state.filters['min_closure_rate'] > 0:
            active_filters.append(f"✅ Min Closure Rate: ≥ {st.session_state.filters['min_closure_rate']}%")
        
        if active_filters:
            for f in active_filters:
                st.write(f)
        else:
            st.success("No filters active - showing all data")
        
        # Show sample of filtered data
        st.markdown("#### Sample Filtered Data:")
        if not filtered_data.empty:
            display_cols = ['measure_name', 'plan_size_category', 'member_count', 'financial_value', 'predicted_closure_probability']
            # Only show columns that exist
            available_cols = [col for col in display_cols if col in filtered_data.columns]
            if available_cols:
                st.dataframe(
                    filtered_data[available_cols].head(10),
                    use_container_width=True
                )
    
    # ========================================================================
    # CHECK IF FILTERS REMOVED ALL DATA
    # ========================================================================
    if filtered_data.empty:
        st.error("⚠️ **No data matches current filters!**")
        st.info("Try one of these:")
        st.markdown("""
        - Click **Reset All** in the sidebar
        - Select more HEDIS measures
        - Select more plan sizes
        - Lower the threshold sliders
        """)
        st.stop()  # Don't continue if no data
    
    # ========================================================================
    # GENERATE SUMMARY FROM FILTERED DATA
    # ========================================================================
    summary = generate_synthetic_summary(filtered_data)
    
    # ========================================================================
    # CALCULATE SCALED VALUES based on membership size
    # ========================================================================
    BASELINE_MEMBERS = 10000
    membership_size = st.session_state.membership_size
    scale_factor = membership_size / BASELINE_MEMBERS
    
    # Extract baseline values
    baseline_investment = safe_float(summary.get('total_investment', 0))
    baseline_closures = safe_float(summary.get('total_closures', 0))
    baseline_revenue = safe_float(summary.get('revenue_impact', 0))
    baseline_net_benefit = safe_float(summary.get('net_benefit', 0))
    baseline_interventions = safe_float(summary.get('total_interventions', 0))
    
    # Performance metrics (don't scale)
    roi_ratio = safe_float(summary.get('roi_ratio', 0))
    success_rate = safe_float(summary.get('overall_success_rate', 0))
    
    # Scaled values (based on membership size)
    scaled_investment = baseline_investment * scale_factor
    scaled_closures = baseline_closures * scale_factor
    scaled_revenue = baseline_revenue * scale_factor
    scaled_net_benefit = baseline_net_benefit * scale_factor
    scaled_interventions = baseline_interventions * scale_factor
    
    # Cost per closure (doesn't change with scale)
    avg_cost_per_closure = baseline_investment / baseline_closures if baseline_closures > 0 else 0
    
    # Main Content Grid - 2x2 layout (always displayed)
    st.markdown('<div class="kpi-section-wrapper">', unsafe_allow_html=True)
    st.markdown("#### 📈 Key Performance Indicators")
    
    # Row 1: Investment and Closures
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        st.markdown("""
        <div class="plotly-container">
            <h4>Total Investment</h4>
            <p style="font-size: 2.5rem; font-weight: 700; color: #0066cc;">
                {}
            </p>
            <p style="color: #666;">
                {} per member
            </p>
        </div>
        """.format(
            format_currency(scaled_investment),  # ← No decimals
            format_currency(scaled_investment / st.session_state.membership_size if st.session_state.membership_size > 0 else 0, decimals=2)
        ),
        unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="plotly-container">
            <h4>Successful Closures</h4>
            <p style="font-size: 2.5rem; font-weight: 700; color: #0066cc;">
                {}
            </p>
            <p style="color: #666;">
                {} success rate
            </p>
        </div>
        """.format(
            format_number(scaled_closures),  # ← No decimals
            format_percent(success_rate)
        ),
        unsafe_allow_html=True)
    
    # Row 2: Revenue and Net Benefit
    col3, col4 = st.columns(2, gap="small")
    
    with col3:
        st.markdown("""
        <div class="plotly-container">
            <h4>Revenue Impact</h4>
            <p style="font-size: 2.5rem; font-weight: 700; color: #0066cc;">
                {}
            </p>
            <p style="color: #666;">
                {} per member
            </p>
        </div>
        """.format(
            format_currency(scaled_revenue),  # ← No decimals
            format_currency(scaled_revenue / st.session_state.membership_size if st.session_state.membership_size > 0 else 0, decimals=2)
        ),
        unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="plotly-container">
            <h4>Net Benefit</h4>
            <p style="font-size: 2.5rem; font-weight: 700; color: #00cc66;">
                {}
            </p>
            <p style="color: #666;">
                ROI: {:.2f}x
            </p>
        </div>
        """.format(
            format_currency(scaled_net_benefit),  # ← No decimals
            roi_ratio
        ),
        unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Industry Benchmark Comparison
    st.markdown("#### 📊 Industry Benchmark Comparison")
    benchmark_data = {
        'Metric': ['Gap Closure Rate', 'Cost Per Closure', 'ROI (First Quarter)', 'Digital Success Rate'],
        'Industry Average': ['28-35%', '$95-150', '1.0-1.2x', '25-30%'],
        'This Plan': ['42.4%', f'${avg_cost_per_closure:.2f}', f'{roi_ratio:.2f}x', '46.4%'],
        'Performance': ['✅ Above', '✅ Below', '✅ Above', '✅ Above']
    }
    
    benchmark_df = pd.DataFrame(benchmark_data)
    st.dataframe(benchmark_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Plan Profile Context
    st.markdown("#### 📋 Plan Profile")
    plan_profile_col1, plan_profile_col2 = st.columns(2, gap="small")
    
    with plan_profile_col1:
        st.markdown(f"""
        <div style="text-align: left;">
        <p><strong>Plan Name:</strong> {plan_context['plan_name']}</p>
        <p><strong>Members:</strong> {plan_context['total_members']:,}</p>
        <p><strong>Geographic Region:</strong> {plan_context['geographic_region']}</p>
        <p><strong>Plan Type:</strong> {plan_context['plan_type']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with plan_profile_col2:
        st.markdown(f"""
        <div style="text-align: left;">
        <p><strong>Star Rating:</strong> {plan_context['star_rating_2024']:.1f} → Projected {plan_context['star_rating_projected_2025']:.1f}</p>
        <p><strong>At Risk:</strong> ${plan_context['bonus_revenue_at_risk']:,.0f}</p>
        <p><strong>Member Growth:</strong> {plan_context['member_growth_yoy']:.1f}% YoY</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: MEASURE DEEP-DIVE
# ============================================================================
with tab2:
    st.markdown("### Measure Deep-Dive Analysis")
    st.info("📊 Detailed analysis of individual HEDIS measures with ROI breakdown and intervention effectiveness.")
    
    # ========================================================================
    # LOAD AND FILTER DATA (same as Tab 1)
    # ========================================================================
    if 'portfolio_data' not in st.session_state:
        st.session_state.portfolio_data = generate_synthetic_portfolio_data()
        st.session_state.data_loaded = True
    
    # Get the data and apply filters
    raw_data = st.session_state.portfolio_data.copy()
    filtered_data = apply_all_filters(raw_data)
    
    # ========================================================================
    # MEASURE-LEVEL ANALYSIS - Use filtered portfolio data
    # ========================================================================
    
    # Aggregate filtered data by measure
    if not filtered_data.empty:
        measure_summary = filtered_data.groupby('measure_name').agg({
            'investment': 'sum',
            'revenue_impact': 'sum',
            'successful_closures': 'sum',
            'total_interventions': 'sum',
            'member_count': 'sum'
        }).reset_index()
        
        # Calculate measure-level metrics
        measure_summary['ROI'] = (measure_summary['revenue_impact'] / measure_summary['investment'].replace(0, np.nan)).fillna(0)
        measure_summary['Success Rate'] = (measure_summary['successful_closures'] / measure_summary['total_interventions'].replace(0, np.nan) * 100).fillna(0)
        measure_summary['Cost per Closure'] = (measure_summary['investment'] / measure_summary['successful_closures'].replace(0, np.nan)).fillna(0)
        measure_summary['Measure'] = measure_summary['measure_name']
        
        measures_df = measure_summary
        filtered_measures_df = measures_df  # Already filtered from portfolio data
    else:
        st.error("⚠️ No data available after filtering")
        st.stop()
    
    # Show how many measures after filtering
    st.info(f"📊 Showing **{len(measures_df)}** HEDIS measures (filtered from {len(ALL_HEDIS_MEASURES)} total)")
    
    # ========================================================================
    # DIAGNOSTIC OUTPUT
    # ========================================================================
    st.markdown("### 🔍 Filter Diagnostics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Raw Data Rows", f"{len(measures_df):,}")
    
    with col2:
        st.metric("Filtered Rows", f"{len(filtered_measures_df):,}")
    
    with col3:
        filter_pct = (len(filtered_measures_df) / len(measures_df) * 100) if len(measures_df) > 0 else 0
        st.metric("% Remaining", f"{filter_pct:.1f}%")
    
    st.markdown("---")
    
    # Show filter impact
    if len(filtered_measures_df) < len(measures_df):
        st.info(f"📊 Showing {len(filtered_measures_df)} of {len(measures_df)} measures (filters applied)")
    
    # Display filtered data
    if len(filtered_measures_df) > 0:
        display_df = filtered_measures_df[['Measure', 'ROI', 'Cost per Closure', 'Success Rate']].copy()
        display_df['Success Rate'] = display_df['Success Rate'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ No data matches the current filters. Try adjusting your filter selections.")
    
    st.markdown("---")
    
    # Interactive charts
    if len(filtered_measures_df) > 0:
        st.markdown("#### 📈 ROI by Measure (Interactive Chart)")
        
        # Create interactive bar chart
        fig_roi = px.bar(
            filtered_measures_df,
            x='Measure',
            y='ROI',
            title='Return on Investment by HEDIS Measure',
            labels={'ROI': 'ROI Ratio', 'Measure': 'HEDIS Measure'},
            color='ROI',
            color_continuous_scale='RdYlGn',
            text='ROI'
        )
        
        # Customize layout
        fig_roi.update_traces(
            texttemplate='%{text:.2f}x',
            textposition='outside'
        )
        
        fig_roi.update_layout(
            height=500,
            xaxis_tickangle=-45,
            showlegend=False,
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # Add target line at 1.0x (break-even)
        fig_roi.add_hline(
            y=1.0,
            line_dash="dash",
            line_color="red",
            annotation_text="Break-Even (1.0x)",
            annotation_position="right"
        )
        
        st.plotly_chart(fig_roi, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("#### 💰 Cost Efficiency Analysis")
        
        if len(filtered_measures_df) > 0:
            # Create scatter plot
            fig_scatter = px.scatter(
                filtered_measures_df,
                x='Cost per Closure',
                y='Success Rate',
                size='ROI',
                color='ROI',
                hover_name='Measure',
                title='Cost Efficiency vs Success Rate',
                labels={
                    'Cost per Closure': 'Cost per Closure ($)',
                    'Success Rate': 'Success Rate (%)',
                    'ROI': 'ROI Ratio'
                },
                color_continuous_scale='RdYlGn',
                size_max=30
            )
            
            # Update layout with proper title wrapping
            fig_scatter.update_layout(
                height=500,
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode='closest',
                title={
                    'text': 'Cost Efficiency vs Success Rate',
                    'font': {'size': 16, 'family': 'Arial, sans-serif'},
                    'x': 0.5,
                    'xanchor': 'center',
                    'y': 0.98,
                    'yanchor': 'top',
                    'pad': {'t': 10, 'b': 5},
                    'automargin': True
                },
                margin={'l': 60, 'r': 20, 't': 70, 'b': 60},  # Extra top margin for wrapped title
                autosize=True
            )
            
            # Add quadrant lines
            median_cost = filtered_measures_df['Cost per Closure'].median()
            median_success = filtered_measures_df['Success Rate'].median()
            
            fig_scatter.add_vline(
                x=median_cost,
                line_dash="dash",
                line_color="gray",
                annotation_text=f"Median Cost: ${median_cost:.2f}"
            )
            
            fig_scatter.add_hline(
                y=median_success,
                line_dash="dash",
                line_color="gray",
                annotation_text=f"Median Success: {median_success:.1f}%"
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Quadrant analysis
            st.markdown("##### 📊 Quadrant Analysis")
            
            col1, col2 = st.columns(2, gap="small")
            
            with col1:
                st.success("""
                **🎯 High Performers (High Success, Low Cost)**
                - Best ROI opportunities
                - Scale these interventions first
                """)
            
            with col2:
                st.info("""
                **⚠️ Improvement Opportunities (Low Success, High Cost)**
                - Review intervention strategies
                - Consider alternative approaches
                """)
        else:
            st.warning("⚠️ No data to display. Adjust filters to see charts.")
        
    else:
        st.markdown("#### 📈 ROI by Measure (Interactive Chart)")
        st.warning("⚠️ No data available to display charts. Please adjust your filters.")
        
        st.markdown("#### 💰 Cost Efficiency Analysis")
        st.warning("⚠️ No data available to display charts. Please adjust your filters.")

# ============================================================================
# TAB 3: MEMBER LISTS
# ============================================================================
with tab3:
    st.markdown("### Member Lists & Segmentation")
    st.info("👥 Detailed member lists with eligibility, intervention status, and outcomes.")
    
    # Placeholder for member lists
    st.markdown("#### Eligible Members by Measure")
    st.info("💡 Filterable member lists will be displayed here with export functionality.")
    
    st.markdown("---")
    
    st.markdown("#### Member Segmentation")
    segmentation_col1, segmentation_col2 = st.columns(2, gap="small")
    
    with segmentation_col1:
        st.markdown("""
        **High Priority Members:**
        - Members with multiple gap opportunities
        - High-value intervention targets
        - Estimated impact: $XX,XXX
        """)
    
    with segmentation_col2:
        st.markdown("""
        **Standard Members:**
        - Single gap opportunities
        - Standard intervention protocols
        - Estimated impact: $XX,XXX
        """)
    
    st.markdown("---")
    
    st.markdown("#### Export Options")
    col_export1, col_export2, col_export3 = st.columns(3, gap="small")
    
    with col_export1:
        st.button("📥 Export High Priority", use_container_width=True)
    
    with col_export2:
        st.button("📥 Export All Members", use_container_width=True)
    
    with col_export3:
        st.button("📥 Export by Measure", use_container_width=True)

# ============================================================================
# TAB 4: ROI ANALYSIS - Fixed NoneType Handling
# ============================================================================
with tab4:
    st.markdown("### ROI Analysis & Projections")
    st.info("💰 Comprehensive ROI analysis with projections and scenario modeling.")
    
    # ========================================================================
    # PORTFOLIO OVERVIEW DASHBOARD - Fixed NoneType Handling
    # ========================================================================
    try:
        # Try to load portfolio summary data
        query = get_portfolio_summary_query(
            start_date=st.session_state.filters['date_range_start'].strftime("%Y-%m-%d"),
            end_date=st.session_state.filters['date_range_end'].strftime("%Y-%m-%d")
        )
        summary_df = execute_query(query)
        
        if not summary_df.empty:
            # Portfolio summary query returns aggregated data, not measure-level
            # Only apply filters if the dataframe has the required columns
            if 'measure_name' in summary_df.columns:
                summary_df = apply_all_filters(summary_df)
            # If no measure_name, it's already aggregated - use as is
            if not summary_df.empty:
                portfolio_data = summary_df.iloc[0].to_dict()
            else:
                portfolio_data = {}
        else:
            portfolio_data = {}
        
        # Safe conversions with defaults
        total_roi = safe_float(portfolio_data.get('roi_ratio'), 1.29)
        roi_change = safe_float(portfolio_data.get('roi_change'), 0.29)
        net_benefit = safe_float(portfolio_data.get('net_benefit'), 66000)
        payback_period = safe_float(portfolio_data.get('payback_period'), 0.77)
        
        # Display metrics
        roi_col1, roi_col2, roi_col3 = st.columns(3, gap="small")
        
        with roi_col1:
            st.metric(
                "Total ROI",
                f"{total_roi:.2f}x",
                f"+{roi_change:.0%}"
            )
        
        with roi_col2:
            st.metric(
                "Net Benefit",
                f"${net_benefit:,.0f}",
                "Q4 2024"
            )
        
        with roi_col3:
            st.metric(
                "Payback Period",
                f"{payback_period:.2f} quarters",
                f"~{payback_period * 3:.1f} months"
            )
    
    except Exception as e:
        st.error(f"❌ Error loading portfolio summary: {str(e)}")
        
        # Show default/placeholder values
        roi_col1, roi_col2, roi_col3 = st.columns(3, gap="small")
        
        with roi_col1:
            st.metric("Total ROI", "1.29x", "+29%")
        
        with roi_col2:
            st.metric("Net Benefit", "$66,000", "Q4 2024")
        
        with roi_col3:
            st.metric("Payback Period", "0.77 quarters", "~2.3 months")
        
    st.markdown("---")
    
    # ROI Projections
    st.markdown("#### 📈 ROI Projections by Plan Size")
    
    # Example projection data
    projection_data = {
        'Plan Size': ['10K', '25K', '50K', '100K', '250K'],
        'Investment': ['$155K', '$388K', '$775K', '$1.55M', '$3.88M'],
        'Revenue Impact': ['$200K', '$500K', '$1.0M', '$2.0M', '$5.0M'],
        'Net Benefit': ['$45K', '$112K', '$225K', '$450K', '$1.13M'],
        'ROI': ['1.29x', '1.29x', '1.29x', '1.29x', '1.29x']
    }
    
    projection_df = pd.DataFrame(projection_data)
    st.dataframe(projection_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Scenario Analysis
    st.markdown("#### 🎯 Scenario Analysis")
    scenario_col1, scenario_col2 = st.columns(2, gap="small")
    
    with scenario_col1:
        st.markdown("""
        **Conservative Scenario:**
        - 35% success rate
        - ROI: 1.15x
        - Net Benefit: $XX,XXX
        """)
    
    with scenario_col2:
        st.markdown("""
        **Optimistic Scenario:**
        - 50% success rate
        - ROI: 1.45x
        - Net Benefit: $XX,XXX
        """)
    
    st.markdown("---")
    
    # ROI Trend Over Time Chart
    st.markdown("#### 📊 ROI Trend Over Time")
    
    # Create synthetic time series data
    months = pd.date_range(start='2024-01-01', end='2024-12-31', freq='ME')
    
    trend_data = pd.DataFrame({
        'Month': months,
        'Conservative': [1.05, 1.08, 1.10, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.18, 1.19, 1.20],
        'Actual': [1.10, 1.15, 1.18, 1.22, 1.24, 1.26, 1.27, 1.28, 1.29, 1.30, 1.31, 1.32],
        'Optimistic': [1.15, 1.20, 1.25, 1.30, 1.33, 1.36, 1.39, 1.41, 1.43, 1.44, 1.45, 1.46]
    })
    
    # Create line chart
    fig_trend = go.Figure()
    
    # Add traces for each scenario
    fig_trend.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['Conservative'],
        name='Conservative',
        line=dict(color='#ff6b6b', width=2, dash='dash'),
        mode='lines+markers'
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['Actual'],
        name='Actual Performance',
        line=dict(color='#0066cc', width=3),
        mode='lines+markers',
        fill='tonexty'
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['Optimistic'],
        name='Optimistic',
        line=dict(color='#51cf66', width=2, dash='dash'),
        mode='lines+markers'
    ))
    
    # Update layout
    fig_trend.update_layout(
        title='ROI Performance Trends - 2024',
        xaxis_title='Month',
        yaxis_title='ROI Ratio',
        height=500,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add break-even line
    fig_trend.add_hline(
        y=1.0,
        line_dash="dot",
        line_color="red",
        annotation_text="Break-Even"
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Summary metrics
    st.markdown("##### 📈 Trend Summary")
    trend_col1, trend_col2, trend_col3 = st.columns(3, gap="small")
    
    with trend_col1:
        st.metric(
            "YTD ROI Growth",
            "+20%",
            "vs. Q1 2024"
        )
    
    with trend_col2:
        st.metric(
            "Consecutive Profitable Quarters",
            "4",
            "All 2024"
        )
    
    with trend_col3:
        st.metric(
            "Projected EOY ROI",
            "1.32x",
            "+32% return"
        )

# ============================================================================
# TAB 5: SECURE QUERY INTERFACE
# ============================================================================
with tab5:
    st.markdown("### 🔒 Secure Query Interface")
    st.markdown("#### Zero External API Exposure | On-Premises AI Processing")
    
    # Security badge - Prominent display
    st.markdown("""
    <div style="background-color: #e8f5e9; padding: 20px; border-radius: 8px; border-left: 6px solid #2d7d32; margin-bottom: 20px; text-align: center;">
        <h2 style="color: #2d7d32; margin: 0; font-size: 1.8rem;">🔒 ZERO PHI TRANSMITTED TO EXTERNAL APIS</h2>
        <p style="margin: 10px 0 0 0; color: #1b5e20; font-size: 1.1rem;">All processing occurs on-premises using local models (Ollama/ChromaDB)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Data Flow Architecture Diagram
    st.markdown("---")
    st.markdown("### 📊 Security Architecture: User → Local Model → Internal DB")
    
    # Create interactive data flow diagram using Plotly
    import plotly.graph_objects as go
    
    fig_flow = go.Figure()
    
    # Define flow steps
    flow_steps = [
        {"name": "User Question", "x": 0, "y": 0, "color": "#4CAF50"},
        {"name": "Local Embedding<br>(Ollama)", "x": 1, "y": 0, "color": "#2196F3"},
        {"name": "Vector Search<br>(ChromaDB)", "x": 2, "y": 0, "color": "#FF9800"},
        {"name": "SQL Generation<br>(Local LLM)", "x": 3, "y": 0, "color": "#9C27B0"},
        {"name": "Database Query<br>(Internal)", "x": 4, "y": 0, "color": "#F44336"},
        {"name": "Response<br>(De-identified)", "x": 5, "y": 0, "color": "#00BCD4"}
    ]
    
    # Add nodes
    for step in flow_steps:
        fig_flow.add_trace(go.Scatter(
            x=[step["x"]],
            y=[step["y"]],
            mode='markers+text',
            marker=dict(
                size=80,
                color=step["color"],
                line=dict(width=2, color='white')
            ),
            text=[step["name"]],
            textposition="middle center",
            textfont=dict(size=10, color='white', family='Arial Black'),
            name=step["name"],
            showlegend=False,
            hovertemplate=f"<b>{step['name']}</b><extra></extra>"
        ))
    
    # Add arrows (connections)
    for i in range(len(flow_steps) - 1):
        fig_flow.add_annotation(
            x=flow_steps[i+1]["x"],
            y=flow_steps[i+1]["y"],
            ax=flow_steps[i]["x"],
            ay=flow_steps[i]["y"],
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor="#666"
        )
    
    # Update layout
    fig_flow.update_layout(
        title=dict(
            text="<b>Secure Data Flow: Zero External API Calls</b>",
            x=0.5,
            font=dict(size=16, color="#2d7d32")
        ),
        xaxis=dict(showgrid=False, showticklabels=False, range=[-0.5, 5.5]),
        yaxis=dict(showgrid=False, showticklabels=False, range=[-0.5, 0.5]),
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig_flow, use_container_width=True)
    
    # Initialize chat interface
    if 'secure_chat_history' not in st.session_state:
        st.session_state.secure_chat_history = []
    
    # Try to import secure chatbot service
    try:
        from src.services.secure_chatbot_service import SecureChatbotService
        if 'secure_chatbot_service' not in st.session_state:
            try:
                st.session_state.secure_chatbot_service = SecureChatbotService()
            except Exception as e:
                st.session_state.secure_chatbot_service = None
                st.warning(f"⚠️ Could not initialize secure chatbot service: {e}. Using demo mode.")
        HAS_SERVICE = st.session_state.secure_chatbot_service is not None
    except ImportError:
        HAS_SERVICE = False
        st.session_state.secure_chatbot_service = None
        st.warning("⚠️ Secure chatbot service not available. Using demo mode.")
    
    # Main chat interface
    st.markdown("---")
    st.markdown("### 💬 Ask a Question About Your HEDIS Data")
    
    # Sample questions
    col1, col2, col3 = st.columns(3)
    sample_questions = [
        "Which measures have declining trends?",
        "What's the ROI for HbA1c testing?",
        "Show me measures with low compliance rates"
    ]
    
    for i, (col, question) in enumerate(zip([col1, col2, col3], sample_questions)):
        with col:
            if st.button(question, key=f"sample_q_{i}", use_container_width=True):
                st.session_state.current_secure_question = question
                st.rerun()
    
    # Chat input
    user_question = st.text_input(
        "Ask a question:",
        value=st.session_state.get('current_secure_question', ''),
        key="secure_chat_input",
        placeholder="e.g., Which measures have declining trends?"
    )
    
    if st.button("🔍 Ask", type="primary", key="secure_ask_btn") or (user_question and user_question != st.session_state.get('last_secure_question', '')):
        if user_question:
            st.session_state.last_secure_question = user_question
            
            # Use secure chatbot service if available
            if HAS_SERVICE:
                with st.spinner("🔄 Processing locally (no external API calls)..."):
                    try:
                        portfolio_data = st.session_state.portfolio_data.copy() if 'portfolio_data' in st.session_state else None
                        result = st.session_state.secure_chatbot_service.process_query(
                            user_question,
                            portfolio_data
                        )
                        
                        # Add to chat history
                        st.session_state.secure_chat_history.append({
                            'role': 'user',
                            'content': user_question
                        })
                        st.session_state.secure_chat_history.append({
                            'role': 'assistant',
                            'content': result['response'],
                            'processing_steps': result.get('processing_steps', []),
                            'context_measures': result.get('context_measures', []),
                            'sql_query': result.get('sql_query', '')
                        })
                    except Exception as e:
                        st.error(f"Error processing query: {e}")
                        st.session_state.secure_chat_history.append({
                            'role': 'user',
                            'content': user_question
                        })
                        st.session_state.secure_chat_history.append({
                            'role': 'assistant',
                            'content': "I encountered an error processing your query. Please try again."
                        })
            else:
                # Fallback to pattern matching
                with st.spinner("🔄 Processing locally (no external API calls)..."):
                    st.session_state.secure_chat_history.append({
                        'role': 'user',
                        'content': user_question
                    })
                    
                    # Simple pattern matching for demo
                    question_lower = user_question.lower()
                    portfolio_data = st.session_state.portfolio_data.copy() if 'portfolio_data' in st.session_state else None
                    
                    if portfolio_data is not None and not portfolio_data.empty:
                        if 'declining' in question_lower or 'trend' in question_lower:
                            if 'trend' in portfolio_data.columns:
                                declining = portfolio_data[portfolio_data['trend'] < 0].copy()
                                if len(declining) > 0:
                                    response = f"**Measures with declining trends:**\n\n"
                                    for _, row in declining.head(5).iterrows():
                                        response += f"- **{row['measure_name']}**: {row['trend']:.1f}% trend\n"
                                    response += f"\n*Found {len(declining)} measures with declining trends.*"
                                else:
                                    response = "No measures currently show declining trends."
                            else:
                                response = "Trend data not available in current dataset."
                        elif 'roi' in question_lower:
                            if 'hba1c' in question_lower or 'cdc' in question_lower:
                                hba1c = portfolio_data[portfolio_data['measure_name'].str.contains('HbA1c|CDC', case=False, na=False)]
                                if len(hba1c) > 0:
                                    avg_roi = hba1c['roi_ratio'].mean() if 'roi_ratio' in hba1c.columns else 1.35
                                    avg_impact = hba1c['financial_impact'].mean() if 'financial_impact' in hba1c.columns else 150000
                                    response = f"""**HbA1c Testing ROI Analysis:**

- **Average ROI Ratio**: {avg_roi:.2f}x
- **Average Financial Impact**: ${avg_impact:,.0f}
- **Net Benefit**: ${avg_impact * (avg_roi - 1):,.0f}

*This measure shows strong return on investment.*"""
                                else:
                                    response = "HbA1c Testing data not found in current dataset."
                            else:
                                if 'roi_ratio' in portfolio_data.columns:
                                    top_roi = portfolio_data.nlargest(3, 'roi_ratio')
                                    response = "**Top 3 Measures by ROI:**\n\n"
                                    for _, row in top_roi.iterrows():
                                        response += f"- **{row['measure_name']}**: {row['roi_ratio']:.2f}x ROI\n"
                                else:
                                    response = "ROI data not available in current dataset."
                        elif 'compliance' in question_lower:
                            if 'compliance_rate' in portfolio_data.columns:
                                low_compliance = portfolio_data[portfolio_data['compliance_rate'] < 50].copy()
                                if len(low_compliance) > 0:
                                    response = f"**Measures with Low Compliance Rates (<50%):**\n\n"
                                    for _, row in low_compliance.head(5).iterrows():
                                        response += f"- **{row['measure_name']}**: {row['compliance_rate']:.1f}%\n"
                                else:
                                    response = "All measures show compliance rates above 50%."
                            else:
                                response = "Compliance data not available in current dataset."
                        else:
                            response = "I can help you analyze your HEDIS data. Try asking about trends, ROI, compliance rates, or cost-effectiveness."
                    else:
                        response = "Portfolio data not available. Please ensure data is loaded in other tabs."
                    
                    st.session_state.secure_chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })
            
            # Clear the input
            if 'current_secure_question' in st.session_state:
                del st.session_state.current_secure_question
    
    # Display chat history
    st.markdown("---")
    st.markdown("### 💬 Conversation History")
    
    if st.session_state.secure_chat_history:
        for i, message in enumerate(st.session_state.secure_chat_history):
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.write(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.markdown(message['content'])
                    
                    # Show processing steps if available
                    if 'processing_steps' in message and message['processing_steps']:
                        with st.expander("🔍 View Processing Steps", expanded=False):
                            for step in message['processing_steps']:
                                st.markdown(f"**{step['step']}**")
                                st.markdown(f"Status: {step['status']}")
                                st.markdown(f"Details: {step['details']}")
                                st.markdown("---")
                    
                    # Show SQL query if available
                    if 'sql_query' in message and message['sql_query']:
                        with st.expander("📝 Generated SQL Query", expanded=False):
                            st.code(message['sql_query'], language='sql')
    else:
        st.info("👆 Ask a question above to start a conversation. All processing happens locally with zero external API calls.")
    
    # Compliance Architecture Documentation
    st.markdown("---")
    st.markdown("### 📋 Compliance Architecture Documentation")
    
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        with st.expander("🔐 How This Scales to Production PHI Data", expanded=False):
            st.markdown("""
            **Infrastructure Requirements:**
            - On-premises servers (application, database, vector store, LLM inference)
            - Encrypted database (AES-256)
            - Local vector store (ChromaDB with encryption)
            - LLM inference server (Ollama or Azure Private Endpoint)
            
            **Security Controls:**
            - Encryption at rest (database, vector store, files)
            - Encryption in transit (TLS 1.3)
            - Access logging (all queries logged)
            - Audit trails (7-year retention, immutable logs)
            - Role-based access control (RBAC) with MFA
            - Data minimization (automatic de-identification)
            
            **Compliance Certifications:**
            - HIPAA Compliance
            - SOC 2 Type II
            - HITRUST
            - ISO 27001
            """)
    
    with col2:
        with st.expander("📊 Comparison: Cloud AI vs Secure Approach", expanded=False):
            comparison_data = {
                'Aspect': [
                    'Data Location',
                    'PHI Transmission',
                    'Compliance Risk',
                    'Cost Model',
                    'Data Control',
                    'Offline Capability'
                ],
                'Traditional Cloud AI': [
                    'External cloud servers',
                    'Data sent to external APIs',
                    'High (data leaves organization)',
                    'Per-API-call pricing',
                    'Limited (vendor-dependent)',
                    'Requires internet'
                ],
                'Secure On-Premises': [
                    'On-premises infrastructure',
                    'Zero external transmission',
                    'Low (data stays internal)',
                    'Fixed infrastructure cost',
                    'Full control',
                    'Works offline'
                ]
            }
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    # Link to full documentation
    st.markdown("---")
    st.info("""
    **📚 Full Documentation Available:**
    - `COMPLIANCE_ARCHITECTURE.md` - Detailed compliance architecture
    - `COMPLIANCE_ONE_PAGER.md` - One-page summary
    - `SECURE_CHATBOT_IMPLEMENTATION.md` - Implementation guide
    """)

# ============================================================================
# FOOTER
# ============================================================================
# Footer sections - desktop full text, mobile abbreviated
from src.ui.layout import render_page_footer
render_page_footer()  # Main content footer
# Note: render_sidebar_footer() is already called inside the sidebar context (line 1214)
# Do not call it here as it will render HTML as text in the main content area


