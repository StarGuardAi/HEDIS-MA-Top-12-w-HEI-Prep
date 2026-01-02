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
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# Page configuration
st.set_page_config(
    page_title="AI Executive Insights - HEDIS Portfolio",
    page_icon="🤖",
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

/* ========== HEADER CONTAINER STYLES (Match Home Page) ========== */
.header-container {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%);
    padding: 0.5rem 0.75rem 0.6rem 0.75rem;
    border-radius: 6px;
    margin-top: -1rem !important;
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
    padding-top: 0rem !important;
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

# Apply sidebar styling (purple gradient matching StarGuard AI header)
from utils.sidebar_styling import apply_sidebar_styling
apply_sidebar_styling()

# Custom CSS for executive insights page - READABLE fonts, compact spacing - CENTER ALIGNED
st.markdown("""
<style>
    /* Center align all headers */
    h1, h2, h3, h4, h5, h6 {
        text-align: center !important;
    }
    
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4,
    div[data-testid="stMarkdownContainer"] h5,
    div[data-testid="stMarkdownContainer"] h6 {
        text-align: center !important;
    }
    
    /* Center align all metrics */
    [data-testid="stMetric"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"],
    [data-testid="metric-container"] {
        text-align: center !important;
    }
    
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.6rem 0.8rem;
        border-radius: 10px;
        color: white;
        margin: 0.2rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center !important;
    }
    
    .insight-card p {
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
        text-align: center !important;
    }
    
    .recommendation-card {
        background: white;
        padding: 0.5rem 0.7rem;
        border-radius: 8px;
        border-left: 4px solid #00cc66;
        margin: 0.2rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        text-align: center !important;
    }
    
    .recommendation-card h4 {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        margin: 0 0 0.2rem 0 !important;
        text-align: center !important;
    }
    
    .recommendation-card p {
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
        text-align: center !important;
    }
    
    .why-matters-box {
        background: #f0f4f8;
        padding: 0.5rem 0.7rem;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        margin: 0.2rem 0;
        text-align: center !important;
    }
    
    .why-matters-box p {
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
        text-align: center !important;
    }
    
    .metric-highlight {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0066cc;
        text-align: center !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.7rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'insights_generated' not in st.session_state:
    st.session_state.insights_generated = False
if 'insights_data' not in st.session_state:
    st.session_state.insights_data = None
if 'metrics_data' not in st.session_state:
    st.session_state.metrics_data = None

# Sidebar configuration
st.sidebar.header("🤖 AI Insights Configuration")

# Check API provider availability
api_provider = get_api_provider()

if api_provider == "none":
    # Provide more detailed diagnostic information
    missing_packages = []
    if not ANTHROPIC_AVAILABLE:
        missing_packages.append("anthropic")
    if not OPENAI_AVAILABLE:
        missing_packages.append("openai")
    
    st.sidebar.error("⚠️ No AI API configured")
    
    if missing_packages:
        st.sidebar.warning(f"📦 Missing packages: {', '.join(missing_packages)}")
        st.sidebar.code(f"pip install {' '.join(missing_packages)}", language="bash")
    
    st.sidebar.info("""
    To enable AI insights:
    
    1. **Install packages** (if missing above):
       `pip install anthropic` or `pip install openai`
    
    2. **Configure API key** (choose one):
       - Set environment variable: `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`
       - Or add to `.streamlit/secrets.toml`:
         ```
         [anthropic]
         api_key = "your-key-here"
         ```
    
    3. **Restart Streamlit** after installing packages
    """)
else:
    st.sidebar.success(f"✅ Using {api_provider.upper()} API")

# Date range selector
st.sidebar.subheader("📅 Date Range")
default_end = datetime.now().strftime("%Y-%m-%d")
default_start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

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
st.sidebar.subheader("🎯 Focus Area")
focus_option = st.sidebar.radio(
    "Select focus:",
    ["Portfolio Overview", "Top Opportunity", "Specific Measure"],
    index=0
)

selected_measure = None
if focus_option == "Specific Measure":
    # Get list of measures
    measures_query = """
        SELECT DISTINCT mi.measure_id, hm.measure_name
        FROM member_interventions mi
        LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
        WHERE mi.intervention_date >= '{start_date}' AND mi.intervention_date <= '{end_date}'
        ORDER BY hm.measure_name
    """.format(start_date=start_date_str, end_date=end_date_str)
    measures_df = execute_query(measures_query)
    
    if not measures_df.empty:
        measure_options = [f"{row['measure_name']} ({row['measure_id']})" 
                          for _, row in measures_df.iterrows()]
        selected_measure_display = st.sidebar.selectbox("Select Measure", measure_options)
        if selected_measure_display:
            selected_measure = selected_measure_display.split("(")[1].split(")")[0]
    else:
        st.sidebar.warning("No measures found for selected date range")

# Sidebar value proposition - at bottom
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

# Sidebar footer
render_sidebar_footer()

# Main content
st.title("🤖 AI-Powered Executive Insights")
st.markdown("---")

# Show portfolio summary metrics
portfolio_summary = get_portfolio_summary_metrics(start_date_str, end_date_str)

col1, col2, col3, col4 = st.columns(4, gap="small")
with col1:
    st.metric(
        "Total Investment",
        f"${portfolio_summary.get('total_investment', 0):,.0f}"
    )
with col2:
    st.metric(
        "Total Closures",
        f"{portfolio_summary.get('total_closures', 0):,}"
    )
with col3:
    st.metric(
        "ROI Ratio",
        f"{portfolio_summary.get('roi_ratio', 0):.2f}"
    )
with col4:
    st.metric(
        "Net Benefit",
        f"${portfolio_summary.get('net_benefit', 0):,.0f}"
    )

st.markdown("---")

# Generate insights button
if api_provider != "none":
    col1, col2, col3 = st.columns([1, 2, 1], gap="small")
    with col2:
        generate_button = st.button(
            "✨ Generate AI Insights",
            use_container_width=True,
            type="primary"
        )
    
    if generate_button or st.session_state.insights_generated:
        if generate_button:
            st.session_state.insights_generated = True
            
            # Show loading state
            with st.spinner("🤖 AI is analyzing your HEDIS portfolio data..."):
                try:
                    # Get metrics data
                    if focus_option == "Top Opportunity":
                        opportunities = get_top_opportunities(limit=1)
                        if opportunities:
                            selected_measure = opportunities[0].get("measure_id")
                    
                    metrics_data = format_metrics_for_ai(selected_measure)
                    st.session_state.metrics_data = metrics_data
                    
                    # Generate insights
                    insights = generate_executive_insights(metrics_data)
                    st.session_state.insights_data = insights
                    
                except Exception as e:
                    st.error(f"Error generating insights: {str(e)}")
                    st.info("Please check your API key configuration and try again.")
                    st.session_state.insights_generated = False
                    st.stop()
        
        # Display insights
        if st.session_state.insights_data:
            insights = st.session_state.insights_data
            
            # Executive Summary
            st.markdown("### 📊 Executive Summary")
            st.markdown(f'<div class="insight-card"><p style="font-size: 1.2rem; line-height: 1.8;">{insights.get("summary", "No summary available")}</p></div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Recommendations
            st.markdown("### 🎯 Actionable Recommendations")
            recommendations = insights.get("recommendations", [])
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(
                        f'<div class="recommendation-card">'
                        f'<h4 style="color: #0066cc; margin-bottom: 0.2rem;">Recommendation {i}</h4>'
                        f'<p style="font-size: 1rem; line-height: 1.6; color: #333;">{rec}</p>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.info("No specific recommendations generated. Review the metrics above for insights.")
            
            st.markdown("---")
            
            # Why This Matters
            st.markdown("### 💡 Why This Matters")
            why_matters = insights.get("why_matters", "These insights help optimize HEDIS performance.")
            st.markdown(
                f'<div class="why-matters-box">'
                f'<p style="font-size: 1rem; line-height: 1.8; color: #333;">{why_matters}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            
            # Show underlying metrics (expandable)
            with st.expander("📈 View Underlying Metrics Data"):
                if st.session_state.metrics_data:
                    st.json(st.session_state.metrics_data)
            
            # Regenerate button
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1], gap="small")
            with col2:
                if st.button("🔄 Regenerate Insights", use_container_width=True):
                    st.session_state.insights_generated = False
                    st.rerun()
        
else:
    st.info("""
    ### ⚠️ AI API Not Configured
    
    To enable AI-powered insights, please configure one of the following:
    
    1. **OpenAI API**: Set `OPENAI_API_KEY` environment variable
    2. **Anthropic Claude API**: Set `ANTHROPIC_API_KEY` environment variable
    3. **Streamlit Secrets**: Add API keys to `.streamlit/secrets.toml`
    
    Example `.streamlit/secrets.toml`:
    ```toml
    [openai]
    api_key = "sk-your-key-here"
    
    # OR
    
    [anthropic]
    api_key = "sk-ant-your-key-here"
    ```
    """)
    
    # Show sample insights format
    st.markdown("---")
    st.markdown("### 📋 Sample Insights Format")
    st.markdown("""
    When configured, AI insights will include:
    
    - **Executive Summary**: High-level findings in natural language
    - **Actionable Recommendations**: Specific, prioritized actions with numbers and timelines
    - **Why This Matters**: Business impact explanation for executives
    
    Example output:
    > "Your HbA1c testing program shows 93% predicted closure rate with $285K potential. 
    > Recommend prioritizing 847 members in the next 30 days for maximum ROI."
    """)

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer

