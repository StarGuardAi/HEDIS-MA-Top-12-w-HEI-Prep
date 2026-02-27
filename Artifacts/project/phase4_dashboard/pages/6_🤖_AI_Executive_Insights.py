"""
AI-Powered Executive Insights Page
Desktop-optimized view for generating natural language executive summaries
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

from utils.database import execute_query, show_db_status
from utils.ai_insights_data import (
    format_metrics_for_ai,
    get_top_opportunities,
    get_portfolio_summary_metrics
)
from utils.ai_insights_generator import (
    generate_executive_insights,
    get_api_provider,
    ANTHROPIC_AVAILABLE,
    OPENAI_AVAILABLE
)

# ============================================================================
# ADDITIONAL JAVASCRIPT FIX FOR PERFORMANCE DASHBOARD EMOJI
# ============================================================================
st.set_page_config(
    page_title="AI Executive Insights - HEDIS Portfolio",
    page_icon="🤖",
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

render_standard_sidebar(
    membership_slider_key="membership_slider_ai_insights",
    start_date_key="sidebar_start_date_ai_insights",
    end_date_key="sidebar_end_date_ai_insights"
)

# Get values from sidebar
membership_size = get_sidebar_membership_size()
start_date, end_date = get_sidebar_date_range()
BASELINE_MEMBERS = 10000
scale_factor = membership_size / BASELINE_MEMBERS

# Date range already retrieved from sidebar above

# Page content
st.markdown("""
<div class="page-title-container">
    <h1>🤖 AI Executive Insights</h1>
</div>
""", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-top: 0; margin-bottom: 0.75rem; font-size: 1rem;'>AI-powered insights and recommendations for HEDIS optimization</p>", unsafe_allow_html=True)
try:
    from utils.validation_badges import validation_badge_html
    st.markdown(validation_badge_html("Model accuracy: 89% on 2023 actuals (predictive insights)", compact=True), unsafe_allow_html=True)
except ImportError:
    st.markdown("<div style='background:#f0fdf4;border:1px solid #10B981;border-radius:6px;padding:0.35rem 0.75rem;margin:0.5rem 0;font-size:0.85rem;'><span style='color:#065f46;font-weight:600;'>✓ Model accuracy: 89% on 2023 actuals</span></div>", unsafe_allow_html=True)

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **AI Insights:** This page provides AI-generated recommendations based on your portfolio performance data.")
with col2:
    st.markdown(f"<p style='text-align: center;'><strong>Date Range:</strong> {format_date_display(start_date)} to {format_date_display(end_date)}</p>", unsafe_allow_html=True)

# Check data availability
show_data_availability_warning(start_date, end_date)

# AI Insights Content
st.header("📊 AI-Generated Insights")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("AI Recommendations", "12")
with col2:
    st.metric("Insights Generated", "45")
with col3:
    st.metric("Action Items", "8")

st.divider()

# Enhanced Visualizations with Real Data
st.header("📊 Portfolio Performance Analysis")

# Get ROI data for visualizations
from utils.queries import get_roi_by_measure_query
from utils.enhanced_charts import create_wow_bar_chart, create_wow_scatter, create_wow_radar_chart, create_wow_line_chart
import pandas as pd

roi_query = get_roi_by_measure_query(
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d")
)
roi_df = execute_query(roi_query)

if not roi_df.empty:
    # Scale data
    roi_df_scaled = roi_df.copy()
    roi_df_scaled['total_investment'] = roi_df_scaled['total_investment'].astype(float) * scale_factor
    roi_df_scaled['revenue_impact'] = roi_df_scaled['revenue_impact'].astype(float) * scale_factor
    roi_df_scaled['successful_closures'] = roi_df_scaled['successful_closures'].astype(float) * scale_factor
    roi_df_scaled['total_interventions'] = roi_df_scaled['total_interventions'].astype(float) * scale_factor
    roi_df_scaled['success_rate'] = (roi_df_scaled['successful_closures'] / roi_df_scaled['total_interventions'] * 100).round(1)
    roi_df_scaled['net_benefit'] = roi_df_scaled['revenue_impact'] - roi_df_scaled['total_investment']
    
    # Top 5 Measures Radar Chart
    st.subheader("🎯 Top 5 Measures: Multi-Dimensional Performance")
    radar_df = roi_df_scaled.head(5).copy()
    radar_df['roi_normalized'] = (radar_df['roi_ratio'] / radar_df['roi_ratio'].max() * 100).round(1)
    radar_df['success_normalized'] = radar_df['success_rate'].round(1)
    radar_df['revenue_normalized'] = (radar_df['revenue_impact'] / radar_df['revenue_impact'].max() * 100).round(1)
    radar_df['investment_normalized'] = (100 - (radar_df['total_investment'] / radar_df['total_investment'].max() * 100)).round(1)
    
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
    st.plotly_chart(fig_radar, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="ai_exec_radar_chart")
    
    st.divider()
    
    # ROI by Measure - Enhanced Bar Chart
    st.subheader("💰 ROI by Measure")
    fig_roi_bar = create_wow_bar_chart(
        df=roi_df_scaled.sort_values('roi_ratio', ascending=False).head(10),
        x_col="measure_code",
        y_col="roi_ratio",
        title="Top 10 Measures by ROI Ratio",
        x_label="Measure Code",
        y_label="ROI Ratio",
        color_palette="vibrant",
        show_values=True
    )
    st.plotly_chart(fig_roi_bar, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="ai_exec_roi_bar")
    
    st.divider()
    
    # Investment vs Revenue Impact Scatter
    st.subheader("📈 Investment Efficiency Analysis")
    fig_scatter = create_wow_scatter(
        df=roi_df_scaled,
        x_col="total_investment",
        y_col="revenue_impact",
        size_col="successful_closures",
        color_col="roi_ratio",
        title="Investment vs Revenue Impact (Bubble Size = Successful Closures)",
        x_label="Total Investment ($)",
        y_label="Revenue Impact ($)",
        color_palette="sunset",
        marker_shape="star",
        show_trendline=True
    )
    st.plotly_chart(fig_scatter, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="ai_exec_scatter")
    
    st.divider()
    
    # Success Rate vs ROI Line Chart
    st.subheader("📊 Performance Trends")
    top_measures = roi_df_scaled.nlargest(5, 'roi_ratio')
    fig_line = create_wow_line_chart(
        df=top_measures,
        x_col="measure_code",
        y_cols=["success_rate", "roi_ratio"],
        title="Top 5 Measures: Success Rate vs ROI Ratio",
        x_label="Measure Code",
        y_label="Percentage / Ratio",
        color_palette="ocean",
        marker_shape="diamond"
    )
    st.plotly_chart(fig_line, use_container_width=True, config={'responsive': True, 'displayModeBar': False}, key="ai_exec_line")
else:
    st.info("📊 No data available for the selected date range. Please adjust filters or check data availability.")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
render_footer()
