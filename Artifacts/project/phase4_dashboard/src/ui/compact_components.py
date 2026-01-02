"""
Compact UI components for reduced vertical spacing
"""
import streamlit as st


def get_compact_css():
    """Get improved compact CSS - READABLE fonts, reduced spacing only"""
    return """
    <style>
    /* ========== AGGRESSIVE VERTICAL SPACING REDUCTION ========== */
    .main .block-container { 
        padding-top: 0.25rem !important; 
        padding-bottom: 0.25rem !important; 
        padding-left: 0.8rem !important; 
        padding-right: 0.8rem !important; 
        max-width: 100% !important; 
    }

    /* CRITICAL: Reduce vertical block gaps - this is the main culprit */
    div[data-testid="stVerticalBlock"] {
        gap: 0.1rem !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.1rem !important;
        margin-bottom: 0.1rem !important;
    }
    
    section[data-testid="stVerticalBlock"] {
        gap: 0.1rem !important;
    }

    /* Section spacing - MINIMAL gaps between sections - CENTER ALIGNED */
    h1 { 
        font-size: 1.8rem !important; 
        margin-top: 0.2rem !important; 
        margin-bottom: 0.15rem !important; 
        line-height: 1.2 !important; 
        padding-top: 0 !important;
        text-align: center !important;
    }

    h2 { 
        font-size: 1.4rem !important; 
        margin-top: 0.15rem !important; 
        margin-bottom: 0.1rem !important; 
        line-height: 1.2 !important; 
        padding-top: 0 !important;
        text-align: center !important;
    }

    h3 { 
        font-size: 1.1rem !important; 
        margin-top: 0.1rem !important; 
        margin-bottom: 0.1rem !important; 
        line-height: 1.2 !important; 
        padding-top: 0 !important;
        text-align: center !important;
    }
    
    h4, h5, h6 {
        text-align: center !important;
    }
    
    /* Center align markdown headers */
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4,
    div[data-testid="stMarkdownContainer"] h5,
    div[data-testid="stMarkdownContainer"] h6 {
        text-align: center !important;
    }

    /* Reduce spacing between elements - AGGRESSIVE */
    .element-container { 
        margin-bottom: 0.1rem !important; 
        padding: 0 !important;
    }
    
    .stMarkdown { 
        margin-bottom: 0.1rem !important; 
        margin-top: 0 !important;
    }
    
    div[data-testid="stMarkdownContainer"] {
        margin-bottom: 0.1rem !important;
        margin-top: 0 !important;
    }

    /* Readable metric fonts - CENTER ALIGNED */
    [data-testid="stMetric"] {
        margin-bottom: 0.1rem !important;
        padding: 0.2rem !important;
        text-align: center !important;
    }
    
    [data-testid="stMetricValue"] { 
        font-size: 1.6rem !important; 
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
    }
    [data-testid="stMetricLabel"] { 
        font-size: 0.95rem !important; 
        padding-bottom: 0.1rem !important; 
        margin-bottom: 0 !important;
        text-align: center !important;
    }
    [data-testid="stMetricDelta"] {
        text-align: center !important;
    }
    [data-testid="metric-container"] { 
        padding: 0.3rem !important; 
        margin-bottom: 0.1rem !important;
        text-align: center !important;
    }

    /* Chart and data spacing - MINIMAL */
    .stPlotlyChart { 
        margin-bottom: 0.2rem !important; 
        margin-top: 0.1rem !important;
    }
    .stDataFrame { 
        margin-bottom: 0.2rem !important; 
        margin-top: 0.1rem !important;
    }

    /* Column spacing - TIGHT */
    [data-testid="column"] { 
        padding: 0.1rem !important; 
    }
    
    [data-testid="column"] > div {
        padding: 0.2rem !important;
        margin-bottom: 0.1rem !important;
    }

    /* Interactive elements - MINIMAL spacing */
    [data-testid="stExpander"] { 
        margin-bottom: 0.15rem !important; 
        margin-top: 0.1rem !important;
    }
    [data-testid="stTabs"] { 
        margin-bottom: 0.2rem !important; 
        margin-top: 0.1rem !important;
    }
    .stTabs [data-baseweb="tab-list"] { 
        gap: 0.1rem !important; 
    }
    .stTabs [data-baseweb="tab"] { 
        padding: 0.3rem 0.6rem !important; 
        font-size: 0.95rem !important; 
    }

    /* Buttons - keep readable but compact */
    .stButton { 
        margin-bottom: 0.1rem !important;
        margin-top: 0 !important;
    }
    
    .stButton > button { 
        padding: 0.4rem 0.8rem !important; 
        font-size: 0.95rem !important; 
        margin-bottom: 0 !important;
    }

    /* Form inputs - MINIMAL spacing */
    .stSelectbox, .stTextInput, .stNumberInput { 
        margin-bottom: 0.1rem !important; 
        margin-top: 0 !important;
    }
    
    .stDateInput {
        margin-bottom: 0.1rem !important;
        margin-top: 0 !important;
    }

    /* Alerts - keep readable but compact */
    .stAlert { 
        padding: 0.4rem 0.6rem !important; 
        margin-bottom: 0.15rem !important; 
        margin-top: 0.1rem !important;
        font-size: 0.95rem !important; 
    }
    
    [data-testid="stAlert"] {
        margin-bottom: 0.15rem !important;
        margin-top: 0.1rem !important;
    }

    /* Horizontal rules - MINIMAL spacing */
    hr { 
        margin: 0.3rem 0 !important; 
    }
    
    div[data-testid="stDivider"] {
        margin: 0.3rem 0 !important;
    }

    /* Compact metric card styling - TIGHTER - CENTER ALIGNED */
    .compact-metric-card {
        background: white;
        padding: 0.4rem 0.6rem;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 0.2rem;
        text-align: center !important;
    }
    
    .compact-metric-title {
        font-size: 0.8rem;
        color: #333;
        font-weight: 500;
        margin: 0 0 0.1rem 0;
        text-align: center !important;
    }
    
    .compact-metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0.05rem 0;
        line-height: 1.1;
        text-align: center !important;
    }
    
    .compact-metric-subtitle {
        font-size: 0.7rem;
        color: #666;
        margin: 0.05rem 0 0 0;
        text-align: center !important;
    }
    
    /* Compact insight box styling - TIGHTER */
    .compact-insight-box {
        padding: 0.3rem 0.5rem;
        border-radius: 4px;
        margin-bottom: 0.15rem;
        font-size: 0.75rem;
        line-height: 1.3;
    }
    
    .compact-insight-icon {
        font-size: 0.9rem;
        margin-right: 0.2rem;
    }
    
    /* Remove all unnecessary padding/margins from containers */
    .row-widget {
        margin-bottom: 0.1rem !important;
        margin-top: 0 !important;
    }
    
    /* Reduce spacing in all Streamlit containers */
    div[data-testid="stAppViewContainer"] {
        padding: 0 !important;
    }
    
    /* Reduce header spacing */
    .header-container {
        margin-bottom: 0.3rem !important;
        margin-top: 0.3rem !important;
        padding: 0.5rem 1rem !important;
    }

    /* Mobile adjustments - EVEN TIGHTER */
    @media (max-width: 768px) {
        .main .block-container { 
            padding: 0.2rem 0.4rem !important; 
        }
        
        h1 { 
            font-size: 1.5rem !important; 
            margin-top: 0.15rem !important; 
            margin-bottom: 0.1rem !important;
            text-align: center !important;
        }
        h2 { 
            font-size: 1.2rem !important; 
            margin-top: 0.1rem !important; 
            margin-bottom: 0.1rem !important;
            text-align: center !important;
        }
        h3 { 
            font-size: 1rem !important; 
            margin-top: 0.1rem !important; 
            margin-bottom: 0.05rem !important;
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
        
        [data-testid="stMetric"],
        [data-testid="stMetricValue"],
        [data-testid="stMetricLabel"],
        [data-testid="stMetricDelta"],
        [data-testid="metric-container"] {
            text-align: center !important;
        }
        
        [data-testid="stMetricValue"] { font-size: 1.4rem !important; }
        
        .compact-metric-card,
        .kpi-card {
            text-align: center !important;
        }
        [data-testid="column"] { padding: 0.05rem !important; }
        div[data-testid="stVerticalBlock"] > div { 
            gap: 0.05rem !important; 
        }
        
        .header-container {
            margin-bottom: 0.2rem !important;
            margin-top: 0.2rem !important;
            padding: 0.4rem 0.6rem !important;
        }
    }
    </style>
    """


def compact_metric_card(title, value, subtitle="", value_color="#0066cc"):
    """
    Generate HTML for a compact metric card.
    
    Args:
        title: Metric title/label
        value: Main metric value
        subtitle: Optional subtitle text
        value_color: Color for the value (default: #0066cc)
    
    Returns:
        HTML string for the metric card
    """
    subtitle_html = f'<div class="compact-metric-subtitle">{subtitle}</div>' if subtitle else ""
    
    return f"""
    <div class="compact-metric-card">
        <div class="compact-metric-title">{title}</div>
        <div class="compact-metric-value" style="color: {value_color};">{value}</div>
        {subtitle_html}
    </div>
    """


def compact_insight_box(content, icon="💡", bg_color="#e3f2fd", border_color="#2196f3"):
    """
    Generate HTML for a compact insight box.
    
    Args:
        content: HTML content for the insight box
        icon: Icon emoji or character
        bg_color: Background color (default: light blue)
        border_color: Left border color (default: blue)
    
    Returns:
        HTML string for the insight box
    """
    return f"""
    <div class="compact-insight-box" style="background-color: {bg_color}; border-left: 3px solid {border_color};">
        <span class="compact-insight-icon">{icon}</span>{content}
    </div>
    """


def apply_compact_css_once():
    """Apply compact CSS stylesheet once per page"""
    if 'compact_css_applied' not in st.session_state:
        st.markdown(get_compact_css(), unsafe_allow_html=True)
        st.session_state.compact_css_applied = True

