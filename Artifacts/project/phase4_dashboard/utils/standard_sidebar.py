"""
Standard Sidebar Component
Reusable sidebar with filters, database status, and call-to-action elements
for recruiters, hiring managers, and influencers
"""
import streamlit as st
from datetime import datetime, date
from typing import Optional


def render_standard_sidebar(
    membership_slider_key: str = "membership_slider",
    start_date_key: str = "sidebar_start_date",
    end_date_key: str = "sidebar_end_date",
    show_membership_slider: bool = True,
    show_date_range: bool = True,
    show_db_status: bool = True,
    custom_filters: Optional[list] = None
):
    """
    Render a standardized sidebar with filters, database status, and CTA elements.
    
    Args:
        membership_slider_key: Unique key for membership size slider
        start_date_key: Unique key for start date input
        end_date_key: Unique key for end date input
        show_membership_slider: Whether to show membership size slider
        show_date_range: Whether to show date range filters
        show_db_status: Whether to show database connection status
        custom_filters: Optional list of custom filter functions to call
    """
    # Apply sidebar styling
    try:
        from utils.sidebar_styling import apply_sidebar_styling
        apply_sidebar_styling()
    except ImportError:
        pass
    
    # Apply global CSS to center metric labels across all pages - AGGRESSIVE TARGETING
    st.markdown("""
    <style>
    /* Center metric labels and values across all pages - COMPREHENSIVE */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricLabel"] > div,
    [data-testid="stMetricLabel"] > div > div,
    [data-testid="stMetricLabel"] > div > div > div {
        text-align: center !important;
        justify-content: center !important;
        width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        display: block !important;
    }
    
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] *,
    [data-testid="stMetricValue"] > div,
    [data-testid="stMetricValue"] > div > div,
    [data-testid="stMetricValue"] > div > div > div {
        text-align: center !important;
        justify-content: center !important;
        width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] *,
    [data-testid="stMetricDelta"] > div,
    [data-testid="stMetricDelta"] > div > div {
        text-align: center !important;
        justify-content: center !important;
        width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* Center metric container and all nested elements */
    div[data-testid="stMetricContainer"],
    div[data-testid="stMetricContainer"] *,
    div[data-testid="stMetricContainer"] > div,
    div[data-testid="stMetricContainer"] > div > div {
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
    }
    
    /* Force center alignment for metric text content */
    div[data-testid="stMetricContainer"] p,
    div[data-testid="stMetricContainer"] span,
    div[data-testid="stMetricContainer"] div {
        text-align: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* Center metric columns */
    div[data-testid="column"] [data-testid="stMetricContainer"],
    div[data-testid="column"] [data-testid="stMetricContainer"] * {
        text-align: center !important;
        align-items: center !important;
        justify-content: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<p style='color: white; font-size: 1rem; font-weight: 600;'>🎛️ Filters</p>", unsafe_allow_html=True)
        
        # Membership Size Control
        if show_membership_slider:
            st.markdown("<p style='color: white; font-size: 0.9rem; font-weight: 600;'>👥 Plan Membership Size</p>", unsafe_allow_html=True)
            membership_size = st.slider(
                "Membership Size",
                min_value=5000,
                max_value=200000,
                value=st.session_state.get('membership_size', 10000),
                step=5000,
                key=membership_slider_key,
                help="Adjust to scale calculations for different plan sizes"
            )
            st.session_state.membership_size = membership_size
            st.caption(f"📊 Scaling calculations to {membership_size:,} members")
            
            st.markdown("---")
        
        # Date Range Filters
        if show_date_range:
            st.markdown("<p style='color: white; font-size: 0.9rem; font-weight: 600;'>📅 Date Range</p>", unsafe_allow_html=True)
            
            date_col1, date_col2 = st.columns(2, gap="small")
            
            with date_col1:
                # Explicitly show Start Date label - reduced spacing
                st.markdown("<p style='color: white; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.15rem;'>Start Date</p>", unsafe_allow_html=True)
                start_date_sidebar = st.date_input(
                    "",  # Empty label - label is shown above
                    value=st.session_state.get('sidebar_start_date', date(2024, 10, 1)),
                    key=start_date_key,
                    format="MM/DD/YYYY",
                    label_visibility="collapsed"  # Hide default label, we use custom above
                )
            
            with date_col2:
                # Explicitly show End Date label - reduced spacing
                st.markdown("<p style='color: white; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.15rem;'>End Date</p>", unsafe_allow_html=True)
                end_date_sidebar = st.date_input(
                    "",  # Empty label - label is shown above
                    value=st.session_state.get('sidebar_end_date', date(2024, 12, 31)),
                    key=end_date_key,
                    format="MM/DD/YYYY",
                    label_visibility="collapsed"  # Hide default label, we use custom above
                )
            
            if start_date_sidebar <= end_date_sidebar:
                days = (end_date_sidebar - start_date_sidebar).days
                st.markdown(f"<p style='color: white; font-size: 0.85rem; margin-top: 0.5rem;'>📆 {days} days selected</p>", unsafe_allow_html=True)
            else:
                st.error("⚠️ Start date must be before end date")
            
            st.markdown("---")
        
        # Custom Filters
        if custom_filters:
            for filter_func in custom_filters:
                filter_func()
            # Add separator only if database status will be shown
            # (custom filters should NOT add separators at the end to avoid duplicates)
            if show_db_status:
                st.markdown("---")
        
        # Database Status
        if show_db_status:
            # No separator before database status - custom filters already added one if needed
            try:
                from utils.database import get_connection
                conn, count = get_connection()
                if conn:
                    st.success(f"✅ Database Connected ({count:,} records)")
                else:
                    st.warning("⚠️ Database connection issue")
            except Exception as e:
                st.warning("⚠️ Database status unavailable")
            
            st.markdown("---")
        
        # Sidebar footer content (matching app.py)
        st.markdown("**Built by:** Robert Reichert")
        st.markdown("**Version:** 4.0")
        
        st.markdown("---")
        
        # Secure AI Architect box - Call to Action for Recruiters/Hiring Managers
        st.sidebar.markdown("""
        <style>
        #secure-ai-box, #secure-ai-box * { color: #000 !important; }
        </style>
        <div id='secure-ai-box' style='background: #e8f5e9; padding: 12px; border-radius: 12px; margin: 16px auto; text-align: center; border: 2px solid #4caf50; max-width: 280px;'>
            <div style='color: #000 !important; font-weight: 700; font-size: 1.1rem; margin-bottom: 8px;'><font color='#000000'>🔒 Secure AI Architect</font></div>
            <div style='color: #000 !important; font-size: 0.85rem; line-height: 1.5;'><font color='#000000'>Healthcare AI insights without data exposure. On-premises intelligence delivering 2.8-4.1x ROI and full HIPAA compliance.</font></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mobile Optimized badge removed - no longer needed
        # st.sidebar.markdown("""
        # <style>
        # @media (max-width: 768px) {
        #     .mobile-optimized-badge { display: none !important; }
        # }
        # </style>
        # <div class='mobile-optimized-badge' style='background: linear-gradient(135deg, #10B981 0%, #059669 100%); border-radius: 50px; padding: 10px 24px; text-align: center; margin: 24px auto; color: white; font-weight: 700; font-size: 1rem; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4); border: 3px solid rgba(255, 255, 255, 0.5); max-width: 220px; display: block; width: fit-content;'>
        #     📱 Mobile Optimized
        # </div>
        # """, unsafe_allow_html=True)
        
        # Call to Action for Recruiters/Hiring Managers/Influencers
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        <div style='background: rgba(255, 255, 255, 0.15); padding: 12px; border-radius: 8px; margin-top: 16px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.3);'>
            <div style='color: #FFFFFF !important; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;'>💼 Hiring?</div>
            <div style='color: #FFFFFF !important; font-size: 0.8rem; line-height: 1.4;'>Looking for a healthcare AI architect who bridges the gap between innovation and compliance? Let's connect!</div>
        </div>
        """, unsafe_allow_html=True)


def get_sidebar_date_range():
    """Get date range from sidebar session state"""
    start_date = st.session_state.get('sidebar_start_date', datetime(2024, 10, 1))
    end_date = st.session_state.get('sidebar_end_date', datetime(2024, 12, 31))
    return start_date, end_date


def get_sidebar_membership_size():
    """Get membership size from sidebar session state"""
    return st.session_state.get('membership_size', 10000)

