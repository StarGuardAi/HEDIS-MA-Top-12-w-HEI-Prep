"""
Script to apply master update to all remaining pages.
This applies the 5-step update process to each page file.
"""
import os
import re

# Define the pages to update
PAGES = [
    "pages/6_🤖_AI_Executive_Insights.py",
    "pages/7_📊_What-If_Scenario_Modeler.py",
    "pages/8_🎓_AI_Capabilities_Demo.py",
    "pages/8_📋_Campaign_Builder.py",
    "pages/9_🔔_Alert_Center.py",
    "pages/10_📈_Historical_Tracking.py",
    "pages/11_💰_ROI_Calculator.py",
    "pages/13_📋_Measure_Analysis.py",
    "pages/14_⭐_Star_Rating_Simulator.py",
    "pages/15_🔄_Gap_Closure_Workflow.py",
    "pages/16_🤖_ML_Gap_Closure_Predictions.py",
    "pages/17_📊_Competitive_Benchmarking.py",
    "pages/18_🤖_Secure_AI_Chatbot.py",
    "pages/18_📋_Compliance_Reporting.py",
    "pages/19_⚖️_Health_Equity_Index.py",
    "pages/z_Performance_Dashboard.py",
]

# Compact CSS to add after st.set_page_config
COMPACT_CSS = '''st.markdown("""
<style>
/* Compact header spacing */
.block-container { padding-top: 1rem !important; }
.main h1:first-of-type { margin-top: 1rem !important; }
.element-container { margin: 0.2rem 0 !important; }

/* Sidebar button fix */
[data-testid="stSidebar"] button[kind="header"] { color: white !important; }
[data-testid="stSidebar"] button svg { fill: white !important; stroke: white !important; }

/* Sidebar text centering */
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label { text-align: center !important; }

/* Mobile sidebar overlap fix */
@media (max-width: 768px) {
    section[data-testid="stSidebar"][aria-expanded="true"] ~ .main .block-container {
        margin-left: 280px !important;
        transition: margin-left 0.3s ease;
    }
    section[data-testid="stSidebar"][aria-expanded="true"] ~ .main::before {
        content: ""; position: fixed; top: 0; left: 280px; right: 0; bottom: 0;
        background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(2px); z-index: 999;
    }
}
</style>
""", unsafe_allow_html=True)'''

# New header HTML
NEW_HEADER = '''st.markdown("""
<div style='background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%); padding: 14px 24px; border-radius: 10px; margin-bottom: 14px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
    <h1 style='color: white; font-size: 1.7rem; font-weight: 700; margin: 0 0 6px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>⭐ StarGuard AI | Turning Data Into Stars</h1>
    <p style='color: rgba(255, 255, 255, 0.92); font-size: 0.82rem; margin: 0; line-height: 1.4;'>Powered by Predictive Analytics & Machine Learning | Healthcare AI Architect | $148M+ Savings in HEDIS & Star Ratings | Context Engineering + Agentic RAG</p>
</div>
""", unsafe_allow_html=True)'''

# Sidebar additions
SIDEBAR_ADDITIONS = '''# Secure AI box and Mobile Optimized badge
st.sidebar.markdown("""
<style>
#secure-ai-box, #secure-ai-box * { color: #000 !important; }
.mobile-optimized-badge { display: block !important; }
@media (max-width: 768px) { .mobile-optimized-badge { display: none !important; } }
</style>

<div id='secure-ai-box' style='background: #e8f5e9; padding: 12px; border-radius: 12px; margin: 16px auto; text-align: center; border: 2px solid #4caf50; max-width: 280px;'>
    <div style='color: #000 !important; font-weight: 700; font-size: 1.1rem; margin-bottom: 8px;'>
        <font color='#000000'>🔒 Secure AI Architect</font>
    </div>
    <div style='color: #000 !important; font-size: 0.85rem; line-height: 1.5;'>
        <font color='#000000'>Healthcare AI insights without data exposure. On-premises intelligence delivering 2.8-4.1x ROI and full HIPAA compliance.</font>
    </div>
</div>

<div class='mobile-optimized-badge' style='background: linear-gradient(135deg, #10B981 0%, #059669 100%); border-radius: 50px; padding: 10px 24px; text-align: center; margin: 24px auto; color: white; font-weight: 700; font-size: 1rem; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4); border: 3px solid rgba(255, 255, 255, 0.5); max-width: 220px;'>
    📱 Mobile Optimized
</div>
""", unsafe_allow_html=True)'''

# New footer HTML
NEW_FOOTER = '''st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1.5rem; margin-top: 1.5rem; background: #f8f9fa;'>
    <p style='font-weight: 700; font-size: 1.1rem; color: #333; margin-bottom: 0.8rem;'>HEDIS Portfolio Optimizer | StarGuard AI</p>
    <p style='color: #666; font-size: 0.9rem; margin-bottom: 1.2rem;'>Built with Streamlit • Plotly • PostgreSQL | Development: 2024-2026</p>
    <div style='background: #e3f2fd; border-left: 4px solid #2196f3; padding: 12px 16px; margin: 12px auto; max-width: 1200px; text-align: left; border-radius: 6px;'>
        <p style='color: #1565c0; font-size: 0.9rem; line-height: 1.5; margin: 0;'>🔒 <strong>Secure AI Architect</strong> | Healthcare AI that sees everything, exposes nothing. On-premises architecture delivers 2.8-4.1x ROI and $148M+ proven savings while keeping PHI locked down. Zero API transmission • HIPAA-first design.</p>
    </div>
    <div style='background: #fff9e6; border-left: 4px solid #ff9800; padding: 12px 16px; margin: 12px auto; max-width: 1200px; text-align: left; border-radius: 6px;'>
        <p style='color: #d84315; font-size: 0.9rem; line-height: 1.5; margin: 0;'>⚠️ <strong>Portfolio demonstration</strong> using synthetic data to showcase real methodology.</p>
    </div>
    <p style='color: #999; font-size: 0.85rem; margin-top: 1.2rem;'>© 2024-2026 Robert Reichert | StarGuard AI™</p>
</div>
""", unsafe_allow_html=True)'''

print("This script shows the patterns to apply. Manual updates are safer for complex files.")
print(f"Remaining pages to update: {len(PAGES)}")

