"""
Page 2: Cost per Closure by Activity
Scatter plot showing cost-effectiveness of intervention activities
"""
import streamlit as st

st.set_page_config(page_title="Cost Per Closure", page_icon="💰", layout="wide")

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
    
    /* Hide "Mobile Optimized" message on mobile */
    [data-testid="stSidebar"] [data-testid="stSuccess"] {
        display: none !important;
    }
}

/* Desktop: Show "Mobile Optimized" message */
@media (min-width: 769px) {
    [data-testid="stSidebar"] [data-testid="stSuccess"] {
        display: block !important;
    }
}
</style>
""", unsafe_allow_html=True)


import pandas as pd
from datetime import datetime

from utils.database import execute_query
from utils.queries import get_cost_per_closure_by_activity_query
from utils.data_helpers import show_data_availability_warning, format_date_display
from utils.plan_context import get_plan_size_scenarios
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header, apply_compact_css

# ============================================================================
# RESPONSIVE DESIGN SYSTEM - Desktop & Mobile Formatting
# ============================================================================
st.markdown("""
<style>
/* ========== DESKTOP STYLES (default, 769px+) ========== */
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
    box-shadow: 0 3px 6px rgba(74, 61, 111, 0.2);
}

.header-title {
    color: white !important;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 0.35rem;
    display: block !important;
    line-height: 1.4;
}

.header-subtitle {
    color: #E8D4FF !important;
    font-size: 0.8rem;
    font-style: italic;
    display: block !important;
    line-height: 1.3;
}

div.block-container {
    padding-top: 0rem !important;
}

/* Zero-top enforcement - Headers flush to top */
.main > div:first-child {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

.block-container {
    padding-top: 0rem !important;
}

h1 {
    margin-top: 0.75rem !important;
    font-size: 2rem !important;
}

/* ========== MOBILE STYLES (max-width: 768px) ========== */
@media (max-width: 768px) {
    .header-container {
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: -1rem !important;
        margin-bottom: 0.1rem;
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
    
    div.block-container {
        padding-top: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    h1 {
        margin-top: 0.5rem !important;
        font-size: 1.5rem !important;
        line-height: 1.3;
    }
    
    h2 {
        font-size: 1.25rem !important;
    }
    
    [data-testid="column"] {
        width: 100% !important;
    }
    
    button[kind="primary"],
    button[kind="secondary"] {
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Responsive Header - Adapts to Desktop/Mobile
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
    
    /* Ensure chart titles wrap */
    .js-plotly-plot .gtitle text,
    .plotly .gtitle text {
        word-wrap: break-word !important;
        white-space: normal !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.sidebar.success("📱 Mobile Optimized")

# Sidebar footer
render_sidebar_footer()
import plotly.express as px

# Initialize session state if not exists
if 'membership_size' not in st.session_state:
    st.session_state.membership_size = 10000

BASELINE_MEMBERS = 10000
scale_factor = st.session_state.membership_size / BASELINE_MEMBERS
membership_size = st.session_state.membership_size

st.title("📈 Intervention Performance Analysis")
st.markdown(f"### Breakthrough: Low-touch digital outperforms traditional - {membership_size:,} member plan")
st.markdown("**Scalable strategy for plans of any size**")
st.markdown("Analyze cost-effectiveness of different intervention activities")

# Get plan context for storytelling
plan_scenarios = get_plan_size_scenarios()
current_scenario = plan_scenarios.get(membership_size, plan_scenarios[10000])

# Storytelling context
if membership_size == 10000:
    st.info("💡 **Small Plans:** Proves ROI before scaling - This demonstrates low-touch digital can outperform traditional methods.")
elif membership_size <= 25000:
    st.success("💡 **Mid-Size Plans:** Your typical turnaround scenario - Scalable strategies proven at smaller scale.")
else:
    st.warning("💡 **Large/Enterprise Plans:** Enterprise-scale impact projection - Strategies proven at smaller scale adapted for larger operations.")

st.divider()

# Filters
col1, col2, col3 = st.columns([1, 1, 1], gap="small")
with col1:
    start_date = st.date_input("Start Date", value=datetime(2024, 10, 1), key="scatter_start", format="MM/DD/YYYY")
with col2:
    end_date = st.date_input("End Date", value=datetime(2024, 12, 31), key="scatter_end", format="MM/DD/YYYY")
with col3:
    min_uses = st.number_input("Minimum Uses", min_value=1, value=10, help="Filter activities with at least this many uses")
    st.markdown(f"**Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

# Execute query
try:
    query = get_cost_per_closure_by_activity_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
        int(min_uses)
    )
    df = execute_query(query)
    
    if df.empty:
        st.warning("No data found for the selected criteria.")
    else:
        # Scale data (cost_per_closure and success_rate are constants, but times_used and successful_closures scale)
        # Convert to float first to avoid Decimal type issues
        df_scaled = df.copy()
        df_scaled['times_used'] = df_scaled['times_used'].astype(float) * scale_factor
        df_scaled['successful_closures'] = df_scaled['successful_closures'].astype(float) * scale_factor
        # Ensure success_rate is float (not Decimal or string)
        df_scaled['success_rate'] = df_scaled['success_rate'].astype(float)
        
        # Summary metrics (cost_per_closure and success_rate are constants)
        col1, col2, col3, col4 = st.columns(4, gap="small")
        with col1:
            most_cost_effective = df_scaled.loc[df_scaled['cost_per_closure'].idxmin()]
            st.metric(
                "Most Cost-Effective",
                f"${most_cost_effective['cost_per_closure']:.2f}",
                delta=f"{most_cost_effective['activity_name']}"
            )
        with col2:
            highest_success = df_scaled.loc[df_scaled['success_rate'].idxmax()]
            st.metric(
                "Highest Success Rate",
                f"{highest_success['success_rate']:.1f}%",
                delta=f"{highest_success['activity_name']}"
            )
        with col3:
            avg_cost = df_scaled['avg_cost'].mean()
            st.metric("Average Cost", f"${avg_cost:.2f}")
        with col4:
            avg_success = df_scaled['success_rate'].mean()
            st.metric("Average Success Rate", f"{avg_success:.1f}%")
        
        st.divider()
        
        # Scatter plot (scaled) - Simple version without text labels
        # Use line break for mobile wrapping
        chart_title = "Cost Efficiency Analysis<br>by Intervention Type"
        if membership_size != BASELINE_MEMBERS:
            chart_title += f"<br>({membership_size:,} member plan)"
        
        # Create simple scatter plot WITHOUT text labels - show names on hover only
        fig = px.scatter(
            df_scaled,
            x='avg_cost',
            y='success_rate',
            size='times_used',
            title=chart_title,
            labels={
                'avg_cost': 'Average Cost per Intervention ($)',
                'success_rate': 'Success Rate (%)',
                'times_used': 'Volume',
            },
            hover_name='activity_name',  # Show name on hover
            hover_data={
                'avg_cost': ':.2f',
                'success_rate': ':.1f',
                'times_used': ':,.0f',
                'cost_per_closure': ':.2f',
            },
            color_discrete_sequence=['#4e2a84'],  # Use theme color
        )
        
        # Update layout for mobile - no text labels
        fig.update_layout(
            height=350,
            autosize=True,
            margin=dict(l=80, r=40, t=120, b=80),
            title={
                'text': chart_title + '<br><sub>Hover over points for details</sub>',
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 18, 'color': '#4e2a84'},
                'automargin': True  # Allow title to wrap automatically
            },
            xaxis_title='Average Cost per Intervention ($)',
            yaxis_title='Success Rate (%)',
            showlegend=False,  # No legend needed for single color
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
        )
        
        # Remove any text labels completely (text=None removes labels, no textposition needed)
        fig.update_traces(text=None)
        
        st.plotly_chart(fig, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Data table (scaled)
        with st.expander("📋 View Detailed Data"):
            display_df = df_scaled[[
                "activity_name",
                "avg_cost",
                "success_rate",
                "times_used",
                "successful_closures",
                "cost_per_closure"
            ]].copy()
            display_df.columns = [
                "Activity Name",
                "Avg Cost ($)",
                "Success Rate (%)",
                "Times Used",
                "Successful Closures",
                "Cost per Closure ($)"
            ]
            st.dataframe(display_df.sort_values("Cost per Closure ($)"), use_container_width=True, hide_index=True)
            
            # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"cost_per_closure_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        
        # Insights
        st.divider()
        st.subheader("💡 Key Insights")
        
        # Best performers
        col1, col2 = st.columns(2, gap="small")
        
        with col1:
            best_combo = df_scaled.loc[(df_scaled['success_rate'] - df_scaled['avg_cost']/10).idxmax()]
            st.success(
                f"**Best Value:** {best_combo['activity_name']}\n"
                f"- Cost: ${best_combo['avg_cost']:.2f}\n"
                f"- Success Rate: {best_combo['success_rate']:.1f}%\n"
                f"- Cost per Closure: ${best_combo['cost_per_closure']:.2f}"
            )
        
        with col2:
            st.info(
                f"**Activity Count:** {len(df_scaled)} activities analyzed\n"
                f"- Average usage: {df_scaled['times_used'].mean():.0f} times\n"
                f"- Total closures: {int(df_scaled['successful_closures'].sum())}\n"
                f"- Cost range: ${df_scaled['avg_cost'].min():.2f} - ${df_scaled['avg_cost'].max():.2f}"
            )
            
except Exception as e:
    st.error(f"Error loading data: {e}")

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer



