"""
Development Timeline Infographic Page
Shows the 6-month development journey of StarGuard AI
"""

import streamlit as st
from utils.timeline_infographic import render_timeline_infographic

# Page config
st.set_page_config(
    page_title="Development Timeline | StarGuard AI",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="auto"
)

# Import sidebar styling function (same as Home page)
try:
    from utils.sidebar_styling import apply_sidebar_styling
except ImportError:
    def apply_sidebar_styling():
        pass

# Apply consistent sidebar styling (same as Home page)
apply_sidebar_styling()

# Page header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #4A3D6F; font-size: 2.5rem; margin-bottom: 0.5rem;">
        ⏱️ StarGuard AI Development Timeline
    </h1>
    <p style="color: #666666; font-size: 1.1rem;">
        From Concept to Production in 6 Months
    </p>
</div>
""", unsafe_allow_html=True)

# Option to show static image or interactive chart
view_mode = st.radio(
    "View Mode:",
    ["Interactive Timeline", "Static Image (LinkedIn-ready)"],
    horizontal=True,
    label_visibility="collapsed"
)

if view_mode == "Static Image (LinkedIn-ready)":
    # Display the static LinkedIn-ready image
    image_path = "timeline_infographic_linkedin.png"
    try:
        st.image(image_path, use_container_width=True)
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <p style="color: #666666; font-size: 0.9rem;">
                📥 Ready to download and upload to Buffer/LinkedIn
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Download button
        with open(image_path, "rb") as file:
            st.download_button(
                label="📥 Download Image for LinkedIn",
                data=file,
                file_name="timeline_infographic_linkedin.png",
                mime="image/png"
            )
    except FileNotFoundError:
        st.warning("Timeline image not found. Generating now...")
        from utils.generate_timeline_image_enhanced import create_enhanced_timeline_image
        image_path = create_enhanced_timeline_image(image_path)
        st.image(image_path, use_container_width=True)
else:
    # Render the interactive timeline infographic
    render_timeline_infographic()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: left; color: #666666; font-size: 0.85rem; line-height: 1.6;">
    <p><strong>HEDIS Portfolio Optimizer | StarGuard AI</strong></p>
    <p>Built with Streamlit • Plotly • PostgreSQL | Development: 2024-2026</p>
    <p>🔒 <strong>Secure AI Architect</strong> | Healthcare AI that sees everything, exposes nothing.</p>
    <p>On-premises architecture delivers 2.8-4.1x ROI and $148M+ proven savings while keeping PHI locked down. Zero API transmission • HIPAA-first design.</p>
    <p>⚠️ Portfolio demonstration using synthetic data to showcase real methodology.</p>
    <p>© 2024-2026 Robert Reichert | StarGuard AI™</p>
</div>
""", unsafe_allow_html=True)
