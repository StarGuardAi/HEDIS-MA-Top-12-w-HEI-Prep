"""
Competitive Benchmarking Analysis Dashboard

Comprehensive benchmarking against:
- CMS Star Ratings
- HEDIS benchmarks
- Regional performance
- NQF standards
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.competitive_benchmarking import CompetitiveBenchmarking
from utils.database import get_db_connection
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header, apply_compact_css

st.set_page_config(
    page_title="Competitive Benchmarking",
    page_icon="📊",
    layout="wide"
)

# Rename "app" to "Home" in sidebar navigation
st.markdown("""
<style>
/* Method 1: Replace text content with CSS */
[data-testid="stSidebarNav"] ul li:first-child a {
    font-size: 0 !important;  /* Hide original "app" text */
    background: linear-gradient(135deg, rgba(139,122,184,0.3), rgba(111,95,150,0.3)) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="stSidebarNav"] ul li:first-child a::before {
    content: "🏠 Home";  /* Replace with "Home" */
    font-size: 1.1rem !important;
    color: white !important;
    font-weight: 700 !important;
}

[data-testid="stSidebarNav"] ul li:first-child a:hover {
    background: linear-gradient(135deg, rgba(139,122,184,0.5), rgba(111,95,150,0.5)) !important;
}

/* Method 2: Also target by href */
[data-testid="stSidebarNav"] a[href="/"],
[data-testid="stSidebarNav"] a[href="./"] {
    font-size: 0 !important;
    background: linear-gradient(135deg, rgba(139,122,184,0.3), rgba(111,95,150,0.3)) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
}

[data-testid="stSidebarNav"] a[href="/"]::before,
[data-testid="stSidebarNav"] a[href="./"]::before {
    content: "🏠 Home";
    font-size: 1.1rem !important;
    color: white !important;
    font-weight: 700 !important;
}

/* ========== PURPLE SIDEBAR THEME (Match Home Page) ========== */
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

st.title("📊 Competitive Benchmarking Analysis")
st.markdown("Compare your plan's performance against national, regional, and similar plan benchmarks")

# Initialize benchmarking engine
@st.cache_resource
def get_benchmarking_engine():
    db = get_db_connection()
    return CompetitiveBenchmarking(db_connection=db)

benchmarking = get_benchmarking_engine()

# Summary Statistics
st.header("📈 Summary Overview")
summary = benchmarking.get_summary_statistics()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Avg National Percentile",
        f"{summary['avg_national_percentile']:.0f}th",
        delta=f"{summary['top_quartile_measures']} in top quartile"
    )
with col2:
    st.metric(
        "Measures Above Regional",
        f"{summary['measures_above_regional']}/{summary['total_measures']}",
        delta=f"{summary['measures_above_regional'] - summary['total_measures']//2} vs average"
    )
with col3:
    st.metric(
        "Improving Measures",
        f"{summary['improving_measures']}/{summary['total_measures']}",
        delta=f"{summary['total_measures'] - summary['improving_measures']} declining"
    )
with col4:
    st.metric(
        "Bottom Quartile Measures",
        f"{summary['bottom_quartile_measures']}",
        delta="Needs attention" if summary['bottom_quartile_measures'] > 0 else "None"
    )

# Insights Section
st.header("💡 Key Insights")
insights = benchmarking.generate_insights()

if insights:
    for insight in insights[:5]:  # Show top 5
        severity_color = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }
        with st.expander(f"{severity_color[insight['severity']]} {insight['message']}"):
            st.write(f"**Action:** {insight['action']}")
            st.write(f"**Type:** {insight['type'].replace('_', ' ').title()}")

# Main Comparison Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 National Comparison",
    "🗺️ Regional Comparison",
    "👥 Similar Plans",
    "📅 Year-over-Year"
])

with tab1:
    st.subheader("National Benchmarking")
    st.markdown("Compare your plan's performance against national percentiles")
    
    # National ranking table
    st.markdown("### National Percentile Rankings")
    rankings_data = []
    for measure in benchmarking.benchmark_data['measures']:
        ranking = benchmarking.get_national_ranking(measure)
        rankings_data.append({
            'Measure': measure,
            'Your Rate (%)': f"{ranking['current_rate']:.1f}",
            'National Percentile': f"{ranking['percentile']}th",
            '90th Percentile': f"{ranking['90th_percentile']:.1f}",
            'Gap to 90th': f"{ranking['gap_to_90th']:.1f}",
            'Status': '✅ Above Median' if ranking['above_benchmark'] else '⚠️ Below Median'
        })
    
    df_rankings = pd.DataFrame(rankings_data)
    st.dataframe(df_rankings, use_container_width=True, hide_index=True)
    
    # Radar chart
    st.markdown("### Multi-Measure Comparison")
    radar_fig = benchmarking.create_radar_chart(comparison_type='national')
    st.plotly_chart(radar_fig, use_container_width=True)
    
    # Benchmark bands for selected measure
    st.markdown("### Detailed Measure Analysis")
    selected_measure = st.selectbox(
        "Select measure for detailed analysis",
        benchmarking.benchmark_data['measures'],
        key='national_measure'
    )
    
    col1, col2 = st.columns(2)
    with col1:
        bands_fig = benchmarking.create_benchmark_bands_chart(selected_measure)
        st.plotly_chart(bands_fig, use_container_width=True)
    with col2:
        dist_fig = benchmarking.create_performance_distribution(selected_measure)
        st.plotly_chart(dist_fig, use_container_width=True)

with tab2:
    st.subheader("Regional Comparison")
    st.markdown("Compare your plan's performance against regional benchmarks")
    
    # State selection
    plan_state = benchmarking.plan_data['metadata']['state']
    selected_state = st.selectbox(
        "Select state for comparison",
        ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI'],
        index=0 if plan_state in ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI'] else 0,
        key='regional_state'
    )
    
    regional_data = benchmarking.get_regional_comparison(selected_state)
    
    # Regional comparison metrics
    st.markdown("### Regional Performance Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Measures Above Regional Average",
            f"{regional_data['measures_above']}/{len(benchmarking.benchmark_data['measures'])}"
        )
    with col2:
        st.metric(
            "Measures Below Regional Average",
            f"{regional_data['measures_below']}/{len(benchmarking.benchmark_data['measures'])}"
        )
    
    # Regional comparison table
    st.markdown("### Measure-by-Measure Comparison")
    regional_table_data = []
    for measure, comp in regional_data['comparisons'].items():
        regional_table_data.append({
            'Measure': measure,
            'Your Rate (%)': f"{comp['plan_rate']:.1f}",
            f'{selected_state} Regional (%)': f"{comp['regional_rate']:.1f}",
            'Difference': f"{comp['difference']:+.1f}",
            'Percent Difference': f"{comp['percent_difference']:+.1f}%",
            'Status': '✅ Above' if comp['above_regional'] else '⚠️ Below'
        })
    
    df_regional = pd.DataFrame(regional_table_data)
    st.dataframe(df_regional, use_container_width=True, hide_index=True)
    
    # Regional radar chart
    st.markdown("### Regional Radar Comparison")
    regional_radar = benchmarking.create_radar_chart(comparison_type='regional')
    st.plotly_chart(regional_radar, use_container_width=True)
    
    # Top/bottom measures
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🏆 Top 5 vs Regional")
        top_measures = sorted(
            [(m, c['difference']) for m, c in regional_data['comparisons'].items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        for measure, diff in top_measures:
            st.write(f"**{measure}**: +{diff:.1f}% above regional")
    with col2:
        st.markdown("#### ⚠️ Bottom 5 vs Regional")
        bottom_measures = sorted(
            [(m, c['difference']) for m, c in regional_data['comparisons'].items()],
            key=lambda x: x[1]
        )[:5]
        for measure, diff in bottom_measures:
            st.write(f"**{measure}**: {diff:.1f}% below regional")

with tab3:
    st.subheader("Similar Plans Comparison")
    st.markdown("Compare against plans with similar size and model type")
    
    similar_data = benchmarking.get_similar_plan_comparison()
    plan_metadata = benchmarking.plan_data['metadata']
    
    st.markdown(f"### Your Plan Profile")
    st.write(f"- **Size**: {plan_metadata['size'].title()}")
    st.write(f"- **Type**: {plan_metadata['type']}")
    st.write(f"- **Members**: {plan_metadata['member_count']:,}")
    
    # Similar plans comparison table
    st.markdown("### Comparison to Similar Plans")
    similar_table_data = []
    for measure, comp in similar_data['comparisons'].items():
        similar_table_data.append({
            'Measure': measure,
            'Your Rate (%)': f"{comp['plan_rate']:.1f}",
            f'Similar {plan_metadata["size"].title()} Plans (%)': f"{comp['size_benchmark']:.1f}",
            f'Similar {plan_metadata["type"]} Plans (%)': f"{comp['type_benchmark']:.1f}",
            'Average Benchmark': f"{comp['avg_benchmark']:.1f}",
            'vs Average': f"{comp['vs_avg']:+.1f}",
            'Status': '✅ Above' if comp['vs_avg'] > 0 else '⚠️ Below'
        })
    
    df_similar = pd.DataFrame(similar_table_data)
    st.dataframe(df_similar, use_container_width=True, hide_index=True)
    
    # Similar plans radar chart
    st.markdown("### Similar Plans Radar Comparison")
    similar_radar = benchmarking.create_radar_chart(comparison_type='similar')
    st.plotly_chart(similar_radar, use_container_width=True)

with tab4:
    st.subheader("Year-over-Year Trends")
    st.markdown("Track performance changes over time")
    
    yoy_data = benchmarking.get_year_over_year()
    
    # YoY summary
    st.markdown("### Overall Trend Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Improving Measures",
            f"{yoy_data['improving_measures']}/{len(benchmarking.benchmark_data['measures'])}"
        )
    with col2:
        st.metric(
            "Declining Measures",
            f"{yoy_data['declining_measures']}/{len(benchmarking.benchmark_data['measures'])}"
        )
    with col3:
        st.metric(
            "Average Change",
            f"{yoy_data['net_change']:+.1f}%"
        )
    
    # YoY comparison table
    st.markdown("### Measure-by-Measure Changes")
    yoy_table_data = []
    for measure, change in yoy_data['changes'].items():
        yoy_table_data.append({
            'Measure': measure,
            'Current (%)': f"{change['current']:.1f}",
            'Previous (%)': f"{change['previous']:.1f}",
            'Change': f"{change['change']:+.1f}",
            'Percent Change': f"{change['percent_change']:+.1f}%",
            'Trend': '📈 Improving' if change['improving'] else '📉 Declining'
        })
    
    df_yoy = pd.DataFrame(yoy_table_data)
    st.dataframe(df_yoy, use_container_width=True, hide_index=True)
    
    # YoY visualization
    st.markdown("### Year-over-Year Change Chart")
    measures = list(yoy_data['changes'].keys())
    changes = [yoy_data['changes'][m]['change'] for m in measures]
    colors = ['green' if c > 0 else 'red' for c in changes]
    
    fig_yoy = go.Figure()
    fig_yoy.add_trace(go.Bar(
        x=measures,
        y=changes,
        marker_color=colors,
        text=[f"{c:+.1f}%" for c in changes],
        textposition='outside'
    ))
    fig_yoy.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_yoy.update_layout(
        title="Year-over-Year Change by Measure",
        xaxis_title="Measure",
        yaxis_title="Change (Percentage Points)",
        height=350,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_yoy, use_container_width=True)
    
    # Top improvements and declines
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📈 Top 5 Improvements")
        top_improvements = sorted(
            [(m, c['change']) for m, c in yoy_data['changes'].items() if c['improving']],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        for measure, change in top_improvements:
            st.write(f"**{measure}**: +{change:.1f}%")
    with col2:
        st.markdown("#### 📉 Top 5 Declines")
        top_declines = sorted(
            [(m, c['change']) for m, c in yoy_data['changes'].items() if c['declining']],
            key=lambda x: x[1]
        )[:5]
        for measure, change in top_declines:
            st.write(f"**{measure}**: {change:.1f}%")

# Market Share vs Quality
st.header("📊 Market Position")
st.markdown("Your plan's position in the market share vs quality landscape")

market_fig = benchmarking.create_market_share_scatter()
st.plotly_chart(market_fig, use_container_width=True)

# Export options
st.header("📥 Export Options")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Export National Rankings"):
        csv = df_rankings.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="national_rankings.csv",
            mime="text/csv"
        )
with col2:
    if st.button("🗺️ Export Regional Comparison"):
        csv = df_regional.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="regional_comparison.csv",
            mime="text/csv"
        )
with col3:
    if st.button("📅 Export YoY Trends"):
        csv = df_yoy.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="yoy_trends.csv",
            mime="text/csv"
        )

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer

