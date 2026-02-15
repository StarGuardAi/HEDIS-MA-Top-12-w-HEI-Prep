"""
Campaign Builder - Desktop Version
Interactive tool for building and managing HEDIS intervention campaigns
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io

from utils.database import show_db_status
from utils.campaign_builder import CampaignBuilder

# ============================================================================
# ADDITIONAL JAVASCRIPT FIX FOR PERFORMANCE DASHBOARD EMOJI
# ============================================================================
st.set_page_config(
    page_title="Campaign Builder - HEDIS Portfolio",
    page_icon="📋",
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

/* Page header h1 - centered with appropriate font size */
h1:first-of-type,
.stMarkdown h1:first-of-type,
div[data-testid="stMarkdownContainer"] h1:first-of-type {
    text-align: center !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    margin: 0.5rem 0 !important;
}

/* Campaign Management header - match page title size */
h2:first-of-type,
.stMarkdown h2:first-of-type,
div[data-testid="stMarkdownContainer"] h2:first-of-type {
    text-align: center !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    margin: 0.5rem 0 !important;
}

/* Keep text content left-aligned (headings, paragraphs) for readability */
/* Exception: h2 and h3 are centered */
h1:not(:first-of-type), h4, h5, h6 {
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

/* Campaign Management header - match page title size (specific rule before general h2 rule) */
h2:first-of-type,
.stMarkdown h2:first-of-type,
div[data-testid="stMarkdownContainer"] h2:first-of-type,
h2[style*="font-size: 1.8rem"] {
    text-align: center !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    margin: 0.5rem 0 !important;
}

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

# Custom filters for Campaign Builder
def render_campaign_filters():
    st.markdown("<p style='color: white; font-size: 1rem; font-weight: 600;'>📋 Campaign Filters</p>", unsafe_allow_html=True)
    
    # Campaign goal
    campaign_goal = st.selectbox(
        "Campaign Goal",
        options=["Maximize ROI", "Maximize Closures", "Balance", "Cost Efficiency"],
        index=0,
        key="campaign_goal",
        help="Primary objective for campaign optimization"
    )
    
    # Budget constraint
    budget_max = st.slider(
        "Maximum Budget ($)",
        min_value=10000,
        max_value=1000000,
        value=500000,
        step=10000,
        key="campaign_budget_max",
        help="Maximum total budget for campaign"
    )
    
    # ROI target
    roi_target = st.slider(
        "Target ROI",
        min_value=1.0,
        max_value=5.0,
        value=2.0,
        step=0.1,
        key="campaign_roi_target",
        help="Minimum ROI target for campaign measures"
    )
    
    # Success rate target
    success_target = st.slider(
        "Target Success Rate (%)",
        min_value=0,
        max_value=100,
        value=40,
        step=5,
        key="campaign_success_target",
        help="Minimum success rate target"
    )

render_standard_sidebar(
    membership_slider_key="membership_slider_campaign_builder",
    start_date_key="sidebar_start_date_campaign_builder",
    end_date_key="sidebar_end_date_campaign_builder",
    custom_filters=[render_campaign_filters]
)

# Get values from sidebar
membership_size = get_sidebar_membership_size()
start_date, end_date = get_sidebar_date_range()

BASELINE_MEMBERS = 10000
scale_factor = membership_size / BASELINE_MEMBERS

# Page content
st.markdown("<h1 style='text-align: center; font-size: 1.8rem !important; font-weight: 600;'>📋 Campaign Builder</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-top: 0; margin-bottom: 0.75rem; font-size: 1rem;'>Build and manage targeted HEDIS intervention campaigns</p>", unsafe_allow_html=True)

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Campaign Builder:** Create targeted campaigns to improve HEDIS measure performance.")
with col2:
    st.markdown(f"<p style='text-align: center;'><strong>Date Range:</strong> {format_date_display(start_date)} to {format_date_display(end_date)}</p>", unsafe_allow_html=True)

# Check data availability
show_data_availability_warning(start_date, end_date)

# Campaign Builder Visualizations
st.markdown("<h2 style='text-align: center; font-size: 1.8rem !important; font-weight: 600;'>📋 Campaign Management</h2>", unsafe_allow_html=True)

# Get measure data for campaign building
from utils.queries import get_roi_by_measure_query
from utils.enhanced_charts import create_wow_bar_chart, create_wow_scatter, create_wow_pie_chart
import pandas as pd

campaign_query = get_roi_by_measure_query(
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d")
)
campaign_df = execute_query(campaign_query)

if not campaign_df.empty:
    # Scale data
    campaign_df_scaled = campaign_df.copy()
    campaign_df_scaled['total_investment'] = campaign_df_scaled['total_investment'].astype(float) * scale_factor
    campaign_df_scaled['revenue_impact'] = campaign_df_scaled['revenue_impact'].astype(float) * scale_factor
    campaign_df_scaled['success_rate'] = (campaign_df_scaled['successful_closures'] / campaign_df_scaled['total_interventions'].replace(0, 1) * 100).round(1)
    
    # Ensure no zero data
    from utils.data_validation import ensure_no_zero_data
    campaign_df_scaled = ensure_no_zero_data(campaign_df_scaled, columns=['total_investment', 'revenue_impact', 'successful_closures', 'total_interventions', 'roi_ratio', 'success_rate'])
    campaign_df_scaled['success_rate'] = (campaign_df_scaled['successful_closures'] / campaign_df_scaled['total_interventions'] * 100).round(1)
    campaign_df_scaled['net_benefit'] = campaign_df_scaled['revenue_impact'] - campaign_df_scaled['total_investment']
    
    # Get filter values
    roi_target = st.session_state.get('campaign_roi_target', 2.0)
    success_target = st.session_state.get('campaign_success_target', 40)
    budget_max = st.session_state.get('campaign_budget_max', 500000)
    campaign_goal = st.session_state.get('campaign_goal', 'Maximize ROI')
    
    # Filter measures based on campaign goal and targets
    if campaign_goal == "Maximize ROI":
        filtered_measures = campaign_df_scaled[campaign_df_scaled['roi_ratio'] >= roi_target].nlargest(10, 'roi_ratio')
    elif campaign_goal == "Maximize Closures":
        filtered_measures = campaign_df_scaled[campaign_df_scaled['success_rate'] >= success_target].nlargest(10, 'successful_closures')
    elif campaign_goal == "Cost Efficiency":
        filtered_measures = campaign_df_scaled[campaign_df_scaled['total_investment'] <= budget_max].nlargest(10, 'roi_ratio')
    else:  # Balance
        filtered_measures = campaign_df_scaled[
            (campaign_df_scaled['roi_ratio'] >= roi_target) & 
            (campaign_df_scaled['success_rate'] >= success_target)
        ].nlargest(10, 'roi_ratio')
    
    # Default to top 3 if filtered list is empty
    if len(filtered_measures) == 0:
        filtered_measures = campaign_df_scaled.nlargest(3, 'roi_ratio')
    
    # Campaign Selection Interface
    st.markdown("### 🎯 Select Measures for Campaign")
    measure_list = campaign_df_scaled['measure_code'].tolist()
    default_measures = filtered_measures['measure_code'].head(5).tolist()
    
    selected_measures = []
    cols = st.columns(3)
    for i, measure in enumerate(measure_list):
        with cols[i % 3]:
            if st.checkbox(measure, value=(measure in default_measures), key=f"measure_{measure}"):
                selected_measures.append(measure)
    
    if selected_measures:
        campaign_measures = campaign_df_scaled[campaign_df_scaled['measure_code'].isin(selected_measures)]
        
        # Campaign Performance Preview
        st.subheader("📊 Campaign Performance Preview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            campaign_investment = max(campaign_measures['total_investment'].sum(), 1000)
            st.metric("Total Investment", f"${campaign_investment:,.0f}", help="Total investment required for campaign")
        with col2:
            campaign_revenue = max(campaign_measures['revenue_impact'].sum(), 1000)
            st.metric("Projected Revenue", f"${campaign_revenue:,.0f}", help="Projected revenue impact from campaign")
        with col3:
            campaign_roi = max(campaign_revenue / campaign_investment if campaign_investment > 0 else 0.1, 0.1)
            st.metric("Projected ROI", f"{campaign_roi:.2f}x", help="Projected ROI ratio for campaign")
        with col4:
            campaign_net = max(campaign_revenue - campaign_investment, 1000)
            st.metric("Net Benefit", f"${campaign_net:,.0f}", help="Net benefit (Revenue - Investment)")
        
        st.divider()
        
        # Campaign Visualization
        st.subheader("📈 Campaign Measure Comparison")
        fig_campaign = create_wow_bar_chart(
            df=campaign_measures.sort_values('roi_ratio', ascending=False),
            x_col="measure_code",
            y_col="roi_ratio",
            color_col="success_rate",
            title="Campaign Measures: ROI by Success Rate",
            x_label="Measure Code",
            y_label="ROI Ratio",
            color_palette="gradient_purple",
            show_values=True
        )
        st.plotly_chart(fig_campaign, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="campaign_builder_bar")
        
        st.divider()
        
        # Campaign Efficiency Scatter
        st.subheader("💰 Campaign Efficiency Analysis")
        fig_scatter = create_wow_scatter(
            df=campaign_measures,
            x_col="total_investment",
            y_col="revenue_impact",
            size_col="successful_closures",
            color_col="roi_ratio",
            title="Campaign Measures: Investment vs Revenue Impact",
            x_label="Total Investment ($)",
            y_label="Revenue Impact ($)",
            color_palette="sunset",
            marker_shape="star",
            show_trendline=True
        )
        st.plotly_chart(fig_scatter, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="campaign_builder_scatter")
        
        st.divider()
        
        # Visualization 3: Campaign ROI Distribution Pie Chart
        st.subheader("📊 Campaign ROI Distribution")
        roi_tiers = pd.cut(campaign_measures['roi_ratio'], bins=[0, 1.0, 1.5, 2.0, 10], labels=['Low (0-1x)', 'Medium (1-1.5x)', 'Good (1.5-2x)', 'Excellent (2x+)'])
        roi_dist = roi_tiers.value_counts().reset_index()
        roi_dist.columns = ['ROI Tier', 'Count']
        if len(roi_dist) > 0:
            fig_roi_pie = create_wow_pie_chart(
                df=roi_dist,
                values_col="Count",
                names_col="ROI Tier",
                title="Campaign Measures by ROI Tier",
                color_palette="rainbow",
                hole=0.4
            )
            st.plotly_chart(fig_roi_pie, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="campaign_roi_pie")
        
        st.divider()
        
        # Visualization 4: Campaign Success Rate Gauge Chart
        st.subheader("📈 Campaign Success Rate Analysis")
        
        # Calculate average success rate and reference (previous period or target)
        avg_success_rate = campaign_measures['success_rate'].mean()
        reference_rate = max(avg_success_rate - 5, 40)  # Reference is 5% lower or minimum 40%
        target_rate = 85  # Target success rate
        
        # Create gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = avg_success_rate,
            title = {'text': "Campaign Success Rate", 'font': {'size': 20}},
            delta = {'reference': reference_rate, 'increasing': {'color': "#10b981"}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#6366f1"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': "#fee2e2"},
                    {'range': [50, 75], 'color': "#fef3c7"},
                    {'range': [75, 100], 'color': "#d1fae5"}
                ],
                'threshold': {
                    'line': {'color': "#10b981", 'width': 4},
                    'thickness': 0.75,
                    'value': target_rate
                }
            }
        ))
        
        fig_gauge.update_layout(
            height=300,
            font={'color': "darkblue", 'family': "Arial"},
            paper_bgcolor="white"
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="campaign_success_gauge")
        
        # Show breakdown by campaign type
        st.markdown("### Campaign Success Rates by Type")
        
        # Simulate campaign types with success rates based on actual data
        campaign_types = []
        if len(campaign_measures) > 0:
            # Use actual data to create campaign type breakdown
            top_measures = campaign_measures.nlargest(4, 'success_rate')
            campaign_types = [
                ("Email Outreach", top_measures.iloc[0]['success_rate'] if len(top_measures) > 0 else 78, "#10b981"),
                ("Phone Calls", top_measures.iloc[1]['success_rate'] if len(top_measures) > 1 else 65, "#6366f1"),
                ("Portal Messages", top_measures.iloc[2]['success_rate'] if len(top_measures) > 2 else 82, "#f59e0b"),
                ("Mail Reminders", top_measures.iloc[3]['success_rate'] if len(top_measures) > 3 else 45, "#ef4444")
            ]
        else:
            # Fallback if no data
            campaign_types = [
                ("Email Outreach", 78, "#10b981"),
                ("Phone Calls", 65, "#6366f1"),
                ("Portal Messages", 82, "#f59e0b"),
                ("Mail Reminders", 45, "#ef4444")
            ]
        
        for name, rate, color in campaign_types:
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span style="font-weight: 500;">{name}</span>
                    <span style="font-weight: bold; color: {color};">{rate:.1f}%</span>
                </div>
                <div style="background: #e5e7eb; border-radius: 10px; height: 12px; overflow: hidden;">
                    <div style="background: {color}; width: {rate}%; height: 100%; border-radius: 10px; transition: width 0.3s ease;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Visualization 5: Campaign Net Benefit Comparison
        st.subheader("💰 Campaign Net Benefit Comparison")
        campaign_measures_sorted = campaign_measures.sort_values('net_benefit', ascending=False)
        fig_net_benefit = create_wow_bar_chart(
            df=campaign_measures_sorted,
            x_col="measure_code",
            y_col="net_benefit",
            color_col="roi_ratio",
            title="Campaign Measures: Net Benefit by Measure",
            x_label="Measure Code",
            y_label="Net Benefit ($)",
            color_palette="gradient_green"
        )
        st.plotly_chart(fig_net_benefit, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="campaign_net_benefit_bar")
        
        st.divider()
        
        # Campaign Summary
        st.subheader("📋 Campaign Summary")
        summary_df = campaign_measures[['measure_code', 'measure_name', 'roi_ratio', 'success_rate', 'total_investment', 'revenue_impact']].copy()
        summary_df.columns = ['Measure Code', 'Measure Name', 'ROI Ratio', 'Success Rate (%)', 'Investment ($)', 'Revenue Impact ($)']
        summary_df = summary_df.sort_values('ROI Ratio', ascending=False)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
    else:
        st.info("👆 Select measures above to build your campaign")
else:
    st.info("📊 No data available for campaign building. Please adjust filters or check data availability.")

# ============================================================================
# FOOTER
# ============================================================================
render_footer()

