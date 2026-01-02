"""
Medicare Advantage Star Rating Simulator
Interactive simulator to answer "How do we get to X stars?"
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

from utils.star_rating_calculator import StarRatingCalculator, Domain
from utils.star_rating_financial import StarRatingFinancial
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# Page configuration
st.set_page_config(
    page_title="Star Rating Simulator - HEDIS Portfolio",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="auto"  # Auto: Let Streamlit decide based on screen size (iOS Safari optimized)
)

# Rename "app" to "Home" in sidebar navigation
st.markdown("""
<style>
/* ========== DESKTOP AND MOBILE - WHITE "HOME" LABEL ========== */

/* Desktop: First navigation item */
[data-testid="stSidebarNav"] ul li:first-child a {
    font-size: 0 !important;
    background: linear-gradient(135deg, rgba(139,122,184,0.3), rgba(111,95,150,0.3)) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="stSidebarNav"] ul li:first-child a::before {
    content: "🏠 Home";
    font-size: 1.1rem !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    display: block !important;
}

/* Force white on all child elements */
[data-testid="stSidebarNav"] ul li:first-child a *,
[data-testid="stSidebarNav"] ul li:first-child a span,
[data-testid="stSidebarNav"] ul li:first-child a div,
[data-testid="stSidebarNav"] ul li:first-child a p {
    color: #FFFFFF !important;
}

/* Target by href (works on mobile) */
[data-testid="stSidebarNav"] a[href="/"],
[data-testid="stSidebarNav"] a[href="./"],
[data-testid="stSidebarNav"] a[href*="app.py"] {
    font-size: 0 !important;
    background: linear-gradient(135deg, rgba(139,122,184,0.3), rgba(111,95,150,0.3)) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

[data-testid="stSidebarNav"] a[href="/"]::before,
[data-testid="stSidebarNav"] a[href="./"]::before,
[data-testid="stSidebarNav"] a[href*="app.py"]::before {
    content: "🏠 Home";
    font-size: 1.1rem !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    display: block !important;
}

/* Hover state - maintain white */
[data-testid="stSidebarNav"] ul li:first-child a:hover::before,
[data-testid="stSidebarNav"] a[href="/"]:hover::before,
[data-testid="stSidebarNav"] a[href="./"]:hover::before {
    color: #FFFFFF !important;
    background: linear-gradient(135deg, rgba(139,122,184,0.5), rgba(111,95,150,0.5)) !important;
}

/* Mobile-specific adjustments */
@media (max-width: 768px) {
    [data-testid="stSidebarNav"] ul li:first-child a {
        padding: 0.6rem 0.8rem !important;
    }
    
    [data-testid="stSidebarNav"] ul li:first-child a::before {
        font-size: 1rem !important;
        color: #FFFFFF !important;
    }
    
    /* Ensure mobile drawer shows white text */
    [data-testid="stSidebarNav"] a[href="/"]::before,
    [data-testid="stSidebarNav"] a[href="./"]::before {
        color: #FFFFFF !important;
    }
}

/* Mobile drawer open state */
[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarNav"] a[href="/"]::before,
[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarNav"] a[href="./"]::before {
    color: #FFFFFF !important;
}

/* Force white text in all states */
[data-testid="stSidebarNav"] li:first-child *,
[data-testid="stSidebarNav"] a[href="/"] *,
[data-testid="stSidebarNav"] a[href="./"] * {
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

# ========== AGGRESSIVE SPACING REDUCTION ==========
# MATCHED TO INTERVENTION PERFORMANCE ANALYSIS PAGE (Perfect Spacing Template)
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
    padding-top: 0rem !important;
}

/* Zero-top enforcement - Headers flush to top */
.main > div:first-child {
    padding-top: 0 !important;
    margin-top: 0 !important;
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

# Apply sidebar styling (purple gradient matching StarGuard AI header)
from utils.sidebar_styling import apply_sidebar_styling
apply_sidebar_styling()

# Custom CSS
st.markdown("""
<style>
    .star-gauge {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .star-display {
        font-size: 4rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .domain-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    
    .impact-positive {
        color: #00cc66;
        font-weight: bold;
    }
    
    .impact-negative {
        color: #cc0000;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize calculators
star_calculator = StarRatingCalculator()
financial_calculator = StarRatingFinancial()

# Sidebar - Configuration
st.sidebar.header("⭐ Star Rating Simulator")
st.sidebar.markdown("Configure current state and scenarios")

# Current rates (default values - would come from database)
st.sidebar.subheader("Current Measure Rates")

current_rates = {}
available_measures = ["HBA1C", "BP", "COL", "MAM", "CCS", "CAHPS", "ACCESS"]

for measure_id in available_measures:
    default_rate = {
        "HBA1C": 85.5,
        "BP": 82.3,
        "COL": 75.2,
        "MAM": 78.1,
        "CCS": 81.5,
        "CAHPS": 4.2,
        "ACCESS": 88.7
    }.get(measure_id, 80.0)
    
    current_rates[measure_id] = st.sidebar.slider(
        f"{measure_id}",
        min_value=0.0,
        max_value=100.0,
        value=default_rate,
        step=0.1,
        key=f"rate_{measure_id}"
    )

# Financial assumptions
st.sidebar.markdown("---")
st.sidebar.subheader("Financial Assumptions")

total_revenue = st.sidebar.number_input(
    "Total Revenue ($)",
    min_value=0,
    value=100000000,
    step=1000000,
    format="%d"
)

current_members = st.sidebar.number_input(
    "Current Members",
    min_value=0,
    value=10000,
    step=100,
    format="%d"
)

# Sidebar value proposition - at bottom
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

# Sidebar footer
render_sidebar_footer()

# Main Content
st.title("⭐ Medicare Advantage Star Rating Simulator")
st.markdown("Interactive tool to answer: **'How do we get to X stars?'**")

# 1. Current State Assessment
st.markdown("---")
st.header("📊 Current State Assessment")

# Calculate current state
current_state = star_calculator.calculate_current_state(current_rates)

# Overall Rating Display
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    overall_rating = current_state["overall_rating"]
    next_tier = current_state["next_tier"]
    distance = current_state["distance_to_next"]
    
    st.markdown(f"""
    <div class="star-gauge">
        <div class="star-display">{overall_rating:.1f} ⭐</div>
        <p>Current Overall Star Rating</p>
        <p>Distance to {next_tier:.1f} stars: {distance:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.metric("Next Tier", f"{next_tier:.1f} ⭐")
    st.metric("Distance", f"{distance:.2f}")

with col3:
    # Quality bonus
    current_bonus = financial_calculator.calculate_quality_bonus(overall_rating, total_revenue)
    st.metric("Quality Bonus", f"${current_bonus['bonus_amount']/1e6:.2f}M")
    st.metric("PMPM", f"${current_bonus['pmpm']:.2f}")

# Domain Scores
st.subheader("Rating by Domain")

domain_cols = st.columns(4)

for i, (domain, domain_score) in enumerate(current_state["domain_scores"].items()):
    with domain_cols[i]:
        domain_star = domain_score.domain_star
        st.markdown(f"""
        <div class="domain-card" style="border-left-color: {'#667eea' if i == 0 else '#764ba2' if i == 1 else '#f093fb' if i == 2 else '#4facfe'};">
            <h4>{domain.value}</h4>
            <div style="font-size: 2rem; font-weight: bold;">{domain_star:.1f} ⭐</div>
            <small>Weight: {star_calculator.domain_weights.get(domain, 0)*100:.0f}%</small>
        </div>
        """, unsafe_allow_html=True)

# Measure Scores Table
st.subheader("Measure Scores")

measure_data = []
for measure_score in current_state["measure_scores"]:
    measure_data.append({
        "Measure": measure_score.measure_id,
        "Domain": measure_score.domain.value,
        "Current Rate": f"{measure_score.current_rate:.1f}%",
        "Current Star": f"{measure_score.current_star:.1f} ⭐",
        "Weight": f"{measure_score.weight*100:.0f}%"
    })

measure_df = pd.DataFrame(measure_data)
st.dataframe(measure_df, use_container_width=True, hide_index=True)

# 2. Measure Improvement Selector
st.markdown("---")
st.header("🎯 Measure Improvement Selector")

improvement_cols = st.columns(2)

with improvement_cols[0]:
    st.subheader("Select Measures to Improve")
    
    selected_measures = st.multiselect(
        "Measures",
        available_measures,
        default=["HBA1C", "BP"]
    )

with improvement_cols[1]:
    st.subheader("Set Target Improvements")
    
    improvements = {}
    for measure_id in selected_measures:
        improvements[measure_id] = st.number_input(
            f"{measure_id} Improvement (%)",
            min_value=0.0,
            max_value=20.0,
            value=5.0,
            step=0.1,
            key=f"improve_{measure_id}"
        )

# Simulate improvement
if improvements:
    simulation = star_calculator.simulate_improvement(current_rates, improvements)
    
    # Display results
    result_cols = st.columns(3)
    
    with result_cols[0]:
        st.metric(
            "Current Rating",
            f"{simulation['current_rating']:.1f} ⭐"
        )
    
    with result_cols[1]:
        rating_change = simulation["rating_change"]
        change_class = "impact-positive" if rating_change >= 0 else "impact-negative"
        st.metric(
            "Projected Rating",
            f"{simulation['projected_rating']:.1f} ⭐",
            delta=f"{rating_change:+.2f}"
        )
    
    with result_cols[2]:
        # Financial impact
        financial_impact = financial_calculator.calculate_rating_change_impact(
            simulation['current_rating'],
            simulation['projected_rating'],
            total_revenue,
            current_members
        )
        st.metric(
            "Total Impact",
            f"${financial_impact['total_impact']/1e6:.2f}M"
        )
    
    # Domain impact visualization
    st.subheader("Domain Impact")
    
    domain_impact_data = []
    for domain in Domain:
        current_domain_star = simulation['current_domain_scores'][domain].domain_star
        projected_domain_star = simulation['projected_domain_scores'][domain].domain_star
        change = projected_domain_star - current_domain_star
        
        domain_impact_data.append({
            "Domain": domain.value,
            "Current": current_domain_star,
            "Projected": projected_domain_star,
            "Change": change
        })
    
    domain_impact_df = pd.DataFrame(domain_impact_data)
    
    fig_domain = go.Figure()
    fig_domain.add_trace(go.Bar(
        name="Current",
        x=domain_impact_df["Domain"],
        y=domain_impact_df["Current"],
        marker_color="lightblue",
        marker_line_color="black",
        marker_line_width=1
    ))
    fig_domain.add_trace(go.Bar(
        name="Projected",
        x=domain_impact_df["Domain"],
        y=domain_impact_df["Projected"],
        marker_color="darkblue",
        marker_line_color="black",
        marker_line_width=1
    ))
    fig_domain.update_layout(
        title="Domain Star Rating Impact",
        yaxis_title="Star Rating",
        barmode="group",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        title_font=dict(color='black', size=14),
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
        )
    )
    st.plotly_chart(fig_domain, use_container_width=True)

# 3. What-If Scenarios
st.markdown("---")
st.header("🔮 What-If Scenarios")

scenario_tabs = st.tabs(["Preset Scenarios", "Custom Scenario"])

with scenario_tabs[0]:
    st.subheader("Preset Scenarios")
    
    preset_scenarios = {
        "Moderate Improvement": {
            "HBA1C": 3.0,
            "BP": 5.0
        },
        "Aggressive Improvement": {
            "HBA1C": 5.0,
            "BP": 7.0,
            "COL": 5.0
        },
        "Outcome Focus": {
            "HBA1C": 4.0,
            "BP": 6.0
        },
        "Process Focus": {
            "COL": 5.0,
            "MAM": 4.0,
            "CCS": 3.0
        }
    }
    
    selected_preset = st.selectbox("Select Preset", list(preset_scenarios.keys()))
    
    if st.button("Run Scenario", key="run_preset"):
        preset_improvements = preset_scenarios[selected_preset]
        scenario_result = star_calculator.simulate_improvement(current_rates, preset_improvements)
        
        # Display scenario results
        scenario_cols = st.columns(4)
        
        with scenario_cols[0]:
            st.metric("Current", f"{scenario_result['current_rating']:.1f} ⭐")
        with scenario_cols[1]:
            st.metric("Projected", f"{scenario_result['projected_rating']:.1f} ⭐")
        with scenario_cols[2]:
            st.metric("Change", f"{scenario_result['rating_change']:+.2f}")
        with scenario_cols[3]:
            scenario_financial = financial_calculator.calculate_rating_change_impact(
                scenario_result['current_rating'],
                scenario_result['projected_rating'],
                total_revenue,
                current_members
            )
            st.metric("Impact", f"${scenario_financial['total_impact']/1e6:.2f}M")

with scenario_tabs[1]:
    st.subheader("Custom What-If Scenario")
    
    st.markdown("**Example**: 'What if we improve HbA1c by 3% and BP Control by 5%?'")
    
    custom_improvements = {}
    custom_cols = st.columns(3)
    
    for i, measure_id in enumerate(available_measures[:6]):  # Show first 6
        with custom_cols[i % 3]:
            custom_improvements[measure_id] = st.number_input(
                f"{measure_id}",
                min_value=0.0,
                max_value=20.0,
                value=0.0,
                step=0.1,
                key=f"custom_{measure_id}"
            )
    
    if st.button("Run Custom Scenario", key="run_custom"):
        # Filter out zero improvements
        active_improvements = {k: v for k, v in custom_improvements.items() if v > 0}
        
        if active_improvements:
            custom_result = star_calculator.simulate_improvement(current_rates, active_improvements)
            
            st.success(f"**Projected Rating**: {custom_result['projected_rating']:.1f} ⭐ (Change: {custom_result['rating_change']:+.2f})")
            
            # Financial impact
            custom_financial = financial_calculator.calculate_rating_change_impact(
                custom_result['current_rating'],
                custom_result['projected_rating'],
                total_revenue,
                current_members
            )
            
            st.info(f"**Total Financial Impact**: ${custom_financial['total_impact']/1e6:.2f}M")

# 4. Prioritization Recommendation
st.markdown("---")
st.header("🎯 Prioritization Recommendation")

target_rating = st.number_input(
    "Target Star Rating",
    min_value=1.0,
    max_value=5.0,
    value=4.5,
    step=0.5,
    key="target_rating"
)

if st.button("Calculate Required Improvements"):
    priorities = star_calculator.prioritize_measures(current_rates, target_rating)
    
    st.subheader(f"To Reach {target_rating:.1f} Stars, Focus on These Measures:")
    
    # Display top 3 recommendations
    top_3 = priorities[:3]
    
    for i, priority in enumerate(top_3, 1):
        st.markdown(f"""
        <div class="domain-card">
            <h4>#{i}: {priority['measure_id']}</h4>
            <p><strong>Current:</strong> {priority['current_rate']:.1f}% ({priority['current_star']:.1f} ⭐)</p>
            <p><strong>Improvement Needed:</strong> {priority['improvement_needed']:.1f} percentage points</p>
            <p><strong>Impact:</strong> {priority['impact']:.3f} | <strong>Effort:</strong> {priority['effort']:.2f}</p>
            <p><strong>Efficiency:</strong> {priority['efficiency']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Effort vs Impact Matrix
    st.subheader("Effort vs Impact Matrix")
    
    priority_df = pd.DataFrame(priorities)
    
    fig_matrix = px.scatter(
        priority_df,
        x="effort",
        y="impact",
        size="efficiency",
        color="efficiency",
        hover_data=["measure_id", "improvement_needed"],
        title="Effort vs Impact Matrix",
        labels={"effort": "Effort", "impact": "Impact", "efficiency": "Efficiency"}
    )
    fig_matrix.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        title_font=dict(color='black', size=14),
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
        )
    )
    fig_matrix.update_traces(marker_line_color='black', marker_line_width=1)
    st.plotly_chart(fig_matrix, use_container_width=True)
    
    # Required improvements table
    st.subheader("Required Improvements by Measure")
    
    required_df = pd.DataFrame([{
        "Measure": p["measure_id"],
        "Current Rate": f"{p['current_rate']:.1f}%",
        "Current Star": f"{p['current_star']:.1f} ⭐",
        "Improvement Needed": f"{p['improvement_needed']:.1f}%",
        "Next Cut Point": f"{p['next_cut_point']:.1f}%",
        "Efficiency": f"{p['efficiency']:.2f}"
    } for p in priorities])
    
    st.dataframe(required_df, use_container_width=True, hide_index=True)

# 5. Financial Impact
st.markdown("---")
st.header("💰 Financial Impact")

if improvements:
    financial_impact = financial_calculator.calculate_rating_change_impact(
        simulation['current_rating'],
        simulation['projected_rating'],
        total_revenue,
        current_members
    )
    
    financial_cols = st.columns(4)
    
    with financial_cols[0]:
        st.metric(
            "Quality Bonus Change",
            f"${financial_impact['bonus_change']/1e6:.2f}M",
            delta=f"{financial_impact['bonus_change']/1e6:+.2f}M"
        )
    
    with financial_cols[1]:
        st.metric(
            "Member Impact",
            f"{financial_impact['member_change']:+.0f}",
            delta=f"{financial_impact['member_change']:+.0f} members"
        )
    
    with financial_cols[2]:
        st.metric(
            "Revenue Impact",
            f"${financial_impact['revenue_change']/1e6:.2f}M",
            delta=f"{financial_impact['revenue_change']/1e6:+.2f}M"
        )
    
    with financial_cols[3]:
        st.metric(
            "Total Impact",
            f"${financial_impact['total_impact']/1e6:.2f}M",
            delta=f"{financial_impact['total_impact']/1e6:+.2f}M"
        )
    
    # Detailed breakdown
    st.subheader("Detailed Financial Breakdown")
    
    breakdown_data = {
        "Component": [
            "Quality Bonus (Current)",
            "Quality Bonus (Projected)",
            "Quality Bonus Change",
            "Member Revenue (Current)",
            "Member Revenue (Projected)",
            "Member Revenue Change",
            "Total Impact"
        ],
        "Amount ($M)": [
            financial_impact['current_bonus']['bonus_amount'] / 1e6,
            financial_impact['projected_bonus']['bonus_amount'] / 1e6,
            financial_impact['bonus_change'] / 1e6,
            financial_impact['current_members']['revenue_impact'] / 1e6,
            financial_impact['projected_members']['revenue_impact'] / 1e6,
            financial_impact['revenue_change'] / 1e6,
            financial_impact['total_impact'] / 1e6
        ]
    }
    
    breakdown_df = pd.DataFrame(breakdown_data)
    st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
    
    # Brand value
    brand_current = financial_calculator.estimate_brand_value_impact(simulation['current_rating'])
    brand_projected = financial_calculator.estimate_brand_value_impact(simulation['projected_rating'])
    
    st.subheader("Brand Value Impact")
    
    brand_cols = st.columns(3)
    
    with brand_cols[0]:
        st.metric("Current Brand Value", f"${brand_current['brand_value']/1e6:.2f}M")
    with brand_cols[1]:
        st.metric("Projected Brand Value", f"${brand_projected['brand_value']/1e6:.2f}M")
    with brand_cols[2]:
        brand_change = brand_projected['brand_value'] - brand_current['brand_value']
        st.metric("Brand Value Change", f"${brand_change/1e6:.2f}M", delta=f"{brand_change/1e6:+.2f}M")

# 6. Timeline Projections
st.markdown("---")
st.header("📅 Timeline Projections")

timeline_cols = st.columns(2)

with timeline_cols[0]:
    target_date = st.date_input(
        "Target Achievement Date",
        value=datetime.now().date() + timedelta(days=365),
        format="MM/DD/YYYY"
    )

with timeline_cols[1]:
    intervention_start = st.date_input(
        "Intervention Start Date",
        value=datetime.now().date(),
        format="MM/DD/YYYY"
    )

if improvements and st.button("Generate Timeline"):
    # Calculate months to target
    months_to_target = (target_date - intervention_start).days / 30
    
    # Monthly improvement plan
    st.subheader("Monthly Intervention Plan")
    
    monthly_plan = []
    cumulative_improvements = {}
    
    for month in range(int(months_to_target) + 1):
        month_date = intervention_start + timedelta(days=30 * month)
        
        # Calculate monthly progress (linear assumption)
        for measure_id, total_improvement in improvements.items():
            monthly_improvement = total_improvement / months_to_target if months_to_target > 0 else 0
            cumulative_improvements[measure_id] = cumulative_improvements.get(measure_id, 0) + monthly_improvement
        
        # Calculate projected rating at this point
        projected_rates = current_rates.copy()
        for measure_id, improvement in cumulative_improvements.items():
            if measure_id in projected_rates:
                projected_rates[measure_id] = min(100.0, projected_rates[measure_id] + improvement)
        
        projected_state = star_calculator.calculate_current_state(projected_rates)
        projected_rating = projected_state["overall_rating"]
        
        monthly_plan.append({
            "Month": month,
            "Date": month_date.strftime("%Y-%m-%d"),
            "Projected Rating": f"{projected_rating:.2f}",
            "Status": "✅ Target Achieved" if projected_rating >= target_rating else "⏳ In Progress"
        })
    
    timeline_df = pd.DataFrame(monthly_plan)
    st.dataframe(timeline_df, use_container_width=True, hide_index=True)
    
    # Timeline visualization
    fig_timeline = px.line(
        timeline_df,
        x="Date",
        y="Projected Rating",
        title="Projected Star Rating Timeline",
        markers=True
    )
    fig_timeline.update_traces(line_color='#0066cc', marker_color='#0066cc')
    fig_timeline.add_hline(y=target_rating, line_dash="dash", line_color="red", annotation_text="Target")
    fig_timeline.add_hline(y=current_state["overall_rating"], line_dash="dash", line_color="blue", annotation_text="Current")
    fig_timeline.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        title_font=dict(color='black', size=14),
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
        )
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Risk mitigation
    st.subheader("Risk Mitigation")
    st.info("""
    **Underperforming Measures**: Monitor measures that are below target.
    **Intervention Adjustments**: Adjust interventions if progress is slower than projected.
    **Contingency Plans**: Have backup strategies for critical measures.
    """)

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer

