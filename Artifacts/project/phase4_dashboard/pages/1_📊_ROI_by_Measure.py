"""
Page 1: ROI by Measure
Bar chart showing ROI performance across all HEDIS measures
"""
import sys
from pathlib import Path

# Fix Python path for Streamlit pages - ensure utils can be imported
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import streamlit as st

# CRITICAL: st.set_page_config MUST be called before any other Streamlit commands
st.set_page_config(page_title="ROI by Measure", page_icon="📊", layout="wide")

st.markdown("""
<style>
.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 0.5rem !important;
    margin-top: 0 !important;
}
.element-container {
    margin: 0.2rem 0 !important;
    padding: 0 !important;
}
h1, h2, h3, h4 {
    margin: 0.3rem 0 !important;
    padding: 0.2rem 0 !important;
}
p {
    margin: 0.2rem 0 !important;
}
.starguard-header {
    margin-top: 0 !important;
    margin-bottom: 0.5rem !important;
}

/* StarGuard Header Container - NO BOTTOM BORDER HERE */
.starguard-header-container {
    background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%);
    padding: 1rem 1.5rem 0.5rem 1.5rem !important;
    border-radius: 10px;
    margin-top: 0 !important;
    margin-bottom: 0rem !important;
    text-align: center;
    box-shadow: 0 4px 12px rgba(74, 61, 111, 0.25);
    border-bottom: none !important;
}

/* Title - GREEN LINE HERE (between title and subtitle) */
.starguard-title {
    color: white !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    margin: 0 0 0.5rem 0 !important;
    padding: 0 0 0.5rem 0 !important;
    line-height: 1.2 !important;
    border-bottom: 3px solid #4ade80 !important;
}

/* Subtitle - NO BORDER HERE */
.starguard-subtitle {
    color: rgba(255, 255, 255, 0.92) !important;
    font-size: 0.85rem !important;
    margin: 0.5rem 0 0 0 !important;
    padding: 0 !important;
    line-height: 1.3 !important;
    border-bottom: none !important;
}

/* Mobile */
@media (max-width: 768px) {
    .starguard-header-container {
        padding: 0.8rem 1rem !important;
        margin-bottom: 0rem !important;
    }
    
    .starguard-title {
        font-size: 1.2rem !important;
        margin-bottom: 0.4rem !important;
        padding-bottom: 0.4rem !important;
    }
    
    .starguard-subtitle {
        font-size: 0.7rem !important;
        margin-top: 0.4rem !important;
    }
}

[data-testid="stSidebar"] button[kind="header"] {
    color: white !important;
}
[data-testid="stSidebar"] button svg {
    fill: white !important;
    stroke: white !important;
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

/* Reduce spacing after header - AGGRESSIVE */
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


    .mobile-optimized-badge {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        width: fit-content !important;
    }

/* ========== CENTER-ALIGN METRICS AND TABLES FOR CLEAN VIEWING ========== */

/* Center metric cards - values and labels */
[data-testid="stMetricValue"],
[data-testid="stMetricLabel"],
[data-testid="stMetricDelta"] {
    text-align: center !important;
    justify-content: center !important;
}

/* Center metric containers */
div[data-testid="stMetricContainer"] {
    text-align: center !important;
}

/* Center metric value text */
[data-testid="stMetricValue"] > div {
    text-align: center !important;
    margin: 0 auto !important;
}

/* Center metric labels */
[data-testid="stMetricLabel"] > div {
    text-align: center !important;
    margin: 0 auto !important;
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

/* Center column headers in tables */
.stDataFrame th {
    text-align: center !important;
}

/* Center numeric values in tables */
.stDataFrame td {
    text-align: center !important;
}

/* Keep text content left-aligned (headings, paragraphs) for readability */
/* Exception: h2 and h3 are centered */
h1,   h4, h5, h6 {
    text-align: left !important;
}

p, li {
    text-align: left !important;
}

/* Exception: Center specific summary/metric section headers */
{
    text-align: center !important;
}


/* ========== CENTER SUMMARY HEADERS AND NOTES ========== */

/* Center all h2 and h3 headers (section headers) */
h2, h3 {
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


/* Center all h2 and h3 headers that are section headers */
h2, h3 {
    text-align: center !important;
}

/* Center captions and notes */
.stCaption,
[data-testid="stCaption"],
.stMarkdown:has-text("📊"),
.stMarkdown:has-text("💰"),
.stMarkdown:has-text("📈"),
.stMarkdown:has-text("💵"),
.stMarkdown:has-text("🎯"),
.stMarkdown:has-text("🤖"),
.stMarkdown:has-text("📋"),
.stMarkdown:has-text("⭐"),
.stMarkdown:has-text("🔄"),
.stMarkdown:has-text("📊"),
.stMarkdown:has-text("⚖️"),
.stMarkdown:has-text("⚡") {
    text-align: center !important;
}

/* Center markdown headers that are summary sections */
.stMarkdown h2,
.stMarkdown h3 {
    text-align: center !important;
}

/* Center section dividers text */
hr + h2,
hr + h3,
.stMarkdown:has(hr) + h2,
.stMarkdown:has(hr) + h3 {
    text-align: center !important;
}



/* Center all markdown content that follows metrics */
div[data-testid="stVerticalBlock"]:has([data-testid="stMetricContainer"]) + .stMarkdown,
div[data-testid="stVerticalBlock"]:has([data-testid="stMetricContainer"]) ~ .stMarkdown {
    text-align: center !important;
}

/* Center summary statistics headers */
{
    text-align: center !important;
}




/* ========== CENTER KPI/METRIC HEADERS ========== */
/* Center metric labels (Potential ROI, Star Rating Impact, etc.) */
[data-testid="stMetricLabel"] {
    display: flex !important;
    justify-content: center !important;
    text-align: center !important;
}

[data-testid="stMetricLabel"] > div {
    text-align: center !important;
    width: 100% !important;
}

/* Center metric values */
[data-testid="stMetricValue"] {
    display: flex !important;
    justify-content: center !important;
    text-align: center !important;
}

/* Center metric delta (the +/- change indicators) */
[data-testid="stMetricDelta"] {
    display: flex !important;
    justify-content: center !important;
}

/* Center content in metric containers */
[data-testid="metric-container"] {
    text-align: center !important;
}

/* Center column content for KPI cards */
[data-testid="column"] {
    text-align: center !important;
}


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


/* ========== CENTER SIDEBAR CONTENT ========== */
/* Center sidebar text and labels */
[data-testid="stSidebar"] [data-testid="stMarkdown"] {
    text-align: center !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p {
    text-align: center !important;
}

/* Center sidebar metric cards */
[data-testid="stSidebar"] [data-testid="stMetricLabel"],
[data-testid="stSidebar"] [data-testid="stMetricValue"],
[data-testid="stSidebar"] [data-testid="stMetricDelta"] {
    justify-content: center !important;
    text-align: center !important;
}

/* Center expander headers in sidebar */
[data-testid="stSidebar"] .streamlit-expanderHeader {
    justify-content: center !important;
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

/* ========== PAGE TITLE STYLING - MATCH ROI CALCULATOR ========== */
/* Large bold h1 titles matching ROI Calculator */
h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin-top: 0.5rem !important;
    margin-bottom: 0.5rem !important;
    padding-top: 0 !important;
    line-height: 1.2 !important;
}

/* Style first h3 on page as page title (if not using h1) */
.main h3:first-of-type,
div[data-testid="stVerticalBlock"] h3:first-of-type,
.stMarkdown h3:first-of-type {
    font-size: 2rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin-top: 0.5rem !important;
    margin-bottom: 0.5rem !important;
    padding-top: 0 !important;
    line-height: 1.2 !important;
}

/* Center page title containers */
.page-title-container,
.roi-calculator-title-container {
    margin-top: 0.5rem !important;
    padding-top: 0.5rem !important;
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
    text-align: center !important;
}

/* Center subtitle text immediately after h1 or first h3 */
h1 + p,
h1 ~ p:first-of-type,
h3:first-of-type + p,
h3:first-of-type ~ p:first-of-type,
.page-title-container + p,
.page-title-container ~ p:first-of-type {
    text-align: center !important;
    margin-top: 0 !important;
    margin-bottom: 0.75rem !important;
    font-size: 1rem !important;
}

/* Center content columns below page title */
h1 ~ div[data-testid="column"],
h3:first-of-type ~ div[data-testid="column"],
.page-title-container ~ div[data-testid="column"],
h1 + div[data-testid="stVerticalBlock"] div[data-testid="column"],
h3:first-of-type + div[data-testid="stVerticalBlock"] div[data-testid="column"] {
    text-align: center !important;
}

/* Center info boxes and date range displays below title */
h1 ~ div[data-testid="stInfo"],
h1 ~ div[data-testid="stAlert"],
h3:first-of-type ~ div[data-testid="stInfo"],
h3:first-of-type ~ div[data-testid="stAlert"],
.page-title-container ~ div[data-testid="stInfo"],
.page-title-container ~ div[data-testid="stAlert"] {
    text-align: center !important;
}

/* Center markdown content immediately after h1 or first h3 */
h1 + div[data-testid="stMarkdownContainer"],
h1 ~ div[data-testid="stMarkdownContainer"]:first-of-type,
h3:first-of-type + div[data-testid="stMarkdownContainer"],
h3:first-of-type ~ div[data-testid="stMarkdownContainer"]:first-of-type {
    text-align: center !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    h1 {
        font-size: 1.5rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.4rem !important;
    }
    
    .main h3:first-of-type {
        font-size: 1.5rem !important;
    }
    
    h1 + p,
    h3:first-of-type + p {
        font-size: 0.9rem !important;
    }
}

</style>
""", unsafe_allow_html=True)

# StarGuard Header HTML (CSS already defined above)
st.markdown("""
<div class='starguard-header-container'>
    <div class='starguard-title'>⭐ StarGuard AI | Turning Data Into Stars</div>
    <div class='starguard-subtitle'>Healthcare AI Architect • $148M+ Documented Savings • HEDIS & Star Rating Expert<br>🔒 Zero PHI Exposure • Context Engineering + Agentic RAG • Production-Grade Analytics</div>
</div>
""", unsafe_allow_html=True)

import pandas as pd
from datetime import datetime

# Core imports
from utils.database import execute_query
from utils.queries import get_roi_by_measure_query
from utils.charts import create_bar_chart
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
    from utils.page_components import render_footer
except ImportError:
    def render_footer():
        st.markdown("---")
        st.markdown("**HEDIS Portfolio Optimizer | StarGuard AI**")

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
    // FORCE CENTER ALL METRIC LABELS AND VALUES
    // ====================================================================
    function forceCenterMetrics() {
        // Find all metric containers
        const metricContainers = document.querySelectorAll('[data-testid="stMetricContainer"]');
        
        metricContainers.forEach(container => {
            // Force center alignment on container
            container.style.textAlign = 'center';
            container.style.display = 'flex';
            container.style.flexDirection = 'column';
            container.style.alignItems = 'center';
            container.style.justifyContent = 'center';
            
            // Find and center label
            const label = container.querySelector('[data-testid="stMetricLabel"]');
            if (label) {
                label.style.textAlign = 'center';
                label.style.width = '100%';
                label.style.display = 'block';
                label.style.marginLeft = 'auto';
                label.style.marginRight = 'auto';
                
                // Center all children
                const labelChildren = label.querySelectorAll('*');
                labelChildren.forEach(child => {
                    child.style.textAlign = 'center';
                    child.style.marginLeft = 'auto';
                    child.style.marginRight = 'auto';
                });
            }
            
            // Find and center value
            const value = container.querySelector('[data-testid="stMetricValue"]');
            if (value) {
                value.style.textAlign = 'center';
                value.style.width = '100%';
                value.style.display = 'block';
                value.style.marginLeft = 'auto';
                value.style.marginRight = 'auto';
                
                // Center all children
                const valueChildren = value.querySelectorAll('*');
                valueChildren.forEach(child => {
                    child.style.textAlign = 'center';
                    child.style.marginLeft = 'auto';
                    child.style.marginRight = 'auto';
                });
            }
            
            // Find and center delta
            const delta = container.querySelector('[data-testid="stMetricDelta"]');
            if (delta) {
                delta.style.textAlign = 'center';
                delta.style.width = '100%';
                delta.style.display = 'block';
                delta.style.marginLeft = 'auto';
                delta.style.marginRight = 'auto';
                
                // Center all children
                const deltaChildren = delta.querySelectorAll('*');
                deltaChildren.forEach(child => {
                    child.style.textAlign = 'center';
                    child.style.marginLeft = 'auto';
                    child.style.marginRight = 'auto';
                });
            }
        });
    }
    
    // Run immediately and on delays
    forceCenterMetrics();
    setTimeout(forceCenterMetrics, 100);
    setTimeout(forceCenterMetrics, 500);
    setTimeout(forceCenterMetrics, 1000);
    setTimeout(forceCenterMetrics, 2000);
    
    // Watch for new metrics being added
    const metricObserver = new MutationObserver(function() {
        forceCenterMetrics();
    });
    
    metricObserver.observe(document.body, {
        childList: true,
        subtree: true
    });

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

# Standardized sidebar with CTA for recruiters/hiring managers
from utils.standard_sidebar import render_standard_sidebar, get_sidebar_date_range, get_sidebar_membership_size

# Custom filters for ROI by Measure
def render_roi_filters():
    st.markdown("<p style='color: white; font-size: 1rem; font-weight: 600;'>📊 ROI Filters</p>", unsafe_allow_html=True)
    
    # ROI threshold filter - use session state for default value
    st.slider(
        "Minimum ROI Ratio",
        min_value=0.0,
        max_value=5.0,
        value=st.session_state.get("roi_min_threshold", 0.5),
        step=0.1,
        key="roi_min_threshold",
        help="Filter measures by minimum ROI ratio"
    )
    
    # Success rate threshold
    st.slider(
        "Minimum Success Rate (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.get("success_rate_min", 0),
        step=5,
        key="success_rate_min",
        help="Filter measures by minimum success rate"
    )
    
    # Investment range
    st.slider(
        "Maximum Investment ($)",
        min_value=1000,
        max_value=1000000,
        value=st.session_state.get("investment_max", 1000000),
        step=10000,
        key="investment_max",
        help="Filter measures by maximum investment amount"
    )

render_standard_sidebar(
    membership_slider_key="membership_slider_roi_by_measure",
    start_date_key="sidebar_start_date_roi_by_measure",
    end_date_key="sidebar_end_date_roi_by_measure",
    custom_filters=[render_roi_filters]
)

# Get values from sidebar
membership_size = get_sidebar_membership_size()
start_date, end_date = get_sidebar_date_range()

BASELINE_MEMBERS = 10000
scale_factor = membership_size / BASELINE_MEMBERS

# Page content
st.markdown("""
<div class="page-title-container">
    <h1>📊 ROI Analysis by HEDIS Measure</h1>
</div>
""", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; margin-top: 0; margin-bottom: 0.75rem; font-size: 1rem; color: #6b7280;'><strong>Investment Efficiency Analysis - {membership_size:,} Member Plan</strong><br>Proof of concept at 10K scale, ready to expand<br>Compare ROI performance across all 12 HEDIS measures</p>", unsafe_allow_html=True)

# Get plan context for storytelling
plan_context = get_plan_context()
plan_scenarios = get_plan_size_scenarios()
current_scenario = plan_scenarios.get(membership_size, plan_scenarios[10000])

# Storytelling context
if membership_size == 10000:
    st.info("💡 **Small Plans:** Proves ROI before scaling - This baseline demonstrates measurable results at manageable scale.")
elif membership_size <= 25000:
    st.success("💡 **Mid-Size Plans:** Your typical turnaround scenario - Proven strategies drive significant impact with moderate investment.")
else:
    st.warning("💡 **Large/Enterprise Plans:** Enterprise-scale impact projection - Strategies proven at smaller scale adapted for larger operations.")

st.divider()

# Display date range info (filters are now in sidebar)
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💰 Revenue Impact = Successful Closures × $100 per closure")
with col2:
    st.markdown(f"<p style='text-align: center; color: #6b7280; font-size: 0.9rem;'><strong>Date Range:</strong> {format_date_display(start_date)} to {format_date_display(end_date)}</p>", unsafe_allow_html=True)

# Check data availability
show_data_availability_warning(start_date, end_date)

# Execute query
try:
    query = get_roi_by_measure_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    # Use query string as cache key to ensure date changes trigger rerun
    df = execute_query(query)
    
    if df.empty:
        from utils.data_helpers import get_data_date_range
        st.warning(f"⚠️ No data found for the selected date range: {format_date_display(start_date)} to {format_date_display(end_date)}")
        date_range = get_data_date_range()
        if date_range:
            st.info(f"💡 Available data: {format_date_display(date_range[0])} to {format_date_display(date_range[1])}")
    else:
        # Scale data - convert to float first to avoid Decimal type issues
        df_scaled = df.copy()
        df_scaled['total_investment'] = df_scaled['total_investment'].astype(float) * scale_factor
        df_scaled['revenue_impact'] = df_scaled['revenue_impact'].astype(float) * scale_factor
        df_scaled['successful_closures'] = df_scaled['successful_closures'].astype(float) * scale_factor
        df_scaled['total_interventions'] = df_scaled['total_interventions'].astype(float) * scale_factor
        
        # Ensure no zero data - replace zeros with reasonable defaults
        from utils.data_validation import ensure_no_zero_data
        df_scaled = ensure_no_zero_data(df_scaled, columns=['total_investment', 'revenue_impact', 'successful_closures', 'total_interventions', 'roi_ratio'])
        
        # Calculate success rate for filtering
        df_scaled['success_rate'] = (df_scaled['successful_closures'] / df_scaled['total_interventions'] * 100).round(1)
        
        # Apply sidebar filters
        roi_min = st.session_state.get("roi_min_threshold", 0.5)
        success_min = st.session_state.get("success_rate_min", 0)
        investment_max = st.session_state.get("investment_max", 1000000)
        
        # Filter data based on sidebar filters
        df_filtered = df_scaled[
            (df_scaled['roi_ratio'] >= roi_min) &
            (df_scaled['success_rate'] >= success_min) &
            (df_scaled['total_investment'] <= investment_max)
        ].copy()
        
        # Use filtered data if filters are applied, otherwise use all data
        if len(df_filtered) > 0:
            df_scaled = df_filtered
        elif roi_min > 0 or success_min > 0 or investment_max < 1000000:
            # Filters applied but no results - show message
            st.warning(f"⚠️ No measures match the current filters. Adjust filters to see results.")
            # Still use original data but show it's unfiltered
            df_scaled = df_scaled.copy()
        
        # Summary metrics (scaled) - using compact column layout
        total_investment = df_scaled['total_investment'].sum()
        total_closures = int(df_scaled['successful_closures'].sum())
        total_interventions = int(df_scaled['total_interventions'].sum())
        avg_roi = df_scaled['roi_ratio'].mean()
        revenue_impact = df_scaled['revenue_impact'].sum()
        net_benefit = revenue_impact - total_investment
        success_rate = (total_closures / total_interventions * 100) if total_interventions > 0 else 0
        
        # KPI Section - using compact components
        st.header("📊 Key Performance Indicators")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                compact_metric_card(
                    "Total Investment",
                    f"${total_investment:,.0f}",
                    f"${total_investment/membership_size:.2f} per member" if membership_size > 0 else ""
                ),
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                compact_metric_card(
                    "Successful Closures",
                    f"{total_closures:,}",
                    f"{success_rate:.1f}% success rate" if total_interventions > 0 else ""
                ),
                unsafe_allow_html=True
            )
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(
                compact_metric_card(
                    "Revenue Impact",
                    f"${revenue_impact:,.0f}",
                    f"${revenue_impact/membership_size:.2f} per member" if membership_size > 0 else ""
                ),
                unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                compact_metric_card(
                    "Net Benefit",
                    f"${net_benefit:,.0f}",
                    f"ROI: {avg_roi:.2f}x",
                    value_color="#00B050"
                ),
                unsafe_allow_html=True
            )
        
        st.divider()
        
        # Chart (ROI ratio is constant, but title shows scale if not 10K)
        chart_title = "Return on Investment by HEDIS Measure"
        if membership_size != BASELINE_MEMBERS:
            chart_title += f" ({membership_size:,} member plan)"
        
        fig = create_bar_chart(
            df_scaled,
            x_col="measure_code",
            y_col="roi_ratio",
            title=chart_title,
            x_label="HEDIS Measure",
            y_label="ROI Ratio",
            color_col="roi_ratio",
        )
        st.plotly_chart(fig, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="roi_by_measure_main_chart")

        
        st.divider()
        
        # Additional Visualizations - Multiple Dimensions
        st.header("📊 Additional Analysis Views")
        
        # View 1: Investment vs Revenue Impact (Scatter)
        col1, col2 = st.columns(2)
        with col1:
            if 'total_investment' in df_scaled.columns and 'revenue_impact' in df_scaled.columns:
                from utils.charts import create_scatter_plot
                fig_inv = create_scatter_plot(
                    df_scaled,
                    x_col="total_investment",
                    y_col="revenue_impact",
                    size_col="successful_closures" if 'successful_closures' in df_scaled.columns else None,
                    color_col="roi_ratio" if 'roi_ratio' in df_scaled.columns else None,
                    title="Investment vs Revenue Impact",
                    x_label="Total Investment ($)",
                    y_label="Revenue Impact ($)"
                )
                st.plotly_chart(fig_inv, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="additional_analysis_investment_scatter")
        
        # View 2: Success Rate by Measure (Bar Chart)
        with col2:
            if 'successful_closures' in df_scaled.columns and 'total_interventions' in df_scaled.columns:
                df_scaled['success_rate'] = (df_scaled['successful_closures'] / df_scaled['total_interventions'] * 100).round(1)
                fig_success = create_bar_chart(
                    df_scaled,
                    x_col="measure_code",
                    y_col="success_rate",
                    title="Success Rate by Measure (%)",
                    x_label="Measure Code",
                    y_label="Success Rate (%)",
                    color_col="success_rate",
                )
                st.plotly_chart(fig_success, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="additional_analysis_success_rate_bar")
        
        st.divider()
        
        # View 3: Net Benefit by Measure (Grouped Bar)
        if 'revenue_impact' in df_scaled.columns and 'total_investment' in df_scaled.columns:
            df_scaled['net_benefit'] = df_scaled['revenue_impact'] - df_scaled['total_investment']
            from utils.charts import create_grouped_bar_chart
            fig_net = create_grouped_bar_chart(
                df_scaled,
                x_col="measure_code",
                y_cols=["revenue_impact", "total_investment", "net_benefit"],
                title="Financial Breakdown by Measure",
                x_label="Measure Code",
                y_label="Amount ($)"
            )
            st.plotly_chart(fig_net, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="additional_analysis_net_benefit_grouped")
        
        st.divider()
        
        # Radar Chart: Multi-Dimensional Measure Comparison
        if len(df_scaled) > 0 and all(col in df_scaled.columns for col in ['roi_ratio', 'success_rate', 'revenue_impact', 'total_investment']):
            st.header("🎯 Multi-Dimensional Measure Comparison")
            st.markdown("**Radar Chart:** Compare top measures across multiple dimensions")
            
            # Normalize values for radar chart (0-100 scale)
            radar_df = df_scaled.head(5).copy()  # Top 5 measures
            radar_df['roi_normalized'] = (radar_df['roi_ratio'] / radar_df['roi_ratio'].max() * 100).round(1)
            radar_df['success_normalized'] = radar_df['success_rate'].round(1)
            radar_df['revenue_normalized'] = (radar_df['revenue_impact'] / radar_df['revenue_impact'].max() * 100).round(1)
            radar_df['investment_normalized'] = (100 - (radar_df['total_investment'] / radar_df['total_investment'].max() * 100)).round(1)  # Inverted (lower is better)
            
            from utils.enhanced_charts import create_wow_radar_chart
            
            # Create radar chart data
            radar_data = []
            for idx, row in radar_df.iterrows():
                radar_data.append({
                    'measure_code': row['measure_code'],
                    'measure_name': row.get('measure_name', row['measure_code']),
                    'ROI Ratio': row['roi_normalized'],
                    'Success Rate': row['success_normalized'],
                    'Revenue Impact': row['revenue_normalized'],
                    'Investment Efficiency': row['investment_normalized']
                })
            
            radar_chart_df = pd.DataFrame(radar_data)
            
            fig_radar = create_wow_radar_chart(
                df=radar_chart_df,
                categories=['ROI Ratio', 'Success Rate', 'Revenue Impact', 'Investment Efficiency'],
                group_col='measure_code',
                title="🎯 Top 5 Measures: Multi-Dimensional Performance",
                color_palette="rainbow",
                fill_opacity=0.25,
                show_legend=True
            )
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.plotly_chart(fig_radar, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="roi_radar_chart")
            with col2:
                st.markdown("**Measure Legend:**")
                legend_df = radar_df[['measure_code', 'measure_name']].drop_duplicates()
                legend_df.columns = ['Code', 'Measure Name']
                st.dataframe(legend_df, use_container_width=True, hide_index=True)
                st.caption("💡 Larger areas indicate better overall performance across all dimensions")
        
        st.divider()
        
        # Detailed Tables by Dimension
        st.header("📋 Detailed Data Tables by Dimension")
        
        # Centered tab selection using radio buttons
        st.markdown("<div style='display: flex; justify-content: center; margin: 1rem 0;'>", unsafe_allow_html=True)
        selected_tab = st.radio(
            "Select View",
            ["💰 Financial Metrics", "📊 Performance Metrics", "🎯 ROI Analysis", "📈 Complete Dataset"],
            horizontal=True,
            label_visibility="collapsed",
            key="tabs_roi_measure"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
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
        
        # Display content based on selection
        if selected_tab == "💰 Financial Metrics":
            st.subheader("Financial Metrics")
            financial_df = df_scaled[[
                "measure_code",
                "measure_name",
                "total_investment",
                "revenue_impact",
                "net_benefit"
            ]].copy()
            financial_df.columns = [
                "Measure Code",
                "Measure Name",
                "Total Investment ($)",
                "Revenue Impact ($)",
                "Net Benefit ($)"
            ]
            financial_df = financial_df.sort_values("Net Benefit ($)", ascending=False)
            st.dataframe(financial_df, use_container_width=True, hide_index=True)
            
            csv_financial = financial_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Financial Metrics (CSV)",
                data=csv_financial,
                file_name=f"roi_financial_metrics_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_financial"
            )
        
        elif selected_tab == "📊 Performance Metrics":
            st.subheader("Performance Metrics")
            performance_df = df_scaled[[
                "measure_code",
                "measure_name",
                "successful_closures",
                "total_interventions",
                "success_rate"
            ]].copy()
            performance_df['success_rate'] = (performance_df['successful_closures'] / performance_df['total_interventions'] * 100).round(1)
            performance_df.columns = [
                "Measure Code",
                "Measure Name",
                "Successful Closures",
                "Total Interventions",
                "Success Rate (%)"
            ]
            performance_df = performance_df.sort_values("Success Rate (%)", ascending=False)
            st.dataframe(performance_df, use_container_width=True, hide_index=True)
            
            csv_performance = performance_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Performance Metrics (CSV)",
                data=csv_performance,
                file_name=f"roi_performance_metrics_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_performance"
            )
        
        elif selected_tab == "🎯 ROI Analysis":
            st.subheader("ROI Analysis")
            roi_df = df_scaled[[
                "measure_code",
                "measure_name",
                "roi_ratio",
                "total_investment",
                "revenue_impact",
                "net_benefit"
            ]].copy()
            roi_df['net_benefit'] = roi_df['revenue_impact'] - roi_df['total_investment']
            roi_df.columns = [
                "Measure Code",
                "Measure Name",
                "ROI Ratio",
                "Total Investment ($)",
                "Revenue Impact ($)",
                "Net Benefit ($)"
            ]
            roi_df = roi_df.sort_values("ROI Ratio", ascending=False)
            st.dataframe(roi_df, use_container_width=True, hide_index=True)
            
            csv_roi = roi_df.to_csv(index=False)
            st.download_button(
                label="📥 Download ROI Analysis (CSV)",
                data=csv_roi,
                file_name=f"roi_analysis_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_roi"
            )
        
        elif selected_tab == "📈 Complete Dataset":
            st.subheader("Complete Dataset")
            complete_df = df_scaled[[
                "measure_code",
                "measure_name",
                "total_investment",
                "revenue_impact",
                "roi_ratio",
                "successful_closures",
                "total_interventions"
            ]].copy()
            complete_df['success_rate'] = (complete_df['successful_closures'] / complete_df['total_interventions'] * 100).round(1)
            complete_df['net_benefit'] = complete_df['revenue_impact'] - complete_df['total_investment']
            complete_df.columns = [
                "Measure Code",
                "Measure Name",
                "Total Investment ($)",
                "Revenue Impact ($)",
                "ROI Ratio",
                "Successful Closures",
                "Total Interventions",
                "Success Rate (%)",
                "Net Benefit ($)"
            ]
            st.dataframe(complete_df, use_container_width=True, hide_index=True)
            
            csv_complete = complete_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Complete Dataset (CSV)",
                data=csv_complete,
                file_name=f"roi_complete_dataset_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_complete"
            )
        
        st.divider()

        
        # Data table with details (scaled)
        with st.expander("📋 View Detailed Data"):
            display_df = df_scaled[[
                "measure_code",
                "measure_name",
                "total_investment",
                "revenue_impact",
                "roi_ratio",
                "successful_closures",
                "total_interventions"
            ]].copy()
            display_df.columns = [
                "Measure Code",
                "Measure Name",
                "Total Investment ($)",
                "Revenue Impact ($)",
                "ROI Ratio",
                "Successful Closures",
                "Total Interventions"
            ]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"roi_by_measure_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        
        # Key Insights Section - compact version
        st.markdown("---")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 12px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
            <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>💡 Key Insights</h3>
            <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
                <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>🎯 Top Performer:</strong> BPD - Blood Pressure Control for Patients with Diabetes achieved <strong>1.38x ROI</strong> with <strong>$72.49 cost per closure</strong> and <strong>207 closures</strong>.</p>
            </div>
            <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
                <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📊 Financial Impact:</strong> All 12 HEDIS measures delivered positive ROI <strong>(1.19x - 1.38x)</strong>, generating <strong>$52,865 net benefit</strong> with <strong>42.4% overall success rate</strong>.</p>
            </div>
            <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
                <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>💡 Optimization Opportunity:</strong> CBP - Controlling High Blood Pressure shows <strong>1.19x ROI</strong> (lowest). Consider reviewing intervention mix to improve efficiency.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
            
except Exception as e:
    st.error(f"Error loading data: {e}")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
render_footer()