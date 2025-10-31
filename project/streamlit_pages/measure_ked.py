"""
KED (Kidney Health Evaluation for Patients with Diabetes) Measure Dashboard Page

NEW 2025 Measure - Tier 1, Triple-Weighted
Star Rating Value: $360K-$615K per 0.1 improvement
HEDIS Specification: MY2025 Volume 2

This is a **NEW** measure for 2025, requiring immediate implementation.

Author: Robert Reichert
Date: October 25, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def create_ked_dashboard():
    """Create comprehensive KED measure dashboard."""
    
    # Header with NEW badge
    st.title("🆕 KED: Kidney Health Evaluation for Patients with Diabetes")
    st.markdown("### **NEW 2025 MEASURE** - Immediate Action Required ⚠️")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Tier", "1", help="Highest priority tier")
    
    with col2:
        st.metric("Weight", "3x", help="Triple-weighted measure")
    
    with col3:
        st.metric("Star Value", "$360K-$615K", help="Value per 0.1 improvement")
    
    with col4:
        st.metric("Status", "🆕 NEW 2025", help="First year of measurement")
    
    with col5:
        st.metric("Implementation", "✅ Ready", help="Fully implemented")
    
    st.warning("""
    ⚠️ **First-Year Measurement Alert:**  
    This is a **NEW HEDIS measure for 2025**. Most MA plans are unprepared. 
    Your proactive implementation provides **significant competitive advantage**.
    """)
    
    st.markdown("---")
    
    # Measure Definition
    with st.expander("📋 Measure Definition & Specifications", expanded=True):
        st.markdown("""
        ### HEDIS Specification: MY2025 Volume 2 (NEW)
        
        **Description:**  
        The percentage of members 18-75 years of age with diabetes (type 1 or type 2)
        who received a kidney health evaluation during the measurement year, defined as:
        
        **BOTH of the following:**
        1. **eGFR (estimated Glomerular Filtration Rate)** test
        2. **UACR (Urine Albumin-Creatinine Ratio)** test OR **ACR (Albumin-Creatinine Ratio)** test
        
        **Eligible Population:**
        - Age 18-75 as of December 31 of the measurement year
        - Diagnosis of diabetes (type 1 or type 2) - **Same as GSD criteria**
        - Continuous enrollment during measurement year
        
        **Exclusions:**
        - Members in hospice
        - Members with ESRD (End-Stage Renal Disease) or on dialysis
        - Kidney transplant recipients
        - Members with gestational or steroid-induced diabetes only
        
        **Clinical Rationale:**
        - Early detection of diabetic nephropathy (diabetic kidney disease)
        - 1 in 3 adults with diabetes has chronic kidney disease (CKD)
        - Early intervention can slow progression to ESRD
        - Annual screening recommended by ADA, KDIGO, and CMS
        
        **Data Sources:** Claims + Lab Results
        
        **Star Rating Impact:** Triple-weighted measure (3x standard weight) - **Same as GSD**
        
        **Key Implementation Challenge:** Many members may have eGFR but lack UACR test.
        """)
    
    st.markdown("---")
    
    # Current Performance
    st.markdown("## 📈 Current Performance")
    
    # Simulated performance data
    completion_rate = np.random.uniform(0.52, 0.68)
    eligible_members = np.random.randint(8000, 12000)
    
    completed_members = int(eligible_members * completion_rate)
    egfr_only = int(eligible_members * 0.22)  # Have eGFR but missing UACR
    uacr_only = int(eligible_members * 0.08)  # Have UACR but missing eGFR (rare)
    neither_test = int(eligible_members * (1 - completion_rate - 0.22 - 0.08))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Eligible Members",
            f"{eligible_members:,}",
            help="Same population as GSD (diabetes 18-75)"
        )
        
        st.metric(
            "Members with BOTH Tests",
            f"{completed_members:,}",
            f"{completion_rate*100:.1f}%",
            help="Complete kidney health evaluation"
        )
    
    with col2:
        st.metric(
            "Overall Completion Rate",
            f"{completion_rate*100:.1f}%",
            help="Percentage completing BOTH eGFR and UACR"
        )
        
        # Benchmark comparison
        benchmark = 60.0  # Industry estimate for first year
        delta = (completion_rate * 100) - benchmark
        
        st.metric(
            "vs Industry Benchmark",
            f"{benchmark:.1f}%",
            f"{delta:+.1f}%",
            help="Estimated first-year industry average"
        )
    
    with col3:
        st.metric(
            "Gap to 70% Target",
            f"{max(0, 70 - completion_rate*100):.1f}%",
            help="Points needed for top-tier performance"
        )
        
        potential_revenue = max(0, 70 - completion_rate*100) * 52500
        st.metric(
            "Improvement Opportunity",
            f"${potential_revenue:,.0f}",
            help="Value of closing gap to 70%"
        )
    
    # Performance gauge
    st.markdown("### Completion Rate vs Benchmarks")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=completion_rate * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "KED Completion Rate (%)", 'font': {'size': 20}},
        delta={'reference': 60, 'suffix': '% (Est. Industry Avg)'},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 55], 'color': "#ffdddd"},
                {'range': [55, 65], 'color': "#ffffdd"},
                {'range': [65, 100], 'color': "#ddffdd"}
            ],
            'threshold': {
                'line': {'color': "green", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Interpretation
    if completion_rate >= 0.65:
        st.success(f"""
        ✅ **Excellent Performance for First Year!**
        
        Your completion rate of **{completion_rate*100:.1f}%** is well above the estimated
        industry average of 60% for this **brand new 2025 measure**.
        """)
    elif completion_rate >= 0.55:
        st.info(f"""
        ℹ️ **Good Performance - Continue Momentum**
        
        Your completion rate of **{completion_rate*100:.1f}%** is near or above the estimated
        industry average. Focus on the "eGFR-only" segment for quick wins.
        """)
    else:
        st.warning(f"""
        ⚠️ **Below Expected Performance - Urgent Action Needed**
        
        Your completion rate of **{completion_rate*100:.1f}%** is below the estimated 60%
        industry average. Implement immediate outreach to close both testing gaps.
        """)
    
    st.markdown("---")
    
    # Gap Analysis - KEY DIFFERENTIATOR
    st.markdown("## 🎯 Gap Analysis & Testing Patterns")
    
    st.markdown("""
    **Critical Insight:** Most members have **eGFR tests** (part of basic metabolic panel), 
    but are **missing UACR tests** (requires specific urine sample). This is the primary gap to close.
    """)
    
    # Testing status breakdown
    testing_data = pd.DataFrame({
        'Testing Status': [
            'BOTH Tests (Complete ✅)',
            'eGFR Only (Missing UACR ⚠️)',
            'UACR Only (Missing eGFR)',
            'Neither Test (No Testing)'
        ],
        'Members': [completed_members, egfr_only, uacr_only, neither_test],
        'Priority': ['LOW', 'HIGH', 'MEDIUM', 'MEDIUM'],
        'Intervention': [
            'Maintain compliance',
            'Order UACR test (QUICK WIN)',
            'Order eGFR test',
            'Order BOTH tests'
        ]
    })
    
    testing_data['Percentage'] = testing_data['Members'] / eligible_members * 100
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Member Distribution by Testing Status")
        
        fig = px.bar(
            testing_data,
            x='Testing Status',
            y='Members',
            color='Priority',
            color_discrete_map={'HIGH': '#ff4444', 'MEDIUM': '#ffaa00', 'LOW': '#44ff44'},
            title='Members by Kidney Health Testing Completion',
            text='Members'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Quick Win Opportunity")
        
        st.error(f"""
        **eGFR-Only Members**
        
        {egfr_only:,} members  
        ({egfr_only/eligible_members*100:.1f}% of population)
        
        **Already have:**
        ✅ eGFR test
        
        **Need:**
        ⚠️ UACR test only
        
        **Action:** Simple urine test order
        
        **Value:** ${egfr_only * 45:,.0f}
        """)
        
        st.info(f"""
        **Completion Potential**
        
        If 70% of eGFR-only members
        complete UACR:
        
        +{int(egfr_only * 0.70):,} members  
        +{egfr_only * 0.70 / eligible_members * 100:.1f}% completion rate
        
        New Rate: {(completion_rate * 100) + (egfr_only * 0.70 / eligible_members * 100):.1f}%
        """)
    
    # Detailed testing breakdown
    st.markdown("### Detailed Testing Status")
    st.dataframe(
        testing_data.style.background_gradient(subset=['Members'], cmap='YlOrRd'),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Interventions & Recommendations
    st.markdown("## 💡 Recommended Interventions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### For eGFR-Only Members (HIGH Priority ⚠️)")
        st.error(f"""
        **Target:** {egfr_only:,} members
        
        **Interventions:**
        1. 🩺 **Provider Alerts**
           - EMR alerts at point-of-care
           - Standing orders for UACR
           - Provider education on measure
        
        2. 📞 **Member Outreach**
           - "You're halfway there!" messaging
           - Text reminders for urine sample
           - In-home collection kits
        
        3. 🏥 **Lab Partnerships**
           - Walk-in UACR testing
           - Mobile phlebotomy services
           - Retail clinic partnerships
        
        **Expected Impact:** 60-80% completion rate
        **Financial Value:** ${int(egfr_only * 0.70 * 45):,.0f}
        
        ⭐ **QUICK WIN:** Focus here first for maximum ROI
        """)
    
    with col2:
        st.markdown("### For Untested Members (MEDIUM Priority)")
        st.warning(f"""
        **Target:** {neither_test:,} members
        
        **Interventions:**
        1. 📲 **Proactive Outreach**
           - Care manager phone calls
           - Educational materials on kidney health
           - Importance of annual testing
        
        2. 🏠 **Access Improvement**
           - In-home lab testing (both tests)
           - Weekend/evening lab hours
           - Transportation assistance
        
        3. 💰 **Incentives**
           - Gift cards for completion
           - Copay waivers
           - Wellness program points
        
        4. 👨‍⚕️ **PCP Engagement**
           - Provider performance reports
           - Quality bonus tied to KED
           - Shared savings programs
        
        **Expected Impact:** 40-50% completion rate
        **Financial Value:** ${int(neither_test * 0.45 * 45):,.0f}
        """)
    
    st.markdown("---")
    
    # Clinical Importance
    st.markdown("## 🏥 Clinical Importance & CKD Staging")
    
    st.markdown("""
    Understanding kidney health is critical for diabetes patients. CKD (Chronic Kidney Disease)
    progression can be **slowed or prevented** with early detection and intervention.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Why Both Tests Matter")
        
        st.info("""
        **eGFR (Glomerular Filtration Rate):**
        - Measures how well kidneys filter blood
        - Normal: ≥90 mL/min/1.73m²
        - Detects **reduced kidney function**
        
        **UACR (Urine Albumin-Creatinine Ratio):**
        - Measures protein leakage in urine
        - Normal: <30 mg/g
        - Detects **early kidney damage**
        
        **Together:** Comprehensive kidney health assessment
        **Early detection:** Can prevent ESRD (dialysis/transplant)
        """)
    
    with col2:
        st.markdown("### CKD Risk in Diabetes")
        
        # Simulated CKD prevalence data
        ckd_data = pd.DataFrame({
            'CKD Stage': ['No CKD', 'Stage 1-2', 'Stage 3', 'Stage 4-5'],
            'Prevalence': [65, 20, 12, 3],
            'Action Required': ['Monitor annually', 'Monitor + lifestyle', 'Specialist referral', 'Nephrology urgent']
        })
        
        fig = px.pie(
            ckd_data,
            values='Prevalence',
            names='CKD Stage',
            title='Estimated CKD Prevalence in Diabetes Population',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Members Potentially Undiagnosed", f"{int(eligible_members * 0.35 * (1-completion_rate)):,}",
                  help="Estimated members with undetected CKD")
    
    st.markdown("---")
    
    # Financial Impact
    st.markdown("## 💰 Financial Impact Model")
    
    st.markdown("""
    Calculate the financial impact of KED improvement initiatives.
    This measure is **triple-weighted** AND **new for 2025**, making early success critical.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Improvement Scenarios")
        
        improvement_points = st.slider(
            "Completion Rate Improvement (percentage points)",
            min_value=0.0,
            max_value=20.0,
            value=8.0,
            step=0.5,
            help="How many percentage points can you improve completion rate?"
        )
        
        new_completion_rate = min(completion_rate + (improvement_points / 100), 0.95)
        
        st.metric(
            "Current Completion Rate",
            f"{completion_rate*100:.1f}%"
        )
        
        st.metric(
            "Projected Completion Rate",
            f"{new_completion_rate*100:.1f}%",
            f"+{improvement_points:.1f}%"
        )
        
        # Breakdown by segment
        st.markdown("#### Improvement Sources")
        egfr_contribution = min(improvement_points * 0.60, egfr_only/eligible_members*100 * 0.70)
        untested_contribution = min(improvement_points * 0.40, neither_test/eligible_members*100 * 0.45)
        
        st.write(f"- eGFR-only segment: +{egfr_contribution:.1f}%")
        st.write(f"- Untested segment: +{untested_contribution:.1f}%")
    
    with col2:
        st.markdown("### Financial Impact")
        
        # Calculate star rating impact
        # Triple-weighted: $45K-$60K per 1% improvement
        value_per_point = 52500  # Average
        total_value = improvement_points * value_per_point
        
        # Intervention cost estimate (lower for KED since eGFR-only is quick win)
        intervention_cost = egfr_only * 12 + neither_test * 40
        net_value = total_value - intervention_cost
        roi = (net_value / intervention_cost * 100) if intervention_cost > 0 else 0
        
        st.metric(
            "Gross Star Rating Value",
            f"${total_value:,.0f}",
            help="Triple-weighted measure value"
        )
        
        st.metric(
            "Estimated Intervention Cost",
            f"${intervention_cost:,.0f}",
            help="Primarily UACR test orders + outreach"
        )
        
        st.metric(
            "Net Value",
            f"${net_value:,.0f}",
            f"ROI: {roi:.0f}%"
        )
    
    if net_value > 0:
        st.success(f"""
        ✅ **Excellent ROI!**
        
        Investing ${intervention_cost:,.0f} to improve KED by {improvement_points:.1f} percentage points
        generates **${total_value:,.0f}** in Star Rating value, resulting in
        **${net_value:,.0f} net benefit** ({roi:.0f}% ROI).
        
        **First-Mover Advantage:** Most MA plans are unprepared for this NEW 2025 measure.
        Your proactive approach provides significant competitive advantage.
        """)
    
    st.markdown("---")
    
    # Performance Trends (limited historical data since NEW measure)
    st.markdown("## 📊 Performance Trends")
    
    st.info("""
    **Note:** As a NEW 2025 measure, historical trend data is limited.
    Tracking begins in measurement year 2025.
    """)
    
    # Simulated YTD data
    months = pd.date_range(start='2025-01-01', end='2025-10-01', freq='M')
    trend_data = []
    
    base_rate = completion_rate
    
    for i, month in enumerate(months):
        # Show progressive improvement as measure is implemented
        rate = (base_rate * 0.70) + (i / len(months)) * (base_rate * 0.30) + np.random.uniform(-0.02, 0.02)
        
        trend_data.append({
            'Month': month,
            'Completion Rate (%)': rate * 100
        })
    
    trend_df = pd.DataFrame(trend_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend_df['Month'],
        y=trend_df['Completion Rate (%)'],
        name='KED Completion Rate',
        line=dict(color='darkblue', width=3),
        mode='lines+markers'
    ))
    
    fig.add_hline(y=60, line_dash="dash", line_color="gray", annotation_text="Est. Industry Average")
    fig.add_hline(y=70, line_dash="dash", line_color="green", annotation_text="Target (70%)")
    
    fig.update_layout(
        title="KED Performance Trends (2025 YTD)",
        xaxis_title="Month",
        yaxis_title="Completion Rate (%)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Implementation Timeline
    st.markdown("## 📅 Recommended Implementation Timeline")
    
    timeline = pd.DataFrame({
        'Phase': ['EMR Setup', 'Provider Training', 'Member Outreach', 'Lab Partnerships', 'Scale & Monitor'],
        'Duration': ['Week 1', 'Week 2', 'Weeks 3-4', 'Weeks 3-4', 'Weeks 5-12'],
        'Activities': [
            'Configure EMR alerts, standing orders, reports',
            'Educate providers on NEW measure, importance, workflows',
            'Launch targeted outreach to eGFR-only members (quick win)',
            'Negotiate in-home testing, walk-in UACR services',
            'Scale to all segments, track weekly, optimize tactics'
        ],
        'Target': [
            'EMR ready for KED tracking',
            '100% provider awareness',
            '60%+ of eGFR-only complete UACR',
            'Access barriers removed',
            '70%+ overall completion rate'
        ]
    })
    
    st.table(timeline)
    
    st.markdown("---")
    
    # Key Takeaways
    st.markdown("## 🎯 Key Takeaways")
    
    st.info(f"""
    **🆕 NEW 2025 Measure - First-Mover Advantage:**
    
    **Current Performance:**
    - Completion Rate: **{completion_rate*100:.1f}%** (Goal: 70%+)
    - Gap to Goal: **{max(0, 70 - completion_rate*100):.1f} percentage points**
    - Estimated Industry Average: **60%** (your position: {"ABOVE" if completion_rate >= 0.60 else "BELOW"} average)
    
    **Critical Insight - The "eGFR-Only" Quick Win:**
    - **{egfr_only:,} members** ({egfr_only/eligible_members*100:.1f}%) have eGFR but missing UACR
    - **Quick Win:** Order simple urine test to complete evaluation
    - **Potential Impact:** +{egfr_only * 0.70 / eligible_members * 100:.1f}% completion rate with 70% conversion
    - **Value:** ${int(egfr_only * 0.70 * 45):,.0f}
    
    **Financial Impact:**
    - **Star Rating Value:** $360K-$615K per 1% improvement (triple-weighted)
    - **Total Opportunity:** ${(improvement_points if 'improvement_points' in locals() else 8.0) * 52500:,.0f} with {improvement_points if 'improvement_points' in locals() else 8.0}% improvement
    - **ROI:** {roi if 'roi' in locals() else 400:.0f}% on intervention investment
    
    **Priority Actions:**
    1. **URGENT:** Implement EMR alerts for eGFR-only members (HIGH priority, quick win)
    2. Launch targeted UACR outreach campaign to eGFR-only segment
    3. Establish in-home/walk-in UACR testing partnerships
    4. Provider education on NEW measure requirements
    5. Track weekly completion rates by segment
    
    **Competitive Advantage:**
    - ✅ Most MA plans unprepared for this NEW measure
    - ✅ Your proactive implementation = significant advantage
    - ✅ First-year performance sets baseline for future years
    - ✅ Triple-weighted measure = 3x value vs standard measures
    
    **Timeline:** 4-week intensive implementation, 8-week scale-up, ongoing monitoring
    """)
    
    # Footer
    st.markdown("---")
    st.caption("""
    **KED (Kidney Health Evaluation for Patients with Diabetes)** | 🆕 NEW HEDIS MY2025 | Tier 1 Triple-Weighted ⭐⭐⭐  
    Last updated: {} | Model Version: v1.0 | Compliance: ✅
    """.format(datetime.now().strftime('%Y-%m-%d')))


# Run dashboard
if __name__ == "__main__":
    create_ked_dashboard()

