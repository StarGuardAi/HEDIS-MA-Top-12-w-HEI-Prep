"""
Alert Center - Desktop Version
Intelligent alert system with priority inbox and filtering
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time

from utils.database import show_db_status
from utils.alert_system import AlertSystem, AlertType, AlertPriority
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# Page configuration
st.set_page_config(
    page_title="Alert Center - HEDIS Portfolio",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="auto"  # Auto: Let Streamlit decide based on screen size (iOS Safari optimized)
)

# ========== AGGRESSIVE SPACING REDUCTION ==========
# MATCHED TO INTERVENTION PERFORMANCE ANALYSIS PAGE (Perfect Spacing Template)
st.markdown("""
<style>
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

/* Zero-top enforcement - Headers flush to top */
.main > div:first-child {
    padding-top: 0 !important;
    margin-top: 0 !important;
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
    padding-top: 0rem !important;
}

.stMarkdown {
    margin-bottom: 0.25rem !important;
}

div[data-testid="stMetric"] {
    padding: 0.25rem !important;
}
</style>
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
    padding: 0.5rem 1rem;
    border-radius: 10px;
    margin-top: -1rem !important;
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
        margin-top: -1rem !important;
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
        padding-top: 0rem !important;
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

# Page header (already rendered above)

# Apply sidebar styling (purple gradient matching StarGuard AI header)
from utils.sidebar_styling import apply_sidebar_styling
apply_sidebar_styling()

# Custom CSS
st.markdown("""
<style>
    .alert-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    
    .alert-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    .alert-critical {
        border-left-color: #cc0000;
        background: #ffe6e6;
    }
    
    .alert-high {
        border-left-color: #ff6600;
        background: #fff4e6;
    }
    
    .alert-medium {
        border-left-color: #ffcc00;
        background: #fffef0;
    }
    
    .alert-low {
        border-left-color: #0066cc;
        background: #e6f3ff;
    }
    
    .alert-unread {
        font-weight: 600;
    }
    
    .alert-read {
        opacity: 0.7;
    }
    
    .priority-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .badge-critical {
        background: #cc0000;
        color: white;
    }
    
    .badge-high {
        background: #ff6600;
        color: white;
    }
    
    .badge-medium {
        background: #ffcc00;
        color: #333;
    }
    
    .badge-low {
        background: #0066cc;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'alert_system' not in st.session_state:
    st.session_state.alert_system = AlertSystem()
if 'alerts_generated' not in st.session_state:
    st.session_state.alerts_generated = False
    # Auto-generate alerts on page load
    try:
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        _ = st.session_state.alert_system.generate_all_alerts(start_date, end_date)
        st.session_state.alerts_generated = True
    except Exception:
        pass  # Silently fail if generation fails on init

# Sidebar
# Sidebar value proposition
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

st.sidebar.header("🔔 Alert Center")
st.sidebar.markdown("Monitor HEDIS portfolio for risks and opportunities.")

# Alert configuration
with st.sidebar.expander("⚙️ Alert Configuration"):
    star_threshold = st.number_input(
        "Star Rating Threshold (%)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.alert_system.config.get("star_rating_threshold", 85.0),
        step=1.0,
        key="star_threshold"
    )
    
    opportunity_threshold = st.number_input(
        "Opportunity Value Threshold ($)",
        min_value=0,
        value=int(st.session_state.alert_system.config.get("opportunity_value_threshold", 10000)),
        step=1000,
        key="opportunity_threshold"
    )
    
    deadline_days = st.number_input(
        "Deadline Alert Days Ahead",
        min_value=1,
        max_value=90,
        value=st.session_state.alert_system.config.get("deadline_days_ahead", 30),
        key="deadline_days"
    )
    
    anomaly_threshold = st.slider(
        "Anomaly Threshold (%)",
        min_value=5,
        max_value=50,
        value=int(st.session_state.alert_system.config.get("anomaly_threshold", 0.15) * 100),
        key="anomaly_threshold"
    )
    
    # Alert type toggles
    st.markdown("**Enabled Alert Types:**")
    enable_star = st.checkbox("Star Rating Risks", value=True, key="enable_star")
    enable_opp = st.checkbox("Opportunities", value=True, key="enable_opp")
    enable_deadline = st.checkbox("Deadlines", value=True, key="enable_deadline")
    enable_anomaly = st.checkbox("Performance Anomalies", value=True, key="enable_anomaly")
    
    enabled_types = []
    if enable_star:
        enabled_types.append(AlertType.STAR_RATING_RISK)
    if enable_opp:
        enabled_types.append(AlertType.OPPORTUNITY)
    if enable_deadline:
        enabled_types.append(AlertType.DEADLINE)
    if enable_anomaly:
        enabled_types.append(AlertType.PERFORMANCE_ANOMALY)
    
    # Update config
    if st.button("💾 Save Configuration", use_container_width=True):
        st.session_state.alert_system.update_config({
            "star_rating_threshold": star_threshold,
            "opportunity_value_threshold": float(opportunity_threshold),
            "deadline_days_ahead": deadline_days,
            "anomaly_threshold": anomaly_threshold / 100.0,
            "enabled_alert_types": enabled_types
        })
        st.success("Configuration saved!")
        st.session_state.alerts_generated = False  # Regenerate alerts

# Sidebar value proposition - at bottom
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

# Sidebar footer
render_sidebar_footer()

# Main content
st.title("🔔 Alert Center")
st.markdown("Intelligent monitoring for HEDIS portfolio risks and opportunities")

# Generate alerts
col1, col2, col3 = st.columns([2, 1, 1], gap="small")
with col1:
    if st.button("🔄 Generate Alerts", type="primary", use_container_width=True):
        with st.spinner("Analyzing portfolio and generating alerts..."):
            try:
                start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
                end_date = datetime.now().strftime("%Y-%m-%d")
                alerts = st.session_state.alert_system.generate_all_alerts(start_date, end_date)
                st.session_state.alerts_generated = True
                if len(alerts) > 0:
                    st.success(f"✅ Generated {len(alerts)} alerts")
                else:
                    st.info(f"ℹ️ Generated {len(alerts)} alerts. No issues detected - your portfolio is performing well!")
            except Exception as e:
                st.error(f"❌ Error generating alerts: {str(e)}")
                st.info("💡 Check database connection and ensure data is available for analysis.")
                st.exception(e)

with col2:
    if st.button("✅ Mark All Read", use_container_width=True):
        st.session_state.alert_system.mark_all_as_read()
        st.rerun()

with col3:
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.alert_system.alert_history = []
        st.rerun()

# Alert statistics
stats = st.session_state.alert_system.get_alert_stats()

if stats["total"] > 0:
    st.markdown("---")
    st.subheader("📊 Alert Statistics")
    
    stat_cols = st.columns(4, gap="small")
    with stat_cols[0]:
        st.metric("Total Alerts", stats["total"])
    with stat_cols[1]:
        st.metric("Unread", stats["unread"], delta=f"-{stats['read']} read")
    with stat_cols[2]:
        critical_count = stats["by_priority"].get("critical", 0)
        st.metric("Critical", critical_count)
    with stat_cols[3]:
        high_count = stats["by_priority"].get("high", 0)
        st.metric("High Priority", high_count)
    
    # Filter options
    st.markdown("---")
    st.subheader("📋 Priority Inbox")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3, gap="small")
    
    with filter_col1:
        filter_type = st.selectbox(
            "Filter by Type",
            options=[None, "star_rating_risk", "opportunity", "deadline", "performance_anomaly"],
            format_func=lambda x: "All Types" if x is None else x.replace("_", " ").title(),
            key="filter_type"
        )
    
    with filter_col2:
        filter_priority = st.selectbox(
            "Filter by Priority",
            options=[None, "critical", "high", "medium", "low"],
            format_func=lambda x: "All Priorities" if x is None else x.title(),
            key="filter_priority"
        )
    
    with filter_col3:
        show_unread_only = st.checkbox("Unread Only", value=False, key="show_unread_only")
    
    # Get filtered alerts
    alerts = st.session_state.alert_system.get_alerts(
        alert_type=filter_type,
        priority=filter_priority,
        unread_only=show_unread_only
    )
    
    if alerts:
        st.info(f"Showing {len(alerts)} alert(s)")
        
        # Display alerts
        for alert in alerts:
            priority = alert.get("priority", "low")
            is_read = alert.get("read", False)
            alert_type = alert.get("type", "unknown")
            
            # Determine CSS class
            priority_class = f"alert-{priority}"
            read_class = "alert-read" if is_read else "alert-unread"
            
            # Priority badge
            badge_class = f"badge-{priority}"
            
            with st.container():
                st.markdown(
                    f'<div class="alert-card {priority_class} {read_class}">',
                    unsafe_allow_html=True
                )
                
                col1, col2, col3 = st.columns([3, 1, 1], gap="small")
                
                with col1:
                    st.markdown(
                        f'<span class="priority-badge {badge_class}">{priority.upper()}</span>'
                        f'<strong>{alert.get("title", "Alert")}</strong>',
                        unsafe_allow_html=True
                    )
                    st.caption(alert.get("message", ""))
                    st.caption(f"Type: {alert_type.replace('_', ' ').title()} | {alert.get('timestamp', '')}")
                
                with col2:
                    if not is_read:
                        if st.button("✅ Read", key=f"read_{alert.get('alert_id')}"):
                            st.session_state.alert_system.mark_as_read(alert.get("alert_id"))
                            st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{alert.get('alert_id')}"):
                        st.session_state.alert_system.delete_alert(alert.get("alert_id"))
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Visualizations
        st.markdown("---")
        st.subheader("📈 Alert Analysis")
        
        viz_col1, viz_col2 = st.columns(2, gap="small")
        
        with viz_col1:
            # Alerts by type
            type_counts = stats["by_type"]
            if type_counts:
                fig_type = px.pie(
                    values=list(type_counts.values()),
                    names=[t.replace("_", " ").title() for t in type_counts.keys()],
                    title="Alerts by Type"
                )
                st.plotly_chart(fig_type, use_container_width=True)
        
        with viz_col2:
            # Alerts by priority
            priority_counts = stats["by_priority"]
            if priority_counts:
                priority_order = ["critical", "high", "medium", "low"]
                priority_values = [priority_counts.get(p, 0) for p in priority_order]
                priority_labels = [p.title() for p in priority_order]
                
                fig_priority = px.bar(
                    x=priority_labels,
                    y=priority_values,
                    title="Alerts by Priority",
                    color=priority_values,
                    color_continuous_scale="Reds"
                )
                fig_priority.update_layout(showlegend=False)
                st.plotly_chart(fig_priority, use_container_width=True)
    
    else:
        st.info("No alerts match the selected filters.")
else:
    st.info("No alerts generated yet. Click 'Generate Alerts' to analyze your portfolio.")

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer

