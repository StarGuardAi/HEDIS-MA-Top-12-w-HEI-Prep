"""
Layout and page configuration utilities
"""
import streamlit as st
from config.settings import APP_CONFIG


def setup_page_config():
    """Setup Streamlit page configuration"""
    st.set_page_config(
        page_title=APP_CONFIG['app_title'],
        page_icon=APP_CONFIG['page_icon'],
        layout=APP_CONFIG['layout'],
        initial_sidebar_state=APP_CONFIG['initial_sidebar_state'],
        menu_items={
            'Get Help': 'mailto:reichert.starguardai@gmail.com',
            'Report a bug': 'mailto:reichert.starguardai@gmail.com',
            'About': 'HEDIS Portfolio Optimizer - Built by Robert Reichert\n\nLinkedIn: https://www.linkedin.com/in/sentinel-analytics/\nGitHub: https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep\nPortfolio: https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit'
        }
    )
    
    # Apply custom CSS
    _apply_custom_css()


def render_starguard_header():
    """2-line header - purple background matching sidebar"""
    st.markdown("""
    <div style="
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%);
        padding: 0.6rem 0.75rem;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 4px rgba(74, 61, 111, 0.15);
        text-align: center;
    ">
        <p style="
            color: #FFFFFF;
            font-size: 0.95rem;
            font-weight: 600;
            margin: 0 0 0.3rem 0;
            line-height: 1.3;
        ">
            ⭐ StarGuard AI | Turning Data Into Stars
        </p>
        <p style="
            color: #E8D4FF;
            font-size: 0.7rem;
            font-weight: 400;
            font-style: italic;
            margin: 0;
            line-height: 1.2;
        ">
            Powered by Predictive Analytics & Machine Learning
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_header():
    """Render StarGuard AI header at top of every page - responsive for mobile"""
    st.markdown("""
    <style>
    /* Sidebar styling - matches StarGuard AI header purple gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #4e2a84 0%, #6f5f96 100%) !important;
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span:not([class*="icon"]),
    [data-testid="stSidebar"] div:not([class*="button"]),
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    .starguard-header {
        background: linear-gradient(135deg, #4e2a84 0%, #6f5f96 100%); 
        padding: 1rem 1.5rem; 
        border-radius: 8px; 
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(78, 42, 132, 0.2);
    }
    .starguard-header-title {
        color: #FFFFFF; 
        margin: 0; 
        font-size: 1.8rem; 
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .starguard-header-subtitle {
        color: #E8D4FF; 
        margin: 0.5rem 0 0 0; 
        font-size: 0.95rem;
        font-weight: 500;
    }
    /* Mobile - 2 lines layout */
    @media (max-width: 768px) {
        .starguard-header {
            padding: 0.75rem 1rem;
        }
        .starguard-header-title {
            font-size: 1.4rem;
            flex-wrap: wrap;
        }
        .starguard-header-subtitle {
            font-size: 0.85rem;
            line-height: 1.4;
            display: block;
        }
        .starguard-header-subtitle .mobile-line1 {
            display: block;
            margin-bottom: 0.25rem;
        }
        .starguard-header-subtitle .mobile-line2 {
            display: block;
        }
    }
    </style>
    <div class="starguard-header">
        <h1 class="starguard-header-title">
            ⭐ StarGuard AI
        </h1>
        <p class="starguard-header-subtitle">
            <span class="mobile-line1">HEDIS Portfolio Optimizer</span>
            <span class="mobile-line2">AI-powered decision platform for Medicare Advantage Star Ratings</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


def apply_compact_css():
    """Improved compact CSS - READABLE fonts, reduced spacing only"""
    st.markdown("""
    <style>
    .main .block-container { 
        padding-top: 0.5rem !important; 
        padding-bottom: 0.5rem !important; 
        padding-left: 0.8rem !important; 
        padding-right: 0.8rem !important; 
        max-width: 100% !important; 
    }

    /* Section spacing - REDUCE GAPS between sections */
    h1 { 
        font-size: 1.8rem !important; 
        margin-top: 0.4rem !important; 
        margin-bottom: 0.3rem !important; 
        line-height: 1.2 !important; 
    }

    h2 { 
        font-size: 1.4rem !important; 
        margin-top: 0.3rem !important; 
        margin-bottom: 0.25rem !important; 
        line-height: 1.2 !important; 
    }

    h3 { 
        font-size: 1.1rem !important; 
        margin-top: 0.25rem !important; 
        margin-bottom: 0.2rem !important; 
        line-height: 1.2 !important; 
    }

    /* Reduce spacing between elements */
    .element-container { margin-bottom: 0.25rem !important; }
    .stMarkdown { margin-bottom: 0.25rem !important; }

    /* Readable metric fonts */
    [data-testid="stMetricValue"] { font-size: 1.6rem !important; }
    [data-testid="stMetricLabel"] { font-size: 0.95rem !important; padding-bottom: 0.2rem !important; }
    [data-testid="metric-container"] { padding: 0.5rem !important; }

    /* Chart and data spacing */
    .stPlotlyChart { margin-bottom: 0.4rem !important; }
    .stDataFrame { margin-bottom: 0.4rem !important; }

    /* Column spacing */
    [data-testid="column"] { padding: 0.2rem !important; }

    /* Interactive elements */
    [data-testid="stExpander"] { margin-bottom: 0.3rem !important; }
    [data-testid="stTabs"] { margin-bottom: 0.4rem !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 0.2rem !important; }
    .stTabs [data-baseweb="tab"] { 
        padding: 0.4rem 0.8rem !important; 
        font-size: 0.95rem !important; 
    }

    /* Buttons - keep readable */
    .stButton > button { 
        padding: 0.5rem 1rem !important; 
        font-size: 0.95rem !important; 
    }

    /* Form inputs */
    .stSelectbox, .stTextInput, .stNumberInput { margin-bottom: 0.25rem !important; }

    /* Alerts - keep readable */
    .stAlert { 
        padding: 0.5rem !important; 
        margin-bottom: 0.3rem !important; 
        font-size: 0.95rem !important; 
    }

    /* Reduce gaps between blocks */
    div[data-testid="stVerticalBlock"] > div { gap: 0.25rem !important; }

    /* Horizontal rules */
    hr { margin: 0.6rem 0 !important; }

    /* Mobile adjustments */
    @media (max-width: 768px) {
        .main .block-container { 
            padding: 0.4rem 0.5rem !important; 
        }
        
        h1 { font-size: 1.5rem !important; margin-top: 0.3rem !important; margin-bottom: 0.25rem !important; }
        h2 { font-size: 1.2rem !important; margin-top: 0.25rem !important; margin-bottom: 0.2rem !important; }
        h3 { font-size: 1rem !important; margin-top: 0.2rem !important; margin-bottom: 0.15rem !important; }
        
        [data-testid="stMetricValue"] { font-size: 1.4rem !important; }
        [data-testid="column"] { padding: 0.15rem !important; }
        div[data-testid="stVerticalBlock"] > div { gap: 0.2rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)


def _apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
        /* Main page background - professional healthcare theme */
        .stApp {
            background: linear-gradient(to bottom, #f0f4f8 0%, #ffffff 100%);
        }
        
        /* Main content container - desktop padding */
        .main .block-container {
            padding: 0.5rem 1rem;
            max-width: 100%;
        }
        
        /* Typography - desktop optimized */
        h1 {
            font-size: 2.5rem !important;
            color: #0066cc;
            font-weight: 700;
            margin-bottom: 1rem;
            border-bottom: 3px solid #00cc66;
            padding-bottom: 0.5rem;
        }
        
        h2 {
            font-size: 2rem !important;
            color: #0066cc;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        
        /* Metric cards - enhanced styling */
        [data-testid="stMetricValue"] {
            font-size: 2.5rem !important;
            font-weight: 700;
            color: #0066cc;
        }
        
        [data-testid="stMetricContainer"] {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #00cc66;
        }
        
        /* Sidebar styling - matches StarGuard AI header purple gradient */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #4e2a84 0%, #6f5f96 100%);
            padding-top: 2rem;
        }
        
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] li,
        [data-testid="stSidebar"] span:not([class*="icon"]),
        [data-testid="stSidebar"] div:not([class*="button"]),
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] label {
            color: #ffffff !important;
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)


def render_page_footer():
    """Render footer at bottom of main page content - copyright notice with security messaging"""
    from datetime import datetime, date
    
    current_year = datetime.now().year
    year_display = f"2024-{current_year}" if current_year > 2024 else "2024"
    
    # Get date range from session state if available, otherwise use defaults
    try:
        start_date = st.session_state.filters.get('date_range_start', date(2025, 10, 1))
        end_date = st.session_state.filters.get('date_range_end', date(2025, 12, 31))
        date_range_str = f"{start_date.strftime('%m/%d/%Y')} - {end_date.strftime('%m/%d/%Y')}"
    except (AttributeError, KeyError):
        # Fallback if session state not available
        date_range_str = "10/01/2025 - 12/31/2025"
    
    st.markdown("""
<div style="background:#f8f9fa;padding:0.8rem;margin-top:1.5rem;border-top:2px solid #e0e0e0;font-size:0.75rem;line-height:1.3;border-radius:4px;">
    <div style="font-size:0.95rem;font-weight:600;margin-bottom:0.2rem;color:#333;">HEDIS Portfolio Optimizer | StarGuard AI</div>
    <div style="color:#666;font-size:0.7rem;margin-bottom:0.4rem;">Built with Streamlit, Plotly, PostgreSQL | {}</div>
    <div style="background:#e8f4f8;padding:0.4rem;border-radius:3px;margin:0.3rem 0;border-left:3px solid #0066cc;">
        <strong>🔒 Secure AI Architect</strong> | Enabling LLM insights from PHI without API exposure. On-premises HIPAA-compliant AI: 2.8-4.1x ROI, $148M+ impact. <strong>Zero PHI Transmission | On-Premises | Compliance-First</strong>
    </div>
    <div style="background:#fff3cd;border-left:3px solid #ffa726;padding:0.3rem 0.5rem;margin:0.3rem 0;font-size:0.7rem;border-radius:3px;">
        ⚠️ <strong>Demo Project:</strong> Synthetic data only. Not production data.
    </div>
    <div style="text-align:center;color:#666;font-size:0.65rem;margin-top:0.4rem;padding-top:0.4rem;border-top:1px solid #e0e0e0;">
        © {} Robert Reichert | StarGuard AI™
    </div>
</div>
""".format(date_range_str, year_display), unsafe_allow_html=True)


def render_sidebar_footer():
    """Render footer at bottom of sidebar - currently empty, placeholder for future use"""
    # Footer content removed - no longer displaying disclaimer
    pass


def render_compact_metrics(metrics_list):
    """
    Render metrics in ultra-compact 2-column grid format.
    
    Args:
        metrics_list: List of dicts with keys: 'label', 'main', 'sub' (optional), 'full_width' (optional)
                     Example: [
                         {'label': 'Total Investment', 'main': '$4.25M', 'sub': '$531.52/member'},
                         {'label': 'Successful Closures', 'main': '37,514', 'sub': '35.1% rate'},
                         {'label': 'Revenue Impact', 'main': '$5,657,911', 'sub': '133% ROI', 'full_width': True}
                     ]
    """
    st.markdown("""
    <style>
    .compact-grid-2col {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.3rem;
        margin: 0.4rem 0;
    }
    .mini-metric-card {
        background: #ffffff;
        border-radius: 4px;
        padding: 0.35rem 0.4rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.08);
    }
    .mini-title {
        font-size: 0.7rem;
        color: #666666;
        margin-bottom: 0.15rem;
    }
    .mini-value {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0066cc;
        line-height: 1.05;
    }
    .mini-sub {
        font-size: 0.6rem;
        color: #888888;
        margin-top: 0.1rem;
    }
    .full-width {
        grid-column: 1 / -1;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Build HTML for metrics
    metrics_html = '<div class="compact-grid-2col">'
    for metric in metrics_list:
        sub_html = f'<div class="mini-sub">{metric.get("sub", "")}</div>' if metric.get("sub") else ""
        full_width_class = ' full-width' if metric.get('full_width', False) else ''
        metrics_html += f'''
    <div class="mini-metric-card{full_width_class}">
        <div class="mini-title">{metric["label"]}</div>
        <div class="mini-value">{metric["main"]}</div>
        {sub_html}
    </div>'''
    metrics_html += '</div>'
    
    st.markdown(metrics_html, unsafe_allow_html=True)

