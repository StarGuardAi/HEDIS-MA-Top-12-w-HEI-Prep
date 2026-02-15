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
from utils.page_components import apply_header_spacing, centered_metric
from utils.standard_sidebar_css import STANDARD_SIDEBAR_CSS
# add_mobile_ready_badge removed - badge no longer needed

# Import sidebar styling function (same as ROI page)
try:
    from utils.sidebar_styling import apply_sidebar_styling
except ImportError:
    def apply_sidebar_styling():
        pass

st.set_page_config(
    page_title="HEDIS Portfolio Optimizer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="auto"  # Auto: Let Streamlit decide based on screen size (iOS Safari optimized)
)

# Apply consistent sidebar styling (same as ROI page)
apply_sidebar_styling()

# ============================================================================
# FINAL FIX - All Three Issues Resolved
# Header fully visible + Home button + Performance Dashboard emoji fix
# ============================================================================
st.markdown("""
<style>
/* ========== FINAL CSS - HEADER FULLY VISIBLE + SIDEBAR FIXES ========== */

/* ========== REDUCE VERTICAL PADDING GLOBALLY ========== */
.main .block-container {
    padding-top: 0.1rem !important;
    padding-bottom: 0.1rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    margin-top: 0 !important;
    max-width: 100% !important;
}

/* Note: More specific vertical padding rules are defined below */

.main > div:first-child,
section.main > div:first-child {
    padding-top: 0.1rem !important;
    margin-top: 0 !important;
}

section.main > div {
    padding-top: 0.5rem !important;
    margin-top: 0 !important;
}

/* StarGuard Header Container - NO BOTTOM BORDER HERE */
.starguard-header-container {
    background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%);
    padding: 1rem 1.5rem 0.5rem 1.5rem !important;
    border-radius: 10px;
    margin-top: 0 !important;
    margin-bottom: 0.5rem !important;  /* Reduced spacing after header */
    text-align: center !important;
    box-shadow: 0 4px 12px rgba(74, 61, 111, 0.25);
    border-bottom: none !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Title - GREEN LINE HERE (between title and subtitle) */
.starguard-title {
    color: white !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    margin: 0 auto 0.2rem auto !important;
    padding: 0 0 0.2rem 0 !important;
    line-height: 1.2 !important;
    border-bottom: 3px solid #4ade80 !important;
    text-align: center !important;
    width: 100% !important;
}

/* Tagline */
.starguard-tagline {
    color: white !important;
    font-size: 0.9rem !important;
    margin: 0.1rem auto !important;
    font-weight: 500 !important;
    text-align: center !important;
    width: 100% !important;
}

/* Subtitle - NO BORDER HERE */
.starguard-subtitle {
    color: rgba(255, 255, 255, 0.92) !important;
    font-size: 0.85rem !important;
    margin: 0.2rem auto 0 auto !important;
    padding: 0 !important;
    line-height: 1.3 !important;
    border-bottom: none !important;
    text-align: center !important;
    width: 100% !important;
}

/* ========== MOBILE HEADER FORMATTING ========== */
@media (max-width: 768px) {
    .starguard-header-container {
        padding: 0.5rem !important;
    }
    
    .starguard-title {
        font-size: 1rem !important;
        line-height: 1.2 !important;
        margin-bottom: 0.25rem !important;
    }
    
    .starguard-tagline {
        font-size: 0.8rem !important;
    }
    
    .starguard-subtitle {
        font-size: 0.65rem !important;
        line-height: 1.4 !important;
    }
}

/* ========== SIDEBAR FIXES ========== */
/* ========== STANDARDIZED SIDEBAR CSS - IMPORTED FROM UTILITY ========== */
/* ========== PURPLE SIDEBAR THEME ========== */
/* Match the StarGuard AI header purple gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

/* ========== ALL SIDEBAR TEXT WHITE ========== */
/* Force ALL text in sidebar to be white - match ROI page */
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

/* ========== NAVIGATION STYLING ========== */
/* All navigation styling is handled by apply_sidebar_styling() function */
/* No additional CSS needed here - let the function handle everything */

/* ========== SIDEBAR WIDGET STYLING ========== */
/* Sidebar selectbox and other widgets */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label {
    color: white !important;
}

/* Sidebar widget backgrounds - make them visible on purple */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-radius: 5px !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div *,
[data-testid="stSidebar"] .stMultiSelect > div > div * {
    color: #4A3D6F !important;
}

/* Success/Info boxes in sidebar - white text - match ROI page */
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

/* View less/more links - white - match ROI page */
[data-testid="stSidebar"] button {
    color: #FFFFFF !important;
}

/* CSS Backup: Add emoji via ::before for Performance Dashboard links - match ROI page */
[data-testid="stSidebarNav"] a[href*="Performance_Dashboard"]::before {
    content: "⚡ " !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI Emoji", "Apple Color Emoji", sans-serif !important;
    display: inline !important;
}

/* ========== SIDEBAR SEPARATOR STYLING - SUBTLE GREEN GRADIENT ========== */
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

/* ========== NAVIGATION FORMATTING ========== */
/* Navigation formatting is handled by apply_sidebar_styling() function */
/* No additional CSS needed here */

/* Sidebar dimensions and padding - match ROI page */
[data-testid="stSidebar"] {
    min-width: 280px !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1rem !important;
}

/* ========== SIDEBAR NAVIGATION CONTAINER ========== */
/* Navigation container styling is handled by apply_sidebar_styling() function */
/* Keep this section empty to avoid conflicts - let the function handle it */

/* Sidebar collapse button */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    color: white !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
    border-radius: 50% !important;
}

[data-testid="stSidebarCollapseButton"]:hover {
    background-color: rgba(255, 255, 255, 0.2) !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
}

/* ========== FIX PERFORMANCE DASHBOARD EMOJI ========== */
/* CSS Backup: Add emoji via ::before for Performance Dashboard links */
/* Only keep this minimal CSS - let apply_sidebar_styling() handle everything else */
[data-testid="stSidebarNav"] a[href*="Performance_Dashboard"]::before {
    content: "⚡ " !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI Emoji", "Apple Color Emoji", sans-serif !important;
    display: inline !important;
}

/* Center subheaders in main page content */
.main h2,
.main h3,
.main h4,
.main h5,
.main h6,
h2, h3, h4, h5, h6 {
    text-align: center !important;
}

/* Center markdown subheaders */
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4,
.stMarkdown h5,
.stMarkdown h6,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4,
div[data-testid="stMarkdownContainer"] h5,
div[data-testid="stMarkdownContainer"] h6 {
    text-align: center !important;
}

/* Center Streamlit headers and subheaders */
[data-testid="stHeader"],
[data-testid="stHeader"] h1,
[data-testid="stHeader"] h2,
[data-testid="stHeader"] h3 {
    text-align: center !important;
}

/* ========== REDUCED VERTICAL PADDING - GLOBAL ========== */

/* Main container */
.main .block-container {
    padding-top: 0.1rem !important;
    padding-bottom: 0.1rem !important;
}

/* Headers */
h1 { 
    margin: 0.2rem 0 0.1rem 0 !important; 
    padding-top: 0 !important;
    font-size: 2rem !important;
    line-height: 1.2 !important;
}

h2 { 
    margin: 0.15rem 0 0.1rem 0 !important; 
    font-size: 1.5rem !important;
    line-height: 1.2 !important;
}

h3 { 
    margin: 0.1rem 0 0.05rem 0 !important; 
    font-size: 1.2rem !important;
    line-height: 1.2 !important;
}

/* Sections */
.element-container {
    margin-top: 0.1rem !important;
    margin-bottom: 0.25rem !important;
    padding: 0 !important;
}

/* Charts */
[data-testid="stPlotlyChart"] {
    margin: 0.1rem 0 !important;
}

/* Metric containers */
[data-testid="metric-container"] {
    padding: 0.1rem !important;
    margin: 0.1rem 0 !important;
}

/* StarGuard header */
.starguard-header-container {
    margin-bottom: 0.25rem !important;
    margin-top: 0 !important;
    padding: 0.5rem !important;
}

/* Dividers */
hr {
    margin: 0.25rem 0 !important;
}

/* ========== CENTER PAGE DESCRIPTIONS ========== */
/* Center page descriptions and subtitles */
.page-description, 
.page-subtitle {
    text-align: center !important;
    color: #6b7280 !important;
}

/* Center paragraphs immediately after page titles */
.page-title-container + p,
.page-title-container ~ p:first-of-type,
h1 + p,
h1 ~ p:first-of-type,
h3:first-of-type + p,
h3:first-of-type ~ p:first-of-type {
    text-align: center !important;
    color: #6b7280 !important;
}

/* Center info boxes and captions after page titles */
.page-title-container ~ div[data-testid="stInfo"],
.page-title-container ~ div[data-testid="stAlert"],
.page-title-container ~ .stCaption,
h1 ~ div[data-testid="stInfo"],
h1 ~ div[data-testid="stAlert"],
h1 ~ .stCaption {
    text-align: center !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.3rem !important;
}

hr {
    margin: 0.4rem 0 !important;
}

.stMarkdown {
    margin-bottom: 0.3rem !important;
}

/* Override ANY conflicting styles */
.starguard-header,
.starguard-header * {
    border-bottom: none !important;
}

.starguard-header-container * {
    border-bottom: none !important;
}

.starguard-title {
    border-bottom: 3px solid #4ade80 !important;
}

/* ========== REDUCE SPACING AFTER HEADER - AGGRESSIVE ========== */
.starguard-header-container + *,
.starguard-header-container ~ * {
    margin-top: 0rem !important;
    padding-top: 0 !important;
}

/* Reduce spacing for first content element after header */
.starguard-header-container ~ .element-container:first-of-type,
.starguard-header-container ~ div[data-testid="stVerticalBlock"]:first-of-type,
.starguard-header-container ~ div[data-testid="stVerticalBlock"] {
    margin-top: 0rem !important;
    padding-top: 0 !important;
}

/* Target markdown containers immediately after header */
.starguard-header-container ~ div[data-testid="stMarkdownContainer"],
.starguard-header-container ~ .stMarkdown {
    margin-top: 0rem !important;
    padding-top: 0 !important;
    margin-bottom: 0rem !important;
    padding-bottom: 0 !important;
}

/* Remove all excess padding from Streamlit containers */
div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"],
div[data-testid="stColumn"] {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

/* Remove padding from markdown containers */
div[data-testid="stMarkdownContainer"] {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

/* Remove padding from all Streamlit element wrappers */
.stApp > div > div > div > div {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

/* Target headings immediately after header */
.starguard-header-container ~ h1,
.starguard-header-container ~ h2,
.starguard-header-container ~ h3,
.starguard-header-container ~ div[data-testid="stMarkdownContainer"] h1,
.starguard-header-container ~ div[data-testid="stMarkdownContainer"] h2,
.starguard-header-container ~ div[data-testid="stMarkdownContainer"] h3 {
    margin-top: 0rem !important;
    padding-top: 0 !important;
}

/* Reduce padding on header subtitle */
.starguard-subtitle {
    margin-bottom: 0rem !important;
    padding-bottom: 0rem !important;
}

/* ========== MOBILE OPTIMIZATIONS ========== */
/* Mobile - even tighter spacing */
/* ========== MOBILE - EVEN TIGHTER ========== */
@media (max-width: 768px) {
    .main .block-container {
        padding-top: 0.05rem !important;
        padding-bottom: 0.05rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    
    h1 { 
        margin: 0.1rem 0 !important; 
        font-size: 1.1rem !important; 
    }
    
    h2 { 
        margin: 0.08rem 0 !important; 
        font-size: 1rem !important; 
    }
    
    h3 { 
        margin: 0.05rem 0 !important; 
        font-size: 0.9rem !important; 
    }
    
    h1, h2, h3 {
        text-align: center !important;
    }
    
    .element-container {
        margin-bottom: 0.1rem !important;
        margin-top: 0.05rem !important;
    }
    
    .starguard-header-container {
        margin-bottom: 0.1rem !important;
        margin-top: 0 !important;
        padding: 0.3rem 0.5rem !important;
    }
    
    .starguard-title {
        font-size: 1.2rem !important;
        margin-bottom: 0.15rem !important;
        padding-bottom: 0.15rem !important;
    }
    
    .starguard-subtitle {
        font-size: 0.7rem !important;
        margin-top: 0.15rem !important;
        margin-bottom: 0.1rem !important;
    }
    
    [data-testid="stPlotlyChart"] {
        margin: 0.05rem 0 !important;
    }
    
    [data-testid="metric-container"] {
        padding: 0.05rem !important;
        margin: 0.05rem 0 !important;
    }
    
    hr {
        margin: 0.1rem 0 !important;
    }
    
    /* ========== FIX MOBILE SIDEBAR CLOSE BUTTON ========== */
    /* Ensure close button is clickable - override any JavaScript hiding */
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebar"] button[aria-label*="Close"],
    [data-testid="stSidebar"] button[aria-label*="close"],
    [data-testid="stSidebar"] button[title*="Close"],
    [data-testid="stSidebar"] button[title*="close"] {
        z-index: 9999 !important;
        pointer-events: auto !important;
        cursor: pointer !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Make close button visible - override JavaScript hiding */
    [data-testid="stSidebar"] button[kind="header"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        z-index: 9999 !important;
    }
    
    /* Ensure sidebar header is interactive */
    [data-testid="stSidebarHeader"],
    [data-testid="stSidebar"] > div:first-child {
        pointer-events: auto !important;
    }
    
    /* Fix any overlay blocking clicks */
    [data-testid="stSidebar"] > div {
        pointer-events: auto !important;
    }
    
    /* Ensure close button SVG/icons are visible */
    [data-testid="stSidebar"] button[kind="header"] svg,
    [data-testid="stSidebar"] button[aria-label*="Close"] svg,
    [data-testid="stSidebar"] button[aria-label*="close"] svg {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: none !important; /* SVG itself doesn't need pointer events */
    }
    
    /* ========== GLOBAL MOBILE TEXT FIX ========== */
    /* Center everything */
    .main .block-container,
    .main .block-container * {
        text-align: center !important;
    }
    
    /* But left-align data tables */
    [data-testid="stDataFrame"] * {
        text-align: left !important;
    }
    
    /* Reduce all font sizes */
    .main h1 { font-size: 1.1rem !important; }
    .main h2 { font-size: 1rem !important; }
    .main h3 { font-size: 0.9rem !important; }
    .main p { font-size: 0.85rem !important; }
    
    /* Sidebar - smaller fonts */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 0.9rem !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        font-size: 0.8rem !important;
    }
    
    /* ========== MOBILE SIDEBAR - SMALLER FILTER TITLES ========== */
    /* Reduce filter section headers */
    [data-testid="stSidebar"] h1 {
        font-size: 1rem !important;
    }
    
    [data-testid="stSidebar"] h2 {
        font-size: 0.95rem !important;
    }
    
    [data-testid="stSidebar"] h3 {
        font-size: 0.9rem !important;
    }
    
    [data-testid="stSidebar"] h4 {
        font-size: 0.85rem !important;
    }
    
    /* Specific filter labels */
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        font-size: 0.9rem !important;
        margin: 0.25rem 0 !important;
    }
    
    /* "Plan Membership Size", "Date Range" etc */
    [data-testid="stSidebar"] p {
        font-size: 0.8rem !important;
    }
    
    /* Slider labels */
    [data-testid="stSidebar"] .stSlider label {
        font-size: 0.8rem !important;
    }
    
    /* Caption text */
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        font-size: 0.75rem !important;
    }
    
    /* Fix chart overflow */
    .js-plotly-plot,
    [data-testid="stPlotlyChart"] {
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }
    
    /* Ensure charts don't have cut-off legends */
    .legend {
        font-size: 8px !important;
    }
    
    /* ========== MOBILE CENTER ALIGNMENT ========== */
    /* Center all main content text */
    .main .block-container {
        text-align: center !important;
    }
    
    /* Center metric cards content */
    [data-testid="metric-container"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        text-align: center !important;
        justify-content: center !important;
    }
    
    /* Center KPI list items */
    .element-container {
        text-align: center !important;
    }
    
    /* Center paragraphs */
    .stMarkdown p {
        text-align: center !important;
    }
    
    /* Tagline mobile sizing */
    .starguard-tagline {
        font-size: 0.8rem !important;
    }
}

/* ========== CENTER METRIC LABELS AND VALUES ========== */
/* Center metric labels and values across all pages - AGGRESSIVE TARGETING */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricLabel"] > div,
[data-testid="stMetricLabel"] > div > div,
[data-testid="stMetricLabel"] > div > div > div {
    text-align: center !important;
    justify-content: center !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    display: block !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] > div,
[data-testid="stMetricValue"] > div > div,
[data-testid="stMetricValue"] > div > div > div {
    text-align: center !important;
    justify-content: center !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] *,
[data-testid="stMetricDelta"] > div,
[data-testid="stMetricDelta"] > div > div {
    text-align: center !important;
    justify-content: center !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Center metric container and all nested elements */
div[data-testid="stMetricContainer"],
div[data-testid="stMetricContainer"] *,
div[data-testid="stMetricContainer"] > div,
div[data-testid="stMetricContainer"] > div > div {
    text-align: center !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
}

/* Force center alignment for metric text content */
div[data-testid="stMetricContainer"] p,
div[data-testid="stMetricContainer"] span,
div[data-testid="stMetricContainer"] div {
    text-align: center !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Center metric columns */
div[data-testid="column"] [data-testid="stMetricContainer"],
div[data-testid="column"] [data-testid="stMetricContainer"] * {
    text-align: center !important;
    align-items: center !important;
    justify-content: center !important;
}

/* 
═══════════════════════════════════════════════════════════════════════════════
SITE-WIDE FORMATTING RULES - HEDIS Portfolio Optimizer
═══════════════════════════════════════════════════════════════════════════════

RULE #1: CENTERED METRIC HEADERS
All KPI/metric summary headers must be perfectly centered over their data values.
This applies to:
- st.metric() labels
- st.caption() used as headers
- Custom HTML metric headers
- Any text that serves as a label above a data point

RULE #2: CONSISTENT VISUAL HIERARCHY  
Primary KPIs (top row): Larger values, prominent colors
Secondary KPIs (bottom row): Standard size, supporting data

RULE #3: MOBILE RESPONSIVENESS
All metrics must stack properly on mobile with centered alignment maintained.

═══════════════════════════════════════════════════════════════════════════════
*/

/* ========== CENTER-ALIGN METRICS AND TABLES FOR CLEAN VIEWING ========== */

/* ========== RULE: CENTER ALL METRIC HEADERS OVER DATA ========== */
/* This is a site-wide standard - metric labels center over values */

/* Center the metric label text (header above the number) */
[data-testid="stMetricLabel"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    text-align: center !important;
}

[data-testid="stMetricLabel"] > div {
    width: 100% !important;
    text-align: center !important;
    margin: 0 auto !important;
}

[data-testid="stMetricLabel"] label,
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] span {
    width: 100% !important;
    text-align: center !important;
    display: block !important;
}

/* Center the metric value (the big number) */
[data-testid="stMetricValue"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    text-align: center !important;
}

[data-testid="stMetricValue"] > div {
    width: 100% !important;
    text-align: center !important;
    margin: 0 auto !important;
}

/* Center the delta indicator (+$1,264,020 annually, etc.) */
[data-testid="stMetricDelta"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}

[data-testid="stMetricDelta"] > div {
    text-align: center !important;
}

/* Center metric cards - values and labels (backward compatibility) */
[data-testid="stMetricDelta"] {
    text-align: center !important;
    justify-content: center !important;
}

/* Center the entire metric container */
[data-testid="metric-container"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
    width: 100% !important;
}

/* Center metric containers */
div[data-testid="stMetricContainer"] {
    text-align: center !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

/* Ensure columns containing metrics are centered */
[data-testid="column"] > div > div > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

/* Center any custom metric-style headers (non-st.metric) */
.metric-header, .kpi-header, .summary-header {
    text-align: center !important;
    width: 100% !important;
    display: block !important;
}

/* Center st.caption used as metric labels */
[data-testid="stCaptionContainer"] {
    text-align: center !important;
    width: 100% !important;
}

[data-testid="stCaptionContainer"] p {
    text-align: center !important;
}

/* Fix for columns - ensure flex centering */
.row-widget.stHorizontalBlock > div {
    display: flex !important;
    justify-content: center !important;
}

.row-widget.stHorizontalBlock [data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

/* ========== AGGRESSIVE METRIC CENTERING - TARGET COLUMN STRUCTURE ========== */
/* Force center alignment for metrics inside columns */
[data-testid="column"] [data-testid="stMetricContainer"],
[data-testid="column"] [data-testid="metric-container"],
[data-testid="column"] > div > div > div[data-testid="stMetricContainer"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
    width: 100% !important;
    margin: 0 auto !important;
}

/* Force center for metric labels inside columns */
[data-testid="column"] [data-testid="stMetricLabel"],
[data-testid="column"] [data-testid="stMetricLabel"] > div,
[data-testid="column"] [data-testid="stMetricLabel"] label,
[data-testid="column"] [data-testid="stMetricLabel"] p,
[data-testid="column"] [data-testid="stMetricLabel"] span {
    text-align: center !important;
    width: 100% !important;
    display: block !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Force center for metric values inside columns */
[data-testid="column"] [data-testid="stMetricValue"],
[data-testid="column"] [data-testid="stMetricValue"] > div {
    text-align: center !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Force center for metric deltas inside columns */
[data-testid="column"] [data-testid="stMetricDelta"],
[data-testid="column"] [data-testid="stMetricDelta"] > div {
    text-align: center !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Target the actual Streamlit metric structure */
div[data-testid="stMetricContainer"] {
    text-align: center !important;
    align-items: center !important;
}

div[data-testid="stMetricContainer"] > div {
    text-align: center !important;
    align-items: center !important;
    width: 100% !important;
}

/* Override any inline styles or conflicting rules */
[data-testid="stMetricLabel"] * {
    text-align: center !important;
}

[data-testid="stMetricValue"] * {
    text-align: center !important;
}

[data-testid="stMetricDelta"] * {
    text-align: center !important;
}

/* ========== NUCLEAR OPTION: FORCE CENTER ALL METRIC TEXT ========== */
/* Target every possible element inside metric containers */
div[data-testid="stMetricContainer"] {
    text-align: center !important;
    align-items: center !important;
    justify-content: center !important;
}

div[data-testid="stMetricContainer"] * {
    text-align: center !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Force center for label text specifically */
div[data-testid="stMetricContainer"] > div:first-child,
div[data-testid="stMetricContainer"] > div:first-child * {
    text-align: center !important;
    display: block !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Force center for value text */
div[data-testid="stMetricContainer"] > div:nth-child(2),
div[data-testid="stMetricContainer"] > div:nth-child(2) * {
    text-align: center !important;
    display: block !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Force center for delta text */
div[data-testid="stMetricContainer"] > div:nth-child(3),
div[data-testid="stMetricContainer"] > div:nth-child(3) * {
    text-align: center !important;
    display: block !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* ========== FORCE CENTER ALL MARKDOWN CONTENT IN COLUMNS ========== */
/* This ensures custom HTML metrics are centered */
.centered-metric-container {
    text-align: center !important;
    padding: 0.5rem 0 !important;
    width: 100% !important;
    margin: 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
}

.centered-metric-container p {
    text-align: center !important;
    margin-left: auto !important;
    margin-right: auto !important;
    width: 100% !important;
    display: block !important;
}

[data-testid="column"] .stMarkdown,
[data-testid="column"] .stMarkdownContainer,
[data-testid="column"] .stMarkdown > div,
[data-testid="column"] .stMarkdownContainer > div {
    text-align: center !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
}

[data-testid="column"] .stMarkdown p,
[data-testid="column"] .stMarkdownContainer p,
[data-testid="column"] .stMarkdown div,
[data-testid="column"] .stMarkdownContainer div {
    text-align: center !important;
    margin-left: auto !important;
    margin-right: auto !important;
    width: 100% !important;
}

/* Force center any divs inside columns */
[data-testid="column"] > div > div > div > div {
    text-align: center !important;
}

[data-testid="column"] > div > div > div > div > p {
    text-align: center !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Center data tables - cell content */
.stDataFrame,
.stDataFrame table,
.stDataFrame td,
.stDataFrame th {
    text-align: center !important;
}

/* Center table headers */
.stDataFrame thead th {
    text-align: center !important;
    font-weight: 600 !important;
}

/* Center table cells */
.stDataFrame tbody td {
    text-align: center !important;
}

/* Center sidebar metrics */
[data-testid="stSidebar"] [data-testid="stMetricValue"],
[data-testid="stSidebar"] [data-testid="stMetricLabel"],
[data-testid="stSidebar"] [data-testid="stMetricDelta"] {
    text-align: center !important;
}

[data-testid="stSidebar"] div[data-testid="stMetricContainer"] {
    text-align: center !important;
}

/* Center summary tables in sidebars */
[data-testid="stSidebar"] .stDataFrame,
[data-testid="stSidebar"] .stDataFrame table,
[data-testid="stSidebar"] .stDataFrame td,
[data-testid="stSidebar"] .stDataFrame th {
    text-align: center !important;
}

/* Center caption text */
.stCaption {
    text-align: center !important;
}

/* Center info boxes - selective (only for summary/metric displays) */
.stAlert[data-baseweb="notification"],
.stInfo[data-baseweb="notification"],
.stSuccess[data-baseweb="notification"],
.stWarning[data-baseweb="notification"],
.stError[data-baseweb="notification"] {
    text-align: center !important;
}

/* Keep expander headers left-aligned for readability */
.streamlit-expanderHeader {
    text-align: left !important;
}

/* Center numeric values in tables */
.stDataFrame td {
    text-align: center !important;
}

/* Keep text content left-aligned (headings, paragraphs) for readability */
/* Exception: h2 and h3 are centered (see CENTER SUMMARY HEADERS section below) */
h1, h4, h5, h6 {
    text-align: left !important;
}

p, li {
    text-align: left !important;
}

/* Exception: Center specific summary/metric section headers - handled by h2, h3 rule above */


/* ========== CENTER SUMMARY HEADERS AND NOTES ========== */

/* Center all h2, h3, h4 headers (section headers) */
h2, h3, h4 {
    text-align: center !important;
}

/* Center page subheaders in markdown containers */
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4 {
    text-align: center !important;
}

/* Center markdown headers - comprehensive targeting */
.stMarkdown h2,
.stMarkdown h3,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
.element-container h2,
.element-container h3,
div[data-testid="stVerticalBlock"] h2,
div[data-testid="stVerticalBlock"] h3 {
    text-align: center !important;
}

/* Center all markdown content headers */
.stMarkdown:has(h2),
.stMarkdown:has(h3) {
    text-align: center !important;
}

/* Center captions and notes */
.stCaption,
[data-testid="stCaption"],
p.stCaption,
div.stCaption {
    text-align: center !important;
}

/* Center headers that come after dividers (section headers) */
hr + h2,
hr + h3 {
    text-align: center !important;
}

/* Center notes/details below metrics */
[data-testid="stMetricContainer"] + .stMarkdown,
[data-testid="stMetricContainer"] ~ .stMarkdown,
.stMetric + .stMarkdown {
    text-align: center !important;
}

/* Center all section headers in main content */
.main h2,
.main h3,
section.main h2,
section.main h3 {
    text-align: center !important;
}






/* Center summary section headers (using class-based targeting) */
.stMarkdown:has(h2),
.stMarkdown:has(h3) {
    text-align: center !important;
}

/* ========== CENTER KPI/METRIC HEADERS (ENHANCED) ========== */
/* This section reinforces the site-wide metric centering rule above */
/* All metric labels, values, and deltas are centered */

/* Additional reinforcement for metric labels */
[data-testid="stMetricLabel"] {
    display: flex !important;
    justify-content: center !important;
    text-align: center !important;
    width: 100% !important;
}

[data-testid="stMetricLabel"] > div {
    text-align: center !important;
    width: 100% !important;
}

/* Additional reinforcement for metric values */
[data-testid="stMetricValue"] {
    display: flex !important;
    justify-content: center !important;
    text-align: center !important;
    width: 100% !important;
}

/* Additional reinforcement for metric deltas */
[data-testid="stMetricDelta"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}

/* Additional reinforcement for metric containers */
[data-testid="metric-container"] {
    text-align: center !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    width: 100% !important;
}

/* Additional reinforcement for column content */
[data-testid="column"] {
    text-align: center !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}


/* ========== SIDEBAR FILTER STYLING ========== */
/* Filter section header */
[data-testid="stSidebar"] h3 {
    color: white !important;
    font-size: 1rem !important;
    margin-bottom: 0.5rem !important;
    padding-bottom: 0.25rem !important;
    border-bottom: 1px solid rgba(255,255,255,0.2) !important;
}

/* Compact filter widgets */
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stMultiSelect,
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stRadio {
    margin-bottom: 0.75rem !important;
}

/* Filter labels */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label {
    color: white !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* Dropdown styling on purple background */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background-color: rgba(255,255,255,0.95) !important;
    border-radius: 5px !important;
}

/* ========== LEFT ALIGN SIDEBAR CONTENT ========== */
/* Left align sidebar content */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    text-align: left !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    text-align: left !important;
}

/* ========== CENTER TAB LABELS ========== */
/* Center tab labels */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    justify-content: center !important;
}

[data-testid="stTabs"] button[data-baseweb="tab"] {
    text-align: center !important;
}

/* Stack tabs on mobile */
@media (max-width: 768px) {
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        flex-wrap: wrap !important;
        justify-content: center !important;
    }
    
    [data-testid="stTabs"] button[data-baseweb="tab"] {
        flex: 0 0 45% !important;
        margin: 2px !important;
        font-size: 0.75rem !important;
    }
}

/* ========== LARGER CENTERED KPI VALUES ========== */
/* Larger centered KPI values */
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    justify-content: center !important;
}

[data-testid="stMetricLabel"] {
    text-align: center !important;
    justify-content: center !important;
    font-size: 0.9rem !important;
}

[data-testid="stMetricDelta"] {
    text-align: center !important;
    justify-content: center !important;
}

[data-testid="metric-container"] {
    text-align: center !important;
    align-items: center !important;
}

/* ===== CENTER TAB BUTTONS ===== */
[data-testid="stTabs"] > div:first-child,
[data-baseweb="tab-list"],
[role="tablist"] {
    justify-content: center !important;
    display: flex !important;
}

/* Center all tabs globally */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    justify-content: center !important;
}

.stTabs [data-baseweb="tab-list"] {
    justify-content: center !important;
}

div[data-baseweb="tab-list"] {
    justify-content: center !important;
}

/* FORCE CENTER TABS - NUCLEAR OPTION */
[data-testid="stTabs"] [data-baseweb="tab-list"],
[data-testid="stTabs"] > div > div[data-baseweb="tab-list"],
.stTabs [data-baseweb="tab-list"],
div.stTabs > div > div {
    justify-content: center !important;
    display: flex !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

[role="tablist"] {
    justify-content: center !important;
    width: 100% !important;
}

/* ===== LEFT-ALIGN DATA TABLES ===== */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] table,
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] td {
    text-align: left !important;
}

/* Table header row */
.stDataFrame thead th {
    text-align: left !important;
}

/* Table data cells */
.stDataFrame tbody td {
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
                text.match(/Performance\s*Dashboard/i)
            );
            
            const hasEmoji = text.includes('⚡') || text.includes('\u26A1') || link.innerHTML.includes('⚡');
            
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
    
    // Run after delays to catch late-rendering elements
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
</script>
""", unsafe_allow_html=True)
# ↑↑↑ END OF FINAL FIX CSS + JAVASCRIPT ↑↑↑

# apply_header_spacing() - COMMENTED OUT: Now handled by Nuclear Option CSS above

# ============================================================================
# RESPONSIVE DESIGN SYSTEM - REMOVED (Now handled by Nuclear Option CSS)
# ============================================================================
# This entire section has been replaced by the Nuclear Option CSS above.
# If you need additional responsive styles, add them to the Nuclear Option CSS block.
# ============================================================================

# StarGuard Header HTML (CSS already defined in Nuclear Option above)
st.markdown("""
<div class='starguard-header-container'>
    <div class='starguard-title'>⭐ StarGuard AI | Turning Data Into Stars</div>
    <div class='starguard-subtitle'>Healthcare AI Architect • $148M+ Documented Savings • HEDIS & Star Rating Expert<br>🔒 Zero PHI Exposure • Context Engineering + Agentic RAG • Production-Grade Analytics</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# DUPLICATE CSS REMOVED - All styling now handled by Nuclear Option CSS above
# ============================================================================
# The following sections were removed as duplicates:
# - "AGGRESSIVE SPACING REDUCTION" block (now in Nuclear Option)
# - "Purple Sidebar Theme" block (now in Nuclear Option)
# ============================================================================

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
            
            // Hide sidebar toggle button (but NOT the close button)
            const sidebarToggle = document.querySelector('button[aria-label*="sidebar"], button[aria-label*="menu"]');
            if (sidebarToggle) {
                // Don't hide close buttons
                const ariaLabel = sidebarToggle.getAttribute('aria-label') || '';
                if (!ariaLabel.toLowerCase().includes('close') && !ariaLabel.toLowerCase().includes('collapse')) {
                    sidebarToggle.style.display = 'none';
                }
            }
            
            // Also try to find by class (but preserve close buttons)
            const toggleButtons = document.querySelectorAll('button');
            toggleButtons.forEach(btn => {
                const ariaLabel = btn.getAttribute('aria-label') || '';
                const isCloseButton = ariaLabel.toLowerCase().includes('close') || 
                                     ariaLabel.toLowerCase().includes('collapse') ||
                                     btn.getAttribute('data-testid')?.includes('Collapse');
                if ((ariaLabel.toLowerCase().includes('sidebar') || ariaLabel.toLowerCase().includes('menu')) && !isCloseButton) {
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

/* Reduce section spacing */
.element-container { margin-bottom: 0.5rem !important; }
.stMarkdown { margin-bottom: 0.4rem !important; }

/* Readable metric fonts */
[data-testid="stMetricValue"] { font-size: 1.6rem !important; }
[data-testid="stMetricLabel"] { font-size: 0.95rem !important; padding-bottom: 0.3rem !important; }
[data-testid="metric-container"] { padding: 0.7rem !important; }

/* Chart and data spacing */
.stPlotlyChart { margin-bottom: 0.6rem !important; }
.stDataFrame { margin-bottom: 0.6rem !important; }

/* Global table mobile scrolling - applies to all tables */
@media (max-width: 768px) {
    /* Force all tables to be scrollable on mobile */
    .stDataFrame,
    div[data-testid="stDataFrame"],
    [data-testid="stExpander"] .stDataFrame,
    [data-testid="stExpander"] div[data-testid="stDataFrame"] {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        display: block !important;
        width: 100% !important;
        max-width: 100vw !important;
    }
    
    /* Table wrapper */
    .stDataFrame > div,
    div[data-testid="stDataFrame"] > div {
        overflow-x: auto !important;
        width: 100% !important;
    }
    
    /* Table element */
    .stDataFrame table,
    div[data-testid="stDataFrame"] table {
        min-width: 600px !important; /* Ensure table doesn't shrink too much */
        width: auto !important;
    }
}

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
    /* Mobile header improvements */
    .main .block-container {
        padding-top: 0.25rem !important;
    }
    
    .starguard-header-container {
        padding: 0.5rem !important;
        margin: 0.25rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    .starguard-title {
        font-size: 0.95rem !important;
        margin-bottom: 0.15rem !important;
    }
    
    .starguard-subtitle {
        font-size: 0.6rem !important;
        line-height: 1.3 !important;
    }
    
    /* Reduce gap between header and page title */
    h1:first-of-type {
        margin-top: 0.25rem !important;
    }
    
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
    
    /* Center align metrics on mobile - labels above, values below */
    [data-testid="stMetricContainer"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    [data-testid="stMetric"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"],
    [data-testid="metric-container"],
    .compact-metric-card,
    .kpi-card {
        text-align: center !important;
        width: 100% !important;
    }
    
    /* Ensure metric labels are above values */
    [data-testid="stMetricLabel"] {
        display: block !important;
        text-align: center !important;
        margin-bottom: 0.3rem !important;
        width: 100% !important;
    }
    
    [data-testid="stMetricValue"] {
        display: block !important;
        text-align: center !important;
        margin-top: 0.2rem !important;
        width: 100% !important;
    }
    
    [data-testid="stMetricDelta"] {
        display: block !important;
        text-align: center !important;
        margin-top: 0.2rem !important;
        width: 100% !important;
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
    
    /* Mobile tables - ensure visibility with horizontal scroll - COMPREHENSIVE FIX */
    .stDataFrame,
    div[data-testid="stDataFrame"],
    div[data-testid="stDataFrame"] > div,
    div[data-testid="stDataFrame"] > div > div {
        overflow-x: auto !important;
        overflow-y: visible !important;
        display: block !important;
        width: 100% !important;
        max-width: 100vw !important;
        -webkit-overflow-scrolling: touch !important;
        position: relative !important;
    }
    
    /* Force table wrapper to scroll */
    div[data-testid="stDataFrame"] {
        overflow-x: auto !important;
        overflow-y: visible !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Table container */
    .stDataFrame > div,
    div[data-testid="stDataFrame"] > div {
        overflow-x: auto !important;
        width: 100% !important;
        max-width: 100% !important;
        display: block !important;
    }
    
    /* Actual table element */
    .stDataFrame table,
    div[data-testid="stDataFrame"] table {
        width: auto !important;
        min-width: 100% !important;
        table-layout: auto !important;
        display: table !important;
    }
    
    /* Table cells - allow wrapping for better mobile UX */
    .stDataFrame th,
    .stDataFrame td,
    div[data-testid="stDataFrame"] th,
    div[data-testid="stDataFrame"] td {
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        padding: 0.5rem 0.4rem !important;
        font-size: 0.75rem !important;
        max-width: 200px !important;
    }
    
    /* Table headers - smaller font on mobile */
    .stDataFrame th,
    div[data-testid="stDataFrame"] th {
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        padding: 0.4rem 0.3rem !important;
    }
    
    /* Ensure expander tables also scroll */
    [data-testid="stExpander"] .stDataFrame,
    [data-testid="stExpander"] div[data-testid="stDataFrame"] {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
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
    
    /* Mobile chart fixes */
    .js-plotly-plot .plotly .gtitle {
        font-size: 12px !important;
    }
    
    .js-plotly-plot .plotly .legend {
        font-size: 9px !important;
    }
    
    /* Footer - center all content on mobile */
    div[data-testid="stMarkdownContainer"]:has(> div > p:contains("HEDIS Portfolio Optimizer")) {
        text-align: center !important;
    }
    
    /* Center footer paragraphs */
    div[data-testid="stMarkdownContainer"] p {
        text-align: center !important;
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
    
    /* Sidebar styling - REMOVED: Now handled by STANDARD_SIDEBAR_CSS imported from utility */
    
    /* Navigation visibility is handled by apply_sidebar_styling() function */
    /* No additional CSS needed here */
    
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
    /* ========== DATE INPUT VISIBILITY - DESKTOP & MOBILE ========== */
    
    /* Date input container in sidebar - all screen sizes */
    [data-testid="stSidebar"] [data-testid="stDateInput"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 5px !important;
        padding: 2px 4px !important;
        margin-bottom: 0.25rem !important;
    }
    
    /* Reduce padding inside date input boxes */
    [data-testid="stSidebar"] [data-testid="stDateInput"] input,
    [data-testid="stSidebar"] [data-testid="stDateInput"] > div,
    [data-testid="stSidebar"] [data-testid="stDateInput"] > div > div {
        padding: 0.2rem 0.35rem !important;
        margin: 0 !important;
    }
    
    /* Reduce padding for date input columns */
    [data-testid="stSidebar"] [data-testid="column"] {
        padding: 0.1rem !important;
        gap: 0.25rem !important;
    }
    
    /* ========== HIDE DATE INPUT LABELS INSIDE INPUT BOXES ========== */
    /* Hide labels that appear inside date input boxes (we use custom labels above) */
    [data-testid="stSidebar"] .stDateInput label,
    [data-testid="stSidebar"] [data-testid="stDateInput"] label,
    [data-testid="stSidebar"] .stDateInput > label,
    [data-testid="stSidebar"] [data-testid="stDateInput"] > label,
    [data-testid="stSidebar"] .stDateInput [data-baseweb="form-control"] label,
    [data-testid="stSidebar"] [data-testid="stDateInput"] [data-baseweb="form-control"] label {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        font-size: 0 !important;
    }
    
    /* Hide any placeholder text that might show "Start Date" or "End Date" */
    [data-testid="stSidebar"] .stDateInput input::placeholder,
    [data-testid="stSidebar"] [data-testid="stDateInput"] input::placeholder {
        color: transparent !important;
    }
    
    /* Force the date input text visible - REDUCED PADDING */
    [data-testid="stSidebar"] .stDateInput input,
    [data-testid="stSidebar"] [data-testid="stDateInput"] input,
    [data-testid="stSidebar"] [data-baseweb="input"] input {
        color: #1f2937 !important;
        background-color: white !important;
        -webkit-text-fill-color: #1f2937 !important;
        padding: 0.15rem 0.3rem !important; /* Minimized padding */
        border: 1px solid #d1d5db !important;
        border-radius: 4px !important;
        font-size: 0.9rem !important;
        opacity: 1 !important;
    }
    
    /* Reduce date input container padding */
    [data-testid="stSidebar"] .stDateInput,
    [data-testid="stSidebar"] [data-testid="stDateInput"] {
        padding: 0.05rem 0 !important; /* Minimized container padding */
        margin: 0.05rem 0 !important;
    }
    
    /* Reduce date input wrapper padding */
    [data-testid="stSidebar"] .stDateInput > div,
    [data-testid="stSidebar"] [data-testid="stDateInput"] > div {
        padding: 0.05rem !important; /* Minimized wrapper padding */
    }
    
    /* Reduce padding on date input containers */
    [data-testid="stSidebar"] .stDateInput,
    [data-testid="stSidebar"] [data-testid="stDateInput"] {
        padding: 0.1rem 0 !important;
    }
    
    /* Date input wrapper */
    [data-testid="stSidebar"] [data-testid="stDateInput"] > div > div {
        background-color: white !important;
    }
    
    /* BaseWeb input component */
    [data-testid="stSidebar"] [data-baseweb="input"] {
        background-color: white !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="input"] input {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
    }
    
    /* ========== FORCE DATE VALUES VISIBLE ========== */
    /* Force date values visible - Enhanced */
    [data-testid="stDateInput"] input {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        background-color: white !important;
        font-size: 0.9rem !important;
        padding: 0.5rem !important;
    }
    
    /* Target BaseWeb input */
    [data-baseweb="input"] input {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
    }
    
    /* Also target text type inputs */
    [data-testid="stDateInput"] input[type="text"] {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        background-color: white !important;
        opacity: 1 !important;
    }
    
    /* Sidebar specific */
    [data-testid="stSidebar"] input {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        background-color: white !important;
    }
    
    /* Force the date text to show */
    [data-testid="stDateInput"] [data-baseweb="base-input"] {
        background-color: white !important;
    }
    
    [data-testid="stDateInput"] [data-baseweb="base-input"] input {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        opacity: 1 !important;
    }
    
    /* Date picker button/icon */
    [data-testid="stSidebar"] [data-testid="stDateInput"] button {
        color: #4A3D6F !important;
        background-color: white !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stDateInput"] svg {
        fill: #4A3D6F !important;
    }
    
    /* Caption text (days selected) */
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: white !important;
        font-size: 0.85rem !important;
    }
    
    /* Section headers */
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* ========== MOBILE-SPECIFIC ENHANCEMENTS ========== */
    
    @media (max-width: 768px) {
        /* Larger touch targets for mobile date inputs */
        [data-testid="stSidebar"] [data-testid="stDateInput"] input {
            padding: 0.75rem !important;
            font-size: 1rem !important;
            min-height: 44px !important;  /* Apple's minimum touch target */
        }
        
        /* Larger tap area for calendar icon */
        [data-testid="stSidebar"] [data-testid="stDateInput"] button {
            min-width: 44px !important;
            min-height: 44px !important;
            padding: 0.5rem !important;
        }
        
        /* More spacing between date fields on mobile */
        [data-testid="stSidebar"] [data-testid="stDateInput"] {
            margin-bottom: 0.75rem !important;
        }
        
        /* Ensure date labels are readable on mobile */
        [data-testid="stSidebar"] [data-testid="stDateInput"] label {
            font-size: 0.95rem !important;
        }
        
        /* Mobile specific - force labels visible */
        [data-testid="stSidebar"] .stDateInput label {
            color: white !important;
            font-size: 0.95rem !important;
        }
        
        /* Days selected caption - larger on mobile */
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
            font-size: 0.9rem !important;
            padding: 0.5rem 0 !important;
        }
        
        /* Section header larger on mobile */
        [data-testid="stSidebar"] h3 {
            font-size: 1.1rem !important;
        }
    }
    
    /* ========== HIDE SEARCH/FILTER TEXT BOXES ON MOBILE ========== */
    @media (max-width: 768px) {
        /* Hide dataframe search/filter text boxes on mobile */
        [data-testid="stDataFrame"] input[type="text"],
        [data-testid="stDataFrame"] input[type="search"],
        .stDataFrame input[type="text"],
        .stDataFrame input[type="search"] {
            display: none !important;
        }
        
        /* Hide generic search boxes (chat inputs have different placeholders, so they stay visible) */
        [data-testid="stTextInput"][placeholder*="search" i],
        [data-testid="stTextInput"][placeholder*="filter" i],
        [data-testid="stTextInput"][placeholder*="Search" i],
        [data-testid="stTextInput"][placeholder*="Filter" i] {
            display: none !important;
        }
        
        /* Hide search boxes in expanders and containers */
        .streamlit-expander input[type="text"],
        .streamlit-expander input[type="search"] {
            display: none !important;
        }
        
        /* Fix tables on mobile - prevent off-page overflow */
        [data-testid="stDataFrame"] {
            overflow-x: auto !important;
            max-width: 100% !important;
        }
        
        [data-testid="stDataFrame"] > div {
            max-width: 100vw !important;
        }
        
        /* Ensure table containers don't overflow */
        .stDataFrame {
            overflow-x: auto !important;
            max-width: 100% !important;
            width: 100% !important;
        }
        
        /* Force table scrolling on mobile */
        [data-testid="stDataFrame"] table {
            min-width: 100% !important;
            display: table !important;
        }
    }
    
    /* ========== CALENDAR POPUP FIXES ========== */
    
    /* Ensure calendar popup is visible and usable */
    [data-baseweb="popover"] {
        z-index: 9999 !important;
    }
    
    [data-baseweb="calendar"] {
        background-color: white !important;
        color: #1f2937 !important;
    }
    
    [data-baseweb="calendar"] button {
        color: #1f2937 !important;
    }
    
    /* Mobile calendar sizing */
    @media (max-width: 768px) {
        [data-baseweb="calendar"] {
            font-size: 0.95rem !important;
        }
        
        [data-baseweb="calendar"] button {
            min-width: 40px !important;
            min-height: 40px !important;
        }
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
        text-align: center !important;
    }
    
    .plotly-container h4 {
        text-align: center !important;
        margin: 0.5rem 0 !important;
    }
    
    .plotly-container p {
        text-align: center !important;
        margin: 0.25rem 0 !important;
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
""", unsafe_allow_html=True)

st.markdown("""
<script>
    // Hide mobile pages in sidebar navigation (but NOT the Home button)
    function hideAppLabel() {
        // Wait for sidebar navigation to load
        const sidebarNav = document.querySelector('[data-testid="stSidebarNav"]');
        if (sidebarNav) {
            // Find and hide links to mobile pages only (NOT the Home button)
            const links = sidebarNav.querySelectorAll('a');
            links.forEach(link => {
                const href = link.getAttribute('href') || '';
                const text = link.textContent.trim().toLowerCase();
                
                // DO NOT hide the Home button - it's styled via CSS as "🏠 Home"
                // Only hide mobile page links - More aggressive matching
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
    
    // Navigation container styling is handled by CSS from apply_sidebar_styling() function
    // No JavaScript manipulation needed
    
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
    
    // Fix sidebar label: ALWAYS ensure "⚡ Performance Dashboard" is shown correctly
    function fixPerformanceDashboardLabel() {
        const sidebarNav = document.querySelector('[data-testid="stSidebarNav"]');
        if (sidebarNav) {
            const links = sidebarNav.querySelectorAll('a, [role="link"]');
            links.forEach(link => {
                const text = (link.textContent || link.innerText || '').trim();
                const lowerText = text.toLowerCase();
                
                // Check if it's Performance Dashboard - catch ANY variation including corrupted emojis
                const isPerformanceDashboard = (
                    lowerText.includes('performance dashboard') ||
                    lowerText.includes('performance_dashboard') ||
                    /performance\s*dashboard/i.test(text)
                );
                
                // Check if it needs fixing (missing emoji, has wrong prefix, or corrupted)
                const needsFix = (
                    isPerformanceDashboard && (
                        text.startsWith('z') ||
                        text.startsWith('â') ||
                        text.startsWith('š') ||
                        text.startsWith('¡') ||
                        !text.includes('⚡')
                    )
                );
                
                if (needsFix || (isPerformanceDashboard && text !== '⚡ Performance Dashboard')) {
                    // Force set to correct text
                    link.textContent = '⚡ Performance Dashboard';
                    link.innerText = '⚡ Performance Dashboard';
                    
                    // Fix all child elements
                    link.querySelectorAll('span, div, p, *').forEach(child => {
                        const childText = (child.textContent || child.innerText || '').trim();
                        if (childText.toLowerCase().includes('performance dashboard') && 
                            childText !== '⚡ Performance Dashboard') {
                            child.textContent = '⚡ Performance Dashboard';
                            child.innerText = '⚡ Performance Dashboard';
                        }
                    });
                }
            });
        }
    }
    
    // Run on page load and after delays
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixPerformanceDashboardLabel);
    } else {
        fixPerformanceDashboardLabel();
    }
    setTimeout(fixPerformanceDashboardLabel, 500);
    setTimeout(fixPerformanceDashboardLabel, 1000);
    setTimeout(fixPerformanceDashboardLabel, 2000);
    // ====================================================================
    // FORCE CENTER ALL METRIC LABELS AND VALUES (CUSTOM HTML METRICS)
    // ====================================================================
    function forceCenterCustomMetrics() {
        // Find all custom metric containers
        const customContainers = document.querySelectorAll('.centered-metric-container');
        
        customContainers.forEach(container => {
            // Force center alignment on container
            container.style.textAlign = 'center';
            container.style.display = 'flex';
            container.style.flexDirection = 'column';
            container.style.alignItems = 'center';
            container.style.justifyContent = 'center';
            container.style.width = '100%';
            container.style.marginLeft = 'auto';
            container.style.marginRight = 'auto';
            
            // Center all paragraphs inside
            const paragraphs = container.querySelectorAll('p');
            paragraphs.forEach(p => {
                p.style.textAlign = 'center';
                p.style.marginLeft = 'auto';
                p.style.marginRight = 'auto';
                p.style.width = '100%';
                p.style.display = 'block';
            });
            
            // Center all spans (like help icons)
            const spans = container.querySelectorAll('span');
            spans.forEach(span => {
                span.style.textAlign = 'center';
                span.style.display = 'inline';
            });
        });
        
        // Also target markdown containers in columns
        const columnMarkdowns = document.querySelectorAll('[data-testid="column"] .stMarkdown, [data-testid="column"] .stMarkdownContainer');
        columnMarkdowns.forEach(md => {
            md.style.textAlign = 'center';
            md.style.display = 'flex';
            md.style.flexDirection = 'column';
            md.style.alignItems = 'center';
            
            const mdParagraphs = md.querySelectorAll('p');
            mdParagraphs.forEach(p => {
                p.style.textAlign = 'center';
                p.style.marginLeft = 'auto';
                p.style.marginRight = 'auto';
                p.style.width = '100%';
            });
        });
    }
    
    // Run immediately and on delays
    forceCenterCustomMetrics();
    setTimeout(forceCenterCustomMetrics, 100);
    setTimeout(forceCenterCustomMetrics, 500);
    setTimeout(forceCenterCustomMetrics, 1000);
    setTimeout(forceCenterCustomMetrics, 2000);
    
    // Watch for new metrics being added
    const metricObserver = new MutationObserver(function() {
        forceCenterCustomMetrics();
    });
    
    metricObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // ====================================================================
    // REMOVE DATE INPUT LABELS FROM INPUT BOXES
    // ====================================================================
    function removeDateInputLabels() {
        // Find all date input labels in sidebar
        const dateLabels = document.querySelectorAll('[data-testid="stSidebar"] .stDateInput label, [data-testid="stSidebar"] [data-testid="stDateInput"] label');
        
        dateLabels.forEach(label => {
            const labelText = (label.textContent || label.innerText || '').trim();
            // Hide labels that say "Start Date" or "End Date"
            if (labelText === 'Start Date' || labelText === 'End Date' || labelText.includes('Start Date') || labelText.includes('End Date')) {
                label.style.display = 'none';
                label.style.visibility = 'hidden';
                label.style.height = '0';
                label.style.margin = '0';
                label.style.padding = '0';
            }
        });
    }
    
    // ====================================================================
    // FORCE DARK TEXT ON SIDEBAR DATE INPUTS (for visibility)
    // ====================================================================
    function forceDateInputTextVisible() {
        // Find all date inputs in sidebar
        const sidebarDateInputs = document.querySelectorAll('[data-testid="stSidebar"] .stDateInput input, [data-testid="stSidebar"] [data-testid="stDateInput"] input');
        
        sidebarDateInputs.forEach(input => {
            // Force dark text color for visibility
            input.style.color = '#1f2937';
            input.style.setProperty('color', '#1f2937', 'important');
            input.style.setProperty('-webkit-text-fill-color', '#1f2937', 'important');
            input.style.backgroundColor = 'white';
        });
        
        // Also target BaseWeb input wrappers
        const baseWebInputs = document.querySelectorAll('[data-testid="stSidebar"] [data-baseweb="input"] input');
        baseWebInputs.forEach(input => {
            input.style.color = '#1f2937';
            input.style.setProperty('color', '#1f2937', 'important');
            input.style.setProperty('-webkit-text-fill-color', '#1f2937', 'important');
        });
    }
    
    // Run immediately and on delays
    removeDateInputLabels();
    forceDateInputTextVisible();
    setTimeout(removeDateInputLabels, 100);
    setTimeout(forceDateInputTextVisible, 100);
    setTimeout(removeDateInputLabels, 500);
    setTimeout(forceDateInputTextVisible, 500);
    setTimeout(removeDateInputLabels, 1000);
    setTimeout(forceDateInputTextVisible, 1000);
    setTimeout(removeDateInputLabels, 2000);
    setTimeout(forceDateInputTextVisible, 2000);
    
    // Watch for new date inputs being added
    const dateInputObserver = new MutationObserver(function() {
        removeDateInputLabels();
        forceDateInputTextVisible();
    });
    
    dateInputObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Also run periodically to catch any missed inputs
    setInterval(function() {
        removeDateInputLabels();
        forceDateInputTextVisible();
    }, 2000);
    
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
    const dateVisibilityObserver = new MutationObserver(function() {
        forceDateInputVisibility();
    });
    
    dateVisibilityObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Also run periodically
    setInterval(forceDateInputVisibility, 2000);


</script>
""", unsafe_allow_html=True)


# ============================================================================
# 5. SIDEBAR (AFTER DATA IS LOADED)
# ============================================================================
# Sliders can now safely access raw_portfolio_data
with st.sidebar:
    # ===== FILTERS SECTION - ALL CENTERED =====
    st.markdown("""
    <div style="text-align: center;">
        <h4 style="color: white; margin: 0.5rem 0; font-size: 1rem; font-weight: 600;">🎛️ Filters</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # ====================================================================
    # MEMBERSHIP SIZE CONTROL - REMOVED (CONSOLIDATED WITH PLAN SIZE FILTER)
    # ====================================================================
    # Note: Plan Membership Size is now automatically set based on Plan Size filter selection
    # This eliminates redundancy and simplifies the user experience
    
    # ====================================================================
    # DATE RANGE - Default Q4 2025
    # ====================================================================
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: white; font-size: 0.9rem; font-weight: 600; margin: 0.5rem 0;">📅 Date Range</p>
    </div>
    """, unsafe_allow_html=True)
    
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
        # Explicitly show Start Date label - CENTERED
        st.markdown("<p style='text-align: center; color: white; font-size: 0.8rem; font-weight: 500; margin-top: 0.75rem; margin-bottom: 0.25rem;'>Start Date</p>", unsafe_allow_html=True)
        start_date = st.date_input(
            "",  # Empty label - label is shown above
            value=st.session_state.filters.get('date_range_start', date(2024, 10, 1)),
            key="start_date_filter",
            format="MM/DD/YYYY",
            label_visibility="collapsed"  # Hide label from input box
        )
        st.session_state.filters['date_range_start'] = start_date
    
    with date_col2:
        # Explicitly show End Date label - CENTERED
        st.markdown("<p style='text-align: center; color: white; font-size: 0.8rem; font-weight: 500; margin-top: 0.75rem; margin-bottom: 0.25rem;'>End Date</p>", unsafe_allow_html=True)
        end_date = st.date_input(
            "",  # Empty label - label is shown above
            value=st.session_state.filters.get('date_range_end', date(2024, 12, 31)),
            key="end_date_filter",
            format="MM/DD/YYYY",
            label_visibility="collapsed"  # Hide label from input box
        )
        st.session_state.filters['date_range_end'] = end_date
    
    # Display and validate - CENTERED
    if start_date <= end_date:
        days = (end_date - start_date).days
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="color: white; font-size: 0.8rem; margin: 0.5rem 0;">📆 {start_date.strftime('%m/%d/%Y')} to {end_date.strftime('%m/%d/%Y')} ({days} days)</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ Start date must be before end date")
    
    # Update backward compatibility
    st.session_state.date_range = {'start': start_date, 'end': end_date}
    
    st.markdown("---")
    
    # ====================================================================
    # HEDIS MEASURES - All 12 Selected by Default
    # ====================================================================
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: white; font-size: 0.9rem; font-weight: 600; margin: 0.5rem 0;">📋 HEDIS Measures</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Multiselect label - CENTERED
    st.markdown("<p style='text-align: center; color: white; font-size: 0.8rem; margin: 0.5rem 0;'>Choose measures to analyze:</p>", unsafe_allow_html=True)
    
    # Multiselect with ALL measures selected by default
    selected_measures = st.multiselect(
        "Measures",
        options=ALL_MEASURES,
        default=st.session_state.filters['selected_measures'],  # Will be all 12 by default
        key="measures_multiselect",
        label_visibility="collapsed",
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
    
    # Green separator
    st.markdown("<hr style='border-color: #10b981; margin: 0.75rem 0;'>", unsafe_allow_html=True)
    
    # ========================================================================
    # PLAN SIZE FILTER (CONSOLIDATED - Also sets scaling membership size)
    # ========================================================================
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: white; font-size: 0.9rem; font-weight: 600; margin: 0.5rem 0;">🏥 Plan Size</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Plan Size multiselect label - CENTERED
    st.markdown("<p style='text-align: center; color: white; font-size: 0.8rem; margin: 0.5rem 0;'>Select plan size categories:</p>", unsafe_allow_html=True)
    
    selected_plan_sizes = st.multiselect(
        "Plan Size",
        options=PLAN_SIZE_OPTIONS,
        default=st.session_state.filters['plan_sizes'] if st.session_state.filters['plan_sizes'] else PLAN_SIZE_OPTIONS.copy(),
        key="plan_size_multiselect",
        label_visibility="collapsed",
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
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: white; font-size: 0.9rem; font-weight: 600; margin: 0.5rem 0;">🎯 Threshold Filters</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # ============================================================================
    # LIVE FILTER PREVIEW
    # ============================================================================
    st.markdown("---")
    st.markdown("<p style='color: white; font-size: 0.9rem; font-weight: 600; margin: 0.5rem 0;'>📊 Filter Impact</p>", unsafe_allow_html=True)
    
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
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: white; font-size: 0.9rem; font-weight: 600; margin: 0.5rem 0;">⚙️ Actions</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Database status
    show_db_status()
    st.markdown("---")
    
    st.markdown("**Built by:** Robert Reichert")
    st.markdown("**Version:** 4.0")
    
    # Sidebar footer - must be inside sidebar context
    render_sidebar_footer()
    
    # Secure AI box (Mobile Optimized badge removed)
    st.sidebar.markdown("""
    <style>
    #secure-ai-box, #secure-ai-box * { color: #000 !important; }
    </style>
    
    <div id='secure-ai-box' style='background: #e8f5e9; padding: 12px; border-radius: 12px; margin: 16px auto; text-align: center; border: 2px solid #4caf50; max-width: 280px;'>
        <div style='color: #000 !important; font-weight: 700; font-size: 1.1rem; margin-bottom: 8px;'>
            <font color='#000000'>🔒 Secure AI Architect</font>
        </div>
        <div style='color: #000 !important; font-size: 0.85rem; line-height: 1.5;'>
            <font color='#000000'>Healthcare AI insights without data exposure. On-premises intelligence delivering 2.8-4.1x ROI and full HIPAA compliance.</font>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    
    # 4-column metric cards - USING CENTERED CUSTOM HTML
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        centered_metric(
            label="Potential ROI",
            value=f"{hero_roi_percent:.0f}%",
            delta=f"+{format_currency(hero_net_benefit)} annually",
            help_text=f"Projected return on {format_currency(hero_investment)} investment"
        )
    
    with col2:
        centered_metric(
            label="Star Rating Impact",
            value=f"{projected_stars:.1f} ⭐",
            delta=f"+{star_improvement:.1f} stars",
            help_text="Projected improvement in CMS Star Rating for 2025"
        )
    
    with col3:
        centered_metric(
            label="Members Optimized",
            value=f"{hero_members:,}",
            delta=f"{hero_closures:,} closures",
            help_text=f"Total members in filtered dataset at {st.session_state.membership_size:,} member plan size"
        )
    
    with col4:
        centered_metric(
            label="Compliance Rate",
            value=f"{hero_success_rate:.1f}%",
            delta=f"+{hero_success_rate - baseline_success:.1f}%",
            help_text="Overall HEDIS measure compliance rate vs industry baseline"
        )

else:
    # No data after filtering - show warning
    st.warning("⚠️ No data matches current filters. Showing baseline estimates.")
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        centered_metric(label="Potential ROI", value="--", delta="Adjust filters")
    
    with col2:
        centered_metric(label="Star Rating Impact", value="--", delta="Adjust filters")
    
    with col3:
        centered_metric(label="Members Optimized", value="0", delta="No data")
    
    with col4:
        centered_metric(label="Compliance Rate", value="--", delta="Adjust filters")

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

# Create status bar - USING CENTERED CUSTOM HTML
col1, col2, col3, col4, col5 = st.columns(5, gap="small")

with col1:
    delta_val = f"{len(current_filtered) - len(current_data):,}" if len(current_filtered) != len(current_data) else None
    centered_metric(
        label="📋 Records Shown",
        value=f"{len(current_filtered):,}",
        delta=delta_val
    )

with col2:
    # Show unique measures instead of redundant total members
    if not current_filtered.empty and 'measure_name' in current_filtered.columns:
        unique_measures = current_filtered['measure_name'].nunique()
        total_measures = current_data['measure_name'].nunique() if not current_data.empty else 12
        delta_val = f"{total_measures - unique_measures} filtered out" if unique_measures < total_measures else "All measures"
        centered_metric(
            label="📊 Measures",
            value=f"{unique_measures}",
            delta=delta_val
        )
    else:
        centered_metric(label="📊 Measures", value="--")

with col3:
    if not current_filtered.empty and 'financial_value' in current_filtered.columns:
        total_value = current_filtered['financial_value'].sum()
        scaled_value = total_value * (st.session_state.membership_size / 10000)
        centered_metric(
            label="💰 Total Value",
            value=format_currency(scaled_value),
            delta=None
        )
    else:
        centered_metric(label="💰 Total Value", value="$0")

with col4:
    # Plan Size Count
    plan_sizes_selected = st.session_state.filters.get('plan_sizes', [])
    plan_size_count = len(plan_sizes_selected) if plan_sizes_selected else 0
    membership_size = st.session_state.get('membership_size', 10000)
    
    if plan_size_count > 0:
        help_text = f"Selected plan size categories: {', '.join(plan_sizes_selected[:2])}{'...' if len(plan_sizes_selected) > 2 else ''}"
        centered_metric(
            label="🏥 Plan Sizes",
            value=f"{plan_size_count}",
            delta=f"Scaling: {membership_size:,} members",
            help_text=help_text
        )
    else:
        centered_metric(
            label="🏥 Plan Sizes",
            value="All",
            delta=f"Scaling: {membership_size:,} members",
            help_text="No plan size filter applied - showing all plan sizes"
        )

with col5:
    filter_pct = (len(current_filtered) / len(current_data) * 100) if len(current_data) > 0 else 0
    centered_metric(
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
# NAVIGATION TABS - CENTERED RADIO BUTTONS
# ============================================================================
selected_tab = st.radio(
    "Select View",
    ["📊 Portfolio Overview", "📈 Measure Deep-Dive", "👥 Member Lists", "💰 ROI Analysis", "🔒 Secure Query Interface"],
    horizontal=True,
    label_visibility="collapsed",
    key="home_tabs"
)

# CSS to center radio buttons
st.markdown("""
<style>
div[data-testid="stRadio"] > div {
    justify-content: center !important;
    display: flex !important;
}
div[data-testid="stRadio"] > div[role="radiogroup"] {
    justify-content: center !important;
    display: flex !important;
    gap: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# TAB 1: PORTFOLIO OVERVIEW
# ============================================================================
if selected_tab == "📊 Portfolio Overview":
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
                    use_container_width=True,
                    hide_index=True
                )
                # Add mobile-specific styling for table visibility
                st.markdown("""
                <style>
                @media (max-width: 768px) {
                    /* Ensure sample filtered data table is scrollable */
                    div[data-testid="stDataFrame"]:has(+ div) {
                        overflow-x: auto !important;
                        -webkit-overflow-scrolling: touch !important;
                    }
                }
                </style>
                """, unsafe_allow_html=True)
    
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
    st.markdown("""
    <style>
    /* Center KPI metric containers and all their content */
    .plotly-container {
        text-align: center !important;
    }
    
    .plotly-container h4 {
        text-align: center !important;
        margin: 0.5rem 0 !important;
    }
    
    .plotly-container p {
        text-align: center !important;
        margin: 0.25rem 0 !important;
    }
    
    /* Center columns containing plotly containers */
    [data-testid="column"]:has(.plotly-container) {
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="kpi-section-wrapper">', unsafe_allow_html=True)
    st.markdown("#### 📈 Key Performance Indicators")
    
    # Row 1: Investment and Closures
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        st.markdown("""
        <div class="plotly-container" style="text-align: center;">
            <h4 style="text-align: center; margin: 0.5rem 0;">Total Investment</h4>
            <p style="font-size: 2.5rem; font-weight: 700; color: #0066cc; text-align: center; margin: 0.25rem 0;">
                {}
            </p>
            <p style="color: #666; text-align: center; margin: 0.25rem 0;">
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
        <div class="plotly-container" style="text-align: center;">
            <h4 style="text-align: center; margin: 0.5rem 0;">Successful Closures</h4>
            <p style="font-size: 2.5rem; font-weight: 700; color: #0066cc; text-align: center; margin: 0.25rem 0;">
                {}
            </p>
            <p style="color: #666; text-align: center; margin: 0.25rem 0;">
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
        <div class="plotly-container" style="text-align: center;">
            <h4 style="text-align: center; margin: 0.5rem 0;">Revenue Impact</h4>
            <p style="font-size: 2.5rem; font-weight: 700; color: #0066cc; text-align: center; margin: 0.25rem 0;">
                {}
            </p>
            <p style="color: #666; text-align: center; margin: 0.25rem 0;">
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
        <div class="plotly-container" style="text-align: center;">
            <h4 style="text-align: center; margin: 0.5rem 0;">Net Benefit</h4>
            <p style="font-size: 2.5rem; font-weight: 700; color: #00cc66; text-align: center; margin: 0.25rem 0;">
                {}
            </p>
            <p style="color: #666; text-align: center; margin: 0.25rem 0;">
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
elif selected_tab == "📈 Measure Deep-Dive":
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
            paper_bgcolor='white',
            margin=dict(l=10, r=10, t=50, b=60),
            title=dict(font=dict(size=12), x=0.5),
            legend=dict(
                orientation='h',
                yanchor='top',
                y=-0.2,
                xanchor='center',
                x=0.5,
                font=dict(size=9)
            )
        )
        
        # Add target line at 1.0x (break-even)
        fig_roi.add_hline(
            y=1.0,
            line_dash="dash",
            line_color="red",
            annotation_text="Break-Even (1.0x)",
            annotation_position="right"
        )
        
        st.plotly_chart(fig_roi, use_container_width=True, key="tab2_measure_deepdive_roi_bar_chart")
        
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
                margin=dict(l=10, r=10, t=50, b=60),
                title=dict(font=dict(size=12), x=0.5),
                legend=dict(
                    orientation='h',
                    yanchor='top',
                    y=-0.2,
                    xanchor='center',
                    x=0.5,
                    font=dict(size=9)
                ),
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
            
            st.plotly_chart(fig_scatter, use_container_width=True, key="tab2_measure_deepdive_cost_efficiency_scatter")
            
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
elif selected_tab == "👥 Member Lists":
    st.markdown("### Member Lists & Segmentation")
    st.info("👥 Detailed member lists with eligibility, intervention status, and outcomes.")
    
    # Placeholder for member lists
    st.markdown("#### Eligible Members by Measure")
    st.info("💡 Filterable member lists will be displayed here with export functionality.")
    
    st.markdown("---")
    
    st.markdown("#### Member Segmentation")
    
    # Calculate actual impact values from filtered data
    if not filtered_data.empty:
        # Check if member_id column exists (synthetic data may not have it)
        has_member_id = 'member_id' in filtered_data.columns
        
        if has_member_id:
            # Calculate high priority members (multiple gaps)
            high_priority_data = filtered_data[filtered_data.groupby('member_id')['measure_name'].transform('count') > 1]
            high_priority_count = high_priority_data['member_id'].nunique() if not high_priority_data.empty else 0
            high_priority_impact = high_priority_data['financial_value'].sum() if 'financial_value' in high_priority_data.columns else 0
            
            # Calculate standard members (single gap)
            standard_data = filtered_data[filtered_data.groupby('member_id')['measure_name'].transform('count') == 1]
            standard_count = standard_data['member_id'].nunique() if not standard_data.empty else 0
            standard_impact = standard_data['financial_value'].sum() if 'financial_value' in standard_data.columns else 0
        else:
            # For synthetic data without member_id, use plan_size as proxy
            # High priority = plans with multiple measures
            high_priority_data = filtered_data[filtered_data.groupby('plan_size')['measure_name'].transform('count') > 1]
            high_priority_count = high_priority_data['plan_size'].nunique() if not high_priority_data.empty else 0
            high_priority_impact = high_priority_data['financial_value'].sum() if 'financial_value' in high_priority_data.columns else 0
            
            # Standard = plans with single measure
            standard_data = filtered_data[filtered_data.groupby('plan_size')['measure_name'].transform('count') == 1]
            standard_count = standard_data['plan_size'].nunique() if not standard_data.empty else 0
            standard_impact = standard_data['financial_value'].sum() if 'financial_value' in standard_data.columns else 0
        
        # Format impact values
        def format_impact(value):
            if value >= 1000000:
                return f"${value/1000000:.2f}M"
            elif value >= 1000:
                return f"${value/1000:.1f}K"
            else:
                return f"${value:,.0f}"
        
        high_priority_formatted = format_impact(high_priority_impact)
        standard_formatted = format_impact(standard_impact)
    else:
        high_priority_count = 0
        high_priority_formatted = "$0"
        standard_count = 0
        standard_formatted = "$0"
    
    segmentation_col1, segmentation_col2 = st.columns(2, gap="small")
    
    with segmentation_col1:
        st.markdown(f"""
        **High Priority Members:**
        - Members with multiple gap opportunities
        - High-value intervention targets
        - **Estimated impact: {high_priority_formatted}**
        - **Count: {high_priority_count:,} members**
        """)
    
    with segmentation_col2:
        st.markdown(f"""
        **Standard Members:**
        - Single gap opportunities
        - Standard intervention protocols
        - **Estimated impact: {standard_formatted}**
        - **Count: {standard_count:,} members**
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
elif selected_tab == "💰 ROI Analysis":
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
        title=dict(
            text='ROI Performance Trends - 2024',
            font=dict(size=12),
            x=0.5
        ),
        xaxis_title='Month',
        yaxis_title='ROI Ratio',
        height=500,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=10, r=10, t=50, b=60),
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(size=9)
        )
    )
    
    # Add break-even line
    fig_trend.add_hline(
        y=1.0,
        line_dash="dot",
        line_color="red",
        annotation_text="Break-Even"
    )
    
    st.plotly_chart(fig_trend, use_container_width=True, key="tab4_roi_analysis_trend_chart")
    
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
elif selected_tab == "🔒 Secure Query Interface":
    st.markdown("### 🔒 Secure Query Interface")
    st.markdown("#### Zero External API Exposure | On-Premises AI Processing")
    
    # Security badge - Cleaner, more readable display
    st.markdown("""
    <div style="background-color: #e8f5e9; padding: 1rem 1.25rem; border-radius: 8px; border-left: 4px solid #2d7d32; margin-bottom: 1rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h2 style="color: #2d7d32; margin: 0 0 0.5rem 0; font-size: 1.3rem; font-weight: 700; line-height: 1.3;">🔒 ZERO PHI TRANSMITTED TO EXTERNAL APIS</h2>
        <p style="margin: 0; color: #1b5e20; font-size: 0.9rem; line-height: 1.5;">All processing occurs on-premises using local models (Ollama/ChromaDB)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Data Flow Architecture Diagram
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; margin: 0.5rem 0;'>📊 Security Architecture: User → Local Model → Internal DB</h3>", unsafe_allow_html=True)
    
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
                size=70,
                color=step["color"],
                line=dict(width=2, color='white'),
                opacity=0.9
            ),
            text=[step["name"]],
            textposition="middle center",
            textfont=dict(size=9, color='white', family='Arial Black'),
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
    
    # Update layout - cleaner, more readable
    fig_flow.update_layout(
        title=dict(
            text="<b>Secure Data Flow: Zero External API Calls</b>",
            x=0.5,
            font=dict(size=12, color="#2d7d32", family="Arial")
        ),
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(size=9)
        ),
        xaxis=dict(showgrid=False, showticklabels=False, range=[-0.5, 5.5]),
        yaxis=dict(showgrid=False, showticklabels=False, range=[-0.5, 0.5]),
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=30, r=30, t=60, b=20)
    )
    
    st.plotly_chart(fig_flow, use_container_width=True, key="security_flow_diagram")
    
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
st.markdown("---")

# Hashtags
st.markdown("""
<div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;">
    <span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">#HealthcareAnalytics</span>
    <span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">#MedicareAdvantage</span>
    <span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">#HEDIS</span>
    <span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">#DataScience</span>
    <span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">#HealthcareAI</span>
</div>
""", unsafe_allow_html=True)

# Main card
st.markdown("""
<div style="background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%); border-radius: 16px; padding: 24px; margin-bottom: 16px; border-top: 4px solid #10b981;">
    <div style="text-align: center; margin-bottom: 16px;">
        <div style="color: white; font-size: 22px; font-weight: 700;">⭐ HEDIS Portfolio Optimizer | StarGuard AI</div>
        <div style="color: rgba(255,255,255,0.8); font-size: 14px; font-style: italic;">Turning Data Into Stars</div>
    </div>
    <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;">
        <span style="background: rgba(255,255,255,0.15); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; border: 1px solid rgba(255,255,255,0.2);">🐍 Python</span>
        <span style="background: rgba(255,255,255,0.15); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; border: 1px solid rgba(255,255,255,0.2);">📊 Streamlit</span>
        <span style="background: rgba(255,255,255,0.15); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; border: 1px solid rgba(255,255,255,0.2);">📈 Plotly</span>
        <span style="background: rgba(255,255,255,0.15); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; border: 1px solid rgba(255,255,255,0.2);">🐘 PostgreSQL</span>
        <span style="background: rgba(255,255,255,0.15); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; border: 1px solid rgba(255,255,255,0.2);">🤖 ML/AI</span>
    </div>
    <div style="background: rgba(16, 185, 129, 0.15); border: 2px solid rgba(16, 185, 129, 0.5); border-radius: 12px; padding: 16px; margin: 0 auto; max-width: 600px;">
        <div style="text-align: center; margin-bottom: 8px;">
            <span style="color: #10b981; font-size: 18px; font-weight: 700;">🔒 Secure AI Architecture</span>
        </div>
        <div style="color: rgba(255,255,255,0.9); font-size: 13px; text-align: center; margin-bottom: 12px;">Healthcare AI that sees everything, exposes nothing.</div>
        <div style="display: flex; justify-content: center; gap: 32px; flex-wrap: wrap; margin-bottom: 12px;">
            <div style="text-align: center;">
                <div style="color: #10b981; font-size: 18px; font-weight: 700;">2.8-4.1x</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 11px;">ROI Delivered</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #10b981; font-size: 18px; font-weight: 700;">$148M+</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 11px;">Proven Savings</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #10b981; font-size: 18px; font-weight: 700;">Zero</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 11px;">PHI Exposure</div>
            </div>
        </div>
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 8px;">
            <span style="background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.9); padding: 4px 10px; border-radius: 20px; font-size: 11px;">🏢 On-Premises</span>
            <span style="background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.9); padding: 4px 10px; border-radius: 20px; font-size: 11px;">🚫 Zero API Transmission</span>
            <span style="background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.9); padding: 4px 10px; border-radius: 20px; font-size: 11px;">🏥 HIPAA-First Design</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div style="background: linear-gradient(135deg, #fef3c7, #fde68a); border-left: 4px solid #f59e0b; border-radius: 0 10px 10px 0; padding: 12px 16px; margin-bottom: 12px; display: flex; align-items: center; gap: 10px;">
    <span style="font-size: 20px;">⚠️</span>
    <span style="color: #92400e; font-size: 13px;"><strong>Portfolio Demonstration:</strong> Using synthetic data to showcase real methodology and production-grade analytics capabilities.</span>
</div>
""", unsafe_allow_html=True)

# Copyright
st.markdown("""
<div style="text-align: center; padding: 12px 0; color: #6b7280; font-size: 13px;">
    © 2024-2026 <span style="color: #4A3D6F; font-weight: 600;">Robert Reichert</span> | StarGuard AI™ | Healthcare AI Architect
</div>
""", unsafe_allow_html=True)


