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

from utils.database import show_db_status, execute_query
from utils.roi_calculator import ROICalculator
from utils.queries import get_portfolio_summary_query
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# Page configuration
st.set_page_config(
    page_title="ROI Calculator - HEDIS Portfolio",
    page_icon="💰",
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
    .roi-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #00cc66;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    
    .ci-indicator {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 8px;
        font-size: 0.85rem;
        background: #e6f3ff;
        color: #0066cc;
        margin-left: 0.5rem;
    }
    
    .positive-roi {
        color: #00cc66;
        font-weight: 700;
    }
    
    .negative-roi {
        color: #cc0000;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'roi_calculator' not in st.session_state:
    st.session_state.roi_calculator = ROICalculator()
if 'roi_results' not in st.session_state:
    st.session_state.roi_results = []
    # Auto-generate sample ROI results on page load
    try:
        config = {
            "quality_bonus_per_member_per_star": 50.0,
            "members_per_measure": 1000,
            "revenue_per_closure": 100.0,
            "staff_cost_per_hour": 75.0,
            "outreach_cost_per_member": 15.0,
            "lab_cost_per_test": 25.0,
            "confidence_level": 0.95
        }
        sample_results = st.session_state.roi_calculator.generate_sample_roi_results(config)
        st.session_state.roi_results = sample_results
    except Exception:
        pass  # Silently fail if generation fails on init

# Sidebar
st.sidebar.header("💰 ROI Calculator")
st.sidebar.markdown("Calculate comprehensive ROI with quality bonuses and Star Rating impact")
st.sidebar.divider()

# Configuration
st.sidebar.subheader("⚙️ Configuration")

quality_bonus = st.sidebar.number_input(
    "Quality Bonus per Member per Star ($)",
    min_value=0.0,
    value=50.0,
    step=5.0,
    key="quality_bonus"
)

members_per_measure = st.sidebar.number_input(
    "Members per Measure",
    min_value=1,
    value=1000,
    step=100,
    key="members_per_measure"
)

revenue_per_closure = st.sidebar.number_input(
    "Revenue per Closure ($)",
    min_value=0.0,
    value=100.0,
    step=10.0,
    key="revenue_per_closure"
)

staff_cost_per_hour = st.sidebar.number_input(
    "Staff Cost per Hour ($)",
    min_value=0.0,
    value=75.0,
    step=5.0,
    key="staff_cost"
)

outreach_cost = st.sidebar.number_input(
    "Outreach Cost per Member ($)",
    min_value=0.0,
    value=15.0,
    step=1.0,
    key="outreach_cost"
)

lab_cost = st.sidebar.number_input(
    "Lab Cost per Test ($)",
    min_value=0.0,
    value=25.0,
    step=1.0,
    key="lab_cost"
)

confidence_level = st.sidebar.slider(
    "Confidence Level (%)",
    min_value=80,
    max_value=99,
    value=95,
    step=1,
    key="confidence_level"
)

st.sidebar.divider()
# Date range
st.sidebar.subheader("📅 Date Range")
# Default to data range (2024-10-01 to 2024-12-31) instead of last 90 days
default_start = datetime(2024, 10, 1)
default_end = datetime(2024, 12, 31)

start_date = st.sidebar.date_input(
    "Start Date",
    value=default_start,
    max_value=datetime.now(),
    format="MM/DD/YYYY"
)
end_date = st.sidebar.date_input(
    "End Date",
    value=default_end,
    max_value=datetime.now(),
    format="MM/DD/YYYY"
)

if start_date > end_date:
    st.sidebar.error("Start date must be before end date")
    st.stop()

start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

st.sidebar.divider()
# Measure selection
st.sidebar.subheader("🎯 Measure Selection")
calc_option = st.sidebar.radio(
    "Calculate",
    ["All Measures", "Single Measure"],
    index=0
)

selected_measure = None
if calc_option == "Single Measure":
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

# Sidebar value proposition - at bottom
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

# Sidebar footer
render_sidebar_footer()

# Main content
st.title("💰 Comprehensive ROI Calculator")
st.markdown("Calculate quality bonus impact, Star Rating financial impact, and net ROI with confidence intervals")

# Calculate button
if st.button("🔄 Calculate ROI", type="primary", use_container_width=True):
    with st.spinner("Calculating ROI..."):
        config = {
            "quality_bonus_per_member_per_star": quality_bonus,
            "members_per_measure": members_per_measure,
            "revenue_per_closure": revenue_per_closure,
            "staff_cost_per_hour": staff_cost_per_hour,
            "outreach_cost_per_member": outreach_cost,
            "lab_cost_per_test": lab_cost,
            "confidence_level": confidence_level / 100.0
        }
        
        st.session_state.roi_calculator.defaults.update(config)
        
        if calc_option == "All Measures":
            # Get all measures from hedis_measures table
            measures_query = """
                SELECT DISTINCT hm.measure_id, 
                       COALESCE(NULLIF(hm.measure_name, ''), hm.measure_id) as measure_name
                FROM hedis_measures hm
                WHERE hm.measure_id IS NOT NULL 
                  AND hm.measure_id != ''
                ORDER BY hm.measure_name
            """
            measures_df = execute_query(measures_query)
            
            # Remove any duplicates that might have slipped through
            if not measures_df.empty:
                measures_df = measures_df.drop_duplicates(subset=['measure_id'], keep='first')
            
            # If no measures in hedis_measures, try from interventions
            if measures_df.empty:
                measures_query = """
                    SELECT DISTINCT mi.measure_id, 
                           COALESCE(NULLIF(hm.measure_name, ''), mi.measure_id) as measure_name
                    FROM member_interventions mi
                    LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
                    WHERE mi.measure_id IS NOT NULL 
                      AND mi.measure_id != ''
                    ORDER BY measure_name
                """
                measures_df = execute_query(measures_query)
                
                # Remove duplicates
                if not measures_df.empty:
                    measures_df = measures_df.drop_duplicates(subset=['measure_id'], keep='first')
            
            if measures_df.empty:
                st.warning("⚠️ No measures found in the database. Please check your data.")
                st.session_state.roi_results = []
            else:
                results = []
                seen_measure_ids = set()
                
                # First, deduplicate the DataFrame itself
                measures_df = measures_df.drop_duplicates(subset=['measure_id'], keep='first')
                
                for _, row in measures_df.iterrows():
                    measure_id = str(row['measure_id']).strip() if row['measure_id'] else None
                    
                    # Skip if measure_id is null, empty, or already processed
                    if not measure_id or measure_id in seen_measure_ids:
                        continue
                    seen_measure_ids.add(measure_id)
                    
                    measure_name_from_query = str(row.get('measure_name', '')).strip() if row.get('measure_name') else None
                    if not measure_name_from_query or measure_name_from_query == 'None' or measure_name_from_query == '':
                        measure_name_from_query = f"Measure {measure_id}"
                    
                    roi = st.session_state.roi_calculator.calculate_measure_roi(
                        measure_id,
                        start_date_str,
                        end_date_str,
                        config
                    )
                    
                    # Always use measure_name from query to ensure proper names
                    roi['measure_name'] = measure_name_from_query
                    roi['measure_id'] = measure_id  # Ensure measure_id is set
                    
                    results.append(roi)
                
                # Final deduplication pass on results by measure_id
                # Use a dictionary keyed by measure_id to ensure uniqueness
                unique_results = {}
                for roi in results:
                    measure_id = str(roi.get('measure_id', '')).strip() if roi.get('measure_id') else None
                    
                    # Skip if no measure_id
                    if not measure_id:
                        continue
                    
                    # If we haven't seen this measure_id, add it
                    if measure_id not in unique_results:
                        unique_results[measure_id] = roi
                    else:
                        # If duplicate, keep the one with more data (interventions)
                        existing = unique_results[measure_id]
                        existing_interventions = existing.get('total_interventions', 0) or 0
                        new_interventions = roi.get('total_interventions', 0) or 0
                        
                        if new_interventions > existing_interventions:
                            unique_results[measure_id] = roi
                        # If same data, prefer the one with a better measure_name
                        elif new_interventions == existing_interventions:
                            existing_name = str(existing.get('measure_name', '')).strip()
                            new_name = str(roi.get('measure_name', '')).strip()
                            if new_name and new_name != 'Unknown' and (not existing_name or existing_name == 'Unknown'):
                                unique_results[measure_id] = roi
                
                # Convert to list and ensure all have proper measure_name
                final_results = []
                for measure_id, roi in unique_results.items():
                    if not roi.get('measure_name') or str(roi.get('measure_name', '')).strip() in ['', 'None', 'Unknown']:
                        roi['measure_name'] = f"Measure {measure_id}"
                    final_results.append(roi)
                
                st.session_state.roi_results = final_results
        else:
            if selected_measure:
                roi = st.session_state.roi_calculator.calculate_measure_roi(
                    selected_measure,
                    start_date_str,
                    end_date_str,
                    config
                )
                st.session_state.roi_results = [roi]
            else:
                st.error("Please select a measure")

# Display results
if st.session_state.roi_results and len(st.session_state.roi_results) > 0:
    # Check if all results have zero data
    total_interventions_all = sum(r.get('total_interventions', 0) for r in st.session_state.roi_results)
    if total_interventions_all == 0:
        st.warning(f"⚠️ **No intervention data found for the selected date range ({start_date_str} to {end_date_str}).**")
        st.info("💡 **Tip:** Try adjusting the date range. Default data is typically available from October 2024 to December 2024.")
        st.markdown("---")
    
    # Portfolio summary
    if len(st.session_state.roi_results) > 1:
        st.header("📊 Portfolio ROI Summary")
        
        total_revenue = sum(r.get('total_revenue', 0) for r in st.session_state.roi_results)
        total_bonus = sum(r.get('quality_bonus', 0) for r in st.session_state.roi_results)
        total_costs = sum(r.get('total_costs', 0) for r in st.session_state.roi_results)
        total_roi = sum(r.get('net_roi', 0) for r in st.session_state.roi_results)
        
        summary_cols = st.columns(4, gap="small")
        with summary_cols[0]:
            st.metric("Total Revenue", f"${total_revenue:,.0f}")
        with summary_cols[1]:
            st.metric("Quality Bonus", f"${total_bonus:,.0f}")
        with summary_cols[2]:
            st.metric("Total Costs", f"${total_costs:,.0f}")
        with summary_cols[3]:
            roi_class = "positive-roi" if total_roi >= 0 else "negative-roi"
            st.markdown(f'<div class="{roi_class}">Net ROI: ${total_roi:,.0f}</div>', unsafe_allow_html=True)
    
    # Detailed results
    st.markdown("---")
    st.header("📈 Detailed ROI Analysis")
    
    # Results are already deduplicated before storing in session_state
    # Just ensure measure_name is properly set for display
    for idx, roi in enumerate(st.session_state.roi_results):
        measure_id = str(roi.get('measure_id', '')).strip() if roi.get('measure_id') else None
        measure_name = str(roi.get('measure_name', '')).strip() if roi.get('measure_name') else None
        
        # Ensure measure_name is set
        if not measure_name or measure_name == 'None' or measure_name == '' or measure_name == 'Unknown':
            measure_name = f"Measure {measure_id}" if measure_id else "Unknown"
            roi['measure_name'] = measure_name
        success_rate = roi.get('success_rate', 0)
        total_revenue = roi.get('total_revenue', 0)
        quality_bonus = roi.get('quality_bonus', 0)
        total_costs = roi.get('total_costs', 0)
        net_roi = roi.get('net_roi', 0)
        roi_ratio = roi.get('roi_ratio', 0)
        star_rating = roi.get('star_rating', 0)
        
        with st.expander(f"💰 {measure_name} - ROI Analysis", expanded=True):
            # Key metrics
            metric_cols = st.columns(4, gap="small")
            with metric_cols[0]:
                st.metric("Success Rate", f"{success_rate:.1f}%")
                ci_lower = roi.get('success_rate_ci_lower', 0)
                ci_upper = roi.get('success_rate_ci_upper', 0)
                st.caption(f"95% CI: {ci_lower:.1f}% - {ci_upper:.1f}%")
            with metric_cols[1]:
                st.metric("Star Rating", f"{star_rating} stars")
                st.caption(f"Quality Bonus: ${quality_bonus:,.0f}")
            with metric_cols[2]:
                st.metric("Total Revenue", f"${total_revenue:,.0f}")
                revenue_ci_lower = roi.get('revenue_ci_lower', 0)
                revenue_ci_upper = roi.get('revenue_ci_upper', 0)
                st.caption(f"95% CI: ${revenue_ci_lower:,.0f} - ${revenue_ci_upper:,.0f}")
            with metric_cols[3]:
                roi_class = "positive-roi" if net_roi >= 0 else "negative-roi"
                st.markdown(f'<div class="{roi_class}">Net ROI: ${net_roi:,.0f}</div>', unsafe_allow_html=True)
                st.metric("ROI Ratio", f"{roi_ratio:.2f}")
                net_roi_ci_lower = roi.get('net_roi_ci_lower', 0)
                net_roi_ci_upper = roi.get('net_roi_ci_upper', 0)
                st.caption(f"95% CI: ${net_roi_ci_lower:,.0f} - ${net_roi_ci_upper:,.0f}")
            
            # Cost breakdown
            st.subheader("💵 Cost Breakdown")
            cost_breakdown = roi.get('cost_breakdown', {})
            
            cost_cols = st.columns(4, gap="small")
            with cost_cols[0]:
                st.metric("Staff Costs", f"${cost_breakdown.get('staff_cost', 0):,.2f}")
            with cost_cols[1]:
                st.metric("Outreach Costs", f"${cost_breakdown.get('outreach_cost', 0):,.2f}")
            with cost_cols[2]:
                st.metric("Lab Costs", f"${cost_breakdown.get('lab_cost', 0):,.2f}")
            with cost_cols[3]:
                st.metric("Intervention Costs", f"${cost_breakdown.get('intervention_cost', 0):,.2f}")
            
            # Revenue breakdown
            st.subheader("💵 Revenue Breakdown")
            revenue_cols = st.columns(2, gap="small")
            with revenue_cols[0]:
                st.metric("Revenue from Closures", f"${total_revenue:,.2f}")
            with revenue_cols[1]:
                st.metric("Quality Bonus Impact", f"${quality_bonus:,.2f}")
            
            # Visualization
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Revenue',
                x=['Closures', 'Quality Bonus'],
                y=[total_revenue, quality_bonus],
                marker_color=['#00cc66', '#0066cc']
            ))
            
            fig.add_trace(go.Bar(
                name='Costs',
                x=['Total Costs'],
                y=[total_costs],
                marker_color='#ff6600'
            ))
            
            fig.update_layout(
                title=f"{measure_name} - Revenue vs Costs",
                barmode='group',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True, key=f"roi_chart_{idx}")
    
    # Sensitivity analysis
    st.markdown("---")
    st.header("🔬 Sensitivity Analysis")
    st.markdown("What-if scenarios: 'If closure rate is X% instead of Y%...'")
    
    if len(st.session_state.roi_results) == 1:
        base_roi = st.session_state.roi_results[0]
        
        # Create scenarios
        current_rate = base_roi.get('success_rate', 0)
        
        scenario_cols = st.columns(3, gap="small")
        scenarios = []
        
        with scenario_cols[0]:
            st.subheader("Scenario 1")
            scenario1_rate = st.slider(
                "Success Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=current_rate - 5,
                step=0.5,
                key="scenario1_rate"
            )
            scenarios.append({
                "name": f"Lower Rate ({scenario1_rate:.1f}%)",
                "success_rate": scenario1_rate
            })
        
        with scenario_cols[1]:
            st.subheader("Scenario 2")
            scenario2_rate = st.slider(
                "Success Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=current_rate,
                step=0.5,
                key="scenario2_rate"
            )
            scenarios.append({
                "name": f"Current Rate ({scenario2_rate:.1f}%)",
                "success_rate": scenario2_rate
            })
        
        with scenario_cols[2]:
            st.subheader("Scenario 3")
            scenario3_rate = st.slider(
                "Success Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=current_rate + 5,
                step=0.5,
                key="scenario3_rate"
            )
            scenarios.append({
                "name": f"Higher Rate ({scenario3_rate:.1f}%)",
                "success_rate": scenario3_rate
            })
        
        # Calculate sensitivity
        sensitivity_df = st.session_state.roi_calculator.sensitivity_analysis(base_roi, scenarios)
        
        if not sensitivity_df.empty:
            # Display comparison
            st.subheader("Scenario Comparison")
            st.dataframe(sensitivity_df, use_container_width=True, hide_index=True)
            
            # Visualization
            fig_sens = go.Figure()
            
            fig_sens.add_trace(go.Bar(
                x=sensitivity_df['scenario_name'],
                y=sensitivity_df['net_roi'],
                marker_color=['#cc0000' if x < 0 else '#00cc66' for x in sensitivity_df['net_roi']],
                text=sensitivity_df['net_roi'].apply(lambda x: f"${x:,.0f}"),
                textposition='outside'
            ))
            
            fig_sens.update_layout(
                title="Net ROI by Scenario",
                xaxis_title="Scenario",
                yaxis_title="Net ROI ($)",
                height=300
            )
            
            st.plotly_chart(fig_sens, use_container_width=True, key="sensitivity_analysis_chart")
    else:
        st.info("Select a single measure to perform sensitivity analysis")
    
    # Export CFO report
    st.markdown("---")
    st.header("📄 Export Financial Report")
    
    # Get portfolio summary
    portfolio_summary = None
    try:
        portfolio_query = get_portfolio_summary_query(start_date_str, end_date_str)
        portfolio_df = execute_query(portfolio_query)
        if not portfolio_df.empty:
            portfolio_summary = portfolio_df.iloc[0].to_dict()
    except:
        pass
    
    # Generate report
    cfo_report = st.session_state.roi_calculator.generate_cfo_report(
        st.session_state.roi_results,
        portfolio_summary
    )
    
    export_col1, export_col2 = st.columns(2, gap="small")
    
    with export_col1:
        st.download_button(
            "📊 Download CFO Report (Text)",
            cfo_report,
            file_name=f"cfo_roi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with export_col2:
        # Create Excel export
        try:
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # ROI Summary
                roi_summary_data = []
                for roi in st.session_state.roi_results:
                    roi_summary_data.append({
                        'Measure': roi.get('measure_name', 'Unknown'),
                        'Success Rate (%)': roi.get('success_rate', 0),
                        'Star Rating': roi.get('star_rating', 0),
                        'Revenue ($)': roi.get('total_revenue', 0),
                        'Quality Bonus ($)': roi.get('quality_bonus', 0),
                        'Total Costs ($)': roi.get('total_costs', 0),
                        'Net ROI ($)': roi.get('net_roi', 0),
                        'ROI Ratio': roi.get('roi_ratio', 0)
                    })
                
                pd.DataFrame(roi_summary_data).to_excel(writer, sheet_name="ROI Summary", index=False)
                
                # Cost Breakdown
                cost_data = []
                for roi in st.session_state.roi_results:
                    cost_breakdown = roi.get('cost_breakdown', {})
                    cost_data.append({
                        'Measure': roi.get('measure_name', 'Unknown'),
                        'Staff Cost ($)': cost_breakdown.get('staff_cost', 0),
                        'Outreach Cost ($)': cost_breakdown.get('outreach_cost', 0),
                        'Lab Cost ($)': cost_breakdown.get('lab_cost', 0),
                        'Intervention Cost ($)': cost_breakdown.get('intervention_cost', 0),
                        'Total Cost ($)': roi.get('total_costs', 0)
                    })
                
                pd.DataFrame(cost_data).to_excel(writer, sheet_name="Cost Breakdown", index=False)
            
            st.download_button(
                "📊 Download CFO Report (Excel)",
                excel_buffer.getvalue(),
                file_name=f"cfo_roi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except ImportError:
            st.warning("⚠️ Excel export requires openpyxl")
            st.info("💡 Install openpyxl for Excel export:")
            st.code("pip install openpyxl", language="bash")
            st.info("Then restart Streamlit to enable Excel downloads.")
        except Exception as e:
            st.error(f"❌ Error creating Excel export: {str(e)}")

elif 'roi_results' in st.session_state and len(st.session_state.roi_results) == 0:
    st.warning("⚠️ No ROI results found. Please check your date range and measure selection.")
else:
    st.info("👆 Configure settings and click 'Calculate ROI' to see results")

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer

