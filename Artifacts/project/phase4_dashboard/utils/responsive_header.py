"""
Responsive Header Component
Provides desktop and mobile-optimized header formatting
"""
import streamlit as st

def render_responsive_header():
    """Render responsive header that adapts to desktop and mobile screens"""
    st.markdown("""
    <style>
    /* ========== DESKTOP STYLES (default, 769px+) ========== */
    .header-container {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%);
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin-top: 2rem;
        margin-bottom: 0.75rem;
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
        padding-top: 1.2rem !important;
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
            margin-top: 1.5rem;
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
        
        div.block-container {
            padding-top: 0.8rem !important;
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

    st.markdown("""
    <div class="header-container">
        <div class="header-title">⭐ StarGuard AI | Turning Data Into Stars</div>
        <div class="header-subtitle">Powered by Predictive Analytics & Machine Learning</div>
    </div>
    """, unsafe_allow_html=True)

