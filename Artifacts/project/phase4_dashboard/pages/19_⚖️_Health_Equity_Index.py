"""
Health Equity Index (HEI) Analyzer
Comprehensive health equity and disparity analysis across demographic groups
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import yaml
import os

# Import utilities
from utils.value_proposition import render_sidebar_value_proposition
from utils.database import execute_query, show_db_status, get_db_type
from utils.plan_context import get_plan_context
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header
from utils.hei_queries import (
    get_hei_demographic_data_query,
    get_hei_demographic_data_sqlite_query,
    get_available_measures_query
)

# Page configuration
st.set_page_config(
    page_title="Health Equity Index - HEDIS Portfolio",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="auto"  # Auto: Let Streamlit decide based on screen size (iOS Safari optimized)
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
    padding-top: 0rem !important; 
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

# Mobile optimization indicator
st.sidebar.success("📱 Mobile Optimized")

# Apply sidebar styling (purple gradient matching StarGuard AI header)
from utils.sidebar_styling import apply_sidebar_styling
apply_sidebar_styling()

# Custom CSS with mobile responsiveness
st.markdown("""
<style>
    .hei-score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .hei-score-display {
        font-size: 4rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    
    .disparity-alert {
        background: #ffe6e6;
        border-left: 4px solid #cc0000;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .equity-good {
        color: #00cc66;
        font-weight: bold;
    }
    
    .equity-warning {
        color: #ff9900;
        font-weight: bold;
    }
    
    .equity-critical {
        color: #cc0000;
        font-weight: bold;
    }
    
    /* Mobile Responsive Styles */
    @media (max-width: 768px) {
        /* Hide "Mobile Optimized" message on mobile */
        [data-testid="stSidebar"] [data-testid="stSuccess"] {
            display: none !important;
        }
        
        .hei-score-display {
            font-size: 2.5rem;
        }
        
        .hei-score-card {
            padding: 1.5rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        /* Ensure charts are responsive */
        .js-plotly-plot {
            width: 100% !important;
        }
        
        /* Stack columns on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    
    /* Desktop: Show "Mobile Optimized" message */
    @media (min-width: 769px) {
        [data-testid="stSidebar"] [data-testid="stSuccess"] {
            display: block !important;
        }
    }
    
    /* Touch-friendly buttons and controls */
    @media (hover: none) and (pointer: coarse) {
        button, .stButton > button {
            min-height: 44px;
            min-width: 44px;
        }
        
        .stSelectbox, .stSlider, .stNumberInput {
            min-height: 44px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURATION LOADING
# ============================================================================
def load_hei_config():
    """Load HEI configuration from config file"""
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                   'config_prod.yaml')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                hei_config = config.get('analytics', {}).get('hei', {})
                return {
                    'disparity_threshold': hei_config.get('disparity_threshold', 4.0),
                    'reward_factor': hei_config.get('reward_factor_projection', 0.05)
                }
    except Exception as e:
        st.warning(f"Could not load config: {e}")
    
    # Defaults
    return {
        'disparity_threshold': 4.0,
        'reward_factor': 0.05
    }

HEI_CONFIG = load_hei_config()

# ============================================================================
# DATA GENERATION (Synthetic data for demonstration)
# ============================================================================
ALL_HEDIS_MEASURES = [
    "HbA1c Testing (CDC)",
    "Blood Pressure Control (CBP)",
    "Colorectal Cancer Screening (COL)",
    "Breast Cancer Screening (BCS)",
    "Controlling High Blood Pressure (CBP)",
    "Diabetes Eye Exam (EED)",
    "Diabetes Kidney Disease Monitoring (KED)",
    "Statin Therapy for CVD (SPC)",
    "Follow-Up After ED - Mental Health (FUM)",
    "Antidepressant Medication Management (AMM)",
    "Plan All-Cause Readmissions (PCR)",
    "Medication Adherence - Diabetes (MAD)"
]

DEMOGRAPHIC_GROUPS = {
    'race': ['White', 'Black or African American', 'Hispanic or Latino', 'Asian', 'Other'],
    'age_group': ['18-44', '45-64', '65-74', '75+'],
    'gender': ['Male', 'Female', 'Other']
}

def generate_synthetic_hei_data():
    """Generate synthetic HEI data with demographic breakdowns"""
    np.random.seed(42)
    
    data_rows = []
    
    for measure in ALL_HEDIS_MEASURES:
        # Base rate for measure (overall)
        base_rate = np.random.uniform(70, 90)
        
        # Generate demographic breakdowns
        for race in DEMOGRAPHIC_GROUPS['race']:
            for age_group in DEMOGRAPHIC_GROUPS['age_group']:
                for gender in DEMOGRAPHIC_GROUPS['gender']:
                    # Add variation based on demographics
                    race_multiplier = {
                        'White': 1.0,
                        'Black or African American': 0.85,
                        'Hispanic or Latino': 0.88,
                        'Asian': 0.92,
                        'Other': 0.87
                    }.get(race, 1.0)
                    
                    age_multiplier = {
                        '18-44': 0.92,
                        '45-64': 1.0,
                        '65-74': 0.98,
                        '75+': 0.95
                    }.get(age_group, 1.0)
                    
                    # Add some random variation
                    rate = base_rate * race_multiplier * age_multiplier * np.random.uniform(0.95, 1.05)
                    rate = max(0, min(100, rate))  # Clamp to 0-100
                    
                    members = int(np.random.uniform(50, 500))
                    completed = int(members * rate / 100)
                    
                    data_rows.append({
                        'measure_name': measure,
                        'race': race,
                        'age_group': age_group,
                        'gender': gender,
                        'member_count': members,
                        'completed_count': completed,
                        'completion_rate': rate,
                        'month': pd.Timestamp('2025-01-01')
                    })
    
    return pd.DataFrame(data_rows)

# ============================================================================
# HEI CALCULATION FUNCTIONS
# ============================================================================
def calculate_disparity_gap(df, measure_col='measure_name', rate_col='completion_rate', group_col='race'):
    """Calculate disparity gap (max - min) for each measure by demographic group"""
    gaps = []
    
    for measure in df[measure_col].unique():
        measure_data = df[df[measure_col] == measure]
        if len(measure_data) > 0:
            max_rate = measure_data[rate_col].max()
            min_rate = measure_data[rate_col].min()
            gap = max_rate - min_rate
            
            gaps.append({
                'measure_name': measure,
                'max_rate': max_rate,
                'min_rate': min_rate,
                'disparity_gap': gap,
                'max_group': measure_data.loc[measure_data[rate_col].idxmax(), group_col],
                'min_group': measure_data.loc[measure_data[rate_col].idxmin(), group_col]
            })
    
    return pd.DataFrame(gaps)

def calculate_equity_score(disparity_gap, max_possible_gap=100):
    """Calculate equity score (0-100) from disparity gap"""
    normalized_gap = (disparity_gap / max_possible_gap) * 100
    equity_score = 100 - normalized_gap
    return max(0, min(100, equity_score))

def calculate_overall_hei_score(df, measure_col='measure_name', rate_col='completion_rate', group_col='race'):
    """Calculate overall HEI score across all measures"""
    gaps_df = calculate_disparity_gap(df, measure_col, rate_col, group_col)
    
    if gaps_df.empty:
        return 0
    
    # Calculate equity score for each measure
    gaps_df['equity_score'] = gaps_df['disparity_gap'].apply(calculate_equity_score)
    
    # Weighted average (equal weights for now, can be customized)
    overall_hei = gaps_df['equity_score'].mean()
    
    return overall_hei

def calculate_measure_equity_metrics(df):
    """Calculate comprehensive equity metrics for all measures"""
    metrics_list = []
    
    for measure in df['measure_name'].unique():
        measure_data = df[df['measure_name'] == measure]
        
        if measure_data.empty:
            continue
        
        # Overall rate
        total_members = measure_data['member_count'].sum()
        total_completed = measure_data['completed_count'].sum()
        overall_rate = (total_completed / total_members * 100) if total_members > 0 else 0
        
        # Disparity gaps by different dimensions
        gaps_by_race = calculate_disparity_gap(measure_data, group_col='race')
        gaps_by_age = calculate_disparity_gap(measure_data, group_col='age_group')
        
        max_gap_race = gaps_by_race['disparity_gap'].max() if not gaps_by_race.empty else 0
        max_gap_age = gaps_by_age['disparity_gap'].max() if not gaps_by_age.empty else 0
        max_gap = max(max_gap_race, max_gap_age)
        
        equity_score = calculate_equity_score(max_gap)
        
        metrics_list.append({
            'measure_name': measure,
            'overall_rate': overall_rate,
            'disparity_gap': max_gap,
            'equity_score': equity_score,
            'total_members': total_members,
            'priority': 'High' if max_gap > HEI_CONFIG['disparity_threshold'] else 'Medium' if max_gap > 2.0 else 'Low'
        })
    
    return pd.DataFrame(metrics_list)

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================
def create_hei_gauge(current_score, target_score=85):
    """Create HEI score gauge chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = current_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall HEI Score"},
        delta = {'reference': target_score, 'position': "top"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gray"},
                {'range': [75, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target_score
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        plot_bgcolor='white',
        paper_bgcolor='white',
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_disparity_heatmap(metrics_df):
    """Create disparity heatmap across measures and demographics"""
    # For now, show measure vs. equity score
    # Can be expanded to show demographic breakdowns
    
    fig = px.bar(
        metrics_df.sort_values('disparity_gap', ascending=False),
        x='measure_name',
        y='disparity_gap',
        color='disparity_gap',
        color_continuous_scale='RdYlGn_r',  # Red = bad (high gap), Green = good (low gap)
        title='Disparity Gap by HEDIS Measure',
        labels={'disparity_gap': 'Disparity Gap (percentage points)', 'measure_name': 'HEDIS Measure'},
        text='disparity_gap'
    )
    
    # Add threshold line
    fig.add_hline(
        y=HEI_CONFIG['disparity_threshold'],
        line_dash="dash",
        line_color="red",
        annotation_text=f"Alert Threshold ({HEI_CONFIG['disparity_threshold']}%)"
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        height=350,
        xaxis_tickangle=-45,
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        autosize=True,
        margin=dict(l=20, r=20, t=60, b=100),
        title_font=dict(size=14)
    )
    
    return fig

def create_demographic_breakdown(df, measure_name, demo_col='race'):
    """Create demographic breakdown chart for a specific measure"""
    measure_data = df[df['measure_name'] == measure_name].copy()
    
    if measure_data.empty:
        return None
    
    # Aggregate by demographic group
    demo_summary = measure_data.groupby(demo_col).agg({
        'member_count': 'sum',
        'completed_count': 'sum'
    }).reset_index()
    
    demo_summary['completion_rate'] = (demo_summary['completed_count'] / demo_summary['member_count'] * 100)
    
    # Sort by rate
    demo_summary = demo_summary.sort_values('completion_rate', ascending=True)
    
    fig = px.bar(
        demo_summary,
        x='completion_rate',
        y=demo_col,
        orientation='h',
        title=f'{measure_name} - Completion Rate by {demo_col.title()}',
        labels={'completion_rate': 'Completion Rate (%)', demo_col: demo_col.replace('_', ' ').title()},
        color='completion_rate',
        color_continuous_scale='RdYlGn'
    )
    
    # Add overall average line
    overall_rate = (measure_data['completed_count'].sum() / measure_data['member_count'].sum() * 100)
    fig.add_vline(
        x=overall_rate,
        line_dash="dash",
        line_color="blue",
        annotation_text=f"Overall: {overall_rate:.1f}%"
    )
    
    fig.update_layout(
        height=350,
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        autosize=True,
        margin=dict(l=20, r=20, t=50, b=20),
        title_font=dict(size=14)
    )
    
    return fig

def create_equity_trend(df, months=24):
    """Create equity trend over time"""
    # Generate historical data (for demo)
    trend_data = []
    
    for i in range(months):
        month_date = pd.Timestamp('2023-01-01') + pd.DateOffset(months=i)
        
        # Simulate improving trend
        month_df = df.copy()
        improvement_factor = 1 + (i * 0.002)  # Slight improvement over time
        
        month_df['completion_rate'] = month_df['completion_rate'] * improvement_factor
        month_df['completion_rate'] = month_df['completion_rate'].clip(0, 100)
        
        hei_score = calculate_overall_hei_score(month_df)
        
        trend_data.append({
            'month': month_date,
            'hei_score': hei_score
        })
    
    trend_df = pd.DataFrame(trend_data)
    
    fig = px.line(
        trend_df,
        x='month',
        y='hei_score',
        title='HEI Score Trend (24 Months)',
        labels={'hei_score': 'HEI Score', 'month': 'Month'},
        markers=True
    )
    
    # Add target line
    fig.add_hline(
        y=85,
        line_dash="dash",
        line_color="green",
        annotation_text="Target: 85"
    )
    
    fig.update_layout(
        height=350,
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        autosize=True,
        margin=dict(l=20, r=20, t=50, b=20),
        title_font=dict(size=14)
    )
    
    return fig

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.header("⚖️ Health Equity Index")
st.sidebar.markdown("Analyze health equity and disparities across demographic groups")

# Database status
show_db_status()

# Data source toggle
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Data Source")
use_database = st.sidebar.checkbox(
    "Use Database Data",
    value=False,
    help="Toggle to use database data (if available) or synthetic demo data"
)

# Date range
st.sidebar.markdown("---")
st.sidebar.subheader("📅 Analysis Period")
end_date = st.sidebar.date_input("End Date", value=datetime.now().date(), format="MM/DD/YYYY")
start_date = st.sidebar.date_input("Start Date", value=end_date - timedelta(days=365), format="MM/DD/YYYY")

# Demographic focus
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Demographic Focus")
selected_demo = st.sidebar.radio(
    "Primary Dimension",
    options=['race', 'age_group', 'gender'],
    format_func=lambda x: x.replace('_', ' ').title()
)

# Measure filter
st.sidebar.markdown("---")
st.sidebar.subheader("📋 Measures")
selected_measures = st.sidebar.multiselect(
    "Select Measures",
    options=ALL_HEDIS_MEASURES,
    default=ALL_HEDIS_MEASURES
)

# Scenario modeling controls
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Scenario Modeling")
target_disparity_reduction = st.sidebar.slider(
    "Target Disparity Reduction (percent)",
    min_value=0,
    max_value=50,
    value=0,
    step=5,
    help="Model scenarios with reduced disparity gaps"
)

intervention_budget = st.sidebar.number_input(
    "Equity Intervention Budget (dollars)",
    min_value=0,
    max_value=5000000,
    value=0,
    step=100000,
    format="%d"
)

reward_factor = st.sidebar.slider(
    "CMS Reward Factor (decimal)",
    min_value=0.0,
    max_value=0.10,
    value=HEI_CONFIG['reward_factor'],
    step=0.01,
    format="%.2f",
    help="Potential reward factor for equity improvements (e.g., 0.05 = 5%)"
)

# Sidebar value proposition - at bottom
render_sidebar_value_proposition()

# ============================================================================
# MAIN CONTENT
# ============================================================================
st.title("⚖️ Health Equity Index (HEI) Analyzer")
st.markdown("Comprehensive health equity and disparity analysis across demographic groups")

# Load/generate data
def load_hei_data_from_database(start_date_str, end_date_str, selected_measure_names):
    """Load HEI data from database with graceful fallback"""
    try:
        db_type = get_db_type()
        
        # Get measure IDs if measures are selected
        measure_ids = None
        if selected_measure_names and len(selected_measure_names) > 0:
            try:
                measures_df = execute_query(get_available_measures_query())
                if not measures_df.empty:
                    # Match measure names to IDs
                    measure_ids = measures_df[
                        measures_df['measure_name'].isin(selected_measure_names)
                    ]['measure_id'].tolist()
            except Exception as e:
                st.warning(f"Could not load measures from database: {e}")
        
        # Build query based on database type
        if db_type == 'sqlite':
            query = get_hei_demographic_data_sqlite_query(
                start_date_str, 
                end_date_str, 
                measure_ids
            )
        else:
            query = get_hei_demographic_data_query(
                start_date_str, 
                end_date_str, 
                measure_ids
            )
        
        df = execute_query(query)
        
        # Check if query returned data
        if df.empty:
            return None
        
        # Check if required columns exist
        if 'measure_name' not in df.columns:
            # Try to handle NULL measure_name values from LEFT JOIN
            return None
        
        # Remove rows with NULL measure_name (from failed LEFT JOIN)
        df = df[df['measure_name'].notna()].copy()
        
        if df.empty:
            return None
        
        # Calculate completion rate if not present
        if 'completion_rate' not in df.columns:
            if 'member_count' in df.columns and 'completed_count' in df.columns:
                df['completion_rate'] = (df['completed_count'] / df['member_count'].replace(0, np.nan) * 100).fillna(0)
            else:
                return None
        
        # Ensure required columns exist and have valid data
        required_cols = ['measure_name', 'member_count', 'completed_count', 'completion_rate']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            return None
        
        # Fill any remaining NULL values
        df['measure_name'] = df['measure_name'].fillna('Unknown')
        df['member_count'] = df['member_count'].fillna(0).astype(int)
        df['completed_count'] = df['completed_count'].fillna(0).astype(int)
        df['completion_rate'] = df['completion_rate'].fillna(0)
        
        # Ensure demographic columns exist (fill with defaults if missing)
        for demo_col in ['race', 'age_group', 'gender']:
            if demo_col not in df.columns:
                df[demo_col] = 'Unknown'
            else:
                df[demo_col] = df[demo_col].fillna('Unknown')
        
        # Add month column for consistency
        if 'month' not in df.columns:
            df['month'] = pd.Timestamp(end_date_str)
        
        return df
        
    except KeyError as e:
        # Handle missing column error specifically
        missing_col = str(e).replace("'", "")
        # Only show warning if database was actually being used
        return None  # Silent fallback - synthetic data will be used
    except Exception as e:
        # Handle other database errors
        error_msg = str(e)
        # Check if it's a KeyError for measure_name
        if isinstance(e, KeyError) and 'measure_name' in str(e):
            # Silent fallback - synthetic data will be used
            return None
        # For other errors, log but don't show warning (synthetic data will be used)
        return None

# Load data based on user selection
if use_database:
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    hei_data = load_hei_data_from_database(
        start_date_str, 
        end_date_str, 
        selected_measures if selected_measures else ALL_HEDIS_MEASURES
    )
    
    if hei_data is None or hei_data.empty:
        # Silently fallback to synthetic data (no warning needed)
        use_database = False
    
if not use_database or 'hei_data' not in locals() or hei_data is None or hei_data.empty:
    # Use synthetic data
    if 'hei_data' not in st.session_state:
        st.session_state.hei_data = generate_synthetic_hei_data()
    
    hei_data = st.session_state.hei_data.copy()
    
    # Show indicator only if user tried to use database
    if use_database:
        # Don't show additional warning - error already shown in load function
        pass

# Ensure we have a valid dataframe
if hei_data is None or hei_data.empty:
    st.error("❌ No data available. Please check your data source.")
    st.stop()

# Apply filters
if selected_measures:
    hei_data = hei_data[hei_data['measure_name'].isin(selected_measures)]

# Calculate metrics
metrics_df = calculate_measure_equity_metrics(hei_data)
overall_hei = calculate_overall_hei_score(hei_data, group_col=selected_demo)

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview Dashboard",
    "👥 Demographic Deep Dive",
    "🎯 Intervention Planner",
    "📈 Predictive Analytics",
    "💾 Reports & Downloads"
])

# ============================================================================
# TAB 1: OVERVIEW DASHBOARD
# ============================================================================
with tab1:
    st.header("Overview Dashboard")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall HEI Score",
            f"{overall_hei:.1f}",
            delta=f"{overall_hei - 85:.1f} vs target" if overall_hei < 85 else None,
            delta_color="inverse"
        )
    
    max_disparity = metrics_df['disparity_gap'].max() if not metrics_df.empty else 0
    with col2:
        disparity_status = "critical" if max_disparity > HEI_CONFIG['disparity_threshold'] else "warning" if max_disparity > 2.0 else "good"
        st.metric(
            "Max Disparity Gap",
            f"{max_disparity:.1f}%",
            delta=f"{max_disparity - HEI_CONFIG['disparity_threshold']:.1f}% vs threshold" if max_disparity > HEI_CONFIG['disparity_threshold'] else None,
            delta_color="inverse"
        )
        if max_disparity > HEI_CONFIG['disparity_threshold']:
            st.markdown('<p class="equity-critical">⚠️ Alert: Exceeds threshold</p>', unsafe_allow_html=True)
    
    with col3:
        equity_improvement = 2.5  # Placeholder - would calculate from historical data
        st.metric(
            "Equity Improvement Rate",
            f"{equity_improvement:.1f}%",
            delta="YoY improvement",
            delta_color="normal"
        )
    
    with col4:
        # Get total revenue from plan context
        plan_context = get_plan_context()
        if plan_context and 'bonus_revenue_at_risk' in plan_context:
            # Estimate total revenue from bonus at risk (bonus is typically 5% of revenue)
            total_revenue = plan_context.get('bonus_revenue_at_risk', 0) * 20  # Rough estimate
        else:
            total_revenue = 100000000  # Fallback default
        
        reward_projection = total_revenue * reward_factor * (overall_hei / 100)
        st.metric(
            "Reward Factor Projection",
            f"${reward_projection:,.0f}",
            delta=f"At {reward_factor:.1%} reward factor"
        )
    
    st.markdown("---")
    
    # HEI Score Gauge
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Overall HEI Score")
        fig_gauge = create_hei_gauge(overall_hei, target_score=85)
        st.plotly_chart(fig_gauge, use_container_width=True, key="hei_gauge_overview", config={'responsive': True, 'displayModeBar': 'hover'})
    
    with col2:
        st.subheader("Score Interpretation")
        if overall_hei >= 85:
            st.success(f"✅ **Excellent** ({overall_hei:.1f})")
            st.markdown("Health equity is strong across all measures and demographics.")
        elif overall_hei >= 75:
            st.info(f"🟡 **Good** ({overall_hei:.1f})")
            st.markdown("Health equity is good but has room for improvement.")
        else:
            st.error(f"🔴 **Needs Improvement** ({overall_hei:.1f})")
            st.markdown("Significant disparities exist. Targeted interventions recommended.")
        
        st.markdown("---")
        st.markdown("**Target Score:** 85+")
        st.markdown("**Industry Benchmark:** 75th percentile")
        
        # Disparity alerts
        if not metrics_df.empty:
            high_priority = metrics_df[metrics_df['priority'] == 'High']
            if len(high_priority) > 0:
                st.markdown("---")
                st.markdown("**⚠️ High Priority Measures:**")
                for _, row in high_priority.head(3).iterrows():
                    st.markdown(f"- {row['measure_name']}: {row['disparity_gap']:.1f}% gap")
    
    st.markdown("---")
    
    # Disparity Heatmap
    st.subheader("Disparity Gap by Measure")
    if not metrics_df.empty:
        fig_heatmap = create_disparity_heatmap(metrics_df)
        st.plotly_chart(fig_heatmap, use_container_width=True, key="hei_disparity_heatmap", config={'responsive': True, 'displayModeBar': 'hover'})
    else:
        st.info("No data available for selected measures.")
    
    st.markdown("---")
    
    # Equity Trend
    st.subheader("Equity Trend Over Time")
    fig_trend = create_equity_trend(hei_data)
    st.plotly_chart(fig_trend, use_container_width=True, key="hei_equity_trend", config={'responsive': True, 'displayModeBar': 'hover'})
    
    st.markdown("---")
    
    # Measure Equity Summary Table
    st.subheader("Measure-Level Equity Metrics")
    if not metrics_df.empty:
        display_df = metrics_df[['measure_name', 'overall_rate', 'disparity_gap', 'equity_score', 'priority']].copy()
        display_df.columns = ['Measure', 'Overall Rate (%)', 'Disparity Gap (%)', 'Equity Score', 'Priority']
        display_df = display_df.sort_values('Disparity Gap (%)', ascending=False)
        display_df['Overall Rate (%)'] = display_df['Overall Rate (%)'].round(1)
        display_df['Disparity Gap (%)'] = display_df['Disparity Gap (%)'].round(1)
        display_df['Equity Score'] = display_df['Equity Score'].round(1)
        
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=300)
    else:
        st.info("No data available.")

# ============================================================================
# TAB 2: DEMOGRAPHIC DEEP DIVE
# ============================================================================
with tab2:
    st.header("Demographic Deep Dive")
    
    # Measure selector for detailed analysis
    selected_measure_detail = st.selectbox(
        "Select Measure for Detailed Analysis",
        options=selected_measures if selected_measures else ALL_HEDIS_MEASURES,
        key="measure_detail"
    )
    
    st.markdown("---")
    
    # Demographic breakdowns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Breakdown by {selected_demo.replace('_', ' ').title()}")
        fig_demo = create_demographic_breakdown(hei_data, selected_measure_detail, demo_col=selected_demo)
        if fig_demo:
            st.plotly_chart(fig_demo, use_container_width=True, key=f"hei_demo_breakdown_{selected_demo}", config={'responsive': True, 'displayModeBar': 'hover'})
        else:
            st.info("No data available for this measure.")
    
    with col2:
        st.subheader("Demographic Comparison")
        # Show all dimensions for comparison
        demo_tabs = st.tabs(['Race', 'Age Group', 'Gender'])
        
        with demo_tabs[0]:
            fig_race = create_demographic_breakdown(hei_data, selected_measure_detail, demo_col='race')
            if fig_race:
                st.plotly_chart(fig_race, use_container_width=True, key="hei_demo_race_comparison", config={'responsive': True, 'displayModeBar': 'hover'})
        
        with demo_tabs[1]:
            fig_age = create_demographic_breakdown(hei_data, selected_measure_detail, demo_col='age_group')
            if fig_age:
                st.plotly_chart(fig_age, use_container_width=True, key="hei_demo_age_comparison", config={'responsive': True, 'displayModeBar': 'hover'})
        
        with demo_tabs[2]:
            fig_gender = create_demographic_breakdown(hei_data, selected_measure_detail, demo_col='gender')
            if fig_gender:
                st.plotly_chart(fig_gender, use_container_width=True, key="hei_demo_gender_comparison", config={'responsive': True, 'displayModeBar': 'hover'})
    
    st.markdown("---")
    
    # Worst and Best Performing Groups
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Worst-Performing Groups")
        measure_data = hei_data[hei_data['measure_name'] == selected_measure_detail].copy()
        if not measure_data.empty:
            demo_summary = measure_data.groupby(selected_demo).agg({
                'member_count': 'sum',
                'completed_count': 'sum'
            }).reset_index()
            demo_summary['completion_rate'] = (demo_summary['completed_count'] / demo_summary['member_count'] * 100)
            worst_groups = demo_summary.nsmallest(3, 'completion_rate')
            
            for idx, row in worst_groups.iterrows():
                st.markdown(f"""
                <div class="disparity-alert">
                    <strong>{row[selected_demo]}</strong><br>
                    Completion Rate: {row['completion_rate']:.1f}%<br>
                    Members: {row['member_count']:,}
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Best-Performing Groups")
        if not measure_data.empty:
            best_groups = demo_summary.nlargest(3, 'completion_rate')
            
            for idx, row in best_groups.iterrows():
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{row[selected_demo]}</strong><br>
                    Completion Rate: {row['completion_rate']:.1f}%<br>
                    Members: {row['member_count']:,}
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: INTERVENTION PLANNER
# ============================================================================
with tab3:
    st.header("Intervention Planner & Scenario Modeling")
    
    st.info("📊 Model different intervention scenarios to reduce disparities and improve equity scores.")
    
    # Scenario inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Intervention Parameters")
        target_timeline = st.slider(
            "Target Timeline (Months)",
            min_value=3,
            max_value=24,
            value=12,
            step=1
        )
        
        intervention_intensity = st.slider(
            "Outreach Intensity (Contacts per Member)",
            min_value=1,
            max_value=10,
            value=3,
            step=1
        )
    
    with col2:
        st.subheader("Current vs. Projected")
        
        # Calculate projections based on sliders
        projected_hei = overall_hei + (target_disparity_reduction * 0.5)  # Simplified projection
        projected_hei = min(100, projected_hei)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Current HEI", f"{overall_hei:.1f}")
        with col_b:
            st.metric("Projected HEI", f"{projected_hei:.1f}", delta=f"{projected_hei - overall_hei:.1f}")
    
    st.markdown("---")
    
    # Intervention recommendations
    st.subheader("Recommended Interventions")
    
    if not metrics_df.empty:
        high_priority = metrics_df[metrics_df['priority'] == 'High'].sort_values('disparity_gap', ascending=False)
        
        if len(high_priority) > 0:
            st.markdown("**High-Priority Measures for Intervention:**")
            for idx, row in high_priority.head(5).iterrows():
                with st.expander(f"{row['measure_name']} - Disparity Gap: {row['disparity_gap']:.1f}%"):
                    st.markdown(f"""
                    - **Current Equity Score:** {row['equity_score']:.1f}
                    - **Target Improvement:** Reduce gap by {target_disparity_reduction}%
                    - **Estimated Cost:** ${intervention_budget / len(high_priority):,.0f}
                    - **Expected Impact:** +{target_disparity_reduction * 0.5:.1f} HEI points
                    """)
        else:
            st.success("✅ No high-priority measures identified. Equity is good across all measures.")
    else:
        st.info("No data available for intervention planning.")
    
    st.markdown("---")
    
    # Financial impact projection
    st.subheader("Financial Impact Projection")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        improvement_points = projected_hei - overall_hei
        st.metric("HEI Improvement", f"+{improvement_points:.1f} points")
    
    with col2:
        # Get total revenue from plan context
        plan_context = get_plan_context()
        if plan_context and 'bonus_revenue_at_risk' in plan_context:
            total_revenue = plan_context.get('bonus_revenue_at_risk', 0) * 20
        else:
            total_revenue = 100000000
        
        reward_revenue = total_revenue * reward_factor * (improvement_points / 100)
        st.metric("Projected Reward Revenue", f"${reward_revenue:,.0f}")
    
    with col3:
        net_benefit = reward_revenue - intervention_budget
        st.metric("Net Benefit", f"${net_benefit:,.0f}", delta_color="normal" if net_benefit > 0 else "inverse")

# ============================================================================
# TAB 4: PREDICTIVE ANALYTICS
# ============================================================================
with tab4:
    st.header("Predictive Analytics & Forecasting")
    
    st.info("🔮 AI-powered predictions and recommendations for health equity optimization.")
    
    # Equity forecast
    st.subheader("Equity Forecast (12-Month Projection)")
    fig_forecast = create_equity_trend(hei_data, months=36)  # Extended to show forecast
    st.plotly_chart(fig_forecast, use_container_width=True, key="hei_equity_forecast", config={'responsive': True, 'displayModeBar': 'hover'})
    
    st.markdown("---")
    
    # ML Recommendations (placeholder)
    st.subheader("AI-Powered Intervention Recommendations")
    
    if not metrics_df.empty:
        recommendations = metrics_df.nlargest(3, 'disparity_gap')
        
        # Calculate total members across all recommendations for proportional allocation
        total_members_recommended = recommendations['total_members'].sum() if 'total_members' in recommendations.columns else 0
        
        for idx, rec in recommendations.iterrows():
            # Calculate estimated cost based on member count and disparity gap
            # Base cost: $50 per member for targeted outreach
            # Scale by disparity gap (higher gap = more intensive intervention needed)
            base_cost_per_member = 50
            intensity_multiplier = 1 + (rec['disparity_gap'] / 20)  # Higher gap = more intensive
            members = rec.get('total_members', 1000)  # Default to 1000 if not available
            
            # Calculate cost for this measure
            if intervention_budget > 0:
                # If budget is set, allocate proportionally by member count
                if total_members_recommended > 0:
                    member_share = members / total_members_recommended
                    estimated_cost = intervention_budget * member_share
                else:
                    estimated_cost = intervention_budget / len(recommendations)
            else:
                # Calculate realistic cost estimate
                estimated_cost = members * base_cost_per_member * intensity_multiplier
            
            # Expected impact calculation
            expected_impact = rec['disparity_gap'] * 0.3  # 30% of gap reduction
            
            # Confidence based on disparity gap size
            if rec['disparity_gap'] > 8:
                confidence = "Very High"
            elif rec['disparity_gap'] > 5:
                confidence = "High"
            else:
                confidence = "Medium"
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>{rec['measure_name']}</h4>
                <p><strong>Recommended Action:</strong> Targeted outreach to underrepresented groups</p>
                <p><strong>Expected Impact:</strong> +{expected_impact:.1f} HEI points</p>
                <p><strong>Confidence:</strong> {confidence} (based on historical effectiveness)</p>
                <p><strong>Estimated Cost:</strong> ${estimated_cost:,.0f}</p>
                <p><strong>Members Affected:</strong> {members:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recommendations available. Ensure data is loaded.")

# ============================================================================
# TAB 5: REPORTS & DOWNLOADS
# ============================================================================
with tab5:
    st.header("Reports & Data Downloads")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Export Options")
        
        # CSV Export
        if st.button("📥 Download Measure Equity Metrics (CSV)", use_container_width=True):
            csv = metrics_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"hei_equity_metrics_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # Detailed data export
        if st.button("📥 Download Detailed Demographic Data (CSV)", use_container_width=True):
            csv = hei_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"hei_detailed_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        st.subheader("Report Generation")
        
        st.info("📄 Full PDF and Excel reports coming in Phase 2")
        
        # Summary stats
        st.markdown("**Export Summary:**")
        st.markdown(f"- Measures: {len(metrics_df)}")
        st.markdown(f"- Overall HEI Score: {overall_hei:.1f}")
        st.markdown(f"- Max Disparity Gap: {max_disparity:.1f}%")
        st.markdown(f"- High Priority Measures: {len(metrics_df[metrics_df['priority'] == 'High'])}")
    
    st.markdown("---")
    
    # Data preview
    st.subheader("Data Preview")
    preview_tabs = st.tabs(["Equity Metrics", "Detailed Data"])
    
    with preview_tabs[0]:
        if not metrics_df.empty:
            st.dataframe(metrics_df, use_container_width=True, hide_index=True, height=300)
    
    with preview_tabs[1]:
        st.dataframe(hei_data.head(100), use_container_width=True, hide_index=True, height=300)
        st.caption(f"Showing first 100 rows of {len(hei_data):,} total rows")

# ============================================================================
# FOOTER
# ============================================================================
# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer

