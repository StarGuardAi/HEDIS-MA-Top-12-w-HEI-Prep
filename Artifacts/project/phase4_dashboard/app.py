"""
Phase 4 Dashboard - HEDIS Portfolio Optimizer
Main Streamlit application with home page and navigation
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from utils.database import execute_query, test_connection, get_db_status_message
from utils.queries import get_portfolio_summary_query
from utils.plan_context import get_plan_context, get_plan_size_scenarios, get_industry_benchmarks

# Page configuration
st.set_page_config(
    page_title="HEDIS Star Rating Portfolio Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",  # Hide sidebar on mobile by default
    menu_items={
        'Get Help': 'mailto:reichert.starguardai@gmail.com',
        'Report a bug': 'mailto:reichert.starguardai@gmail.com',
        'About': 'Case Study: Regional MA Plan Turnaround Initiative - Built by Robert Reichert'
    }
)

# Initialize session state for membership size
if 'membership_size' not in st.session_state:
    st.session_state.membership_size = 10000

# Calculate scale factor (baseline is 10,000 members)
BASELINE_MEMBERS = 10000
scale_factor = st.session_state.membership_size / BASELINE_MEMBERS

# Professional medical theme CSS
st.markdown("""
<style>
    /* Main page background */
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Main content container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4e2a84 0%, #8f67d1 100%);
        padding-top: 2rem;
    }
    
    /* All sidebar text elements - white */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span:not([class*="icon"]):not([class*="button"]),
    [data-testid="stSidebar"] div:not([class*="button"]),
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] a,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] .stMarkdown span,
    [data-testid="stSidebar"] .stMarkdown div,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] div,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] a {
        color: #ffffff !important;
        font-weight: 550;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #4e2a84;
    }
    
    /* KPI card styling */
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #4e2a84;
    }
    
    /* Header styling */
    h1 {
        color: #4e2a84;
        border-bottom: 3px solid #8f67d1;
        padding-bottom: 0.5rem;
    }
    
    h2 {
        color: #4e2a84;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #4e2a84;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background-color: #8f67d1;
        color: white;
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess {
        background-color: #e8f5e9;
        border-left: 4px solid #388e3c;
    }
    
    .stInfo {
        background-color: #e3f2fd;
        border-left: 4px solid #1976d2;
    }
    
    .stWarning {
        background-color: #fff3e0;
        border-left: 4px solid #f57c00;
    }
    
    .stError {
        background-color: #ffebee;
        border-left: 4px solid #c62828;
    }
    
    /* Slider styling - make thumb larger and easier to grab */
    .stSlider > div > div > div {
        background-color: #4e2a84;
    }
    
    .stSlider > div > div > div > div {
        background-color: #8f67d1;
        width: 24px !important;
        height: 24px !important;
        border-radius: 50%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .stSlider > div > div > div > div:hover {
        background-color: #6a3fa3;
        transform: scale(1.1);
        transition: all 0.2s ease;
    }
    
    /* Mobile-friendly responsive design */
    @media (max-width: 768px) {
        .kpi-card-container {
            padding: 1rem;
        }
        .kpi-main-value {
            font-size: 1.5rem;
        }
        .comparison-table {
            font-size: 0.9rem;
        }
        .comparison-table th,
        .comparison-table td {
            padding: 0.5rem;
        }
        
        /* Mobile-specific styles */
        [data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.2rem !important;
        }
        
        h3 {
            font-size: 1rem !important;
        }
        
        .dataframe {
            font-size: 0.8rem;
        }
        
        /* Improve table scrolling on mobile */
        .stDataFrame {
            overflow-x: auto;
        }
        
        /* Larger touch targets for buttons */
        .stButton > button {
            min-height: 44px;
            padding: 0.75rem 1rem;
        }
        
        /* Slider improvements for mobile */
        .stSlider > div > div > div > div {
            width: 28px !important;
            height: 28px !important;
        }
    }
    
    /* Button styling for +/- controls */
    button[kind="secondary"] {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        min-width: 50px !important;
        height: 50px !important;
        border-radius: 50% !important;
        background-color: #4e2a84 !important;
        color: white !important;
    }
    
    button[kind="secondary"]:hover {
        background-color: #8f67d1 !important;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("https://via.placeholder.com/200x60/4e2a84/ffffff?text=HEDIS+Optimizer", use_column_width=True)
    st.markdown("# 📊 Phase 4 Dashboard")
    st.markdown("---")
    
    # Current plan size display
    st.markdown("### 📋 Current Plan Size")
    st.info(f"**{st.session_state.membership_size:,} members**")
    st.markdown("---")
    
    st.markdown("## 📊 Home (KPI Dashboard)")
    st.markdown("**Q4 2024 Turnaround Results for 10K Member Plan**")
    st.markdown("Scaled projections for your plan size")
    st.markdown("### 📈 Visualizations")
    st.markdown("- [💰 ROI Analysis](1_roi_by_measure)")
    st.markdown("  _Investment efficiency - Proof of concept at 10K scale_")
    st.markdown("- [📈 Intervention Performance](2_cost_per_closure)")
    st.markdown("  _Low-touch digital outperforms traditional - Scalable strategy_")
    st.markdown("- [💵 Budget Management](4_budget_variance)")
    st.markdown("  _Fiscal discipline during turnaround_")
    st.markdown("- [🎯 Cost Efficiency](5_cost_tier_comparison)")
    st.markdown("  _Cost-effective strategies - Replicable across populations_")
    st.markdown("- [📊 Monthly Trends](3_monthly_trend)")
    
    st.markdown("---")
    
    # Database connection status
    if test_connection():
        status_message = get_db_status_message()
        st.success(status_message)
    else:
        st.error("❌ Database Connection Failed")
        st.info("Check your database credentials in environment variables")
    
    st.markdown("---")
    st.markdown("### 📅 Data Period")
    st.markdown("**Q4 2024**\n(October - December)")
    
    st.markdown("---")
    st.markdown("**Built by:** Robert Reichert")
    st.markdown("**Phase:** 4 - Interactive Dashboard")
    
    # Mobile navigation indicator
    st.markdown("---")
    st.sidebar.caption("📱 Mobile: Use ☰ menu to navigate")

# Main content - Home Page
st.title("📊 HEDIS Star Rating Portfolio Optimizer")
st.markdown("### Case Study: Regional MA Plan Turnaround Initiative")

st.divider()

# Database connection check
if not test_connection():
    st.error("⚠️ **Database Connection Failed**")
    status_message = get_db_status_message()
    if 'SQLite' in status_message or 'sqlite' in status_message.lower():
        st.info("""
        Please ensure:
        1. SQLite database file exists at: `data/hedis_portfolio.db`
        2. The file has proper read permissions
        3. If using PostgreSQL, ensure service is running and credentials are set
        """)
    else:
        st.info("""
        Please ensure:
        1. SQLite database file exists at: `data/hedis_portfolio.db`, OR
        2. PostgreSQL service is running and database `hedis_portfolio` exists
        3. Environment variables are set (if using PostgreSQL):
           - `DB_HOST` (default: localhost)
           - `DB_PORT` (default: 5432)
           - `DB_NAME` (default: hedis_portfolio)
           - `DB_USER` (default: hedis_api)
           - `DB_PASSWORD` (default: hedis_password)
        """)
    st.stop()

# Get plan context (after connection check)
plan_context = get_plan_context()
plan_scenarios = get_plan_size_scenarios()
benchmarks = get_industry_benchmarks()

# KEY INSIGHTS SECTION - Prominent placement for recruiters
st.markdown("""
<div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; 
            border-left: 5px solid #1f77b4; margin-bottom: 30px;">
    <h3 style="color: #1f77b4; margin-top: 0;">🎯 Key Insights - Q4 2024 Turnaround Results</h3>
    <ul style="font-size: 16px; line-height: 1.8; margin-bottom: 0;">
        <li><strong>Breakthrough Discovery:</strong> Low-touch digital interventions (<strong>46.4%</strong> success rate) 
            outperformed traditional high-touch methods (<strong>42.1%</strong>) at <strong>14x lower cost</strong> per member.</li>
        <li><strong>Top Performer:</strong> Blood Pressure Diabetes (BPD) measure achieved <strong>1.38x ROI</strong> with efficient 
            <strong>$72.49</strong> cost per closure through smart intervention mix.</li>
        <li><strong>Financial Impact:</strong> All <strong>12 HEDIS measures</strong> delivered positive ROI (<strong>1.19x - 1.38x</strong>), 
            generating <strong>$66K net benefit</strong> in single quarter with <strong>42.4%</strong> success rate.</li>
        <li><strong>Scalability:</strong> Model proven at <strong>10K member scale</strong>, ready to scale to enterprise plans 
            with consistent ROI performance.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

# PLAN PROFILE CONTEXT BOX
st.markdown("""
<div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
            padding: 1.5rem; 
            border-radius: 10px; 
            border-left: 5px solid #4caf50;
            margin: 1rem 0;'>
    <h3 style='color: #2e7d32; margin-top: 0;'>📋 PLAN PROFILE</h3>
    <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;'>
        <div>
            <strong>• Plan Name:</strong> """ + plan_context['plan_name'] + """<br>
            <strong>• Members:</strong> """ + f"{plan_context['total_members']:,}" + """<br>
            <strong>• Geographic Region:</strong> """ + plan_context['geographic_region'] + """<br>
            <strong>• Plan Type:</strong> """ + plan_context['plan_type'] + """
        </div>
        <div>
            <strong>• Star Rating:</strong> """ + f"{plan_context['star_rating_2024']:.1f}" + """ → Projected """ + f"{plan_context['star_rating_projected_2025']:.1f}" + """ (Q4 2024 initiative)<br>
            <strong>• At Risk:</strong> $""" + f"{plan_context['bonus_revenue_at_risk']:,.0f}" + """ in bonus payments<br>
            <strong>• Challenge:</strong> Low gap closure rates, manual outreach<br>
            <strong>• Member Growth:</strong> """ + f"{plan_context['member_growth_yoy']:.1f}%" + """ YoY (showing trouble)
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# PLAN SIZE SCENARIO SELECTOR
st.markdown("### 🎯 Plan Size Scenarios")
st.markdown("**Select a scenario to see projected outcomes for your plan size:**")

# Create scenario selector buttons
scenario_cols = st.columns(4)
selected_scenario = None

for idx, (size, scenario) in enumerate(plan_scenarios.items()):
    with scenario_cols[idx]:
        is_selected = st.session_state.membership_size == size
        button_label = f"**{scenario['name']}**\n{scenario['label']}"
        
        if st.button(button_label, key=f"scenario_{size}", use_container_width=True,
                    type="primary" if is_selected else "secondary"):
            st.session_state.membership_size = size
            st.rerun()

# Display current scenario details
current_scenario = plan_scenarios.get(st.session_state.membership_size, plan_scenarios[10000])
st.markdown(f"<h3 style='text-align: center; color: #4e2a84; margin: 1rem 0;'>Current Analysis: {current_scenario['name']} ({st.session_state.membership_size:,} members)</h3>", unsafe_allow_html=True)

# Scenario details box
st.markdown(f"""
<div style='background: #f5f5f5; padding: 1rem; border-radius: 8px; border-left: 4px solid #4e2a84; margin: 1rem 0;'>
    <strong>Scenario Characteristics:</strong><br>
    • <strong>Description:</strong> {current_scenario['description']}<br>
    • <strong>Investment Range:</strong> {current_scenario['investment_range']}<br>
    • <strong>Implementation Complexity:</strong> {current_scenario['implementation_complexity']}<br>
    • <strong>Typical Characteristics:</strong> {current_scenario['typical_characteristics']}
</div>
""", unsafe_allow_html=True)

membership_size = st.session_state.membership_size
scale_factor = membership_size / BASELINE_MEMBERS

st.divider()

st.divider()

# Load portfolio summary KPIs
try:
    query = get_portfolio_summary_query(
        start_date="2024-10-01",
        end_date="2024-12-31"
    )
    summary_df = execute_query(query)
    
    if summary_df.empty:
        st.warning("⚠️ No data found in database. Please ensure Phase 3 data is loaded.")
    else:
        summary = summary_df.iloc[0]
        
        # Get baseline values (for 10K members) - convert to float to avoid Decimal type issues
        baseline_investment = float(summary['total_investment'])
        baseline_closures = float(summary['total_closures'])
        baseline_revenue = float(summary['revenue_impact'])
        baseline_net_benefit = float(summary['net_benefit'])
        baseline_interventions = float(summary['total_interventions'])
        roi_ratio = float(summary['roi_ratio'])  # Constant
        success_rate = float(summary['overall_success_rate'])  # Constant
        avg_cost_per_closure = baseline_investment / baseline_closures if baseline_closures > 0 else 0  # Constant
        
        # Calculate scaled values
        scaled_investment = baseline_investment * scale_factor
        scaled_closures = baseline_closures * scale_factor
        scaled_revenue = baseline_revenue * scale_factor
        scaled_net_benefit = baseline_net_benefit * scale_factor
        scaled_interventions = baseline_interventions * scale_factor
        
        # Calculate per-member metrics
        per_member_investment = scaled_investment / membership_size if membership_size > 0 else 0
        per_member_revenue = scaled_revenue / membership_size if membership_size > 0 else 0
        per_member_net_benefit = scaled_net_benefit / membership_size if membership_size > 0 else 0
        
        # KPI CARDS SECTION (6 cards in 2 rows)
        st.subheader("📈 Portfolio KPIs")
        
        # Custom KPI card styling
        st.markdown("""
        <style>
        .kpi-card-container {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #4e2a84;
            margin-bottom: 1rem;
        }
        .kpi-main-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #4e2a84;
            margin: 0.5rem 0;
        }
        .kpi-per-member {
            font-size: 1rem;
            color: #666;
            margin-top: 0.5rem;
        }
        .kpi-label {
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Row 1
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="kpi-card-container">
                <div class="kpi-label">Total Investment</div>
                <div class="kpi-main-value">${scaled_investment:,.0f}</div>
                <div class="kpi-per-member">(${per_member_investment:.2f} per member)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            per_member_closures = scaled_closures / membership_size if membership_size > 0 else 0
            st.markdown(f"""
            <div class="kpi-card-container">
                <div class="kpi-label">Successful Closures</div>
                <div class="kpi-main-value">{int(scaled_closures):,}</div>
                <div class="kpi-per-member">({success_rate:.1f}% success rate)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="kpi-card-container">
                <div class="kpi-label">ROI Ratio</div>
                <div class="kpi-main-value">{roi_ratio:.2f}x</div>
                <div class="kpi-per-member">(Constant across plan sizes)</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Row 2
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.markdown(f"""
            <div class="kpi-card-container">
                <div class="kpi-label">Revenue Impact</div>
                <div class="kpi-main-value">${scaled_revenue:,.0f}</div>
                <div class="kpi-per-member">(${per_member_revenue:.2f} per member)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class="kpi-card-container">
                <div class="kpi-label">Net Benefit</div>
                <div class="kpi-main-value">${scaled_net_benefit:,.0f}</div>
                <div class="kpi-per-member">(${per_member_net_benefit:.2f} per member)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown(f"""
            <div class="kpi-card-container">
                <div class="kpi-label">Avg Cost per Closure</div>
                <div class="kpi-main-value">${avg_cost_per_closure:.2f}</div>
                <div class="kpi-per-member">(Constant across plan sizes)</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # INDUSTRY BENCHMARK COMPARISON
        st.subheader("📊 Industry Benchmark Comparison")
        
        benchmark_data = {
            'Metric': ['Gap Closure Rate', 'Cost Per Closure', 'ROI (First Quarter)', 'Digital Success Rate'],
            'Industry Average': ['28-35%', '$95-150', '1.0-1.2x', '25-30%'],
            'This Plan': ['42.4%', '$77.51', '1.29x', '46.4%'],
            'Performance': ['✅ Above', '✅ Below', '✅ Above', '✅ Above']
        }
        
        benchmark_df = pd.DataFrame(benchmark_data)
        
        st.dataframe(
            benchmark_df,
            use_container_width=True,
            hide_index=True,
            height=None  # Auto-height for mobile scrolling
        )
        
        st.divider()
        
        # SCALING COMPARISON TABLE
        st.subheader("📊 Impact at Key Plan Sizes")
        
        # Get selected size for dynamic highlighting
        selected_size = st.session_state.get('membership_size', 10000)
        selected_size_int = int(selected_size)
        
        # Calculate values for each plan size based on baseline
        plan_sizes_list = []
        for plan_size in [10000, 25000, 50000, 100000]:
            plan_scale = plan_size / BASELINE_MEMBERS
            plan_investment = baseline_investment * plan_scale
            plan_revenue = baseline_revenue * plan_scale
            plan_net_benefit = baseline_net_benefit * plan_scale
            
            # Format values
            if plan_investment >= 1000000:
                inv_str = f"${plan_investment/1000000:.2f}M"
            else:
                inv_rounded = round(plan_investment / 1000)
                inv_str = f"${inv_rounded:.0f}K"
            
            if plan_revenue >= 1000000:
                rev_str = f"${plan_revenue/1000000:.2f}M"
            else:
                rev_rounded = round(plan_revenue / 1000)
                rev_str = f"${rev_rounded:.0f}K"
            
            if plan_net_benefit >= 1000000:
                net_str = f"${plan_net_benefit/1000000:.2f}M"
            else:
                net_rounded = round(plan_net_benefit / 1000)
                net_str = f"${net_rounded:.0f}K"
            
            plan_sizes_list.append({
                'Plan Size': f"{plan_size//1000}K",
                'Investment': inv_str,
                'Revenue': rev_str,
                'Net Benefit': net_str,
                'ROI': f"{roi_ratio:.2f}x"
            })
        
        plan_sizes_df = pd.DataFrame(plan_sizes_list)
        
        # Highlight the selected row based on membership slider
        selected_row_idx = {10000: 0, 25000: 1, 50000: 2, 100000: 3}.get(selected_size_int, 0)
        
        def highlight_selected_row(row):
            if row.name == selected_row_idx:
                return ['background-color: #d4edda; font-weight: bold'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            plan_sizes_df.style.apply(highlight_selected_row, axis=1),
            use_container_width=True,
            hide_index=True,
            height=None  # Auto-height for mobile scrolling
        )
        
        # Note about selected plan
        standard_sizes = [10000, 25000, 50000, 100000]
        if selected_size_int in standard_sizes:
            st.success(f"✅ **Currently selected:** {selected_size:,} member plan (highlighted in green above)")
        else:
            st.info(f"ℹ️ **Currently selected:** {selected_size:,} member plan")
        
        st.divider()
        
        # STORYTELLING CONTEXT
        st.divider()
        st.subheader("💡 Why This Matters")
        
        if membership_size == 10000:
            st.success("""
            **Small Plans (10K members):** ✓ **Proves ROI before scaling** - This baseline case study demonstrates 
            measurable results at manageable scale, providing confidence to expand or replicate strategies.
            """)
        elif membership_size <= 25000:
            st.info("""
            **Mid-Size Plans (25K members):** ✓ **Your typical turnaround scenario** - Many regional plans operate 
            at this scale where proven strategies can drive significant impact with moderate investment.
            """)
        else:
            st.warning("""
            **Large/Enterprise Plans (50K+ members):** ✓ **Enterprise-scale impact projection** - These projections 
            show the potential impact when strategies proven at smaller scale are adapted for larger operations.
            """)
        
        st.divider()
        
        # NAVIGATION CALLOUT
        st.markdown("""
        ---
        
        ### 🚀 Q4 2024 Turnaround Results
        
        **👉 Explore detailed analysis using the sidebar navigation**
        
        • **ROI Analysis:** Investment efficiency and proof of concept at 10K scale, ready to expand
        
        • **Intervention Performance:** Breakthrough insights - Low-touch digital outperforms traditional, scalable strategy for plans of any size
        
        • **Budget Management:** Fiscal discipline during turnaround, budget model adaptable to plan size
        
        • **Cost Efficiency:** Cost-effective strategies identified, replicable across larger member populations
        
        All charts and tables automatically scale to your selected plan size
        """)
        
except Exception as e:
    st.error(f"❌ Error loading portfolio summary: {e}")
    st.info("Please check your database connection and ensure Phase 3 data is loaded.")

# Footer
st.divider()
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p><strong>HEDIS Star Rating Portfolio Optimizer</strong> | Case Study: Regional MA Plan Turnaround</p>
    <p>Built with Streamlit, Plotly, and PostgreSQL</p>
    <p>Data Source: Phase 3 ROI Analysis - Q4 2024 | Baseline: {plan_context['total_members']:,} members ({plan_context['plan_name']})</p>
    <p>Star Rating: {plan_context['star_rating_2024']:.1f} → Projected {plan_context['star_rating_projected_2025']:.1f} | At Risk: ${plan_context['bonus_revenue_at_risk']:,.0f}</p>
</div>
""", unsafe_allow_html=True)

