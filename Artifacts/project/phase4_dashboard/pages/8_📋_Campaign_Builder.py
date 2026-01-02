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
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# Page configuration
st.set_page_config(
    page_title="Campaign Builder - HEDIS Portfolio",
    page_icon="📋",
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

/* All sidebar navigation links white */
[data-testid="stSidebarNav"] a {
    color: #FFFFFF !important;
}

[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a div,
[data-testid="stSidebarNav"] a p {
    color: #FFFFFF !important;
}

/* "Mobile Optimized" badge - white text */
[data-testid="stSidebar"] .element-container div[data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
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

# Custom CSS
st.markdown("""
<style>
    .campaign-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #0066cc;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .metric-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        background: #f0f4f8;
        margin: 0.25rem;
        font-weight: 600;
    }
    
    .coordinator-card {
        background: #e6f3ff;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'campaign_builder' not in st.session_state:
    st.session_state.campaign_builder = CampaignBuilder()
if 'selected_members' not in st.session_state:
    st.session_state.selected_members = []
if 'current_campaign' not in st.session_state:
    st.session_state.current_campaign = None
if 'campaigns' not in st.session_state:
    st.session_state.campaigns = []

# Sidebar
st.sidebar.header("📋 Campaign Builder")
st.sidebar.markdown("Build and manage HEDIS intervention campaigns.")
st.sidebar.markdown("---")

# Navigation
page_option = st.sidebar.radio(
    "Navigation",
    ["Build New Campaign", "View Campaigns", "Campaign Dashboard"],
    index=0
)

# Sidebar value proposition - at bottom
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

# Sidebar footer
render_sidebar_footer()

# Main content based on navigation
if page_option == "Build New Campaign":
    st.title("📋 Campaign Builder")
    st.markdown("Select members and build intervention campaigns with automatic coordinator assignment.")
    
    # Step 1: Filter and select members
    st.header("Step 1: Select Members")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3, gap="small")
    
    with filter_col1:
        # Get available measures - query all statuses first to see what's available
        try:
            all_measures_query = """
                SELECT DISTINCT mi.measure_id, hm.measure_name
                FROM member_interventions mi
                LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
                ORDER BY hm.measure_name
            """
            from utils.database import execute_query
            available_measures = execute_query(all_measures_query)
            measure_options = [None] + (available_measures['measure_id'].unique().tolist() if not available_measures.empty else [])
        except Exception as e:
            measure_options = [None]
        
        measure_filter = st.selectbox(
            "Filter by Measure",
            options=measure_options,
            format_func=lambda x: "All Measures" if x is None else x
        )
    
    with filter_col2:
        # Get available statuses from database
        try:
            status_query = """
                SELECT DISTINCT status
                FROM member_interventions
                ORDER BY status
            """
            from utils.database import execute_query
            status_df = execute_query(status_query)
            available_statuses = status_df['status'].unique().tolist() if not status_df.empty else []
            
            # If no statuses found, use defaults
            if not available_statuses:
                available_statuses = ["pending", "scheduled", "in_progress", "completed"]
            
            # Default to all available statuses if 'pending' and 'scheduled' aren't available
            default_statuses = []
            if "pending" in available_statuses:
                default_statuses.append("pending")
            if "scheduled" in available_statuses:
                default_statuses.append("scheduled")
            if not default_statuses and available_statuses:
                # If no pending/scheduled, default to first available status
                default_statuses = [available_statuses[0]]
            elif not default_statuses:
                default_statuses = ["completed"]  # Fallback
                
        except Exception as e:
            available_statuses = ["pending", "scheduled", "in_progress", "completed"]
            default_statuses = ["pending", "scheduled"]
        
        status_filter = st.multiselect(
            "Status",
            options=available_statuses,
            default=default_statuses,
            help="Select intervention statuses to include. If no data appears, try selecting 'completed' or all statuses."
        )
    
    with filter_col3:
        days_ahead = st.number_input(
            "Days Ahead",
            min_value=1,
            max_value=365,
            value=90,
            help="Number of days forward to look for interventions"
        )
    
    # Get available members
    # Use a wider date range to ensure we find data
    # Start from 365 days ago to catch all historical data, extend forward based on user input
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    
    with st.spinner("Loading members..."):
        # Use selected status filter, or default to all available statuses if none selected
        if not status_filter:
            # If no status selected, try to get all statuses from database
            try:
                status_query = """
                    SELECT DISTINCT status
                    FROM member_interventions
                    ORDER BY status
                """
                from utils.database import execute_query
                status_df = execute_query(status_query)
                status_filter = status_df['status'].unique().tolist() if not status_df.empty else ["completed"]
            except:
                status_filter = ["completed"]  # Fallback to completed
        
        # First try with date filters
        available_members = st.session_state.campaign_builder.get_available_members(
            measure_id=measure_filter if measure_filter else None,
            status_filter=status_filter,
            start_date=start_date,
            end_date=end_date
        )
        
        # If no results with date filter, try without date restrictions
        if available_members.empty:
            available_members = st.session_state.campaign_builder.get_available_members(
                measure_id=measure_filter if measure_filter else None,
                status_filter=status_filter,
                start_date=None,
                end_date=None
            )
    
    if available_members.empty:
        st.warning("No members found with selected filters.")
        
        # Show helpful diagnostic information
        with st.expander("🔍 Diagnostic Information", expanded=False):
            try:
                from utils.database import execute_query
                # Check total interventions
                total_query = "SELECT COUNT(*) as total FROM member_interventions"
                total_df = execute_query(total_query)
                total_count = total_df.iloc[0]['total'] if not total_df.empty else 0
                
                # Check status distribution
                status_query = """
                    SELECT status, COUNT(*) as count
                    FROM member_interventions
                    GROUP BY status
                    ORDER BY count DESC
                """
                status_df = execute_query(status_query)
                
                st.write(f"**Total interventions in database:** {total_count}")
                if not status_df.empty:
                    st.write("**Status distribution:**")
                    st.dataframe(status_df, use_container_width=True, hide_index=True)
                else:
                    st.write("No interventions found in database.")
            except Exception as e:
                st.error(f"Error checking database: {e}")
        
        st.info("💡 **Tip:** Try selecting 'completed' status or all available statuses. The date range has been expanded to 365 days back.")
    else:
        st.info(f"Found {len(available_members)} members available for selection.")
        
        # Member selection table with multi-select
        st.subheader("Select Members")
        
        # Create selection interface with checkboxes
        if 'member_selection' not in st.session_state:
            st.session_state.member_selection = {}
        
        # Display members with checkboxes
        member_display = available_members[[
            'member_id', 'member_name', 'measure_name', 'intervention_date', 
            'status', 'cost_per_intervention'
        ]].copy()
        member_display.columns = ['Member ID', 'Member Name', 'Measure', 'Intervention Date', 'Status', 'Cost']
        
        # Add selection checkboxes
        selected_member_ids = []
        
        # Show member table
        st.dataframe(
            member_display,
            use_container_width=True,
            hide_index=True
        )
        
        # Selection options
        member_options = member_display['Member ID'].unique().tolist()
        
        col1, col2 = st.columns([3, 1], gap="small")
        with col1:
            selected_member_ids = st.multiselect(
                "Select Members for Campaign",
                options=member_options,
                default=st.session_state.get('selected_member_ids', []),
                key="member_multiselect",
                help="Select one or more members to include in the campaign"
            )
        with col2:
            if st.button("Select All", key="select_all_btn"):
                st.session_state.selected_member_ids = member_options
                st.rerun()
        
        st.session_state.selected_members = selected_member_ids
        
        if selected_member_ids:
            st.success(f"✅ {len(selected_member_ids)} members selected")
            
            # Step 2: Calculate metrics
            st.markdown("---")
            st.header("Step 2: Campaign Metrics")
            
            with st.spinner("Calculating campaign metrics..."):
                metrics = st.session_state.campaign_builder.calculate_campaign_metrics(selected_member_ids)
            
            # Display metrics
            metric_cols = st.columns(4, gap="small")
            with metric_cols[0]:
                st.metric("Total Members", f"{metrics['total_members']:,}")
                st.metric("Total Value", f"${metrics['total_value']:,.0f}")
            with metric_cols[1]:
                st.metric("Predicted Success Rate", f"{metrics['predicted_success_rate']:.1f}%")
                st.metric("Predicted Closures", f"{metrics['predicted_closures']:,}")
            with metric_cols[2]:
                st.metric("Required FTE", f"{metrics['required_fte']:.1f}")
                st.metric("Total Cost", f"${metrics['total_cost']:,.0f}")
            with metric_cols[3]:
                st.metric("Predicted Revenue", f"${metrics['predicted_revenue']:,.0f}")
                st.metric("Net Benefit", f"${metrics['predicted_net_benefit']:,.0f}")
            
            # Step 3: Configure campaign
            st.markdown("---")
            st.header("Step 3: Configure Campaign")
            
            config_col1, config_col2 = st.columns(2, gap="small")
            
            with config_col1:
                campaign_name = st.text_input(
                    "Campaign Name",
                    value=f"Campaign {datetime.now().strftime('%Y-%m-%d')}",
                    key="campaign_name"
                )
                
                coordinator_count = st.slider(
                    "Number of Coordinators",
                    min_value=1,
                    max_value=10,
                    value=int(metrics['required_fte']),
                    key="coordinator_count"
                )
            
            with config_col2:
                assignment_strategy = st.selectbox(
                    "Assignment Strategy",
                    options=["balanced", "round_robin", "by_measure"],
                    index=0,
                    format_func=lambda x: {
                        "balanced": "Balanced Workload",
                        "round_robin": "Round Robin",
                        "by_measure": "Group by Measure"
                    }[x],
                    key="assignment_strategy"
                )
                
                target_date = st.date_input(
                    "Target Completion Date",
                    value=datetime.now() + timedelta(days=30),
                    key="target_date",
                    format="MM/DD/YYYY"
                )
            
            # Step 4: Create campaign
            st.markdown("---")
            st.header("Step 4: Create Campaign")
            
            if st.button("🚀 Create Campaign", type="primary", use_container_width=True):
                with st.spinner("Creating campaign and assigning coordinators..."):
                    campaign = st.session_state.campaign_builder.create_campaign(
                        name=campaign_name,
                        member_ids=selected_member_ids,
                        coordinator_count=coordinator_count,
                        assignment_strategy=assignment_strategy,
                        target_date=target_date.strftime("%Y-%m-%d")
                    )
                    
                    st.session_state.current_campaign = campaign
                    st.session_state.campaigns.append(campaign)
                    st.success(f"✅ Campaign '{campaign_name}' created successfully!")
                    st.rerun()
            
            # Preview assignment
            if st.checkbox("Preview Coordinator Assignment", key="preview_assignment"):
                with st.spinner("Calculating assignment..."):
                    preview_members = available_members[available_members['member_id'].isin(selected_member_ids)]
                    preview_assigned = st.session_state.campaign_builder.assign_to_coordinators(
                        preview_members,
                        coordinator_count,
                        assignment_strategy
                    )
                    
                    if not preview_assigned.empty:
                        st.subheader("Assignment Preview")
                        assignment_summary = preview_assigned.groupby('coordinator_name').agg({
                            'member_id': 'count',
                            'cost_per_intervention': 'sum'
                        }).reset_index()
                        assignment_summary.columns = ['Coordinator', 'Members', 'Total Cost']
                        st.dataframe(assignment_summary, use_container_width=True, hide_index=True)

elif page_option == "View Campaigns":
    st.title("📋 Campaign Management")
    
    campaigns = st.session_state.campaign_builder.get_all_campaigns()
    
    if not campaigns:
        st.info("No campaigns created yet. Build a new campaign to get started.")
    else:
        # Campaign list
        st.header("Active Campaigns")
        
        for campaign in campaigns:
            with st.expander(f"📋 {campaign['name']} - {campaign['campaign_id']}"):
                col1, col2, col3 = st.columns(3, gap="small")
                
                with col1:
                    st.metric("Members", campaign['metrics']['total_members'])
                    st.metric("Predicted Closures", campaign['metrics']['predicted_closures'])
                
                with col2:
                    st.metric("Total Value", f"${campaign['metrics']['total_value']:,.0f}")
                    st.metric("Required FTE", f"{campaign['metrics']['required_fte']:.1f}")
                
                with col3:
                    st.metric("Net Benefit", f"${campaign['metrics']['predicted_net_benefit']:,.0f}")
                    st.metric("Status", campaign['status'].title())
                
                # Actions
                action_col1, action_col2, action_col3 = st.columns(3, gap="small")
                
                with action_col1:
                    # Export CRM CSV
                    crm_csv = st.session_state.campaign_builder.export_crm_csv(campaign['campaign_id'])
                    st.download_button(
                        "📥 Export CRM CSV",
                        crm_csv,
                        file_name=f"campaign_{campaign['campaign_id']}_crm.csv",
                        mime="text/csv",
                        key=f"crm_{campaign['campaign_id']}"
                    )
                
                with action_col2:
                    # Generate call list
                    call_list = st.session_state.campaign_builder.generate_call_list(campaign['campaign_id'])
                    if not call_list.empty:
                        call_list_csv = call_list.to_csv(index=False)
                        st.download_button(
                            "📞 Download Call List",
                            call_list_csv,
                            file_name=f"call_list_{campaign['campaign_id']}.csv",
                            mime="text/csv",
                            key=f"call_{campaign['campaign_id']}"
                        )
                
                with action_col3:
                    # Coordinator-specific call lists
                    coordinators = campaign['member_data']['coordinator_name'].unique() if not campaign['member_data'].empty else []
                    if coordinators:
                        selected_coord = st.selectbox(
                            "Coordinator Call List",
                            options=coordinators,
                            key=f"coord_{campaign['campaign_id']}"
                        )
                        coord_call_list = st.session_state.campaign_builder.generate_call_list(
                            campaign['campaign_id'],
                            selected_coord
                        )
                        if not coord_call_list.empty:
                            coord_csv = coord_call_list.to_csv(index=False)
                            st.download_button(
                                "📞 Download",
                                coord_csv,
                                file_name=f"call_list_{selected_coord.replace(' ', '_')}_{campaign['campaign_id']}.csv",
                                mime="text/csv",
                                key=f"coord_call_{campaign['campaign_id']}"
                            )

else:  # Campaign Dashboard
    st.title("📊 Campaign Progress Dashboard")
    
    campaigns = st.session_state.campaign_builder.get_all_campaigns()
    
    if not campaigns:
        st.info("No campaigns to display. Create a campaign to see progress.")
    else:
        # Overall statistics
        st.header("Overall Statistics")
        
        total_members = sum(c['metrics']['total_members'] for c in campaigns)
        total_value = sum(c['metrics']['total_value'] for c in campaigns)
        total_ftes = sum(c['metrics']['required_fte'] for c in campaigns)
        active_campaigns = len([c for c in campaigns if c['status'] == 'active'])
        
        stat_cols = st.columns(4, gap="small")
        with stat_cols[0]:
            st.metric("Active Campaigns", active_campaigns)
        with stat_cols[1]:
            st.metric("Total Members", f"{total_members:,}")
        with stat_cols[2]:
            st.metric("Total Value", f"${total_value:,.0f}")
        with stat_cols[3]:
            st.metric("Total FTEs", f"{total_ftes:.1f}")
        
        # Campaign progress chart
        st.markdown("---")
        st.subheader("Campaign Progress")
        
        campaign_names = [c['name'] for c in campaigns]
        campaign_progress = []
        
        for campaign in campaigns:
            if 'progress' in campaign:
                progress = campaign['progress']['progress_pct']
            else:
                progress = 0
            campaign_progress.append(progress)
        
        if campaign_progress:
            fig = px.bar(
                x=campaign_names,
                y=campaign_progress,
                title="Campaign Completion Progress",
                labels={"x": "Campaign", "y": "Progress %"},
                color=campaign_progress,
                color_continuous_scale="Blues"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Coordinator workload
        st.markdown("---")
        st.subheader("Coordinator Workload Distribution")
        
        all_assignments = []
        for campaign in campaigns:
            if not campaign['member_data'].empty:
                assignments = campaign['member_data'].groupby('coordinator_name').size().reset_index()
                assignments.columns = ['Coordinator', 'Members']
                assignments['Campaign'] = campaign['name']
                all_assignments.append(assignments)
        
        if all_assignments:
            workload_df = pd.concat(all_assignments, ignore_index=True)
            workload_summary = workload_df.groupby('Coordinator')['Members'].sum().reset_index()
            workload_summary = workload_summary.sort_values('Members', ascending=False)
            
            fig = px.bar(
                workload_summary,
                x='Coordinator',
                y='Members',
                title="Total Members per Coordinator",
                labels={"Members": "Number of Members", "Coordinator": "Coordinator"},
                color='Members',
                color_continuous_scale="Greens"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(workload_summary, use_container_width=True, hide_index=True)

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer

