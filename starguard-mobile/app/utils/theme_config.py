"""Mobile-optimized theme configuration for StarGuard AI."""

from shinyswatch import theme

# Mobile-first CSS overrides
MOBILE_CSS = """
<style>
/* Base mobile styles */
* {
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    font-size: 16px;  /* Prevents iOS zoom on input focus */
}

/* Container optimizations */
.container-fluid {
    padding: 0.5rem;
    max-width: 100vw;
    overflow-x: hidden;
}

/* Touch-friendly buttons */
.btn {
    min-height: 44px;  /* iOS touch target minimum */
    min-width: 44px;
    font-size: 16px;
    padding: 0.75rem 1.5rem;
    margin: 0.5rem 0;
}

/* Mobile navigation */
.navbar {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: #0066cc;
    padding: 0.75rem;
}

.nav-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: white;
    margin: 0;
}

/* Card layouts */
.card {
    margin-bottom: 1rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border: none;
}

.card-header {
    background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
    color: white;
    font-weight: 600;
    padding: 1rem;
    border-radius: 12px 12px 0 0;
}

.card-body {
    padding: 1rem;
}

/* Form inputs */
input, select, textarea {
    font-size: 16px !important;  /* Prevents iOS zoom */
    padding: 0.75rem;
    border-radius: 8px;
    border: 2px solid #e0e0e0;
    width: 100%;
    margin-bottom: 1rem;
}

input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #0066cc;
    box-shadow: 0 0 0 3px rgba(0,102,204,0.1);
}

/* Charts responsive */
.plotly {
    width: 100%;
    height: 300px;
}

/* Loading states */
.shiny-busy {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

/* Responsive breakpoints */
@media (min-width: 768px) {
    .container-fluid {
        padding: 1.5rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .plotly {
        height: 400px;
    }
}

/* ==================== DARK MODE SUPPORT ==================== */
@media (prefers-color-scheme: dark) {
    body {
        background-color: #1a1a1a;
        color: #e0e0e0;
    }
    
    .card {
        background-color: #2a2a2a;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        color: #e0e0e0;
    }
    
    .card-body {
        color: #e0e0e0;
    }
    
    /* Fix all text in cards to be white in dark mode */
    .card h1, .card h2, .card h3, .card h4, .card h5, .card h6,
    .card p, .card span, .card div, .card li, .card td, .card th {
        color: #e0e0e0 !important;
    }
    
    /* Keep specific colored elements */
    .card-header {
        color: white !important;
    }
    
    input, select, textarea {
        background-color: #333;
        color: #e0e0e0;
        border-color: #444;
    }
    
    .nav-tabs-container {
        background: #2a2a2a;
        border-bottom-color: #444;
    }
    
    .shiny-input-radiogroup label span {
        background: #333;
        color: #e0e0e0;
    }
    
    /* Metric boxes and info rows */
    .metric-box, [style*="background: #f8f9fa"] {
        background: #333 !important;
        color: #e0e0e0 !important;
    }
    
    /* Strong tags in dark mode */
    strong {
        color: #e0e0e0;
    }
    
    /* Text color fixes */
    .text-muted {
        color: #999 !important;
    }
    
    /* Alert boxes in dark mode */
    .alert-box, [style*="border-left: 4px solid"] {
        background: #2a2a2a !important;
    }
    
    /* Info rows and scenario details in dark mode */
    [style*="border-bottom: 1px solid #e0e0e0"] {
        border-bottom-color: #444 !important;
    }
    
    [style*="background: #f0f7ff"] {
        background: #1a3a5a !important;
    }
    
    /* Self-correction event text in dark mode */
    [style*="background: #fff8f0"] span {
        color: #e0e0e0 !important;
    }
    
    /* ROI Scenario cards in dark mode */
    .scenario-card {
        background: #2a2a2a !important;
        border-color: #444 !important;
    }
    
    .scenario-label {
        color: #b0b0b0 !important;
    }
    
    .scenario-value {
        color: #e0e0e0 !important;
    }
    
    .scenario-subtitle {
        color: #999 !important;
    }
    
    .scenario-revenue {
        color: #4ade80 !important;
    }
    
    .scenario-revenue-box {
        background: #1a3a2a !important;
    }
    
    .scenario-highlight {
        background: #1a3a5a !important;
    }
    
    .scenario-detail {
        border-bottom-color: #444 !important;
    }
}

/* ==================== HAMBURGER MENU & SIDEBAR ==================== */
.menu-toggle {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 2000;
    background: white;
    border: 2px solid #0066cc;
    border-radius: 8px;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}

.menu-toggle:hover {
    background: #f0f7ff;
    transform: scale(1.05);
}

.menu-toggle:active {
    transform: scale(0.95);
}

.hamburger-icon {
    width: 24px;
    height: 20px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.hamburger-icon span {
    display: block;
    height: 3px;
    width: 100%;
    background: #0066cc;
    border-radius: 3px;
    transition: all 0.3s ease;
}

.menu-toggle.active .hamburger-icon span:nth-child(1) {
    transform: translateY(8.5px) rotate(45deg);
}

.menu-toggle.active .hamburger-icon span:nth-child(2) {
    opacity: 0;
}

.menu-toggle.active .hamburger-icon span:nth-child(3) {
    transform: translateY(-8.5px) rotate(-45deg);
}

/* Sidebar overlay */
.sidebar-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1500;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease, visibility 0.3s ease;
}

.sidebar-overlay.active {
    opacity: 1;
    visibility: visible;
}

/* Sidebar */
.nav-sidebar {
    position: fixed;
    top: 0;
    right: -280px;
    width: 280px;
    height: 100%;
    background: white;
    z-index: 1600;
    box-shadow: -4px 0 16px rgba(0,0,0,0.2);
    transition: right 0.3s ease;
    overflow-y: auto;
}

.nav-sidebar.active {
    right: 0;
}

.sidebar-header {
    background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
    color: white;
    padding: 1.5rem;
    position: sticky;
    top: 0;
    z-index: 10;
}

.sidebar-header h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
}

.sidebar-header p {
    margin: 0.25rem 0 0 0;
    font-size: 0.875rem;
    opacity: 0.9;
}

.sidebar-nav {
    padding: 1rem 0;
}

.sidebar-nav-item {
    display: block;
    padding: 1rem 1.5rem;
    color: #333;
    text-decoration: none;
    font-weight: 600;
    font-size: 1rem;
    border-left: 4px solid transparent;
    transition: all 0.2s ease;
    cursor: pointer;
}

.sidebar-nav-item:hover {
    background: #f0f7ff;
    border-left-color: #0066cc;
}

.sidebar-nav-item.active {
    background: #e6f2ff;
    border-left-color: #0066cc;
    color: #0066cc;
}

/* Hide old navigation tabs container on mobile */
.nav-tabs-container {
    display: none;
}

/* Adjust navbar for hamburger menu */
.navbar {
    padding-right: 60px; /* Space for hamburger button */
}

/* Desktop: show tabs, hide hamburger */
@media (min-width: 768px) {
    .menu-toggle {
        display: none;
    }
    
    .nav-tabs-container {
        display: block;
    }
    
    .nav-sidebar {
        display: none;
    }
}
</style>
"""

# Meta tags for mobile optimization
MOBILE_META_TAGS = """
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#0066cc">
"""


def get_theme():
    """Return mobile-optimized theme."""
    return theme.flatly


def get_mobile_css():
    """Return mobile CSS string for head injection."""
    return MOBILE_CSS


def get_mobile_meta():
    """Return mobile meta tags string for head injection."""
    return MOBILE_META_TAGS
