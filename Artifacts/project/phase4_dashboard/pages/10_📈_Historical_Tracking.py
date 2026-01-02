"""
Historical Performance Tracking - Desktop Version
Full interactive time-series explorer with forecasting
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

from utils.database import show_db_status, execute_query
from utils.historical_tracking import HistoricalTracker
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# Page configuration
st.set_page_config(
    page_title="Historical Tracking - HEDIS Portfolio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto"  # Auto: Let Streamlit decide based on screen size (iOS Safari optimized)
)

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
    
    /* Mobile sidebar links - white text */
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
    padding: 0.5rem 0.75rem 0.6rem 0.75rem;
    border-radius: 6px;
    margin-top: 1.5rem;
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

# ========== MOBILE DETECTION ==========
# Use a toggle in sidebar for now, or detect via CSS
# For automatic detection, we'll use CSS classes to show/hide content
def is_mobile():
    """Detect if user is on mobile device - simplified version"""
    # Check if mobile toggle is set in session state
    # Default to False (desktop) - user can toggle if needed
    return st.session_state.get('force_mobile', False)

# Add mobile toggle in sidebar (optional - can be removed for automatic detection)
# For now, we'll render both versions and use CSS to show/hide

# Apply sidebar styling (purple gradient matching StarGuard AI header)
from utils.sidebar_styling import apply_sidebar_styling
apply_sidebar_styling()

# Custom CSS
st.markdown("""
<style>
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-on-track {
        background: #00cc66;
        color: white;
    }
    
    .status-at-risk {
        background: #ffcc00;
        color: #333;
    }
    
    .status-critical {
        background: #cc0000;
        color: white;
    }
    
    .status-unknown {
        background: #999999;
        color: white;
    }
    
    .trend-indicator {
        display: inline-block;
        margin-left: 0.5rem;
        font-size: 1.2rem;
    }
    
    .trend-up {
        color: #00cc66;
    }
    
    .trend-down {
        color: #cc0000;
    }
    
    .trend-stable {
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'historical_tracker' not in st.session_state:
    st.session_state.historical_tracker = HistoricalTracker()

# Sidebar
st.sidebar.header("📈 Historical Tracking")
st.sidebar.markdown("Track performance over time with forecasting")

# Date range selector
st.sidebar.subheader("📅 Date Range")
default_end = datetime.now().strftime("%Y-%m-%d")
default_start = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

start_date = st.sidebar.date_input(
    "Start Date",
    value=datetime.strptime(default_start, "%Y-%m-%d"),
    max_value=datetime.now(),
    format="MM/DD/YYYY"
)
end_date = st.sidebar.date_input(
    "End Date",
    value=datetime.strptime(default_end, "%Y-%m-%d"),
    max_value=datetime.now(),
    format="MM/DD/YYYY"
)

if start_date > end_date:
    st.sidebar.error("Start date must be before end date")
    st.stop()

start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# Measure selector
st.sidebar.subheader("🎯 Measure Selection")
view_option = st.sidebar.radio(
    "View",
    ["All Measures", "Single Measure"],
    index=0
)

selected_measure = None
if view_option == "Single Measure":
    measures_query = """
        SELECT DISTINCT mi.measure_id, hm.measure_name
        FROM member_interventions mi
        LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
        ORDER BY hm.measure_name
    """
    measures_df = execute_query(measures_query)
    
    if not measures_df.empty:
        measure_options = [f"{row['measure_name']} ({row['measure_id']})" 
                          for _, row in measures_df.iterrows()]
        selected_measure_display = st.sidebar.selectbox("Select Measure", measure_options)
        if selected_measure_display:
            selected_measure = selected_measure_display.split("(")[1].split(")")[0]

# Target threshold
st.sidebar.subheader("⚙️ Settings")
target_success_rate = st.sidebar.number_input(
    "Target Success Rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=85.0,
    step=1.0,
    key="target_rate"
)

# Sidebar value proposition - at bottom
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

# Sidebar footer
render_sidebar_footer()

# Main content
st.title("📈 Historical Performance Tracking")
st.markdown("Track HEDIS measure performance over time with forecasting and trend analysis")

# Status overview
st.header("📊 Status Overview")
st.markdown("Current status for all measures")

status_df = st.session_state.historical_tracker.get_all_measures_status(target_success_rate)

if not status_df.empty:
    # Status summary - count each status type
    status_counts = status_df['status'].value_counts().to_dict()
    
    # Get counts for each status (handle missing keys)
    on_track = status_counts.get('on_track', 0)
    at_risk = status_counts.get('at_risk', 0)
    critical = status_counts.get('critical', 0)
    unknown = status_counts.get('unknown', 0)
    
    status_cols = st.columns(4, gap="small")
    with status_cols[0]:
        st.metric("On Track", on_track, delta=None if on_track == 0 else None)
    with status_cols[1]:
        st.metric("At Risk", at_risk, delta=None if at_risk == 0 else None)
    with status_cols[2]:
        st.metric("Critical", critical, delta=None if critical == 0 else None)
    with status_cols[3]:
        st.metric("Total Measures", len(status_df))
    
    # Show helpful info messages based on status distribution
    if unknown == len(status_df) and len(status_df) > 0:
        st.info("ℹ️ **No performance data available yet.** Status will update once interventions are completed and tracked in the system.")
    elif unknown > 0 and (on_track == 0 and at_risk == 0):
        st.info(f"ℹ️ {unknown} measure(s) have no data yet. {critical} measure(s) are below target. Status will update as data becomes available.")
    elif on_track == 0 and at_risk == 0 and critical == len(status_df):
        st.warning("⚠️ **All measures are currently below target.** Consider reviewing intervention strategies to improve performance.")
    
    # Status table with proper HTML rendering
    # Add table header
    col1, col2, col3, col4, col5 = st.columns([3, 2, 1.5, 1.5, 1.5], gap="small")
    with col1:
        st.markdown("**Measure**")
    with col2:
        st.markdown("**Status**")
    with col3:
        st.markdown("**Current Rate**")
    with col4:
        st.markdown("**Target Rate**")
    with col5:
        st.markdown("**Variance**")
    st.markdown("---")
    
    # Display each measure row
    for _, row in status_df.iterrows():
        measure_name = row['measure_name']
        current_rate = row['current_rate']
        target_rate = row['target_rate']
        variance = row['variance']
        status = row['status']
        trend = row['trend']
        
        # Format status badge
        status_class = f"status-{status.replace('_', '-')}"
        status_text = status.replace('_', ' ').title()
        
        trend_symbol = "📈" if trend == "improving" else ("📉" if trend == "declining" else "➡️")
        trend_class = "trend-up" if trend == "improving" else ("trend-down" if trend == "declining" else "trend-stable")
        
        # Create table row with HTML
        col1, col2, col3, col4, col5 = st.columns([3, 2, 1.5, 1.5, 1.5], gap="small")
        
        with col1:
            st.markdown(f"**{measure_name}**")
        
        with col2:
            st.markdown(
                f'<span class="status-badge {status_class}">{status_text}</span> <span class="trend-indicator {trend_class}">{trend_symbol}</span>',
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(f"{current_rate:.1f}%")
        
        with col4:
            st.markdown(f"{target_rate:.1f}%")
        
        with col5:
            st.markdown(f"{variance:+.1f}%")
        
        st.markdown("---")
else:
    st.info("No status data available. Check date range and data availability.")

# ========== CHART FUNCTIONS ==========
def create_desktop_trend_chart(df, selected_measures):
    """Create interactive multi-line chart for desktop"""
    fig = go.Figure()
    
    # Color palette for measures
    colors = [
        '#6F5F96', '#E76F51', '#2A9D8F', '#E9C46A', '#F4A261',
        '#264653', '#E63946', '#A8DADC', '#457B9D', '#1D3557'
    ]
    
    for idx, measure in enumerate(selected_measures):
        # Filter data for this measure
        measure_data = df[df['measure_name'] == measure]
        
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(measure_data['month_start']),
            y=measure_data['success_rate'],
            name=measure,
            mode='lines+markers',
            line=dict(
                color=colors[idx % len(colors)],
                width=2.5
            ),
            marker=dict(
                size=7,
                symbol='circle'
            ),
            hovertemplate=(
                '<b>%{fullData.name}</b><br>' +
                'Month: %{x|%b %Y}<br>' +
                'Success Rate: %{y:.1f}%<br>' +
                '<extra></extra>'
            )
        ))
    
    fig.update_layout(
        title={
            'text': '📈 Monthly Success Rate Trends - All Measures',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#4A3D6F', 'family': 'Arial'}
        },
        xaxis=dict(
            title='Month',
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)',
            tickformat='%b %Y'
        ),
        yaxis=dict(
            title='Success Rate (%)',
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)',
            range=[0, 100]
        ),
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#4A3D6F',
            borderwidth=1
        ),
        height=600,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial', size=12, color='#333')
    )
    
    return fig

def create_mobile_sparkline(df, measure):
    """Create compact sparkline for mobile"""
    measure_data = df[df['measure_name'] == measure].sort_values('month_start')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=pd.to_datetime(measure_data['month_start']),
        y=measure_data['success_rate'],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#6F5F96', width=2),
        fillcolor='rgba(111, 95, 150, 0.2)',
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        height=80,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def render_mobile_measure_card(df, measure):
    """Render a single measure card for mobile"""
    measure_data = df[df['measure_name'] == measure].sort_values('month_start')
    
    if len(measure_data) == 0:
        return
    
    # Get latest values
    current_value = measure_data.iloc[-1]['success_rate']
    if len(measure_data) > 1:
        previous_value = measure_data.iloc[-2]['success_rate']
        change = current_value - previous_value
    else:
        change = 0
    
    # Create card
    with st.container():
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            padding: 0.75rem;
            border-radius: 8px;
            border-left: 4px solid #6F5F96;
            margin-bottom: 0.75rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="font-weight: 600; font-size: 0.9rem; color: #4A3D6F; margin-bottom: 0.5rem;">
                {measure}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sparkline
        fig = create_mobile_sparkline(df, measure)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Stats row
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 700; color: #4A3D6F;">
                    {current_value:.1f}%
                </div>
                <div style="font-size: 0.75rem; color: #6C757D;">
                    Current Rate
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
            color = "#2A9D8F" if change > 0 else "#E76F51" if change < 0 else "#6C757D"
            
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 700; color: {color};">
                    {arrow} {abs(change):.1f}%
                </div>
                <div style="font-size: 0.75rem; color: #6C757D;">
                    vs Last Month
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")

# Monthly trends
st.markdown("---")
st.header("📉 Monthly Trends")

trends_df = st.session_state.historical_tracker.get_monthly_trends(
    measure_id=selected_measure,
    start_date=start_date_str,
    end_date=end_date_str
)

if not trends_df.empty:
    # ========== RESPONSIVE MONTHLY TREND VISUALIZATION ==========
    
    # Get unique measures from data
    all_measures = sorted(trends_df['measure_name'].unique())
    
    # Render based on device type and view option
    if view_option == "All Measures":
        # Add CSS for responsive display
        st.markdown("""
        <style>
        @media (max-width: 768px) {
            .desktop-chart-container {
                display: none !important;
            }
        }
        @media (min-width: 769px) {
            .mobile-cards-container {
                display: none !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # ===== MOBILE VERSION - Vertical Scrollable Cards =====
        with st.container():
            st.markdown('<div class="mobile-cards-container">', unsafe_allow_html=True)
            st.markdown("### 📊 Monthly Trends by Measure")
            st.markdown("*Scroll to view all measures*")
            st.markdown("")
            
            # Render cards for each measure
            for measure in all_measures:
                render_mobile_measure_card(trends_df, measure)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ===== DESKTOP VERSION - Interactive Multi-Line Chart =====
        with st.container():
            st.markdown('<div class="desktop-chart-container">', unsafe_allow_html=True)
            st.markdown("### 📈 Interactive Trend Analysis")
        
        # Measure selector with select all option
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_measures = st.multiselect(
                "Select measures to display (click to toggle)",
                options=all_measures,
                default=all_measures[:5] if len(all_measures) > 5 else all_measures,
                help="Choose which measures to show on the chart"
            )
        
        with col2:
            if st.button("Select All", use_container_width=True):
                selected_measures = all_measures
                st.rerun()
            if st.button("Clear All", use_container_width=True):
                selected_measures = []
                st.rerun()
        
        # Show chart if measures selected
        if selected_measures:
            fig = create_desktop_trend_chart(trends_df, selected_measures)
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
            })
            
            # Summary statistics table below chart
            st.markdown("### 📊 Summary Statistics")
            
            summary_data = []
            for measure in selected_measures:
                measure_df = trends_df[trends_df['measure_name'] == measure].sort_values('month_start')
                
                if len(measure_df) > 0:
                    current = measure_df.iloc[-1]['success_rate']
                    if len(measure_df) > 1:
                        previous = measure_df.iloc[-2]['success_rate']
                        change = current - previous
                    else:
                        previous = current
                        change = 0
                    
                    avg_rate = measure_df['success_rate'].mean()
                    min_rate = measure_df['success_rate'].min()
                    max_rate = measure_df['success_rate'].max()
                    
                    summary_data.append({
                        'Measure': measure,
                        'Current Rate': f"{current:.1f}%",
                        'Change': f"{change:+.1f}%",
                        'Avg Rate': f"{avg_rate:.1f}%",
                        'Min': f"{min_rate:.1f}%",
                        'Max': f"{max_rate:.1f}%"
                    })
            
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("👆 Please select at least one measure to display the trend chart.")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Single measure detailed view
        measure_data = trends_df[trends_df['measure_id'] == selected_measure] if selected_measure else trends_df
        
        if not measure_data.empty:
            measure_name = measure_data['measure_name'].iloc[0]
            
            # Success rate trend
            fig_rate = go.Figure()
            fig_rate.add_trace(go.Scatter(
                x=pd.to_datetime(measure_data['month_start']),
                y=measure_data['success_rate'],
                mode='lines+markers',
                name='Success Rate',
                line=dict(color='#0066cc', width=2),
                fill='tonexty',
                fillcolor='rgba(0, 102, 204, 0.1)'
            ))
            
            # Add target line
            fig_rate.add_hline(
                y=target_success_rate,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Target: {target_success_rate}%"
            )
            
            fig_rate.update_layout(
                title=f"{measure_name} - Success Rate Trend",
                xaxis_title="Month",
                yaxis_title="Success Rate (%)",
                height=300
            )
            
            st.plotly_chart(fig_rate, use_container_width=True)
            
            # Interventions and closures
            fig_volume = go.Figure()
            fig_volume.add_trace(go.Bar(
                x=pd.to_datetime(measure_data['month_start']),
                y=measure_data['total_interventions'],
                name='Total Interventions',
                marker_color='#ffcc00'
            ))
            fig_volume.add_trace(go.Bar(
                x=pd.to_datetime(measure_data['month_start']),
                y=measure_data['successful_closures'],
                name='Successful Closures',
                marker_color='#00cc66'
            ))
            
            fig_volume.update_layout(
                title=f"{measure_name} - Intervention Volume",
                xaxis_title="Month",
                yaxis_title="Count",
                barmode='group',
                height=300
            )
            
            st.plotly_chart(fig_volume, use_container_width=True)
    
    # Forecast next quarter
    st.markdown("---")
    st.header("🔮 Next Quarter Forecast")
    
    if selected_measure or view_option == "Single Measure":
        forecast_measure = selected_measure if selected_measure else trends_df['measure_id'].iloc[0]
        
        with st.spinner("Generating forecast..."):
            forecast_df = st.session_state.historical_tracker.forecast_next_quarter(forecast_measure)
        
        if not forecast_df.empty:
            # Combine historical and forecast
            historical_data = trends_df[trends_df['measure_id'] == forecast_measure].tail(6)
            
            # Create combined chart
            fig_forecast = go.Figure()
            
            # Historical data
            fig_forecast.add_trace(go.Scatter(
                x=pd.to_datetime(historical_data['month_start']),
                y=historical_data['success_rate'],
                mode='lines+markers',
                name='Historical',
                line=dict(color='#0066cc', width=2)
            ))
            
            # Forecast data
            fig_forecast.add_trace(go.Scatter(
                x=pd.to_datetime(forecast_df['month_start']),
                y=forecast_df['forecasted_success_rate'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='#ff6600', width=2, dash='dash'),
                marker=dict(symbol='diamond')
            ))
            
            # Target line
            fig_forecast.add_hline(
                y=target_success_rate,
                line_dash="dot",
                line_color="red",
                annotation_text=f"Target: {target_success_rate}%"
            )
            
            fig_forecast.update_layout(
                title="Historical Trend with Next Quarter Forecast",
                xaxis_title="Month",
                yaxis_title="Success Rate (%)",
                height=300
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Forecast table
            forecast_display = forecast_df[['month', 'forecasted_success_rate', 'forecasted_interventions', 
                                           'forecasted_closures', 'forecasted_revenue']].copy()
            forecast_display.columns = ['Month', 'Forecasted Success Rate (%)', 'Forecasted Interventions', 
                                       'Forecasted Closures', 'Forecasted Revenue ($)']
            forecast_display['Forecasted Success Rate (%)'] = forecast_display['Forecasted Success Rate (%)'].apply(lambda x: f"{x:.1f}%")
            forecast_display['Forecasted Revenue ($)'] = forecast_display['Forecasted Revenue ($)'].apply(lambda x: f"${x:,.0f}")
            
            st.dataframe(forecast_display, use_container_width=True, hide_index=True)
    else:
        st.info("Select a single measure to view forecast")
else:
    st.info("No trend data available for selected filters.")

# Year-over-year comparison
st.markdown("---")
st.header("📅 Year-over-Year Comparison")

yoy_df = st.session_state.historical_tracker.get_year_over_year_comparison(
    measure_id=selected_measure
)

if not yoy_df.empty:
    # YoY comparison chart
    fig_yoy = go.Figure()
    
    fig_yoy.add_trace(go.Bar(
        x=yoy_df['measure_name'],
        y=yoy_df['current_success_rate'],
        name='Current Year',
        marker_color='#0066cc'
    ))
    
    fig_yoy.add_trace(go.Bar(
        x=yoy_df['measure_name'],
        y=yoy_df['previous_success_rate'],
        name='Previous Year',
        marker_color='#999999'
    ))
    
    fig_yoy.update_layout(
        title="Year-over-Year Success Rate Comparison",
        xaxis_title="Measure",
        yaxis_title="Success Rate (%)",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig_yoy, use_container_width=True)
    
    # YoY change indicators
    yoy_display = yoy_df[['measure_name', 'current_success_rate', 'previous_success_rate', 
                         'success_rate_change', 'revenue_change_pct']].copy()
    yoy_display.columns = ['Measure', 'Current Rate (%)', 'Previous Rate (%)', 
                           'Rate Change (%)', 'Revenue Change (%)']
    yoy_display['Current Rate (%)'] = yoy_display['Current Rate (%)'].apply(lambda x: f"{x:.1f}%")
    yoy_display['Previous Rate (%)'] = yoy_display['Previous Rate (%)'].apply(lambda x: f"{x:.1f}%")
    yoy_display['Rate Change (%)'] = yoy_display['Rate Change (%)'].apply(lambda x: f"{x:+.1f}%")
    yoy_display['Revenue Change (%)'] = yoy_display['Revenue Change (%)'].apply(lambda x: f"{x:+.1f}%")
    
    st.dataframe(yoy_display, use_container_width=True, hide_index=True)
else:
    st.info("No year-over-year comparison data available.")

# Seasonal patterns
st.markdown("---")
st.header("🌍 Seasonal Pattern Detection")

if selected_measure or view_option == "Single Measure":
    pattern_measure = selected_measure if selected_measure else trends_df['measure_id'].iloc[0] if not trends_df.empty else None
    
    if pattern_measure:
        with st.spinner("Analyzing seasonal patterns..."):
            patterns = st.session_state.historical_tracker.detect_seasonal_patterns(
                measure_id=pattern_measure,
                start_date=start_date_str,
                end_date=end_date_str
            )
        
        if patterns.get("has_seasonality"):
            st.success(f"✅ Seasonal pattern detected!")
            
            col1, col2 = st.columns(2, gap="small")
            with col1:
                st.metric("Peak Month", patterns.get("peak_month", "N/A"))
            with col2:
                st.metric("Low Month", patterns.get("low_month", "N/A"))
            
            st.caption(f"Seasonal variance: {patterns.get('seasonal_variance', 0):.2f}%")
            
            # Monthly averages chart
            if patterns.get("monthly_averages"):
                monthly_avg = patterns["monthly_averages"]
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                
                fig_seasonal = go.Figure()
                fig_seasonal.add_trace(go.Bar(
                    x=[months[i-1] for i in monthly_avg.keys()],
                    y=list(monthly_avg.values()),
                    marker_color='#0066cc'
                ))
                
                fig_seasonal.update_layout(
                    title="Average Success Rate by Month (Seasonal Pattern)",
                    xaxis_title="Month",
                    yaxis_title="Average Success Rate (%)",
                    height=300
                )
                
                st.plotly_chart(fig_seasonal, use_container_width=True)
        else:
            st.info("No significant seasonal pattern detected.")
else:
    st.info("Select a single measure to analyze seasonal patterns.")

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer

