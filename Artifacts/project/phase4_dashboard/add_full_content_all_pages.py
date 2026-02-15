"""
Add full content to all pages 7+ that are missing it
"""
import os
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Full content templates for each page
FULL_CONTENT = {
    '7_📊_What-If_Scenario_Modeler.py': '''
# Page content
st.markdown("### 📊 What-If Scenario Modeler")
st.markdown("Model different intervention strategies and their projected outcomes")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Scenario Modeling:** Test different investment strategies and see projected ROI.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("📊 Scenario Analysis")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Scenarios Modeled", "0")
with col2:
    st.metric("Best ROI Projection", "0x")
with col3:
    st.metric("Recommended Strategy", "N/A")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>📊 Scenario Modeling Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>💡 Investment Scenarios:</strong> Test different budget allocations across measures.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📊 ROI Projections:</strong> See projected returns for each scenario.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Optimization:</strong> Get AI-recommended optimal strategy.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Scenario modeling functionality coming soon**")
''',

    '8_🎓_AI_Capabilities_Demo.py': '''
# Page content
st.markdown("### 🎓 AI Capabilities Demo")
st.markdown("Demonstration of AI-powered HEDIS optimization capabilities")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **AI Demo:** Explore how AI can enhance your HEDIS performance.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("🤖 AI Capabilities")

st.markdown("""
#### Available AI Features:
- **Predictive Analytics:** Forecast gap closure rates
- **Recommendation Engine:** Suggest optimal intervention strategies  
- **Natural Language Query:** Ask questions about your data
- **Automated Insights:** Get AI-generated performance insights
- **HIPAA-Compliant:** All processing on-premises, zero PHI exposure
""")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>🔒 Secure AI Architecture</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>✅ On-Premises:</strong> All AI processing happens locally, no external API calls.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>🔐 HIPAA-Compliant:</strong> Zero PHI transmission, full audit trails.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ High Performance:</strong> 2.8-4.1x ROI demonstrated in production.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 AI capabilities demo coming soon**")
''',

    '9_🔔_Alert_Center.py': '''
# Page content
st.markdown("### 🔔 Alert Center")
st.markdown("Monitor critical alerts and notifications for your HEDIS portfolio")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Alerts:** Stay informed about important changes and opportunities.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("🔔 Active Alerts")

st.warning("⚠️ No active alerts at this time")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Alerts", "0")
with col2:
    st.metric("Resolved Today", "0")
with col3:
    st.metric("Critical Items", "0")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>🔔 Alert Types</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>📊 Performance Alerts:</strong> Notify when measures fall below targets.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>💰 Budget Alerts:</strong> Warn about cost overruns or opportunities.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Opportunity Alerts:</strong> Highlight high-ROI intervention opportunities.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Alert system coming soon**")
''',

    '10_📈_Historical_Tracking.py': '''
# Page content
st.markdown("### 📈 Historical Tracking")
st.markdown("Track HEDIS performance trends over time")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Historical Analysis:** View performance trends and patterns over time.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("📈 Historical Trends")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Historical Periods", "0")
with col2:
    st.metric("Trend Analysis", "N/A")
with col3:
    st.metric("Performance Change", "0%")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>📈 Tracking Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>📊 Trend Analysis:</strong> View performance changes over multiple periods.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📈 Comparative Views:</strong> Compare current vs historical performance.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Forecasting:</strong> Predict future performance based on trends.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Historical tracking functionality coming soon**")
''',

    '11_💰_ROI_Calculator.py': '''
# Page content
st.markdown("### 💰 ROI Calculator")
st.markdown("Calculate projected ROI for different intervention strategies")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **ROI Calculator:** Estimate returns for various investment scenarios.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("💰 ROI Calculations")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Scenarios Calculated", "0")
with col2:
    st.metric("Best ROI", "0x")
with col3:
    st.metric("Recommended Investment", "$0")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>💰 Calculator Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>💡 Investment Scenarios:</strong> Test different budget allocations.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📊 ROI Projections:</strong> See expected returns for each scenario.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Optimization:</strong> Find the optimal investment mix.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 ROI calculator functionality coming soon**")
''',

    '13_📋_Measure_Analysis.py': '''
# Page content
st.markdown("### 📋 Measure Analysis")
st.markdown("Detailed analysis of individual HEDIS measures")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Measure Analysis:** Deep dive into performance metrics for each measure.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("📋 Measure Performance")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Measures Analyzed", "12")
with col2:
    st.metric("Top Performer", "BPD")
with col3:
    st.metric("Improvement Needed", "CBP")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>📋 Analysis Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>📊 Performance Metrics:</strong> ROI, cost per closure, success rates.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📈 Trend Analysis:</strong> Track performance over time.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Recommendations:</strong> Get AI-suggested improvements.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Detailed measure analysis coming soon**")
''',

    '14_⭐_Star_Rating_Simulator.py': '''
# Page content
st.markdown("### ⭐ Star Rating Simulator")
st.markdown("Simulate impact of HEDIS improvements on Star Ratings")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Star Rating Simulator:** Project how interventions affect your Star Rating.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("⭐ Star Rating Projections")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Rating", "3.5")
with col2:
    st.metric("Projected Rating", "4.0")
with col3:
    st.metric("Rating Change", "+0.5")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>⭐ Simulation Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>📊 Impact Modeling:</strong> See how measure improvements affect ratings.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📈 Scenario Planning:</strong> Test different improvement scenarios.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Optimization:</strong> Find the path to highest rating.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Star rating simulator coming soon**")
''',

    '15_🔄_Gap_Closure_Workflow.py': '''
# Page content
st.markdown("### 🔄 Gap Closure Workflow")
st.markdown("Manage and track gap closure workflows")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Workflow Management:** Track progress through gap closure processes.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("🔄 Active Workflows")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Workflows", "0")
with col2:
    st.metric("Completed Today", "0")
with col3:
    st.metric("Pending Actions", "0")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>🔄 Workflow Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>📊 Progress Tracking:</strong> Monitor workflow completion status.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📈 Task Management:</strong> Assign and track intervention tasks.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Automation:</strong> Automated workflow triggers and notifications.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Workflow management coming soon**")
''',

    '16_🤖_ML_Gap_Closure_Predictions.py': '''
# Page content
st.markdown("### 🤖 ML Gap Closure Predictions")
st.markdown("Machine learning predictions for gap closure success")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **ML Predictions:** AI-powered forecasts for gap closure outcomes.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("🤖 ML Predictions")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Predictions Generated", "0")
with col2:
    st.metric("Accuracy", "0%")
with col3:
    st.metric("High Confidence", "0")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>🤖 ML Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>📊 Success Prediction:</strong> Forecast likelihood of gap closure.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📈 Risk Assessment:</strong> Identify high-risk gaps early.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Optimization:</strong> Recommend best intervention strategies.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 ML prediction functionality coming soon**")
''',

    '17_📊_Competitive_Benchmarking.py': '''
# Page content
st.markdown("### 📊 Competitive Benchmarking")
st.markdown("Compare your performance against industry benchmarks")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Benchmarking:** See how you stack up against industry standards.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("📊 Benchmark Comparison")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Benchmarks Used", "0")
with col2:
    st.metric("Above Average", "0")
with col3:
    st.metric("Below Average", "0")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>📊 Benchmarking Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>📊 Industry Comparison:</strong> Compare against peer organizations.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📈 Performance Gaps:</strong> Identify areas needing improvement.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Best Practices:</strong> Learn from top performers.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Benchmarking functionality coming soon**")
''',

    '18_📋_Compliance_Reporting.py': '''
# Page content
st.markdown("### 📋 Compliance Reporting")
st.markdown("Generate compliance reports for HEDIS measures")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Compliance Reports:** Create detailed reports for regulatory requirements.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("📋 Compliance Status")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Reports Generated", "0")
with col2:
    st.metric("Compliance Rate", "0%")
with col3:
    st.metric("Pending Reviews", "0")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>📋 Reporting Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>📊 Automated Reports:</strong> Generate compliance reports automatically.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📈 Audit Trails:</strong> Full tracking of all compliance activities.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Export Options:</strong> PDF, Excel, and CSV export formats.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Compliance reporting coming soon**")
''',

    '18_🤖_Secure_AI_Chatbot.py': '''
# Page content
st.markdown("### 🤖 Secure AI Chatbot")
st.markdown("Ask questions about your HEDIS data using secure AI")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Secure AI:** HIPAA-compliant AI assistant for your HEDIS questions.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("🤖 AI Chat Interface")

st.markdown("""
#### Chat Interface Features:
- **Natural Language:** Ask questions in plain English
- **Data Insights:** Get AI-powered analysis of your data
- **HIPAA-Compliant:** All processing on-premises, zero PHI exposure
- **Secure:** No external API calls, full audit trails
- **Intelligent:** Context-aware responses based on your portfolio
""")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>🔒 Security Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>✅ On-Premises:</strong> All AI processing happens locally.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>🔐 Zero PHI Exposure:</strong> No data leaves your infrastructure.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Full Compliance:</strong> HIPAA, SOC 2, HITRUST ready.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Secure AI chatbot coming soon**")
''',

    '19_⚖️_Health_Equity_Index.py': '''
# Page content
st.markdown("### ⚖️ Health Equity Index")
st.markdown("Track and analyze health equity metrics across your population")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Health Equity:** Monitor equity metrics and identify disparities.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("⚖️ Equity Metrics")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Equity Score", "0")
with col2:
    st.metric("Disparities Identified", "0")
with col3:
    st.metric("Improvement Areas", "0")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>⚖️ Equity Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>📊 Disparity Analysis:</strong> Identify gaps across demographic groups.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📈 Trend Tracking:</strong> Monitor equity improvements over time.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Interventions:</strong> Target interventions to reduce disparities.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Health equity index coming soon**")
''',

    'Performance_Dashboard.py': '''
# Page content
st.markdown("### ⚡ Performance Dashboard")
st.markdown("Comprehensive overview of HEDIS portfolio performance")

# Display date range info
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.info("💡 **Performance Overview:** Get a high-level view of your portfolio performance.")
with col2:
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

st.header("⚡ Portfolio Performance")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Measures", "12")
with col2:
    st.metric("Avg ROI", "1.25x")
with col3:
    st.metric("Success Rate", "42%")
with col4:
    st.metric("Net Benefit", "$0")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>⚡ Dashboard Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>📊 Real-Time Metrics:</strong> Live performance indicators.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📈 Visualizations:</strong> Charts and graphs for quick insights.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Quick Actions:</strong> Access key functions from one place.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Performance dashboard enhancements coming soon**")
'''
}

# Footer template
FOOTER = '''
# Footer
st.markdown("---")
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
""", unsafe_allow_html=True)
'''

def add_full_content(file_path):
    """Add full content to a page"""
    try:
        page_name = Path(file_path).name
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get page-specific content
        page_content = FULL_CONTENT.get(page_name)
        if not page_content:
            return False, "No content template"
        
        # Find where to replace (after date range)
        date_range_marker = '# Get date range from sidebar'
        date_range_pos = content.find(date_range_marker)
        
        if date_range_pos == -1:
            return False, "Date range marker not found"
        
        # Find end of date range section
        lines = content.split('\n')
        date_range_line = -1
        for i, line in enumerate(lines):
            if date_range_marker in line:
                date_range_line = i
                break
        
        if date_range_line == -1:
            return False, "Could not find date range line"
        
        # Find where date range section ends
        insert_line = date_range_line + 1
        while insert_line < len(lines):
            if lines[insert_line].strip() and not lines[insert_line].strip().startswith('#'):
                if 'start_date' in lines[insert_line] or 'end_date' in lines[insert_line]:
                    insert_line += 1
                    continue
                break
            insert_line += 1
        
        # Check if footer exists
        has_footer = '# Footer' in content or 'HEDIS Portfolio Optimizer | StarGuard AI' in content[-1000:]
        
        # Check if already has good content (not placeholder)
        if 'st.header(' in content[content.find(date_range_marker):] and '🚧' not in content[content.find(date_range_marker):content.find(date_range_marker)+500]:
            return False, "Already has content"
        
        # Replace everything from insert_line to footer (or end)
        footer_start = len(lines)
        for i in range(insert_line, len(lines)):
            if '# Footer' in lines[i] or ('HEDIS Portfolio Optimizer' in lines[i] and i > insert_line + 10):
                footer_start = i
                break
        
        # Reconstruct with new content
        new_lines = (
            lines[:insert_line] +
            [page_content] +
            (lines[footer_start:] if has_footer else [FOOTER] + lines[footer_start:])
        )
        
        new_content = '\n'.join(new_lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Content added"
            
    except Exception as e:
        return None, str(e)

def main():
    """Process all target pages"""
    pages_dir = Path(__file__).parent / 'pages'
    
    target_pages = [
        '7_📊_What-If_Scenario_Modeler.py',
        '8_🎓_AI_Capabilities_Demo.py',
        '9_🔔_Alert_Center.py',
        '10_📈_Historical_Tracking.py',
        '11_💰_ROI_Calculator.py',
        '13_📋_Measure_Analysis.py',
        '14_⭐_Star_Rating_Simulator.py',
        '15_🔄_Gap_Closure_Workflow.py',
        '16_🤖_ML_Gap_Closure_Predictions.py',
        '17_📊_Competitive_Benchmarking.py',
        '18_📋_Compliance_Reporting.py',
        '18_🤖_Secure_AI_Chatbot.py',
        '19_⚖️_Health_Equity_Index.py',
        'Performance_Dashboard.py'
    ]
    
    print("Adding full content to all pages 7+...")
    print("=" * 60)
    
    stats = {'added': 0, 'skipped': 0, 'errors': 0}
    
    for page_name in target_pages:
        page_file = pages_dir / page_name
        if not page_file.exists():
            print(f"[SKIP] {page_name} - File not found")
            stats['skipped'] += 1
            continue
        
        result, info = add_full_content(page_file)
        
        if result is True:
            print(f"[ADDED] {page_name}")
            stats['added'] += 1
        elif result is False:
            print(f"[SKIP] {page_name} - {info}")
            stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  Added: {stats['added']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")

if __name__ == '__main__':
    main()


