"""
What-If Scenario Modeler - Desktop Version
Interactive tool for healthcare managers to model budget and FTE scenarios
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io

# Check for openpyxl availability for Excel export
try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    openpyxl = None

from utils.database import show_db_status
from utils.scenario_modeler import ScenarioModeler

# ============================================================================
# ADDITIONAL JAVASCRIPT FIX FOR PERFORMANCE DASHBOARD EMOJI
# ============================================================================
st.set_page_config(
    page_title="What-If Scenario Modeler - HEDIS Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto"  # Auto: Let Streamlit decide based on screen size (iOS Safari optimized)
)
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

from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# Page configuration

# Aggressive spacing reduction
st.markdown("""
<style>
/* Aggressive spacing reduction */
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

.stMarkdown {
    margin: 0.2rem 0 !important;
}

.stPlotlyChart {
    margin: 0.3rem 0 !important;
}

hr {
    margin: 0.3rem 0 !important;
}

/* Sidebar spacing */
[data-testid="stSidebar"] .element-container {
    margin: 0.2rem 0 !important;
    padding: 0.1rem 0 !important;
}

/* Ensure header is at very top */
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

/* Sidebar button */
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

# Custom filters for What-If Scenario Modeler
def render_scenario_filters():
    st.markdown("<p style='color: white; font-size: 1rem; font-weight: 600;'>⚙️ Scenario Parameters</p>", unsafe_allow_html=True)
    
    # Investment multiplier range - use session state for default value
    st.slider(
        "Min Investment Multiplier",
        min_value=0.5,
        max_value=1.5,
        value=st.session_state.get("scenario_inv_min", 0.7),
        step=0.1,
        key="scenario_inv_min",
        help="Minimum investment multiplier for random scenarios"
    )
    
    st.slider(
        "Max Investment Multiplier",
        min_value=1.0,
        max_value=2.5,
        value=st.session_state.get("scenario_inv_max", 1.8),
        step=0.1,
        key="scenario_inv_max",
        help="Maximum investment multiplier for random scenarios"
    )
    
    # Success rate boost range
    st.slider(
        "Min Success Rate Boost (%)",
        min_value=0,
        max_value=20,
        value=st.session_state.get("scenario_success_min", 0),
        step=5,
        key="scenario_success_min",
        help="Minimum success rate boost for random scenarios"
    )
    
    st.slider(
        "Max Success Rate Boost (%)",
        min_value=10,
        max_value=50,
        value=st.session_state.get("scenario_success_max", 30),
        step=5,
        key="scenario_success_max",
        help="Maximum success rate boost for random scenarios"
    )
    
    # Number of scenarios
    st.slider(
        "Number of Scenarios",
        min_value=3,
        max_value=10,
        value=st.session_state.get("scenario_count", 5),
        step=1,
        key="scenario_count",
        help="Number of random scenarios to generate"
    )
    # Note: Separator is handled by render_standard_sidebar, don't add duplicate

render_standard_sidebar(
    membership_slider_key="membership_slider_scenario",
    start_date_key="sidebar_start_date_scenario",
    end_date_key="sidebar_end_date_scenario",
    custom_filters=[render_scenario_filters]
)

# Get values from sidebar
membership_size = get_sidebar_membership_size()
start_date, end_date = get_sidebar_date_range()

BASELINE_MEMBERS = 10000
scale_factor = membership_size / BASELINE_MEMBERS


# Page content

# Page content
st.markdown("""
<div class="page-title-container">
    <h1>📊 What-If Scenario Modeler</h1>
</div>
""", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-top: 0; margin-bottom: 0.75rem; font-size: 1rem;'>Model different intervention strategies and their projected outcomes</p>", unsafe_allow_html=True)

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Scenario Modeling:** Test different investment strategies and see projected ROI.")
with col2:
    st.markdown(f"<p style='text-align: center;'><strong>Date Range:</strong> {format_date_display(start_date)} to {format_date_display(end_date)}</p>", unsafe_allow_html=True)

# Check data availability
show_data_availability_warning(start_date, end_date)

# Initialize session state for scenarios
if 'scenarios_generated' not in st.session_state:
    st.session_state.scenarios_generated = False
if 'scenario_results' not in st.session_state:
    st.session_state.scenario_results = []
if 'best_scenario' not in st.session_state:
    st.session_state.best_scenario = None
if 'auto_generated' not in st.session_state:
    st.session_state.auto_generated = False

# Enhanced What-If Scenario Visualizations
st.header("📊 Scenario Modeling")

# Get baseline data
from utils.queries import get_roi_by_measure_query
from utils.enhanced_charts import create_wow_bar_chart, create_wow_scatter, create_wow_area_chart
import pandas as pd

baseline_query = get_roi_by_measure_query(
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d")
)
baseline_df = execute_query(baseline_query)

if not baseline_df.empty:
    # Scale baseline data
    baseline_df_scaled = baseline_df.copy()
    baseline_df_scaled['total_investment'] = baseline_df_scaled['total_investment'].astype(float) * scale_factor
    baseline_df_scaled['revenue_impact'] = baseline_df_scaled['revenue_impact'].astype(float) * scale_factor
    
    # Calculate success_rate from available columns
    baseline_df_scaled['successful_closures'] = baseline_df_scaled['successful_closures'].astype(float)
    baseline_df_scaled['total_interventions'] = baseline_df_scaled['total_interventions'].astype(float)
    baseline_df_scaled['success_rate'] = (
        (baseline_df_scaled['successful_closures'] / baseline_df_scaled['total_interventions'].replace(0, 1)) * 100
    ).fillna(0).clip(0, 100)
    
    baseline_df_scaled['net_benefit'] = baseline_df_scaled['revenue_impact'] - baseline_df_scaled['total_investment']
    
    # Ensure no zero data - add minimum values if needed
    baseline_df_scaled['total_investment'] = baseline_df_scaled['total_investment'].replace(0, baseline_df_scaled['total_investment'].median())
    baseline_df_scaled['revenue_impact'] = baseline_df_scaled['revenue_impact'].replace(0, baseline_df_scaled['revenue_impact'].median())
    baseline_df_scaled['success_rate'] = baseline_df_scaled['success_rate'].replace(0, baseline_df_scaled['success_rate'].median())
    
    # Calculate baseline measures count (needed for explanations)
    baseline_measures = len(baseline_df_scaled)
    
    # Generate random scenarios - auto-generate on first load BEFORE displaying metrics
    import random
    import numpy as np
    
    # Auto-generate on first load if not already generated - generate immediately
    if not st.session_state.auto_generated and not st.session_state.scenario_results:
        st.session_state.scenarios_generated = True
        st.session_state.auto_generated = True
        # Generate immediately (don't wait for rerun)
    
    # Generate scenarios if requested or auto-generated
    if (st.session_state.scenarios_generated and not st.session_state.scenario_results) or (not st.session_state.scenario_results and not st.session_state.auto_generated):
        # Get scenario count from sidebar or default
        scenario_count = st.session_state.get('scenario_count', 5)
        inv_min = st.session_state.get('scenario_inv_min', 0.7)
        inv_max = st.session_state.get('scenario_inv_max', 1.8)
        success_min = st.session_state.get('scenario_success_min', 0)
        success_max = st.session_state.get('scenario_success_max', 30)
        
        # Generate scenarios
        scenario_names = [
            "Aggressive Investment",
            "Balanced Growth",
            "Conservative Approach",
            "High-Risk High-Reward",
            "Optimized Efficiency",
            "Strategic Focus",
            "Rapid Scale",
            "Quality First",
            "Cost Optimized",
            "Maximum Impact"
        ][:scenario_count]
        
        for i, name in enumerate(scenario_names):
            # Random parameters using sidebar filter ranges
            inv_mult = random.uniform(inv_min, inv_max)
            success_boost = random.uniform(success_min, success_max)
            focus_measure = random.choice(["All Measures"] + baseline_df_scaled['measure_code'].head(5).tolist())
            
            # Calculate scenario
            test_df = baseline_df_scaled.copy()
            if focus_measure != "All Measures":
                test_df.loc[test_df['measure_code'] == focus_measure, 'total_investment'] *= inv_mult
                test_df.loc[test_df['measure_code'] == focus_measure, 'success_rate'] = (
                    test_df.loc[test_df['measure_code'] == focus_measure, 'success_rate'] + success_boost
                ).clip(0, 100)
            else:
                test_df['total_investment'] *= inv_mult
                test_df['success_rate'] = (test_df['success_rate'] + success_boost).clip(0, 100)
            
            # Recalculate metrics
            baseline_success_rate = baseline_df_scaled['success_rate'].replace(0, 1)
            test_df['revenue_impact'] = test_df['revenue_impact'] * (test_df['success_rate'] / baseline_success_rate).replace([float('inf'), float('-inf')], 0).fillna(1)
            test_df['net_benefit'] = test_df['revenue_impact'] - test_df['total_investment']
            test_df['roi_ratio'] = (test_df['revenue_impact'] / test_df['total_investment']).replace([float('inf'), float('-inf')], 0).fillna(0)
            
            # Ensure no zero values in results
            total_inv = max(test_df['total_investment'].sum(), 1000)  # Minimum $1000
            total_rev = max(test_df['revenue_impact'].sum(), 1000)   # Minimum $1000
            net_ben = total_rev - total_inv
            avg_roi = max(test_df['roi_ratio'].mean(), 0.1)  # Minimum 0.1x ROI
            
            # Store scenario results
            scenario_result = {
                'strategy_name': name,
                'investment_multiplier': inv_mult,
                'success_rate_boost': success_boost,
                'focus_measure': focus_measure,
                'total_investment': total_inv,
                'total_revenue': total_rev,
                'net_benefit': net_ben,
                'roi_ratio': avg_roi,
                'scenario_df': test_df.copy()
            }
            st.session_state.scenario_results.append(scenario_result)
        
        # Find best scenario by ROI
        if st.session_state.scenario_results:
            st.session_state.best_scenario = max(st.session_state.scenario_results, key=lambda x: x['roi_ratio'])
    
    # If no scenarios exist yet, generate a default one immediately for display
    if not st.session_state.scenario_results:
        # Generate a single default reasonable scenario
        default_inv_mult = 1.25  # 25% increase
        default_success_boost = 15.0  # 15% boost
        default_focus = "All Measures"
        
        test_df = baseline_df_scaled.copy()
        test_df['total_investment'] *= default_inv_mult
        test_df['success_rate'] = (test_df['success_rate'] + default_success_boost).clip(0, 100)
        
        baseline_success_rate = baseline_df_scaled['success_rate'].replace(0, 1)
        test_df['revenue_impact'] = test_df['revenue_impact'] * (test_df['success_rate'] / baseline_success_rate).replace([float('inf'), float('-inf')], 0).fillna(1)
        test_df['net_benefit'] = test_df['revenue_impact'] - test_df['total_investment']
        test_df['roi_ratio'] = (test_df['revenue_impact'] / test_df['total_investment']).replace([float('inf'), float('-inf')], 0).fillna(0)
        
        # Ensure no zeros
        total_inv = max(test_df['total_investment'].sum(), 1000)
        total_rev = max(test_df['revenue_impact'].sum(), 1000)
        net_ben = total_rev - total_inv
        avg_roi = max(test_df['roi_ratio'].mean(), 0.1)
        
        # Create default scenario
        default_scenario = {
            'strategy_name': "Balanced Growth (Default)",
            'investment_multiplier': default_inv_mult,
            'success_rate_boost': default_success_boost,
            'focus_measure': default_focus,
            'total_investment': total_inv,
            'total_revenue': total_rev,
            'net_benefit': net_ben,
            'roi_ratio': avg_roi,
            'scenario_df': test_df.copy()
        }
        st.session_state.scenario_results = [default_scenario]
        st.session_state.best_scenario = default_scenario
        st.session_state.scenarios_generated = True
    
    # Add buttons for scenario management (after generation logic)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎲 Generate Random Scenario", type="primary", use_container_width=True):
            st.session_state.scenarios_generated = True
            st.session_state.scenario_results = []
            st.rerun()
    with col2:
        if st.button("🔄 Regenerate All Scenarios", use_container_width=True):
            st.session_state.scenarios_generated = True
            st.session_state.scenario_results = []
            st.rerun()
    with col3:
        if st.button("🗑️ Clear Scenarios", use_container_width=True):
            st.session_state.scenarios_generated = False
            st.session_state.scenario_results = []
            st.session_state.best_scenario = None
            st.session_state.auto_generated = False
            st.rerun()
    
    # Display Scenario Analysis Metrics (scenarios always exist now due to default generation)
    st.subheader("📊 Scenario Analysis Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        scenario_count = len(st.session_state.scenario_results) if st.session_state.scenario_results else 1
        st.metric("Scenarios Modeled", scenario_count)
    with col2:
        if st.session_state.best_scenario:
            best_roi = max(st.session_state.best_scenario.get('roi_ratio', 0), 0.1)
            st.metric("Best ROI Projection", f"{best_roi:.2f}x")
        else:
            # Fallback (shouldn't happen, but safety check)
            best_roi = max(baseline_df_scaled['roi_ratio'].mean() * 1.2, 0.1)
            st.metric("Best ROI Projection", f"{best_roi:.2f}x")
    with col3:
        if st.session_state.best_scenario:
            strategy = st.session_state.best_scenario.get('strategy_name', 'N/A')
            display_strategy = strategy[:20] + "..." if len(strategy) > 20 else strategy
            st.metric("Recommended Strategy", display_strategy)
        else:
            # Fallback (shouldn't happen, but safety check)
            st.metric("Recommended Strategy", "Balanced Growth")
    
    st.divider()
    
    # Display generated scenarios if available
    if st.session_state.scenario_results:
        st.subheader("🎲 Generated Scenarios")
        
        # Explanation of generated scenarios
        num_scenarios = len(st.session_state.scenario_results)
        st.info(f"""
        **📊 Generated {num_scenarios} Scenarios:** These scenarios were created using random parameters within your sidebar filter ranges.
        Each scenario applies different investment multipliers and success rate boosts to demonstrate various strategic approaches.
        All scenarios are based on {baseline_measures} measures from your selected date range.
        """)
        
        scenario_display = pd.DataFrame([
            {
                'Strategy': s['strategy_name'],
                'Investment Mult': f"{s['investment_multiplier']:.2f}x",
                'Success Boost': f"+{s['success_rate_boost']:.1f}%",
                'Focus': s['focus_measure'],
                'ROI': f"{s['roi_ratio']:.2f}x",
                'Net Benefit': f"${s['net_benefit']:,.0f}"
            }
            for s in st.session_state.scenario_results
        ])
        st.dataframe(scenario_display, use_container_width=True, hide_index=True)
        
        if st.session_state.best_scenario:
            st.success(f"🏆 **Best Strategy:** {st.session_state.best_scenario['strategy_name']} "
                      f"(ROI: {st.session_state.best_scenario['roi_ratio']:.2f}x, "
                      f"Net Benefit: ${st.session_state.best_scenario['net_benefit']:,.0f})")
        
        # Visual comparison of all scenarios
        st.subheader("📊 Scenario Comparison")
        scenario_comparison_df = pd.DataFrame([
            {
                'Strategy': s['strategy_name'],
                'ROI Ratio': s['roi_ratio'],
                'Net Benefit': s['net_benefit'] / 1000,  # Scale for better visualization
                'Total Investment': s['total_investment'] / 1000
            }
            for s in st.session_state.scenario_results
        ])
        
        # ROI Comparison Bar Chart
        fig_scenarios = create_wow_bar_chart(
            df=scenario_comparison_df,
            x_col="Strategy",
            y_col="ROI Ratio",
            title="Generated Scenarios: ROI Comparison",
            x_label="Strategy",
            y_label="ROI Ratio",
            color_palette="rainbow"
        )
        st.plotly_chart(fig_scenarios, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="scenarios_roi_comparison")
        
        # Net Benefit Scatter
        fig_scenarios_scatter = create_wow_scatter(
            df=scenario_comparison_df,
            x_col="Total Investment",
            y_col="Net Benefit",
            size_col="ROI Ratio",
            title="Investment vs Net Benefit: All Scenarios",
            x_label="Total Investment ($K)",
            y_label="Net Benefit ($K)",
            color_palette="sunset",
            marker_shape="star",
            show_trendline=True
        )
        st.plotly_chart(fig_scenarios_scatter, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="scenarios_scatter")
        
        st.divider()
    
    # User prompt for scenario generation
    if not st.session_state.scenarios_generated:
        st.info("""
        💡 **Get Started:** Click "🎲 Generate Random Scenario" above to see example scenarios.
        
        **Tip:** Use the sidebar filters to customize scenario parameters. All filtering is done in the sidebar to avoid conflicts.
        """)
    
    # Summary Results Section - Always show when data is available
    st.subheader("📊 Scenario Summary Results")
    
    # Calculate baseline summary
    baseline_total_inv = max(baseline_df_scaled['total_investment'].sum(), 1000)
    baseline_total_rev = max(baseline_df_scaled['revenue_impact'].sum(), 1000)
    baseline_net = baseline_total_rev - baseline_total_inv
    baseline_roi = max(baseline_df_scaled['roi_ratio'].mean(), 0.1)
    baseline_success = max(baseline_df_scaled['success_rate'].mean(), 1.0)
    # baseline_measures already defined earlier after data scaling
    
    # Display summary metrics with explanations
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Total Measures Analyzed",
            f"{baseline_measures}",
            help=f"Number of HEDIS measures included in the analysis based on selected date range"
        )
    with col2:
        st.metric(
            "Baseline Total Investment",
            f"${baseline_total_inv:,.0f}",
            help=f"Total investment across all {baseline_measures} measures"
        )
    with col3:
        st.metric(
            "Baseline Revenue Impact",
            f"${baseline_total_rev:,.0f}",
            help=f"Total revenue impact from successful closures across all measures"
        )
    with col4:
        st.metric(
            "Baseline Net Benefit",
            f"${baseline_net:,.0f}",
            help=f"Net benefit (Revenue - Investment) for baseline scenario"
        )
    
    st.divider()
    
    # Additional baseline metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Baseline Average ROI",
            f"{baseline_roi:.2f}x",
            help=f"Average ROI ratio across all {baseline_measures} measures"
        )
    with col2:
        st.metric(
            "Baseline Success Rate",
            f"{baseline_success:.1f}%",
            help=f"Average success rate (successful closures / total interventions) across all measures"
        )
    with col3:
        baseline_closures = max(int(baseline_df_scaled['successful_closures'].sum()), 1)
        st.metric(
            "Total Successful Closures",
            f"{baseline_closures:,}",
            help=f"Total number of successful gap closures across all measures"
        )
    
    st.markdown("""
    <div style='background: #f0f9ff; border-left: 4px solid #3b82f6; padding: 12px 16px; margin: 16px 0; border-radius: 6px;'>
        <p style='color: #1e40af; font-size: 0.9rem; line-height: 1.5; margin: 0;'>
            <strong>📊 Customize Scenarios:</strong> Use the sidebar filters to adjust scenario parameters. 
            Click "🎲 Generate Random Scenario" to create scenarios based on your filter settings, or "🔄 Regenerate" to create new scenarios with the same parameters.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate custom scenario using sidebar filter values (for comparison)
    # Use midpoint of sidebar filter ranges as default custom scenario
    custom_inv_mult = (st.session_state.get("scenario_inv_min", 0.7) + st.session_state.get("scenario_inv_max", 1.8)) / 2
    custom_success_boost = (st.session_state.get("scenario_success_min", 0) + st.session_state.get("scenario_success_max", 30)) / 2
    
    scenario_df = baseline_df_scaled.copy()
    scenario_df['total_investment'] *= custom_inv_mult
    scenario_df['success_rate'] = (scenario_df['success_rate'] + custom_success_boost).clip(0, 100)
    
    # Recalculate revenue impact based on new success rate
    baseline_success_rate = baseline_df_scaled['success_rate'].replace(0, 1)
    scenario_df['revenue_impact'] = scenario_df['revenue_impact'] * (scenario_df['success_rate'] / baseline_success_rate).replace([float('inf'), float('-inf')], 0).fillna(1)
    scenario_df['net_benefit'] = scenario_df['revenue_impact'] - scenario_df['total_investment']
    scenario_df['roi_ratio'] = (scenario_df['revenue_impact'] / scenario_df['total_investment']).replace([float('inf'), float('-inf')], 0).fillna(0)
    
    # Ensure no zeros
    scenario_total_inv = max(scenario_df['total_investment'].sum(), 1000)
    scenario_total_rev = max(scenario_df['revenue_impact'].sum(), 1000)
    scenario_net = scenario_total_rev - scenario_total_inv
    scenario_roi = max(scenario_df['roi_ratio'].mean(), 0.1)
    scenario_success = max(scenario_df['success_rate'].mean(), 1.0)
    
    # Display Custom Scenario Summary (based on sidebar filters)
    st.subheader("⚙️ Custom Scenario Results")
    st.caption(f"Based on sidebar filter settings: Investment Multiplier = {custom_inv_mult:.2f}x, Success Rate Boost = +{custom_success_boost:.1f}%")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Scenario Total Investment",
            f"${scenario_total_inv:,.0f}",
            f"${scenario_total_inv - baseline_total_inv:,.0f}",
            help=f"Total investment with {custom_inv_mult:.2f}x multiplier applied"
        )
    with col2:
        st.metric(
            "Scenario Revenue Impact",
            f"${scenario_total_rev:,.0f}",
            f"${scenario_total_rev - baseline_total_rev:,.0f}",
            help=f"Revenue impact with {custom_success_boost:.1f}% success rate boost"
        )
    with col3:
        st.metric(
            "Scenario Net Benefit",
            f"${scenario_net:,.0f}",
            f"${scenario_net - baseline_net:,.0f}",
            help=f"Net benefit difference from baseline scenario"
        )
    with col4:
        st.metric(
            "Scenario Average ROI",
            f"{scenario_roi:.2f}x",
            f"{scenario_roi - baseline_roi:.2f}x",
            help=f"Average ROI ratio with scenario parameters applied"
        )
    
    st.divider()
    
    # Comparison Visualizations
    st.subheader("📈 Baseline vs Scenario Comparison")
    
    # Combine baseline and scenario for comparison
    comparison_data = []
    for measure in baseline_df_scaled['measure_code'].head(10):
        baseline_row = baseline_df_scaled[baseline_df_scaled['measure_code'] == measure].iloc[0]
        scenario_row = scenario_df[scenario_df['measure_code'] == measure].iloc[0]
        
        comparison_data.append({
            'measure_code': measure,
            'Baseline ROI': baseline_row['roi_ratio'],
            'Scenario ROI': scenario_row['roi_ratio'],
            'Baseline Net Benefit': baseline_row['net_benefit'],
            'Scenario Net Benefit': scenario_row['net_benefit']
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # ROI Comparison Bar Chart
    fig_comparison = create_wow_bar_chart(
        df=comparison_df.melt(id_vars=['measure_code'], value_vars=['Baseline ROI', 'Scenario ROI'], var_name='Type', value_name='ROI'),
        x_col="measure_code",
        y_col="ROI",
        color_col="Type",
        title="ROI Comparison: Baseline vs Scenario",
        x_label="Measure Code",
        y_label="ROI Ratio",
        color_palette="gradient_purple",
        show_values=True
    )
    st.plotly_chart(fig_comparison, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="scenario_roi_comparison")
    
    st.divider()
    
    # Net Benefit Comparison Scatter
    st.subheader("💰 Net Benefit Impact Analysis")
    fig_scatter = create_wow_scatter(
        df=comparison_df,
        x_col="Baseline Net Benefit",
        y_col="Scenario Net Benefit",
        title="Net Benefit: Baseline vs Scenario",
        x_label="Baseline Net Benefit ($)",
        y_label="Scenario Net Benefit ($)",
        color_palette="ocean",
        marker_shape="diamond",
        show_trendline=True
    )
    st.plotly_chart(fig_scatter, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="scenario_net_benefit_scatter")
else:
    st.info("📊 No data available for scenario modeling. Please adjust filters or check data availability.")


# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
render_footer()
