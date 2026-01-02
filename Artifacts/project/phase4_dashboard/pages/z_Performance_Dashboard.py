"""
Performance Dashboard
Real-time performance metrics and benchmarking
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

from utils.performance_monitor import get_performance_monitor
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# Page configuration
st.set_page_config(
    page_title="Performance Dashboard - HEDIS Portfolio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"  # Auto: Let Streamlit decide based on screen size (iOS Safari optimized)
)

# Purple Sidebar Theme + White Home Label
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

/* ========== WHITE "HOME" LABEL - DESKTOP ========== */
[data-testid="stSidebarNav"] ul li:first-child a {
    font-size: 0 !important;
    background: rgba(255, 255, 255, 0.2) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    margin-bottom: 0.5rem !important;
    display: block !important;
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

/* Target by href for additional coverage */
[data-testid="stSidebarNav"] a[href="/"],
[data-testid="stSidebarNav"] a[href="./"],
[data-testid="stSidebarNav"] a[href*="app"] {
    font-size: 0 !important;
    background: rgba(255, 255, 255, 0.2) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
}

[data-testid="stSidebarNav"] a[href="/"]::before,
[data-testid="stSidebarNav"] a[href="./"]::before,
[data-testid="stSidebarNav"] a[href*="app"]::before {
    content: "🏠 Home" !important;
    font-size: 1.1rem !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    display: block !important;
    -webkit-text-fill-color: #FFFFFF !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
}

/* Hover state - brighter white */
[data-testid="stSidebarNav"] ul li:first-child a:hover,
[data-testid="stSidebarNav"] a[href="/"]:hover,
[data-testid="stSidebarNav"] a[href="./"]:hover {
    background: rgba(255, 255, 255, 0.3) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
}

[data-testid="stSidebarNav"] ul li:first-child a:hover::before,
[data-testid="stSidebarNav"] a[href="/"]:hover::before,
[data-testid="stSidebarNav"] a[href="./"]:hover::before {
    color: #FFFFFF !important;
}

/* ========== OTHER SIDEBAR LINKS - WHITE TEXT ========== */
/* Make all other sidebar navigation links white too */
[data-testid="stSidebarNav"] a {
    color: #FFFFFF !important;
}

[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a div,
[data-testid="stSidebarNav"] a p {
    color: #FFFFFF !important;
}

/* Active/selected page - lighter background */
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(255, 255, 255, 0.15) !important;
    color: #FFFFFF !important;
}

/* ========== MOBILE RESPONSIVE ========== */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
    }
    
    [data-testid="stSidebarNav"] ul li:first-child a {
        padding: 0.6rem 0.8rem !important;
    }
    
    [data-testid="stSidebarNav"] ul li:first-child a::before {
        font-size: 1rem !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    [data-testid="stSidebarNav"] a[href="/"]::before,
    [data-testid="stSidebarNav"] a[href="./"]::before {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    /* Mobile sidebar links - white */
    [data-testid="stSidebarNav"] a {
        color: #FFFFFF !important;
    }
}

/* Mobile drawer open state */
[data-testid="stSidebar"][aria-expanded="true"] {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarNav"] a[href="/"]::before,
[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarNav"] a[href="./"]::before {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Force white on ALL child elements */
[data-testid="stSidebarNav"] li:first-child *,
[data-testid="stSidebarNav"] a[href="/"] *,
[data-testid="stSidebarNav"] a[href="./"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Sidebar collapse button - white */
[data-testid="collapsedControl"] {
    color: #FFFFFF !important;
}

/* ========== HEADER CONTAINER STYLES (Match Home Page) ========== */
.header-container {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%);
    padding: 0.5rem 1rem;
    border-radius: 10px;
    margin-top: 1.5rem;
    margin-bottom: 0.3rem;
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
</style>
""", unsafe_allow_html=True)


# Responsive Header - Adapts to Desktop/Mobile (Match Home Page)
st.markdown("""
<div class="header-container">
    <div class="header-title">⭐ StarGuard AI | Turning Data Into Stars</div>
    <div class="header-subtitle">Powered by Predictive Analytics & Machine Learning</div>
</div>
""", unsafe_allow_html=True)

# ========== AGGRESSIVE SPACING REDUCTION ==========
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

# Improved compact CSS - READABLE fonts, reduced spacing only
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
    
    /* Ensure chart titles wrap - target SVG text elements */
    .js-plotly-plot .gtitle text,
    .plotly .gtitle text {
        word-wrap: break-word !important;
        white-space: normal !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Page header (already rendered above)

# Apply sidebar styling (purple gradient matching StarGuard AI header)
from utils.sidebar_styling import apply_sidebar_styling
apply_sidebar_styling()

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .metric-pass {
        border-left-color: #00cc66;
        background: #f0fff4;
    }
    
    .metric-fail {
        border-left-color: #cc0000;
        background: #ffe6e6;
    }
    
    .metric-warning {
        border-left-color: #ffcc00;
        background: #fffef0;
    }
    
    .benchmark-status {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-pass {
        background: #00cc66;
        color: white;
    }
    
    .status-fail {
        background: #cc0000;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize performance monitor in session state
if 'performance_monitor' not in st.session_state:
    st.session_state.performance_monitor = get_performance_monitor()
    st.session_state.performance_monitor.start_tracing()
    # Initialize with some sample metrics if empty
    if st.session_state.performance_monitor.metrics["cache_hits"] == 0:
        # Simulate some cache activity to show the dashboard working
        st.session_state.performance_monitor.track_cache("sample_key", True)
        st.session_state.performance_monitor.track_cache("sample_key2", True)
        st.session_state.performance_monitor.track_cache("sample_key3", False)
        # Add some sample timing data
        st.session_state.performance_monitor.track_data_fetch(0.45)
        st.session_state.performance_monitor.track_render(0.25)
        st.session_state.performance_monitor.track_filter(0.35)
        st.session_state.performance_monitor.track_export(1.2)

monitor = st.session_state.performance_monitor

# Take a memory snapshot (keep last 50 snapshots)
memory = monitor.get_memory_usage()
monitor.metrics["memory_snapshots"].append({
    "timestamp": datetime.now().isoformat(),
    "memory_mb": memory["current_mb"]
})
# Keep only last 50 snapshots to prevent memory bloat
if len(monitor.metrics["memory_snapshots"]) > 50:
    monitor.metrics["memory_snapshots"] = monitor.metrics["memory_snapshots"][-50:]

# Sidebar
st.sidebar.header("⚡ Performance Dashboard")
st.sidebar.markdown("Monitor performance metrics and benchmarks")

# Auto-refresh option
auto_refresh = st.sidebar.checkbox("Auto-refresh (5s)", value=False, key="perf_auto_refresh")
if auto_refresh:
    time.sleep(5)
    st.rerun()

# Reset metrics
if st.sidebar.button("🔄 Reset Metrics", type="secondary", use_container_width=True):
    monitor.reset_metrics()
    # Re-initialize with sample data
    monitor.track_cache("sample_key", True)
    monitor.track_cache("sample_key2", True)
    monitor.track_cache("sample_key3", False)
    monitor.track_data_fetch(0.45)
    monitor.track_render(0.25)
    monitor.track_filter(0.35)
    monitor.track_export(1.2)
    st.rerun()

# Sidebar value proposition - at bottom
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

# Sidebar footer
render_sidebar_footer()

# Main content
st.title("⚡ Performance Dashboard")
st.markdown("Real-time performance metrics, benchmarks, and optimization tracking")

# Get performance summary
summary = monitor.get_performance_summary()
benchmarks = monitor.check_benchmarks()

# Overview metrics
st.header("📊 Performance Overview")

overview_cols = st.columns(4, gap="small")

with overview_cols[0]:
    cache_rate = summary["cache_hit_rate"] * 100
    st.metric(
        "Cache Hit Rate",
        f"{cache_rate:.1f}%",
        delta=f"Target: {monitor.benchmarks['optimization']['cache_hit_rate']*100:.0f}%"
    )

with overview_cols[1]:
    memory_mb = summary["memory_current_mb"]
    st.metric(
        "Memory Usage",
        f"{memory_mb:.1f} MB",
        delta=f"Peak: {summary['memory_peak_mb']:.1f} MB"
    )

with overview_cols[2]:
    session_kb = summary["session_state_size_kb"]
    st.metric(
        "Session State",
        f"{session_kb:.1f} KB",
        delta=None
    )

with overview_cols[3]:
    total_operations = (
        summary["cache_hits"] + summary["cache_misses"] +
        len(summary["function_timings"])
    )
    st.metric(
        "Total Operations",
        f"{total_operations:,}",
        delta=None
    )

# Desktop Benchmarks
st.markdown("---")
st.header("🖥️ Desktop Performance Benchmarks")

desktop_benchmarks = monitor.benchmarks["desktop"]
desktop_results = benchmarks.get("desktop", {})

benchmark_cols = st.columns(2, gap="small")

with benchmark_cols[0]:
    # Initial Load
    st.subheader("Initial Load")
    target_load = desktop_benchmarks["initial_load"]
    # Simulate or use actual measurement
    st.metric("Target", f"< {target_load}s")
    st.info("💡 Measure actual load time using browser DevTools")
    
    # Time to Interactive
    st.subheader("Time to Interactive")
    target_tti = desktop_benchmarks["time_to_interactive"]
    st.metric("Target", f"< {target_tti}s")
    st.info("💡 Measure using Lighthouse or Performance API")

with benchmark_cols[1]:
    # Chart Render
    if "chart_render" in desktop_results:
        result = desktop_results["chart_render"]
        status_class = "metric-pass" if result["status"] == "pass" else "metric-fail"
        status_badge = "status-pass" if result["status"] == "pass" else "status-fail"
        
        st.markdown(
            f'<div class="metric-card {status_class}">'
            f'<h3>Chart Render</h3>'
            f'<p><strong>Actual:</strong> {result["actual"]:.3f}s</p>'
            f'<p><strong>Target:</strong> < {result["target"]:.1f}s</p>'
            f'<span class="benchmark-status {status_badge}">{result["status"].upper()}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.metric("Chart Render", f"Target: < {desktop_benchmarks['chart_render']}s")
    
    # Filter Apply
    if "filter_apply" in desktop_results:
        result = desktop_results["filter_apply"]
        status_class = "metric-pass" if result["status"] == "pass" else "metric-fail"
        status_badge = "status-pass" if result["status"] == "pass" else "status-fail"
        
        st.markdown(
            f'<div class="metric-card {status_class}">'
            f'<h3>Filter Apply</h3>'
            f'<p><strong>Actual:</strong> {result["actual"]:.3f}s</p>'
            f'<p><strong>Target:</strong> < {result["target"]:.1f}s</p>'
            f'<span class="benchmark-status {status_badge}">{result["status"].upper()}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.metric("Filter Apply", f"Target: < {desktop_benchmarks['filter_apply']}s")
    
    # Export Generation
    if "export_generation" in desktop_results:
        result = desktop_results["export_generation"]
        status_class = "metric-pass" if result["status"] == "pass" else "metric-fail"
        status_badge = "status-pass" if result["status"] == "pass" else "status-fail"
        
        st.markdown(
            f'<div class="metric-card {status_class}">'
            f'<h3>Export Generation</h3>'
            f'<p><strong>Actual:</strong> {result["actual"]:.3f}s</p>'
            f'<p><strong>Target:</strong> < {result["target"]:.1f}s</p>'
            f'<span class="benchmark-status {status_badge}">{result["status"].upper()}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.metric("Export Generation", f"Target: < {desktop_benchmarks['export_generation']}s")

# Mobile Benchmarks
st.markdown("---")
st.header("📱 Mobile Performance Benchmarks")

mobile_benchmarks = monitor.benchmarks["mobile"]

mobile_cols = st.columns(3, gap="small")

with mobile_cols[0]:
    st.metric("Initial Load", f"Target: < {mobile_benchmarks['initial_load']}s")
    st.caption("4G network conditions")

with mobile_cols[1]:
    st.metric("Time to Interactive", f"Target: < {mobile_benchmarks['time_to_interactive']}s")

with mobile_cols[2]:
    st.metric("Chart Render", f"Target: < {mobile_benchmarks['chart_render']}s")

st.info("💡 Mobile benchmarks require testing on actual devices or BrowserStack")

# Optimization Targets
st.markdown("---")
st.header("🎯 Optimization Targets")

opt_results = benchmarks.get("optimization", {})
opt_benchmarks = monitor.benchmarks["optimization"]

opt_cols = st.columns(4, gap="small")

with opt_cols[0]:
    if "cache_hit_rate" in opt_results:
        result = opt_results["cache_hit_rate"]
        status_class = "metric-pass" if result["status"] == "pass" else "metric-fail"
        st.markdown(
            f'<div class="metric-card {status_class}">'
            f'<h4>Cache Hit Rate</h4>'
            f'<p><strong>{result["actual"]*100:.1f}%</strong> / {result["target"]*100:.0f}%</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.metric("Cache Hit Rate", f"Target: > {opt_benchmarks['cache_hit_rate']*100:.0f}%")

with opt_cols[1]:
    if "data_fetch_time" in opt_results:
        result = opt_results["data_fetch_time"]
        status_class = "metric-pass" if result["status"] == "pass" else "metric-fail"
        st.markdown(
            f'<div class="metric-card {status_class}">'
            f'<h4>Data Fetch</h4>'
            f'<p><strong>{result["actual"]:.3f}s</strong> / < {result["target"]:.1f}s</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.metric("Data Fetch", f"Target: < {opt_benchmarks['data_fetch_time']}s")

with opt_cols[2]:
    if "rerender_time" in opt_results:
        result = opt_results["rerender_time"]
        status_class = "metric-pass" if result["status"] == "pass" else "metric-fail"
        st.markdown(
            f'<div class="metric-card {status_class}">'
            f'<h4>Re-render Time</h4>'
            f'<p><strong>{result["actual"]:.3f}s</strong> / < {result["target"]:.1f}s</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.metric("Re-render", f"Target: < {opt_benchmarks['rerender_time']}s")

with opt_cols[3]:
    st.metric("Bundle Size", f"Target: < {opt_benchmarks['bundle_size_mb']} MB")
    st.caption("Streamlit app bundle")

# Detailed Metrics
st.markdown("---")
st.header("📈 Detailed Metrics")

# Function Timings
if summary["function_timings"]:
    st.subheader("Function Execution Times")
    
    timing_data = []
    for func_name, timing_info in summary["function_timings"].items():
        timing_data.append({
            "Function": func_name,
            "Avg (s)": timing_info["avg"],
            "Min (s)": timing_info["min"],
            "Max (s)": timing_info["max"],
            "Count": timing_info["count"]
        })
    
    timing_df = pd.DataFrame(timing_data)
    st.dataframe(timing_df, use_container_width=True, hide_index=True)
    
    # Visualization
    if not timing_df.empty:
        fig = px.bar(
            timing_df,
            x="Function",
            y="Avg (s)",
            title="Average Function Execution Times",
            color="Avg (s)",
            color_continuous_scale="Reds"
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black', size=12),
            xaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(color='black')),
            yaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(color='black')),
            title_font=dict(color='black', size=16)
        )
        fig.update_traces(textfont_color='black', marker_line_color='black', marker_line_width=1)
        st.plotly_chart(fig, use_container_width=True)

# Cache Performance
st.subheader("Cache Performance")

cache_cols = st.columns(3, gap="small")

with cache_cols[0]:
    st.metric("Cache Hits", f"{summary['cache_hits']:,}")
with cache_cols[1]:
    st.metric("Cache Misses", f"{summary['cache_misses']:,}")
with cache_cols[2]:
    st.metric("Hit Rate", f"{summary['cache_hit_rate']*100:.1f}%")

# Cache hit rate visualization
if summary["cache_hits"] + summary["cache_misses"] > 0:
    fig_cache = go.Figure(data=[
        go.Pie(
            labels=["Hits", "Misses"],
            values=[summary["cache_hits"], summary["cache_misses"]],
            hole=0.3,
            marker=dict(colors=['#00cc66', '#ff6600'], line=dict(color='white', width=2)),
            textfont=dict(color='black', size=14)
        )
    ])
    fig_cache.update_layout(
        title=dict(text="Cache Performance", font=dict(color='black', size=16)),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12)
    )
    st.plotly_chart(fig_cache, use_container_width=True)

# Memory Usage
st.subheader("Memory Usage")

memory_cols = st.columns(2, gap="small")

with memory_cols[0]:
    st.metric("Current Memory", f"{summary['memory_current_mb']:.2f} MB")
with memory_cols[1]:
    st.metric("Peak Memory", f"{summary['memory_peak_mb']:.2f} MB")

# Memory trend (if we have snapshots)
if monitor.metrics["memory_snapshots"]:
    memory_df = pd.DataFrame(monitor.metrics["memory_snapshots"])
    # Convert timestamp to datetime if it's a string
    if memory_df['timestamp'].dtype == 'object':
        memory_df['timestamp'] = pd.to_datetime(memory_df['timestamp'])
    
    fig_memory = px.line(
        memory_df,
        x="timestamp",
        y="memory_mb",
        title="Memory Usage Over Time",
        color_discrete_sequence=['#0066cc']
    )
    fig_memory.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        xaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(color='black')),
        yaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(color='black'), title="Memory (MB)"),
        title_font=dict(color='black', size=16)
    )
    fig_memory.update_traces(line=dict(width=3), marker=dict(size=8))
    st.plotly_chart(fig_memory, use_container_width=True)

# Data Processing Times
st.subheader("Data Processing Times")

if summary["avg_data_fetch"] > 0 or summary["avg_render"] > 0 or summary["avg_filter"] > 0:
    processing_data = {
        "Operation": ["Data Fetch", "Render", "Filter", "Export"],
        "Average Time (s)": [
            summary["avg_data_fetch"],
            summary["avg_render"],
            summary["avg_filter"],
            summary["avg_export"]
        ]
    }
    processing_df = pd.DataFrame(processing_data)
    processing_df = processing_df[processing_df["Average Time (s)"] > 0]
    
    if not processing_df.empty:
        fig_processing = px.bar(
            processing_df,
            x="Operation",
            y="Average Time (s)",
            title="Average Processing Times",
            color="Average Time (s)",
            color_continuous_scale="Blues"
        )
        fig_processing.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black', size=12),
            xaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(color='black')),
            yaxis=dict(showgrid=True, gridcolor='#e0e0e0', title_font=dict(color='black')),
            title_font=dict(color='black', size=16)
        )
        fig_processing.update_traces(textfont_color='black', marker_line_color='black', marker_line_width=1)
        st.plotly_chart(fig_processing, use_container_width=True)

# Benchmark Status Summary
st.markdown("---")
st.header("✅ Benchmark Status Summary")

# Count pass/fail
all_results = []
for category, results in benchmarks.items():
    if isinstance(results, dict):
        for metric, result in results.items():
            if isinstance(result, dict) and "status" in result:
                all_results.append({
                    "Category": category.title(),
                    "Metric": metric.replace("_", " ").title(),
                    "Status": result["status"],
                    "Actual": result.get("actual", 0),
                    "Target": result.get("target", 0)
                })

if all_results:
    results_df = pd.DataFrame(all_results)
    
    # Status counts
    status_counts = results_df["Status"].value_counts()
    
    status_cols = st.columns(3, gap="small")
    with status_cols[0]:
        st.metric("Passed", status_counts.get("pass", 0))
    with status_cols[1]:
        st.metric("Failed", status_counts.get("fail", 0))
    with status_cols[2]:
        total = len(results_df)
        pass_count = status_counts.get("pass", 0)
        pass_rate = (pass_count / total * 100) if total > 0 else 0
        st.metric("Pass Rate", f"{pass_rate:.1f}%")
    
    # Detailed table
    st.dataframe(results_df, use_container_width=True, hide_index=True)
else:
    st.info("ℹ️ No benchmark results available yet. Metrics will appear as operations are tracked.")

# Export metrics
st.markdown("---")
st.header("📥 Export Metrics")

if st.button("📊 Export Performance Data", use_container_width=True):
    metrics_export = monitor.export_metrics()
    import json
    export_json = json.dumps(metrics_export, indent=2)
    
    st.download_button(
        "Download JSON",
        export_json,
        file_name=f"performance_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

# Value Proposition Footer
# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer

# Instructions
with st.expander("ℹ️ How to Use"):
    st.markdown("""
    ### Performance Monitoring
    
    1. **Automatic Tracking**: Functions decorated with `@track_performance` are automatically timed
    2. **Cache Tracking**: Cache hits/misses are tracked automatically
    3. **Memory Monitoring**: Memory usage is tracked continuously
    4. **Benchmark Comparison**: Metrics are compared against targets automatically
    
    ### Improving Performance
    
    - **Cache Hit Rate**: Use `@st.cache_data` and `@st.cache_resource` decorators
    - **Data Fetch Time**: Optimize database queries, use indexes
    - **Render Time**: Use `st.experimental_fragment` for granular updates
    - **Memory**: Clear session state when not needed
    
    ### Tools
    
    - **Chrome DevTools**: Performance tab for detailed profiling
    - **Streamlit Profiler**: Built-in performance monitoring
    - **This Dashboard**: Real-time metrics and benchmarks
    """)

