"""
What-If Scenario Modeler - Desktop Version
Interactive tool for healthcare managers to model budget and FTE scenarios
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io

# Check for openpyxl availability for Excel export
try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    openpyxl = None

from utils.database import show_db_status
from utils.scenario_modeler import ScenarioModeler
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# Page configuration
st.set_page_config(
    page_title="What-If Scenario Modeler - HEDIS Portfolio",
    page_icon="📊",
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
    .scenario-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #0066cc;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .metric-highlight {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0066cc;
    }
    
    .constraint-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .constraint-budget {
        background: #ffe6e6;
        color: #cc0000;
    }
    
    .constraint-capacity {
        background: #e6f3ff;
        color: #0066cc;
    }
    
    .stSlider>div>div>div {
        background: linear-gradient(90deg, #0066cc 0%, #00cc66 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = []
if 'modeler' not in st.session_state:
    st.session_state.modeler = None

# Sidebar
st.sidebar.header("📊 Scenario Modeler")
st.sidebar.markdown("Model budget and FTE scenarios to predict ROI impact.")

# Date range for baseline data
st.sidebar.subheader("📅 Baseline Data Period")
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

# Initialize modeler
if st.session_state.modeler is None or True:  # Always refresh for now
    with st.sidebar:
        with st.spinner("Loading baseline data..."):
            st.session_state.modeler = ScenarioModeler(start_date_str, end_date_str)
            st.sidebar.success("✅ Baseline data loaded")
        
        # Sidebar value proposition - at bottom
        from utils.value_proposition import render_sidebar_value_proposition
        render_sidebar_value_proposition()
        
        # Sidebar footer
        render_sidebar_footer()

# Main content
st.title("📊 What-If Scenario Modeler")
st.markdown("Adjust budget and FTE allocations to see predicted ROI impact in real-time.")

# Scenario comparison section
st.header("🎯 Scenario Comparison")

# Create 3 scenarios
scenario_cols = st.columns(3, gap="small")

scenarios_config = []
for i, col in enumerate(scenario_cols, 1):
    with col:
        st.subheader(f"Scenario {i}")
        
        scenario_name = st.text_input(
            f"Name",
            value=f"Scenario {i}",
            key=f"scenario_{i}_name"
        )
        
        budget = st.slider(
            "Budget ($)",
            min_value=50000,
            max_value=500000,
            value=250000 if i == 2 else (150000 if i == 1 else 350000),
            step=10000,
            key=f"scenario_{i}_budget",
            format="$%d"
        )
        
        fte_count = st.slider(
            "FTE Count",
            min_value=1,
            max_value=10,
            value=5 if i == 2 else (3 if i == 1 else 7),
            step=1,
            key=f"scenario_{i}_fte"
        )
        
        strategy = st.selectbox(
            "Strategy",
            options=["balanced", "high_roi", "high_volume"],
            index=0,
            key=f"scenario_{i}_strategy",
            format_func=lambda x: {
                "balanced": "Balanced",
                "high_roi": "High ROI Focus",
                "high_volume": "High Volume Focus"
            }[x]
        )
        
        scenarios_config.append({
            "name": scenario_name,
            "budget": budget,
            "fte_count": fte_count,
            "strategy": strategy
        })

# Calculate scenarios automatically (real-time updates)
# Store scenarios in session state for comparison
current_scenarios_key = f"scenarios_{start_date_str}_{end_date_str}"
if current_scenarios_key not in st.session_state:
    st.session_state[current_scenarios_key] = scenarios_config
else:
    # Update if config changed
    if st.session_state[current_scenarios_key] != scenarios_config:
        st.session_state[current_scenarios_key] = scenarios_config

# Use current scenarios
st.session_state.scenarios = st.session_state[current_scenarios_key]

if st.session_state.scenarios:
    # Calculate all scenarios
    comparison_df = st.session_state.modeler.compare_scenarios(st.session_state.scenarios)
    
    # Display comparison metrics
    st.markdown("---")
    st.subheader("📈 Scenario Comparison Results")
    
    # Key metrics comparison
    metric_cols = st.columns(5, gap="small")
    metrics_to_show = [
        ("predicted_closures", "Predicted Closures"),
        ("predicted_revenue", "Predicted Revenue"),
        ("predicted_roi_ratio", "ROI Ratio"),
        ("predicted_net_benefit", "Net Benefit"),
        ("predicted_success_rate", "Success Rate %")
    ]
    
    for col, (metric_key, metric_label) in zip(metric_cols, metrics_to_show):
        with col:
            st.metric(
                metric_label,
                comparison_df[metric_key].max(),
                delta=f"vs {comparison_df[metric_key].min():.0f} min"
            )
    
    # Detailed comparison table
    st.markdown("### 📋 Detailed Comparison")
    
    display_df = comparison_df[[
        "scenario_name", "budget", "fte_count", "strategy",
        "predicted_interventions", "predicted_closures",
        "predicted_revenue", "actual_cost", "predicted_roi_ratio",
        "predicted_net_benefit", "predicted_success_rate", "constraint"
    ]].copy()
    
    display_df.columns = [
        "Scenario", "Budget", "FTE", "Strategy",
        "Interventions", "Closures", "Revenue", "Cost",
        "ROI Ratio", "Net Benefit", "Success Rate %", "Constraint"
    ]
    
    # Format columns
    display_df["Budget"] = display_df["Budget"].apply(lambda x: f"${x:,.0f}")
    display_df["Revenue"] = display_df["Revenue"].apply(lambda x: f"${x:,.0f}")
    display_df["Cost"] = display_df["Cost"].apply(lambda x: f"${x:,.0f}")
    display_df["Net Benefit"] = display_df["Net Benefit"].apply(lambda x: f"${x:,.0f}")
    display_df["ROI Ratio"] = display_df["ROI Ratio"].apply(lambda x: f"{x:.2f}")
    display_df["Success Rate %"] = display_df["Success Rate %"].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Visualizations
    st.markdown("---")
    st.subheader("📊 Visualizations")
    
    viz_col1, viz_col2 = st.columns(2, gap="small")
    
    with viz_col1:
        # ROI Comparison Bar Chart
        fig_roi = px.bar(
            comparison_df,
            x="scenario_name",
            y="predicted_roi_ratio",
            title="ROI Ratio by Scenario",
            labels={"scenario_name": "Scenario", "predicted_roi_ratio": "ROI Ratio"},
            color="predicted_roi_ratio",
            color_continuous_scale="Blues"
        )
        fig_roi.update_layout(showlegend=False)
        st.plotly_chart(fig_roi, use_container_width=True)
    
    with viz_col2:
        # Net Benefit Comparison
        fig_net = px.bar(
            comparison_df,
            x="scenario_name",
            y="predicted_net_benefit",
            title="Net Benefit by Scenario",
            labels={"scenario_name": "Scenario", "predicted_net_benefit": "Net Benefit ($)"},
            color="predicted_net_benefit",
            color_continuous_scale="Greens"
        )
        fig_net.update_layout(showlegend=False)
        st.plotly_chart(fig_net, use_container_width=True)
    
    # Pareto Frontier Chart
    st.markdown("### 🎯 Pareto Frontier Analysis")
    st.markdown("Shows trade-offs between ROI and volume. Points on the frontier represent optimal configurations.")
    
    with st.spinner("Generating Pareto frontier..."):
        pareto_df = st.session_state.modeler.generate_pareto_frontier(num_points=100)
    
    if not pareto_df.empty:
        fig_pareto = go.Figure()
        
        # Add Pareto frontier line
        fig_pareto.add_trace(go.Scatter(
            x=pareto_df["predicted_roi_ratio"],
            y=pareto_df["predicted_closures"],
            mode="lines+markers",
            name="Pareto Frontier",
            line=dict(color="#0066cc", width=2),
            marker=dict(size=8, color="#00cc66")
        ))
        
        # Add scenario points
        for _, row in comparison_df.iterrows():
            fig_pareto.add_trace(go.Scatter(
                x=[row["predicted_roi_ratio"]],
                y=[row["predicted_closures"]],
                mode="markers+text",
                name=row["scenario_name"],
                marker=dict(size=15, symbol="star", color="#ff6600"),
                text=[row["scenario_name"]],
                textposition="top center"
            ))
        
        fig_pareto.update_layout(
            title="Pareto Frontier: ROI vs Closures",
            xaxis_title="ROI Ratio",
            yaxis_title="Predicted Closures",
            hovermode="closest",
            height=350
        )
        
        st.plotly_chart(fig_pareto, use_container_width=True)
        
        st.caption("💡 Points on the frontier represent optimal trade-offs. Scenarios above the line are suboptimal.")
    
    # Export functionality
    st.markdown("---")
    st.subheader("📥 Export Scenario Report")
    
    export_col1, export_col2, export_col3 = st.columns(3, gap="small")
    
    with export_col1:
        # Export to CSV
        csv_buffer = io.StringIO()
        comparison_df.to_csv(csv_buffer, index=False)
        st.download_button(
            "📄 Download CSV",
            csv_buffer.getvalue(),
            file_name=f"scenario_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with export_col2:
        # Export to Excel
        if OPENPYXL_AVAILABLE:
            try:
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    comparison_df.to_excel(writer, sheet_name="Scenario Comparison", index=False)
                    # Add summary sheet
                    summary_data = {
                        "Metric": ["Best ROI", "Most Closures", "Highest Net Benefit"],
                        "Scenario": [
                            comparison_df.loc[comparison_df["predicted_roi_ratio"].idxmax(), "scenario_name"],
                            comparison_df.loc[comparison_df["predicted_closures"].idxmax(), "scenario_name"],
                            comparison_df.loc[comparison_df["predicted_net_benefit"].idxmax(), "scenario_name"]
                        ],
                        "Value": [
                            f"{comparison_df['predicted_roi_ratio'].max():.2f}",
                            f"{comparison_df['predicted_closures'].max():.0f}",
                            f"${comparison_df['predicted_net_benefit'].max():,.0f}"
                        ]
                    }
                    pd.DataFrame(summary_data).to_excel(writer, sheet_name="Summary", index=False)
                
                st.download_button(
                    "📊 Download Excel",
                    excel_buffer.getvalue(),
                    file_name=f"scenario_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Error creating Excel export: {str(e)}")
        else:
            st.warning("⚠️ Excel export requires openpyxl")
            st.info("💡 Install openpyxl for Excel export:")
            st.code("pip install openpyxl", language="bash")
            st.info("Then restart Streamlit to enable Excel downloads.")
    
    with export_col3:
        # Generate text report
        report_text = f"""
HEDIS Portfolio - Scenario Comparison Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Baseline Period: {start_date_str} to {end_date_str}

SCENARIO SUMMARY
================

"""
        for _, row in comparison_df.iterrows():
            report_text += f"""
{row['scenario_name']}
  Budget: ${row['budget']:,.0f}
  FTE Count: {row['fte_count']}
  Strategy: {row['strategy'].title()}
  
  Predicted Interventions: {row['predicted_interventions']:,.0f}
  Predicted Closures: {row['predicted_closures']:,.0f}
  Predicted Revenue: ${row['predicted_revenue']:,.0f}
  Actual Cost: ${row['actual_cost']:,.0f}
  ROI Ratio: {row['predicted_roi_ratio']:.2f}
  Net Benefit: ${row['predicted_net_benefit']:,.0f}
  Success Rate: {row['predicted_success_rate']:.1f}%
  Constraint: {row['constraint'].title()}

"""
        
        report_text += f"""
BEST SCENARIOS
==============
Best ROI: {comparison_df.loc[comparison_df['predicted_roi_ratio'].idxmax(), 'scenario_name']} 
  (ROI: {comparison_df['predicted_roi_ratio'].max():.2f})

Most Closures: {comparison_df.loc[comparison_df['predicted_closures'].idxmax(), 'scenario_name']}
  (Closures: {comparison_df['predicted_closures'].max():,.0f})

Highest Net Benefit: {comparison_df.loc[comparison_df['predicted_net_benefit'].idxmax(), 'scenario_name']}
  (Net Benefit: ${comparison_df['predicted_net_benefit'].max():,.0f})
"""
        
        st.download_button(
            "📝 Download Text Report",
            report_text,
            file_name=f"scenario_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    st.info("👆 Configure scenarios above and click 'Calculate Scenarios' to see results.")

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer



