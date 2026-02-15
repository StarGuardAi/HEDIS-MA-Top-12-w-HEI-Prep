"""
Comprehensive ROI Calculator - Desktop Version
Calculate quality bonus impact, Star Rating financial impact, and net ROI
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io
import time
import json

from utils.database import show_db_status, execute_query
from utils.roi_calculator import ROICalculator
from utils.queries import get_portfolio_summary_query

# ============================================================================
# ADDITIONAL JAVASCRIPT FIX FOR PERFORMANCE DASHBOARD EMOJI
# ============================================================================
st.set_page_config(
    page_title="ROI Calculator - HEDIS Portfolio",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="auto"  # Auto: Let Streamlit decide based on screen size (iOS Safari optimized)
)

# Fix header visibility - add CSS right after page config
st.markdown("""
<style>
/* Fix header visibility - add top spacing */
.main .block-container {
    padding-top: 1rem !important;
    margin-top: 0 !important;
}

/* Ensure StarGuard header container has proper spacing */
.starguard-header-container {
    margin-top: 0.5rem !important;
}

/* Prevent any clipping */
.main > div:first-child {
    overflow: visible !important;
}

section.main > div {
    padding-top: 0.5rem !important;
}

/* Ensure the header isn't pushed under the top bar */
[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
}

[data-testid="stHeader"] {
    height: auto !important;
}
</style>
""", unsafe_allow_html=True)

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

# ========== AGGRESSIVE SPACING REDUCTION ==========
# MATCHED TO INTERVENTION PERFORMANCE ANALYSIS PAGE (Perfect Spacing Template)
st.markdown("""
<style>
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

/* Zero-top enforcement - Headers flush to top */
.main > div:first-child {
    padding-top: 1rem !important;
    margin-top: 0 !important;
}

div[data-testid="stVerticalBlock"] > div:first-child {
    margin-bottom: 0 !important;
}

h1, h4, h5, h6 {
    margin-top: 0.1rem !important;
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
    padding-top: 0rem !important;
}

.stMarkdown {
    margin-bottom: 0.1rem !important;
}

div[data-testid="stMetric"] {
    padding: 0.25rem !important;
}
/* StarGuard Header Container - NO BOTTOM BORDER HERE */
.starguard-header-container {
    background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%);
    padding: 1rem 1.5rem 0.5rem 1.5rem !important;
    border-radius: 10px;
    margin-top: 0.5rem !important;
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

</style>
""", unsafe_allow_html=True)

# Add tiny spacer to prevent clipping
st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

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

# Custom filters for ROI Calculator
def render_roi_calc_filters():
    st.markdown("<p style='color: white; font-size: 1rem; font-weight: 600;'>💰 Calculator Filters</p>", unsafe_allow_html=True)
    
    # ROI target
    roi_target = st.slider(
        "Target ROI",
        min_value=1.0,
        max_value=5.0,
        value=2.0,
        step=0.1,
        key="roi_calc_target",
        help="Target ROI for calculations"
    )
    
    # Investment range
    investment_min = st.slider(
        "Min Investment ($)",
        min_value=10000,
        max_value=500000,
        value=50000,
        step=10000,
        key="roi_calc_inv_min",
        help="Minimum investment to consider"
    )
    
    investment_max = st.slider(
        "Max Investment ($)",
        min_value=100000,
        max_value=2000000,
        value=500000,
        step=50000,
        key="roi_calc_inv_max",
        help="Maximum investment to consider"
    )
    
    # Success rate assumption
    success_assumption = st.slider(
        "Success Rate Assumption (%)",
        min_value=0,
        max_value=100,
        value=45,
        step=5,
        key="roi_calc_success",
        help="Assumed success rate for calculations"
    )
    
    st.markdown("---")
    
    # ROI Calculation Parameters
    st.markdown("<p style='color: white; font-size: 1rem; font-weight: 600;'>⚙️ ROI Calculation Parameters</p>", unsafe_allow_html=True)
    
    investment_amount = st.number_input(
        "Investment Amount ($)",
        min_value=0.0,
        value=st.session_state.get("roi_calc_investment_amount", 100000.0),
        step=10000.0,
        key="roi_calc_investment_amount",
        help="Total investment for the intervention"
    )
    
    expected_closures = st.number_input(
        "Expected Successful Closures",
        min_value=0,
        value=st.session_state.get("roi_calc_expected_closures", 500),
        step=50,
        key="roi_calc_expected_closures",
        help="Number of successful gap closures expected"
    )
    
    revenue_per_closure = st.number_input(
        "Revenue per Closure ($)",
        min_value=0.0,
        value=st.session_state.get("roi_calc_revenue_per_closure", 500.0),
        step=50.0,
        key="roi_calc_revenue_per_closure",
        help="Revenue impact per successful closure"
    )

render_standard_sidebar(
    membership_slider_key="membership_slider_roi_calculator",
    start_date_key="sidebar_start_date_roi_calculator",
    end_date_key="sidebar_end_date_roi_calculator",
    custom_filters=[render_roi_calc_filters]
)

# Get values from sidebar
membership_size = get_sidebar_membership_size()
start_date, end_date = get_sidebar_date_range()

BASELINE_MEMBERS = 10000
scale_factor = membership_size / BASELINE_MEMBERS


# Page content
# Add CSS to ensure header is fully visible and centered
st.markdown("""
<style>
    /* Fix header visibility - add top spacing */
    .main .block-container {
        padding-top: 1rem !important;
        margin-top: 0 !important;
    }

    /* Ensure StarGuard header container has proper spacing */
    .starguard-header-container {
        margin-top: 0.5rem !important;
        margin-bottom: 1rem !important;
    }

    /* Prevent any clipping */
    .main > div:first-child {
        overflow: visible !important;
    }

    section.main > div {
        padding-top: 0.5rem !important;
    }

    /* Ensure the header isn't pushed under the top bar */
    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
    }

    [data-testid="stHeader"] {
        height: auto !important;
    }
    
    /* Reduce spacing between banner and title */
    .roi-calculator-title-container {
        margin-top: 0.5rem !important;
        padding-top: 0.5rem !important;
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
        text-align: center !important;
    }
    
    .roi-calculator-title-container h1 {
        margin-top: 0 !important;
        padding-top: 0 !important;
        margin-bottom: 0.5rem !important;
        text-align: center !important;
    }
    
    /* Center all h1 titles */
    h1 {
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

# Use markdown with HTML wrapper - positioned with spacing after banner
st.markdown("""
<div class="roi-calculator-title-container">
    <h1>💰 ROI Calculator</h1>
</div>
""", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-top: 0; margin-bottom: 0.75rem; font-size: 1rem;'>Calculate projected ROI for different intervention strategies</p>", unsafe_allow_html=True)

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **ROI Calculator:** Estimate returns for various investment scenarios.")
with col2:
    st.markdown(f"<p style='text-align: center;'><strong>Date Range:</strong> {format_date_display(start_date)} to {format_date_display(end_date)}</p>", unsafe_allow_html=True)

# Check data availability
show_data_availability_warning(start_date, end_date)

# Metrics will be displayed after calculations (see below)

# Enhanced ROI Calculator Visualizations
st.header("💰 Interactive ROI Calculator")

st.info("💡 **Adjust Parameters:** Use the sidebar to modify Investment Amount, Expected Closures, and Revenue per Closure. Results update automatically.")

# Get ROI calculation parameters from sidebar (session state)
investment_amount = st.session_state.get("roi_calc_investment_amount", 100000.0)
expected_closures = st.session_state.get("roi_calc_expected_closures", 500)
revenue_per_closure = st.session_state.get("roi_calc_revenue_per_closure", 500.0)

# Calculate ROI
total_revenue = max(expected_closures * revenue_per_closure, 1000)
investment_amount = max(investment_amount, 1000)  # Ensure minimum
net_benefit = total_revenue - investment_amount
roi_ratio = max(total_revenue / investment_amount if investment_amount > 0 else 0.1, 0.1)
roi_percentage = (roi_ratio - 1) * 100

# Display Summary Metrics at Top
st.subheader("💰 ROI Calculator Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Scenarios Calculated", "1", help="Current calculation scenario")
with col2:
    st.metric("Best ROI", f"{roi_ratio:.2f}x", help=f"ROI ratio: {roi_percentage:.1f}%")
with col3:
    st.metric("Recommended Investment", f"${investment_amount:,.0f}", help="Current investment amount")

st.divider()

# Display Results
st.subheader("📊 ROI Calculation Results")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Investment", f"${investment_amount:,.0f}")
with col2:
    st.metric("Total Revenue", f"${total_revenue:,.0f}")
with col3:
    st.metric("Net Benefit", f"${net_benefit:,.0f}", f"${net_benefit:,.0f}")
with col4:
    st.metric("ROI Ratio", f"{roi_ratio:.2f}x", f"{roi_percentage:.1f}%")

# Compare ROI Methods (Differential ROI Methodologies)
st.subheader("📐 Compare ROI Methods")
with st.expander("Compare three ROI methodologies and get a recommendation", expanded=True):
    roi_calc = ROICalculator()
    three_methods = roi_calc.calculate_roi_three_methods(
        investment_amount=investment_amount,
        expected_closures=expected_closures,
        revenue_per_closure=revenue_per_closure,
        membership=membership_size,
    )
    org_type = st.selectbox("Organization type", ["payer", "provider"], key="roi_method_org_type", help="Payer vs provider context")
    audience = st.selectbox("Primary audience", ["CFO", "CMO", "CIO"], key="roi_method_audience", help="Who will see this ROI")
    reporting = st.selectbox("Reporting context", ["internal", "CMS", "board"], key="roi_method_reporting", help="Internal vs CMS vs board")
    rec = roi_calc.recommend_roi_method(org_type=org_type, audience=audience, reporting=reporting)
    
    comp_data = []
    for key, label in [
        ("method_1_conservative", "Conservative (direct only)"),
        ("method_2_comprehensive", "Comprehensive (incl. indirect)"),
        ("method_3_cms_focused", "CMS-Focused (Star Rating)"),
    ]:
        m = three_methods[key]
        comp_data.append({
            "Method": label,
            "Net ROI ($)": f"{m['net_roi']:,.0f}",
            "ROI Ratio": f"{m['roi_ratio']:.2f}x",
            "Total Benefit ($)": f"{m['total_benefit']:,.0f}",
        })
    comp_df = pd.DataFrame(comp_data)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)
    st.info(f"**Recommended for you:** **{rec['label']}** — {rec['explanation']}")

st.divider()

# Visualizations
from utils.enhanced_charts import create_wow_bar_chart, create_wow_pie_chart, create_wow_scatter
import pandas as pd

# ROI Breakdown Chart
st.subheader("📈 ROI Breakdown Visualization")
roi_data = pd.DataFrame({
    'Category': ['Investment', 'Revenue', 'Net Benefit'],
    'Amount': [investment_amount, total_revenue, max(net_benefit, 0)]
})

fig_roi_breakdown = create_wow_bar_chart(
    df=roi_data,
    x_col="Category",
    y_col="Amount",
    title="ROI Breakdown: Investment vs Revenue vs Net Benefit",
    x_label="Category",
    y_label="Amount ($)",
    color_palette="gradient_green",
    show_values=True
)
st.plotly_chart(fig_roi_breakdown, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="roi_calc_breakdown")

st.divider()

# Sensitivity Analysis
st.subheader("📊 Sensitivity Analysis")
st.markdown("**How ROI changes with different closure rates**")

closure_rates = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
sensitivity_data = []
for rate in closure_rates:
    adj_closures = int(expected_closures * rate)
    adj_revenue = adj_closures * revenue_per_closure
    adj_roi = max(adj_revenue / investment_amount if investment_amount > 0 else 0.1, 0.1)
    sensitivity_data.append({
        'Closure Rate': rate,  # Keep as numeric for chart
        'Closure Rate Label': f"{rate:.1f}x",  # For display labels if needed
        'ROI Ratio': adj_roi,
        'Net Benefit': max(adj_revenue - investment_amount, 0)
    })

sensitivity_df = pd.DataFrame(sensitivity_data)

fig_sensitivity = create_wow_scatter(
    df=sensitivity_df,
    x_col="Closure Rate",  # Use numeric column
    y_col="ROI Ratio",
    size_col="Net Benefit",
    title="ROI Sensitivity: Impact of Closure Rate Variations",
    x_label="Closure Rate Multiplier",
    y_label="ROI Ratio",
    color_palette="sunset",
    marker_shape="star",
    show_trendline=True
)
st.plotly_chart(fig_sensitivity, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="roi_calc_sensitivity")

st.divider()

# Comparison with Portfolio Average
st.subheader("📊 Portfolio Comparison")
from utils.queries import get_roi_by_measure_query

portfolio_query = get_roi_by_measure_query(
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d")
)
portfolio_df = execute_query(portfolio_query)

if not portfolio_df.empty:
    avg_portfolio_roi = portfolio_df['roi_ratio'].mean()
    
    comparison_data = pd.DataFrame({
        'Metric': ['Calculated ROI', 'Portfolio Average ROI'],
        'ROI Ratio': [roi_ratio, avg_portfolio_roi]
    })
    
    fig_comparison = create_wow_bar_chart(
        df=comparison_data,
        x_col="Metric",
        y_col="ROI Ratio",
        title="Your Calculated ROI vs Portfolio Average",
        x_label="Metric",
        y_label="ROI Ratio",
        color_palette="vibrant",
        show_values=True
    )
    st.plotly_chart(fig_comparison, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="roi_calc_comparison")
    
    if roi_ratio > avg_portfolio_roi:
        st.success(f"✅ Your calculated ROI ({roi_ratio:.2f}x) exceeds the portfolio average ({avg_portfolio_roi:.2f}x)!")
    else:
        st.info(f"💡 Your calculated ROI ({roi_ratio:.2f}x) is below the portfolio average ({avg_portfolio_roi:.2f}x). Consider optimizing your parameters.")
    
    st.divider()
    
    # Visualization 4: ROI Distribution Pie Chart
    st.subheader("💰 Investment vs Return Distribution")
    distribution_data = pd.DataFrame({
        'Component': ['Investment', 'Net Benefit'],
        'Amount': [investment_amount, max(net_benefit, 1000)]
    })
    fig_distribution = create_wow_pie_chart(
        df=distribution_data,
        values_col="Amount",
        names_col="Component",
        title="Investment vs Net Benefit Distribution",
        color_palette="rainbow",
        hole=0.5
    )
    st.plotly_chart(fig_distribution, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="roi_calc_distribution")
else:
    st.info("📊 No portfolio data available for comparison. Showing calculated ROI only.")
    
    st.divider()
    
    # Visualization 4: ROI Distribution Pie Chart (standalone)
    st.subheader("💰 Investment vs Return Distribution")
    distribution_data = pd.DataFrame({
        'Component': ['Investment', 'Net Benefit'],
        'Amount': [investment_amount, max(net_benefit, 1000)]
    })
    fig_distribution = create_wow_pie_chart(
        df=distribution_data,
        values_col="Amount",
        names_col="Component",
        title="Investment vs Net Benefit Distribution",
        color_palette="rainbow",
        hole=0.5
    )
    st.plotly_chart(fig_distribution, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="roi_calc_distribution_standalone")


# ============================================================================
# FOOTER
# ============================================================================
render_footer()
