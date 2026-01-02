"""
Streamlit Spacing Standards - Reusable spacing system based on Home page
Extracted from app.py to ensure consistent spacing across all 21 pages
"""

def get_spacing_css() -> str:
    """
    Returns the standard spacing CSS based on Home page patterns.
    
    Usage:
        st.markdown(get_spacing_css(), unsafe_allow_html=True)
    
    Returns:
        str: Complete CSS block with mobile-first responsive spacing
    """
    return """
<style>
/* ========== BASE CONTAINER (Mobile-First) ========== */
.main .block-container { 
    padding-top: 2.5rem !important; 
    padding-bottom: 1rem !important; 
    padding-left: 1rem !important; 
    padding-right: 1rem !important; 
    max-width: 100% !important; 
}

/* ========== HEADER SPACING (Mobile-First) ========== */
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

/* ========== ELEMENT SPACING (Mobile-First) ========== */
.element-container { margin-bottom: 0.2rem !important; }
.stMarkdown { margin-bottom: 0.2rem !important; }
div[data-testid="stVerticalBlock"] > div { gap: 0.2rem !important; }

/* ========== METRIC SPACING (Mobile-First) ========== */
[data-testid="stMetricValue"] { font-size: 1.6rem !important; }
[data-testid="stMetricLabel"] { font-size: 0.95rem !important; padding-bottom: 0.15rem !important; }
[data-testid="metric-container"] { padding: 0.5rem !important; }

/* ========== CHART & DATA SPACING (Mobile-First) ========== */
.stPlotlyChart { margin-bottom: 0.3rem !important; }
.stDataFrame { margin-bottom: 0.3rem !important; }

/* ========== COLUMN SPACING (Mobile-First) ========== */
[data-testid="column"] { padding: 0.2rem !important; }

/* ========== INTERACTIVE ELEMENTS (Mobile-First) ========== */
[data-testid="stExpander"] { 
    margin-bottom: 0 !important; 
    margin-top: 0 !important;
}
.element-container.has-expander {
    margin-bottom: 0 !important;
    margin-top: 0 !important;
}
.element-container.has-info + .element-container.has-expander {
    margin-top: 0 !important;
}
.element-container.has-info {
    margin-bottom: 0.2rem !important;
}
[data-testid="stExpander"] summary {
    padding: 0.3rem 0.5rem !important;
    margin: 0 !important;
}
[data-testid="stTabs"] { margin-bottom: 0.3rem !important; }
.stTabs [data-baseweb="tab-list"] { gap: 0.2rem !important; }
.stTabs [data-baseweb="tab"] { 
    padding: 0.4rem 0.8rem !important; 
    font-size: 0.95rem !important; 
}

/* ========== BUTTONS (Mobile-First) ========== */
.stButton > button { 
    padding: 0.5rem 1rem !important; 
    font-size: 0.95rem !important; 
}

/* ========== FORM INPUTS (Mobile-First) ========== */
.stSelectbox, .stTextInput, .stNumberInput { margin-bottom: 0.2rem !important; }

/* ========== ALERTS (Mobile-First) ========== */
.stAlert { 
    padding: 0.5rem !important; 
    margin-bottom: 0.3rem !important; 
    font-size: 0.95rem !important; 
}

/* ========== SEPARATORS (Mobile-First) ========== */
hr { margin: 0.3rem 0 !important; }

/* ========== DESKTOP ENHANCEMENTS (769px+) ========== */
@media (min-width: 769px) {
    .main .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 4rem !important;
        padding-right: 4rem !important;
        max-width: 1600px !important;
        margin: 0 auto !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
    }
    
    h2 {
        font-size: 1.75rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
        font-weight: 600 !important;
    }
    
    h3 {
        font-size: 1.35rem !important;
        margin-top: 1.25rem !important;
        margin-bottom: 0.5rem !important;
        font-weight: 600 !important;
    }
    
    /* Desktop spacing - more generous */
    .element-container {
        margin-bottom: 1rem !important;
        padding: 1rem !important;
    }
    
    .stMarkdown {
        margin-bottom: 0.75rem !important;
    }
    
    /* Desktop metrics - larger */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    [data-testid="metric-container"] {
        padding: 1rem !important;
    }
    
    /* Desktop charts - better spacing */
    .stPlotlyChart {
        margin-bottom: 1rem !important;
        margin-top: 1rem !important;
    }
    
    .stDataFrame {
        margin-bottom: 1rem !important;
        margin-top: 1rem !important;
    }
    
    /* Desktop columns - better padding */
    [data-testid="column"] {
        padding: 0.75rem !important;
    }
    
    /* Desktop expanders */
    [data-testid="stExpander"] {
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stTabs"] {
        margin-bottom: 1rem !important;
    }
    
    /* Desktop buttons */
    .stButton > button {
        padding: 0.7rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-right: 0.5rem !important;
    }
    
    /* Desktop form inputs */
    .stSelectbox,
    .stTextInput,
    .stNumberInput {
        margin-bottom: 1rem !important;
    }
    
    /* Desktop alerts */
    .stAlert {
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        font-size: 1rem !important;
    }
    
    /* Desktop vertical blocks */
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.75rem !important;
    }
    
    /* Desktop horizontal rules */
    hr {
        margin: 1rem 0 !important;
    }
}

/* ========== LARGE DESKTOP (1025px+) ========== */
@media (min-width: 1025px) {
    .main .block-container {
        padding-left: 5rem !important;
        padding-right: 5rem !important;
        max-width: 1800px !important;
    }
    
    h1 {
        font-size: 2.75rem !important;
    }
    
    h2 {
        font-size: 2rem !important;
    }
}

/* ========== MOBILE ADJUSTMENTS (max-width: 768px) ========== */
@media (max-width: 768px) {
    .main .block-container { 
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    h1 {
        margin-top: 0.5rem !important;
        font-size: 1.5rem !important;
        line-height: 1.3;
    }
    
    h2 {
        margin-top: 0.75rem !important;
        font-size: 1.25rem !important;
        line-height: 1.3;
    }
    
    h3 {
        font-size: 1.1rem !important;
        line-height: 1.3;
    }
    
    [data-testid="stMetricValue"] { 
        font-size: 1.5rem !important; 
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
    }
    
    [data-testid="column"] { 
        padding: 0.2rem !important; 
    }
}
</style>
"""


def apply_spacing_standards():
    """
    Convenience function to apply spacing standards to current page.
    
    Usage:
        from utils.spacing_standards import apply_spacing_standards
        apply_spacing_standards()
    """
    import streamlit as st
    st.markdown(get_spacing_css(), unsafe_allow_html=True)


# Spacing value constants for programmatic use
SPACING_VALUES = {
    'mobile': {
        'container_padding_top': '2.5rem',
        'container_padding_sides': '1rem',
        'container_padding_bottom': '1rem',
        'element_margin': '0.2rem',
        'vertical_block_gap': '0.2rem',
        'chart_margin': '0.3rem',
        'column_padding': '0.2rem',
        'hr_margin': '0.3rem',
        'h1_font_size': '1.8rem',
        'h1_margin_top': '0.8rem',
        'h1_margin_bottom': '0.5rem',
        'h2_font_size': '1.4rem',
        'h2_margin_top': '0.6rem',
        'h2_margin_bottom': '0.4rem',
        'h3_font_size': '1.1rem',
        'h3_margin_top': '0.5rem',
        'h3_margin_bottom': '0.3rem',
    },
    'desktop': {
        'container_padding_top': '2.5rem',
        'container_padding_sides': '4rem',
        'container_padding_bottom': '2rem',
        'container_max_width': '1600px',
        'element_margin': '1rem',
        'element_padding': '1rem',
        'vertical_block_gap': '0.75rem',
        'chart_margin': '1rem',
        'column_padding': '0.75rem',
        'hr_margin': '1rem',
        'h1_font_size': '2.5rem',
        'h1_margin_top': '1rem',
        'h1_margin_bottom': '1rem',
        'h2_font_size': '1.75rem',
        'h2_margin_top': '1.5rem',
        'h2_margin_bottom': '0.75rem',
        'h3_font_size': '1.35rem',
        'h3_margin_top': '1.25rem',
        'h3_margin_bottom': '0.5rem',
    },
    'large_desktop': {
        'container_padding_sides': '5rem',
        'container_max_width': '1800px',
        'h1_font_size': '2.75rem',
        'h2_font_size': '2rem',
    }
}




