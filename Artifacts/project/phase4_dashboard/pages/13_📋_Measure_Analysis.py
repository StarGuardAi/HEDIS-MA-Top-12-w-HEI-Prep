"""
HEDIS Measure Analysis Page
Comprehensive analysis for any HEDIS measure
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from utils.measure_definitions import (
    get_measure_definition,
    get_all_measures,
    get_measure_name
)
from utils.measure_analysis import (
    get_measure_performance,
    get_gap_analysis,
    get_members_with_gaps,
    get_provider_performance,
    get_geographic_performance,
    get_best_practices,
    export_call_list
)
from utils.campaign_builder import CampaignBuilder
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# Page configuration
st.set_page_config(
    page_title="Measure Analysis - HEDIS Portfolio",
    page_icon="📋",
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

# Spacing fix
st.markdown('<style>div.block-container{padding-top:1rem!important}h1{margin-top:0.5rem!important}</style>', unsafe_allow_html=True)

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
    .measure-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    
    .gap-reason-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff6b6b;
        margin: 0.5rem 0;
    }
    
    .priority-high {
        background: #ffe6e6;
        border-left-color: #cc0000;
    }
    
    .priority-medium {
        background: #fff4e6;
        border-left-color: #ff9900;
    }
    
    .priority-low {
        background: #e6f3ff;
        border-left-color: #0066cc;
    }
</style>
""", unsafe_allow_html=True)

# Initialize campaign builder
campaign_builder = CampaignBuilder()

# Sidebar - Measure Selection
st.sidebar.header("📋 Measure Analysis")
st.sidebar.markdown("Select a HEDIS measure to analyze")

available_measures = get_all_measures()
selected_measure_id = st.sidebar.selectbox(
    "Select Measure",
    available_measures,
    format_func=lambda x: f"{x} - {get_measure_name(x)}"
)

# Date range
st.sidebar.markdown("---")
st.sidebar.subheader("Date Range")
end_date = st.sidebar.date_input("End Date", value=datetime.now().date(), format="MM/DD/YYYY")
start_date = st.sidebar.date_input("Start Date", value=end_date - timedelta(days=365), format="MM/DD/YYYY")

# Get measure definition
measure_def = get_measure_definition(selected_measure_id)

if not measure_def:
    st.error(f"Measure {selected_measure_id} not found")
    st.stop()

# Sidebar value proposition - at bottom
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

# Sidebar footer
render_sidebar_footer()

# Main Content
st.title(f"📋 {measure_def.measure_name} Analysis")
st.markdown(f"**Measure ID**: {measure_def.measure_id}")

# 1. Measure Definition Card
st.markdown("---")
st.header("📖 Measure Definition")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
    <div class="measure-card">
        <h2>{measure_def.measure_name}</h2>
        <p><strong>Official Definition:</strong></p>
        <p>{measure_def.official_definition}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### Key Information")
    st.metric("Star Rating Weight", f"{measure_def.star_rating_weight:.0%}")
    st.metric("Typical Benchmark", f"{measure_def.typical_benchmark_rate:.1f}%")
    st.metric("Quality Bonus Impact", measure_def.quality_bonus_impact)

# Numerator/Denominator
st.subheader("Numerator & Denominator")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h4>Numerator</h4>
        <p>Members who meet the measure criteria</p>
    </div>
    """, unsafe_allow_html=True)
    st.write(measure_def.numerator_description)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h4>Denominator</h4>
        <p>Eligible member population</p>
    </div>
    """, unsafe_allow_html=True)
    st.write(measure_def.denominator_description)

# Exclusion Criteria
st.subheader("Exclusion Criteria")
for exclusion in measure_def.exclusion_criteria:
    st.markdown(f"- {exclusion}")

st.caption(f"**Data Collection Period**: {measure_def.data_collection_period}")

# 2. Performance Dashboard
st.markdown("---")
st.header("📊 Performance Dashboard")

# Get performance data
performance = get_measure_performance(
    selected_measure_id,
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d")
)

# Current Rate vs Benchmark
col1, col2, col3, col4 = st.columns(4)

with col1:
    current_rate = performance["current_rate"]
    benchmark = performance["benchmark_rate"]
    delta = current_rate - benchmark
    st.metric(
        "Current Rate",
        f"{current_rate:.1f}%",
        delta=f"{delta:+.1f}% vs benchmark"
    )

with col2:
    st.metric("Numerator", f"{performance['numerator']:,}")

with col3:
    st.metric("Denominator", f"{performance['denominator']:,}")

with col4:
    st.metric("Exclusions", f"{performance['exclusions']:,}")

# Rate by Demographics
st.subheader("Rate by Demographics")

demo_cols = st.columns(3)

with demo_cols[0]:
    st.markdown("**By Age Group**")
    age_df = pd.DataFrame(list(performance["rate_by_age"].items()), columns=["Age Group", "Rate"])
    fig_age = px.bar(
        age_df, 
        x="Age Group", 
        y="Rate", 
        title="Rate by Age Group",
        color_discrete_sequence=['#0066cc']
    )
    fig_age.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        xaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        title=dict(text="Rate by Age Group", font=dict(color='black', size=14))
    )
    fig_age.update_traces(
        marker=dict(color='#0066cc', line=dict(color='#003366', width=2)),
        textfont=dict(color='black'),
        texttemplate='%{y:.1f}%',
        textposition='outside'
    )
    st.plotly_chart(fig_age, use_container_width=True)

with demo_cols[1]:
    st.markdown("**By Gender**")
    gender_df = pd.DataFrame(list(performance["rate_by_gender"].items()), columns=["Gender", "Rate"])
    fig_gender = px.bar(
        gender_df, 
        x="Gender", 
        y="Rate", 
        title="Rate by Gender",
        color_discrete_sequence=['#00cc66']
    )
    fig_gender.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        xaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        title=dict(text="Rate by Gender", font=dict(color='black', size=14))
    )
    fig_gender.update_traces(
        marker=dict(color='#00cc66', line=dict(color='#006633', width=2)),
        textfont=dict(color='black'),
        texttemplate='%{y:.1f}%',
        textposition='outside'
    )
    st.plotly_chart(fig_gender, use_container_width=True)

with demo_cols[2]:
    st.markdown("**By Risk Score**")
    risk_df = pd.DataFrame(list(performance["rate_by_risk_score"].items()), columns=["Risk Score", "Rate"])
    fig_risk = px.bar(
        risk_df, 
        x="Risk Score", 
        y="Rate", 
        title="Rate by Risk Score",
        color_discrete_sequence=['#ff9900']
    )
    fig_risk.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        xaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        title=dict(text="Rate by Risk Score", font=dict(color='black', size=14))
    )
    fig_risk.update_traces(
        marker=dict(color='#ff9900', line=dict(color='#cc6600', width=2)),
        textfont=dict(color='black'),
        texttemplate='%{y:.1f}%',
        textposition='outside'
    )
    st.plotly_chart(fig_risk, use_container_width=True)

# Trend Over 24 Months
st.subheader("Trend Over 24 Months")
trend_data = performance["trend_24_months"]
if trend_data:
    trend_df = pd.DataFrame(trend_data)
    trend_df["month"] = pd.to_datetime(trend_df["month"])
    fig_trend = px.line(
        trend_df,
        x="month",
        y="rate",
        title="Performance Trend (24 Months)",
        labels={"rate": "Rate (%)", "month": "Month"},
        color_discrete_sequence=['#0066cc']
    )
    fig_trend.add_hline(y=benchmark, line_dash="dash", line_color="red", annotation_text="Benchmark")
    fig_trend.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        xaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        title=dict(text="Performance Trend (24 Months)", font=dict(color='black', size=16))
    )
    fig_trend.update_traces(
        line=dict(width=3, color='#0066cc'),
        marker=dict(size=8, color='#0066cc'),
        fill='tonexty',
        fillcolor='rgba(0, 102, 204, 0.1)'
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# Provider Performance
st.subheader("Provider Performance Comparison")
provider_df = get_provider_performance(
    selected_measure_id,
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d")
)

st.dataframe(
    provider_df.head(10),
    use_container_width=True,
    hide_index=True
)

# Geographic Performance
st.subheader("Geographic Performance")
geo_data = get_geographic_performance(
    selected_measure_id,
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d")
)

geo_cols = st.columns(2)

with geo_cols[0]:
    st.markdown("**By Region**")
    region_df = pd.DataFrame(geo_data["regions"])
    fig_region = px.bar(
        region_df,
        x="region",
        y="rate",
        title="Rate by Region",
        labels={"rate": "Rate (%)", "region": "Region"},
        color_discrete_sequence=['#0066cc']
    )
    fig_region.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        xaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        title=dict(text="Rate by Region", font=dict(color='black', size=14))
    )
    fig_region.update_traces(
        marker=dict(color='#0066cc', line=dict(color='#003366', width=2)),
        textfont=dict(color='black'),
        texttemplate='%{y:.1f}%',
        textposition='outside'
    )
    st.plotly_chart(fig_region, use_container_width=True)

with geo_cols[1]:
    st.markdown("**By State**")
    state_df = pd.DataFrame(geo_data["states"])
    fig_state = px.bar(
        state_df,
        x="state",
        y="rate",
        title="Rate by State",
        labels={"rate": "Rate (%)", "state": "State"},
        color_discrete_sequence=['#00cc66']
    )
    fig_state.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        xaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#e0e0e0', 
            title_font=dict(color='black'),
            tickfont=dict(color='black')
        ),
        title=dict(text="Rate by State", font=dict(color='black', size=14))
    )
    fig_state.update_traces(
        marker=dict(color='#00cc66', line=dict(color='#006633', width=2)),
        textfont=dict(color='black'),
        texttemplate='%{y:.1f}%',
        textposition='outside'
    )
    st.plotly_chart(fig_state, use_container_width=True)

# 3. Gap Analysis
st.markdown("---")
st.header("🔍 Gap Analysis")

gap_data = get_gap_analysis(
    selected_measure_id,
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d")
)

gap_cols = st.columns(4)

with gap_cols[0]:
    st.metric("Total Gaps", f"{gap_data['total_gaps']:,}")

with gap_cols[1]:
    st.metric("Avg Days to Close", f"{gap_data['average_days_to_close']:.1f}")

with gap_cols[2]:
    st.metric("Cost per Closed Gap", f"${gap_data['cost_per_closed_gap']:.2f}")

with gap_cols[3]:
    high_priority = gap_data["gaps_by_priority"]["High"]
    st.metric("High Priority Gaps", f"{high_priority:,}")

# Gaps by Reason
st.subheader("Gaps by Reason")
reason_df = pd.DataFrame(
    list(gap_data["gaps_by_reason"].items()),
    columns=["Reason", "Count"]
)
fig_reason = px.pie(
    reason_df,
    values="Count",
    names="Reason",
    title="Gap Distribution by Reason",
    color_discrete_sequence=['#0066cc', '#00cc66', '#ff9900', '#cc0000', '#9966cc', '#ff66cc']
)
fig_reason.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='black', size=12),
    title=dict(text="Gap Distribution by Reason", font=dict(color='black', size=16))
)
fig_reason.update_traces(
    textfont=dict(color='black', size=12),
    marker=dict(line=dict(color='white', width=2)),
    textposition='inside',
    textinfo='percent+label'
)
st.plotly_chart(fig_reason, use_container_width=True)

# Closure Rate by Intervention
st.subheader("Closure Rate by Intervention Type")
intervention_df = pd.DataFrame(
    list(gap_data["closure_rate_by_intervention"].items()),
    columns=["Intervention", "Closure Rate"]
)
intervention_df["Closure Rate"] = intervention_df["Closure Rate"] * 100
fig_intervention = px.bar(
    intervention_df,
    x="Intervention",
    y="Closure Rate",
    title="Closure Rate by Intervention Type",
    labels={"Closure Rate": "Closure Rate (%)"},
    color_discrete_sequence=['#00cc66']
)
fig_intervention.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='black', size=12),
    xaxis=dict(
        showgrid=True, 
        gridcolor='#e0e0e0', 
        title_font=dict(color='black'),
        tickfont=dict(color='black')
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor='#e0e0e0', 
        title_font=dict(color='black'),
        tickfont=dict(color='black')
    ),
    title=dict(
        text="Closure Rate by<br>Intervention Type", 
        font=dict(color='black', size=16),
        automargin=True  # Allow title to wrap automatically
    )
)
fig_intervention.update_traces(
    marker=dict(color='#00cc66', line=dict(color='#006633', width=2)),
    textfont=dict(color='black'),
    texttemplate='%{y:.1f}%',
    textposition='outside'
)
st.plotly_chart(fig_intervention, use_container_width=True)

# 4. Member List (Actionable)
st.markdown("---")
st.header("👥 Members with Gaps")

# Filters
filter_cols = st.columns(4)

with filter_cols[0]:
    priority_filter = st.multiselect(
        "Priority",
        ["High", "Medium", "Low"],
        default=["High", "Medium"]
    )

with filter_cols[1]:
    reason_filter = st.multiselect(
        "Gap Reason",
        ["Not Scheduled", "Missed Appointment", "Lab Pending", "Provider Delay"],
        default=[]
    )

with filter_cols[2]:
    min_probability = st.slider("Min Closure Probability", 0.0, 1.0, 0.5, 0.05)

with filter_cols[3]:
    limit = st.number_input("Max Results", min_value=10, max_value=500, value=100)

# Get members
members_df = get_members_with_gaps(
    selected_measure_id,
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d"),
    limit=limit
)

# Apply filters
if priority_filter:
    members_df = members_df[members_df["priority"].isin(priority_filter)]
if reason_filter:
    members_df = members_df[members_df["gap_reason"].isin(reason_filter)]
members_df = members_df[members_df["closure_probability"] >= min_probability]

# Display members
st.dataframe(
    members_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "closure_probability": st.column_config.NumberColumn(
            "Closure Probability",
            format="%.2f"
        ),
        "days_since_gap": st.column_config.NumberColumn(
            "Days Since Gap",
            format="%d"
        )
    }
)

# Action buttons
action_cols = st.columns(3)

with action_cols[0]:
    if st.button("📞 Export Call List", use_container_width=True):
        call_list = export_call_list(members_df)
        st.download_button(
            "Download CSV",
            call_list,
            file_name=f"{selected_measure_id}_call_list_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with action_cols[1]:
    selected_members = st.multiselect(
        "Select Members to Assign",
        members_df["member_id"].tolist(),
        label_visibility="collapsed"
    )
    if st.button("👤 Assign to Coordinator", use_container_width=True, disabled=len(selected_members) == 0):
        # Assign members to coordinator
        st.success(f"Assigned {len(selected_members)} members to coordinator")

with action_cols[2]:
    if st.button("📋 Track Lab Orders", use_container_width=True):
        st.info("Lab order tracking feature - coming soon")

# 5. Best Practices
st.markdown("---")
st.header("💡 Best Practices")

best_practices = get_best_practices(selected_measure_id)

st.subheader("Evidence-Based Interventions")
for intervention in best_practices.get("interventions", []):
    st.markdown(f"- ✅ {intervention}")

st.subheader("Success Stories")
for story in best_practices.get("success_stories", []):
    st.info(f"💡 {story}")

st.subheader("Recommended Outreach Cadence")
st.success(f"📅 {best_practices.get('recommended_cadence', 'Standard quarterly outreach')}")

# 6. Regulatory Context
st.markdown("---")
st.header("📜 Regulatory Context")

reg_cols = st.columns(3)

with reg_cols[0]:
    st.markdown("""
    <div class="metric-card">
        <h4>CMS Star Rating</h4>
        <p><strong>Weight:</strong> {:.0%}</p>
        <p>Impact on overall Star Rating calculation</p>
    </div>
    """.format(measure_def.star_rating_weight), unsafe_allow_html=True)

with reg_cols[1]:
    st.markdown("""
    <div class="metric-card">
        <h4>Quality Bonus</h4>
        <p><strong>Impact:</strong> {}</p>
        <p>Financial impact on quality bonuses</p>
    </div>
    """.format(measure_def.quality_bonus_impact), unsafe_allow_html=True)

with reg_cols[2]:
    st.markdown("""
    <div class="metric-card">
        <h4>Audit Requirements</h4>
        <p>Documentation and validation requirements</p>
    </div>
    """, unsafe_allow_html=True)

st.subheader("Audit Requirements")
for requirement in measure_def.audit_requirements:
    st.markdown(f"- 📋 {requirement}")

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer

