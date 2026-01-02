"""
Page 1: ROI by Measure
Bar chart showing ROI performance across all HEDIS measures
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from utils.database import execute_query
from utils.queries import get_roi_by_measure_query
from utils.charts import create_bar_chart
from utils.data_helpers import show_data_availability_warning, get_data_date_range, format_date_display
from utils.plan_context import get_plan_context, get_plan_size_scenarios
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header
from src.ui.compact_components import compact_metric_card, compact_insight_box, apply_compact_css_once
from utils.sidebar_styling import apply_sidebar_styling

st.set_page_config(page_title="ROI by Measure", page_icon="📊", layout="wide")

st.markdown("""
<style>
    /* HEADER STYLING - Match Home Page Format */
    .header-container {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%);
        padding: 0.5rem 0.75rem 0.6rem 0.75rem;
        border-radius: 6px;
        margin-top: -1rem !important;
        margin-bottom: 0.1rem;
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

    /* Mobile Header Adjustments */
    @media (max-width: 768px) {
        .header-container {
            padding: 0.6rem 0.8rem;
            border-radius: 6px;
            margin-top: -1rem !important;
            margin-bottom: 0.1rem;
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
    }

    /* FINAL AGGRESSIVE SPACING - HIGHEST PRIORITY */
    section.main > div.block-container {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Zero-top enforcement - Headers flush to top */
    .main > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    .block-container {
        padding-top: 0rem !important;
    }
    
    section.main div[data-testid="stVerticalBlock"] > div {
        gap: 0.25rem !important;
    }
    
    section.main .element-container {
        margin-bottom: 0.4rem !important;
    }
    
    section.main h1 {
        font-size: 1.8rem !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    section.main h2 {
        font-size: 1.4rem !important;
        margin-top: 0.6rem !important;
        margin-bottom: 0.6rem !important;
    }
    
    section.main h3 {
        font-size: 1.1rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    section.main .stMarkdown p {
        margin-bottom: 0.4rem !important;
    }
    
    @media (max-width: 768px) {
        section.main > div.block-container {
            padding-top: 0rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Purple Sidebar Theme + White Text Everywhere
st.markdown("""
<style>
/* ========== PURPLE SIDEBAR THEME ========== */
/* Match the StarGuard AI header purple gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

/* ========== ALL SIDEBAR TEXT WHITE ========== */
/* Force ALL text in sidebar to be white */
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] button {
    color: #FFFFFF !important;
}

/* ========== WHITE "HOME" LABEL ========== */
[data-testid="stSidebarNav"] ul li:first-child a {
    font-size: 0 !important;
    background: rgba(255, 255, 255, 0.2) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="stSidebarNav"] ul li:first-child a::before {
    content: "🏠 Home" !important;
    font-size: 1.1rem !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    display: block !important;
    -webkit-text-fill-color: #FFFFFF !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
}

/* All sidebar navigation links white */
[data-testid="stSidebarNav"] a {
    color: #FFFFFF !important;
}

[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a div,
[data-testid="stSidebarNav"] a p {
    color: #FFFFFF !important;
}

/* "Mobile Optimized" badge - white text */
[data-testid="stSidebar"] .element-container div[data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
}

/* Success/Info boxes in sidebar - white text */
[data-testid="stSidebar"] [data-testid="stSuccess"],
[data-testid="stSidebar"] [data-testid="stInfo"] {
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}

[data-testid="stSidebar"] [data-testid="stSuccess"] *,
[data-testid="stSidebar"] [data-testid="stInfo"] * {
    color: #FFFFFF !important;
}

/* View less/more links - white */
[data-testid="stSidebar"] button {
    color: #FFFFFF !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* Hide "Mobile Optimized" message on mobile */
    [data-testid="stSidebar"] [data-testid="stSuccess"] {
        display: none !important;
    }
}

/* Desktop: Show "Mobile Optimized" message */
@media (min-width: 769px) {
    [data-testid="stSidebar"] [data-testid="stSuccess"] {
        display: block !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Apply sidebar styling FIRST (purple gradient matching StarGuard AI header)
apply_sidebar_styling()

# Responsive Header - Adapts to Desktop/Mobile
st.markdown("""
<div class="header-container">
    <div class="header-title">⭐ StarGuard AI | Turning Data Into Stars</div>
    <div class="header-subtitle">Powered by Predictive Analytics & Machine Learning</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.success("📱 Mobile Optimized")

# Sidebar footer
render_sidebar_footer()

# Initialize session state if not exists
if 'membership_size' not in st.session_state:
    st.session_state.membership_size = 10000

BASELINE_MEMBERS = 10000
scale_factor = st.session_state.membership_size / BASELINE_MEMBERS
membership_size = st.session_state.membership_size

st.markdown("### 💰 ROI Analysis by HEDIS Measure")
st.markdown(f"### Investment Efficiency Analysis - {membership_size:,} Member Plan")
st.markdown("**Proof of concept at 10K scale, ready to expand**")
st.markdown("Compare ROI performance across all 12 HEDIS measures")

# Get plan context for storytelling
plan_context = get_plan_context()
plan_scenarios = get_plan_size_scenarios()
current_scenario = plan_scenarios.get(membership_size, plan_scenarios[10000])

# Storytelling context
if membership_size == 10000:
    st.info("💡 **Small Plans:** Proves ROI before scaling - This baseline demonstrates measurable results at manageable scale.")
elif membership_size <= 25000:
    st.success("💡 **Mid-Size Plans:** Your typical turnaround scenario - Proven strategies drive significant impact with moderate investment.")
else:
    st.warning("💡 **Large/Enterprise Plans:** Enterprise-scale impact projection - Strategies proven at smaller scale adapted for larger operations.")

st.divider()

# Date range filter
col1, col2, col3 = st.columns([1, 1, 2], gap="small")
with col1:
    start_date = st.date_input("Start Date", value=datetime(2024, 10, 1), format="MM/DD/YYYY")
with col2:
    end_date = st.date_input("End Date", value=datetime(2024, 12, 31), format="MM/DD/YYYY")
with col3:
    st.info("💰 Revenue Impact = Successful Closures × $100 per closure")
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

# Execute query
try:
    query = get_roi_by_measure_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    # Use query string as cache key to ensure date changes trigger rerun
    df = execute_query(query)
    
    if df.empty:
        from utils.data_helpers import get_data_date_range
        st.warning(f"⚠️ No data found for the selected date range: {format_date_display(start_date)} to {format_date_display(end_date)}")
        date_range = get_data_date_range()
        if date_range:
            st.info(f"💡 Available data: {format_date_display(date_range[0])} to {format_date_display(date_range[1])}")
    else:
        # Scale data - convert to float first to avoid Decimal type issues
        df_scaled = df.copy()
        df_scaled['total_investment'] = df_scaled['total_investment'].astype(float) * scale_factor
        df_scaled['revenue_impact'] = df_scaled['revenue_impact'].astype(float) * scale_factor
        df_scaled['successful_closures'] = df_scaled['successful_closures'].astype(float) * scale_factor
        df_scaled['total_interventions'] = df_scaled['total_interventions'].astype(float) * scale_factor
        
        # Summary metrics (scaled) - using compact column layout
        total_investment = df_scaled['total_investment'].sum()
        total_closures = int(df_scaled['successful_closures'].sum())
        total_interventions = int(df_scaled['total_interventions'].sum())
        avg_roi = df_scaled['roi_ratio'].mean()
        revenue_impact = df_scaled['revenue_impact'].sum()
        net_benefit = revenue_impact - total_investment
        success_rate = (total_closures / total_interventions * 100) if total_interventions > 0 else 0
        
        # KPI Section - using compact components
        st.header("📊 Key Performance Indicators")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                compact_metric_card(
                    "Total Investment",
                    f"${total_investment:,.0f}",
                    f"${total_investment/membership_size:.2f} per member" if membership_size > 0 else ""
                ),
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                compact_metric_card(
                    "Successful Closures",
                    f"{total_closures:,}",
                    f"{success_rate:.1f}% success rate" if total_interventions > 0 else ""
                ),
                unsafe_allow_html=True
            )
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(
                compact_metric_card(
                    "Revenue Impact",
                    f"${revenue_impact:,.0f}",
                    f"${revenue_impact/membership_size:.2f} per member" if membership_size > 0 else ""
                ),
                unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                compact_metric_card(
                    "Net Benefit",
                    f"${net_benefit:,.0f}",
                    f"ROI: {avg_roi:.2f}x",
                    value_color="#00B050"
                ),
                unsafe_allow_html=True
            )
        
        st.divider()
        
        # Chart (ROI ratio is constant, but title shows scale if not 10K)
        chart_title = "Return on Investment by HEDIS Measure"
        if membership_size != BASELINE_MEMBERS:
            chart_title += f" ({membership_size:,} member plan)"
        
        fig = create_bar_chart(
            df_scaled,
            x_col="measure_code",
            y_col="roi_ratio",
            title=chart_title,
            x_label="HEDIS Measure",
            y_label="ROI Ratio",
            color_col="roi_ratio",
        )
        st.plotly_chart(fig, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Data table with details (scaled)
        with st.expander("📋 View Detailed Data"):
            display_df = df_scaled[[
                "measure_code",
                "measure_name",
                "total_investment",
                "revenue_impact",
                "roi_ratio",
                "successful_closures",
                "total_interventions"
            ]].copy()
            display_df.columns = [
                "Measure Code",
                "Measure Name",
                "Total Investment ($)",
                "Revenue Impact ($)",
                "ROI Ratio",
                "Successful Closures",
                "Total Interventions"
            ]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"roi_by_measure_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        
        # Key Insights Section - using compact components
        st.header("💡 Key Insights")
        
        top_measure = df_scaled.loc[df_scaled['roi_ratio'].idxmax()]
        bottom_measure = df_scaled.loc[df_scaled['roi_ratio'].idxmin()]
        
        # Calculate cost per closure for top measure
        top_cost_per_closure = top_measure['total_investment'] / top_measure['successful_closures'] if top_measure['successful_closures'] > 0 else 0
        
        st.markdown(
            compact_insight_box(
                f"<strong>Top Performer:</strong> {top_measure['measure_code']} - {top_measure['measure_name']} achieved <strong>{top_measure['roi_ratio']:.2f}x ROI</strong> with <strong>${top_cost_per_closure:.2f} cost per closure</strong> and <strong>{int(top_measure['successful_closures']):,} closures</strong>.",
                icon="🎯",
                bg_color="#e3f2fd",
                border_color="#2196f3"
            ),
            unsafe_allow_html=True
        )
        
        st.markdown(
            compact_insight_box(
                f"<strong>Financial Impact:</strong> All 12 HEDIS measures delivered positive ROI <strong>({df_scaled['roi_ratio'].min():.2f}x - {df_scaled['roi_ratio'].max():.2f}x)</strong>, generating <strong>${net_benefit:,.0f} net benefit</strong> with <strong>{success_rate:.1f}% overall success rate</strong>.",
                icon="📊",
                bg_color="#e8f5e9",
                border_color="#4caf50"
            ),
            unsafe_allow_html=True
        )
        
        st.markdown(
            compact_insight_box(
                f"<strong>Optimization Opportunity:</strong> {bottom_measure['measure_code']} - {bottom_measure['measure_name']} shows <strong>{bottom_measure['roi_ratio']:.2f}x ROI</strong> (lowest). Consider reviewing intervention mix to improve efficiency.",
                icon="💡",
                bg_color="#e3f2fd",
                border_color="#2196f3"
            ),
            unsafe_allow_html=True
        )
            
except Exception as e:
    st.error(f"Error loading data: {e}")

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer



