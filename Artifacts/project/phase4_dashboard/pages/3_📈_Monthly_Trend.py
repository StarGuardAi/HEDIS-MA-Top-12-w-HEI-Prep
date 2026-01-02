"""
Page 3: Monthly Intervention Trend
Line chart showing intervention trends over time
"""
import streamlit as st

st.set_page_config(page_title="Monthly Trend", page_icon="📈", layout="wide")

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


import pandas as pd
from datetime import datetime

from utils.database import execute_query
from utils.queries import get_monthly_intervention_trend_query
from utils.charts import create_line_chart
from utils.data_helpers import show_data_availability_warning, format_date_display, format_month_display
from utils.plan_context import get_plan_size_scenarios
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header, apply_compact_css

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

st.sidebar.success("📱 Mobile Optimized")

# Sidebar footer
render_sidebar_footer()

# Initialize session state if not exists
if 'membership_size' not in st.session_state:
    st.session_state.membership_size = 10000

BASELINE_MEMBERS = 10000
scale_factor = st.session_state.membership_size / BASELINE_MEMBERS
membership_size = st.session_state.membership_size

st.title("📊 Monthly Trends Analysis")
st.markdown(f"### Q4 2024 Turnaround Initiative Tracking - {membership_size:,} member plan")
st.markdown("**Intervention volume and success over time**")
st.markdown("Track intervention volume and success over time")

# Get plan context for storytelling
plan_scenarios = get_plan_size_scenarios()
current_scenario = plan_scenarios.get(membership_size, plan_scenarios[10000])

# Storytelling context
if membership_size == 10000:
    st.info("💡 **Small Plans:** Proves ROI before scaling - Monthly trends show consistent improvement during turnaround.")
elif membership_size <= 25000:
    st.success("💡 **Mid-Size Plans:** Your typical turnaround scenario - Proven monthly patterns at this scale.")
else:
    st.warning("💡 **Large/Enterprise Plans:** Enterprise-scale impact projection - Monthly trends scaled for larger operations.")

st.divider()

# Date range filter
col1, col2 = st.columns(2, gap="small")
with col1:
    start_date = st.date_input("Start Date", value=datetime(2024, 10, 1), key="trend_start", format="MM/DD/YYYY")
with col2:
    end_date = st.date_input("End Date", value=datetime(2024, 12, 31), key="trend_end", format="MM/DD/YYYY")

# Check data availability
show_data_availability_warning(start_date, end_date)

# Execute query
try:
    query = get_monthly_intervention_trend_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    df = execute_query(query)
    
    if df.empty:
        st.warning("No data found for the selected date range.")
    else:
        # Scale data (success_rate and avg_cost are constants)
        # Convert to float first to avoid Decimal type issues
        df_scaled = df.copy()
        df_scaled['total_interventions'] = df_scaled['total_interventions'].astype(float) * scale_factor
        df_scaled['successful_closures'] = df_scaled['successful_closures'].astype(float) * scale_factor
        df_scaled['total_investment'] = df_scaled['total_investment'].astype(float) * scale_factor
        # Ensure success_rate is float (not Decimal or string)
        df_scaled['success_rate'] = df_scaled['success_rate'].astype(float)
        
        # Summary metrics (scaled)
        col1, col2, col3, col4 = st.columns(4, gap="small")
        with col1:
            total_interventions = df_scaled['total_interventions'].sum()
            st.metric("Total Interventions", f"{int(total_interventions):,}")
        with col2:
            total_closures = df_scaled['successful_closures'].sum()
            st.metric("Total Closures", f"{int(total_closures):,}")
        with col3:
            avg_success_rate = df_scaled['success_rate'].mean()
            st.metric("Avg Success Rate", f"{avg_success_rate:.1f}%")
        with col4:
            total_investment = df_scaled['total_investment'].sum()
            st.metric("Total Investment", f"${total_investment:,.0f}")
        
        st.divider()
        
        # Format month column for charts (use scaled data)
        df_chart = df_scaled.copy()
        df_chart["month"] = df_chart["month"].apply(format_month_display)
        
        # Chart titles with scale indicator if not 10K
        title_suffix = f" ({membership_size:,} member plan)" if membership_size != BASELINE_MEMBERS else ""
        
        # Line chart - interventions and closures
        col1, col2 = st.columns(2, gap="small")
        
        with col1:
            fig1 = create_line_chart(
                df_chart,
                x_col="month",
                y_cols=["total_interventions", "successful_closures"],
                title=f"Intervention Volume and Success Trends{title_suffix}",
                x_label="Month",
                y_label="Count",
            )
            st.plotly_chart(fig1, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        with col2:
            fig2 = create_line_chart(
                df_chart,
                x_col="month",
                y_cols=["success_rate"],
                title="Success Rate Trend",
                x_label="Month",
                y_label="Success Rate (%)",
            )
            st.plotly_chart(fig2, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Full width chart - investment and cost
        fig3 = create_line_chart(
            df_chart,
            x_col="month",
            y_cols=["total_investment", "avg_cost"],
            title=f"Investment and Cost Trends{title_suffix}",
            x_label="Month",
            y_label="Amount ($)",
        )
        st.plotly_chart(fig3, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Data table (scaled)
        with st.expander("📋 View Detailed Data"):
            display_df = df_scaled[[
                "month",
                "total_interventions",
                "successful_closures",
                "success_rate",
                "avg_cost",
                "total_investment"
            ]].copy()
            # Format month column for display
            display_df["month"] = display_df["month"].apply(format_month_display)
            display_df.columns = [
                "Month",
                "Total Interventions",
                "Successful Closures",
                "Success Rate (%)",
                "Average Cost ($)",
                "Total Investment ($)"
            ]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"monthly_trend_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        
        # Trend insights
        st.divider()
        st.subheader("💡 Trend Insights")
        
        col1, col2 = st.columns(2, gap="small")
        
        # Calculate trend direction (using scaled data)
        if len(df_scaled) >= 2:
            first_rate = df_scaled.iloc[0]['success_rate']
            last_rate = df_scaled.iloc[-1]['success_rate']
            rate_change = last_rate - first_rate
            
            first_volume = df_scaled.iloc[0]['total_interventions']
            last_volume = df_scaled.iloc[-1]['total_interventions']
            volume_change = last_volume - first_volume
            
            with col1:
                if rate_change > 0:
                    st.success(f"✅ Success rate **increased** by {rate_change:.1f}% over the period")
                elif rate_change < 0:
                    st.warning(f"⚠️ Success rate **decreased** by {abs(rate_change):.1f}% over the period")
                else:
                    st.info("➡️ Success rate remained **stable**")
            
            with col2:
                if volume_change > 0:
                    st.info(f"📈 Intervention volume **increased** by {volume_change:.0f} over the period")
                elif volume_change < 0:
                    st.info(f"📉 Intervention volume **decreased** by {abs(volume_change):.0f} over the period")
                else:
                    st.info("➡️ Intervention volume remained **stable**")
        
        # Best and worst months (using scaled data)
        col3, col4 = st.columns(2, gap="small")
        best_month = df_scaled.loc[df_scaled['success_rate'].idxmax()]
        worst_month = df_scaled.loc[df_scaled['success_rate'].idxmin()]
        
        with col3:
            st.success(
                f"**Best Month:** {format_month_display(best_month['month'])}\n"
                f"- Success Rate: {best_month['success_rate']:.1f}%\n"
                f"- Interventions: {int(best_month['total_interventions'])}\n"
                f"- Closures: {int(best_month['successful_closures'])}"
            )
        
        with col4:
            st.info(
                f"**Challenging Month:** {format_month_display(worst_month['month'])}\n"
                f"- Success Rate: {worst_month['success_rate']:.1f}%\n"
                f"- Interventions: {int(worst_month['total_interventions'])}\n"
                f"- Closures: {int(worst_month['successful_closures'])}"
            )
            
except Exception as e:
    st.error(f"Error loading data: {e}")

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer



