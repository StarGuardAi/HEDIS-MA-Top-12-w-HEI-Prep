"""
Historical Performance Tracking - Desktop Version
Full interactive time-series explorer with forecasting
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from utils.database import show_db_status, execute_query
from utils.historical_tracking import HistoricalTracker
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header

# Page configuration
st.set_page_config(
    page_title="Historical Tracking - HEDIS Portfolio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-compact CSS for vertical space reduction
st.markdown("""
<style>
.main .block-container { padding-top: 0.5rem !important; padding-bottom: 1rem !important; padding-left: 1rem !important; padding-right: 1rem !important; max-width: 100% !important; }
h1 { font-size: 1.5rem !important; margin-top: 0.5rem !important; margin-bottom: 0.5rem !important; padding: 0 !important; line-height: 1.2 !important; }
h2 { font-size: 1.2rem !important; margin-top: 0.4rem !important; margin-bottom: 0.4rem !important; padding: 0 !important; line-height: 1.2 !important; }
h3 { font-size: 1rem !important; margin-top: 0.3rem !important; margin-bottom: 0.3rem !important; padding: 0 !important; line-height: 1.2 !important; }
.element-container { margin-bottom: 0.3rem !important; }
.stMarkdown { margin-bottom: 0.3rem !important; }
[data-testid="stMetricValue"] { font-size: 1.5rem !important; }
[data-testid="stMetricLabel"] { font-size: 0.8rem !important; padding-bottom: 0.2rem !important; }
[data-testid="metric-container"] { padding: 0.5rem !important; }
.stPlotlyChart { margin-bottom: 0.5rem !important; }
.stDataFrame { margin-bottom: 0.5rem !important; }
[data-testid="column"] { padding: 0.25rem !important; }
[data-testid="stExpander"] { margin-bottom: 0.3rem !important; }
[data-testid="stTabs"] { margin-bottom: 0.5rem !important; }
.stTabs [data-baseweb="tab-list"] { gap: 0.25rem !important; }
.stTabs [data-baseweb="tab"] { padding: 0.4rem 0.8rem !important; font-size: 0.85rem !important; }
.stButton > button { padding: 0.4rem 0.8rem !important; font-size: 0.85rem !important; }
.stSelectbox, .stTextInput, .stNumberInput { margin-bottom: 0.3rem !important; }
.stAlert { padding: 0.5rem !important; margin-bottom: 0.5rem !important; font-size: 0.85rem !important; }
div[data-testid="stVerticalBlock"] > div { gap: 0.3rem !important; }
hr { margin: 0.5rem 0 !important; }
@media (max-width: 768px) {
    .main .block-container { padding-top: 0.25rem !important; padding-bottom: 0.5rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
    h1 { font-size: 1.2rem !important; margin-top: 0.3rem !important; margin-bottom: 0.3rem !important; }
    h2 { font-size: 1rem !important; margin-top: 0.25rem !important; margin-bottom: 0.25rem !important; }
    h3 { font-size: 0.9rem !important; margin-top: 0.2rem !important; margin-bottom: 0.2rem !important; }
    .element-container { margin-bottom: 0.2rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.2rem !important; }
    [data-testid="stMetricLabel"] { font-size: 0.7rem !important; }
    [data-testid="column"] { padding: 0.15rem !important; }
    .stButton > button { padding: 0.3rem 0.6rem !important; font-size: 0.8rem !important; }
}
</style>
""", unsafe_allow_html=True)

# Page header
render_header()

# Apply sidebar styling (blue gradient like landing page)
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
# Sidebar value proposition
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

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

# Monthly trends
st.markdown("---")
st.header("📉 Monthly Trends")

trends_df = st.session_state.historical_tracker.get_monthly_trends(
    measure_id=selected_measure,
    start_date=start_date_str,
    end_date=end_date_str
)

if not trends_df.empty:
    # Interactive time-series chart
    if view_option == "All Measures":
        # Multi-line chart for all measures
        fig = go.Figure()
        
        for measure_id in trends_df['measure_id'].unique():
            measure_data = trends_df[trends_df['measure_id'] == measure_id]
            measure_name = measure_data['measure_name'].iloc[0]
            
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(measure_data['month_start']),
                y=measure_data['success_rate'],
                mode='lines+markers',
                name=measure_name,
                hovertemplate=f'<b>{measure_name}</b><br>' +
                             'Date: %{x}<br>' +
                             'Success Rate: %{y:.1f}%<br>' +
                             '<extra></extra>'
            ))
        
        fig.update_layout(
            title={
                'text': "Monthly Success Rate Trends - All Measures",
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title="Month",
            yaxis_title="Success Rate (%)",
            hovermode='closest',
            height=350,
            margin=dict(t=100, b=50, l=50, r=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
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

