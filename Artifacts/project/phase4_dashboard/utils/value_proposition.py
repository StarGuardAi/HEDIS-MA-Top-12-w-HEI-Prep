"""
Value Proposition Components
Reusable components for sidebar and footer value proposition
"""
import streamlit as st


def render_sidebar_value_proposition():
    """Render the short value proposition in the sidebar with CSS"""
    # Inject CSS to ensure dark text is visible (use st.markdown for global CSS)
    st.markdown("""
    <style>
        /* Value proposition - modern healthcare theme (override sidebar white text) */
        [data-testid="stSidebar"] .sidebar-value-proposition,
        [data-testid="stSidebar"] div[style*="background"],
        [data-testid="stSidebar"] div[style*="background-color"] {
            color: #1e293b !important;
        }
        
        [data-testid="stSidebar"] .sidebar-value-proposition p,
        [data-testid="stSidebar"] .sidebar-value-proposition span,
        [data-testid="stSidebar"] .sidebar-value-proposition strong,
        [data-testid="stSidebar"] .sidebar-value-proposition div {
            color: #1e293b !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Render the value proposition in the sidebar
    st.sidebar.markdown("""
    <div class="sidebar-value-proposition" style="background: linear-gradient(135deg, #d1fae5 0%, #ecfdf5 100%); padding: 15px; border-radius: 8px; border-left: 4px solid #14b8a6; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(20, 184, 166, 0.1);">
        <p style="margin: 0; color: #1e293b !important; font-size: 0.9rem; font-weight: 600; line-height: 1.5;">
            🔒 <strong style="color: #0f172a !important; font-weight: 700;">Secure AI Architect</strong><br>
            <span style="font-size: 0.85rem; font-weight: 400; color: #334155 !important; display: block; margin-top: 5px;">
            Solving healthcare's AI paradox: LLM capabilities without PHI exposure. On-premises deployment delivering 2.8-4.1x ROI while maintaining HIPAA compliance.
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_footer_value_proposition():
    """Render the full value proposition in the footer"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); padding: 25px; border-radius: 8px; text-align: center; margin-top: 2rem; margin-bottom: 1rem; border-top: 3px solid #14b8a6; box-shadow: 0 2px 8px rgba(20, 184, 166, 0.1);">
        <h4 style="color: #0ea5e9; margin-bottom: 15px; font-size: 1.2rem; font-weight: 700;">
            🔒 Secure AI Architect | Healthcare Data Scientist
        </h4>
        <p style="color: #334155; font-size: 0.95rem; line-height: 1.7; margin: 0; max-width: 900px; margin-left: auto; margin-right: auto;">
            <strong>Solving the industry's biggest challenge:</strong> Enabling LLM-powered insights from protected health information 
            without external API exposure. By architecting on-premises AI solutions, I bridge the $50B healthcare AI adoption barrier 
            while maintaining HIPAA compliance—delivering <strong style="color: #14b8a6;">2.8-4.1x ROI</strong> and <strong style="color: #14b8a6;">$148M+ documented impact</strong>.
        </p>
        <p style="color: #64748b; font-size: 0.85rem; margin-top: 10px; margin-bottom: 0;">
            Zero PHI Transmission | On-Premises Processing | Compliance-First Design
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_demonstration_notice():
    """Render demonstration notice at the bottom of every page"""
    st.markdown("""
    <div style="background-color: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; padding: 20px; margin-top: 1rem; margin-bottom: 2rem;">
        <p style="margin: 0; color: #856404; font-size: 0.95rem; line-height: 1.6; text-align: center;">
            <strong style="font-size: 1.1rem; display: block; margin-bottom: 10px;">⚠️ Demonstration Portfolio Project</strong>
            This dashboard contains synthetic data for demonstration purposes only. Data, metrics, and analyses are not production data 
            and do not represent any actual healthcare organization. Built to showcase healthcare analytics capabilities and technical proficiency.
        </p>
    </div>
    """, unsafe_allow_html=True)

