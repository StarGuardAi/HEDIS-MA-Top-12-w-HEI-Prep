"""
CBP (Controlling High Blood Pressure) Measure Dashboard Page

Tier 1, Triple-Weighted Measure
Star Rating Value: $360K-$615K per 0.1 improvement
HEDIS Specification: MY2025 Volume 2

This is one of the highest-value measures in the cardiovascular portfolio.

Author: Robert Reichert
Date: October 26, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def create_cbp_dashboard():
    """Create comprehensive CBP measure dashboard."""
    
    # Header
    st.title("🫀 CBP: Controlling High Blood Pressure")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tier", "1", help="Highest priority tier")
    
    with col2:
        st.metric("Weight", "3x", help="Triple-weighted measure")
    
    with col3:
        st.metric("Star Value", "$360K-$615K", help="Value per 0.1 improvement")
    
    with col4:
        st.metric("Status", "✅ Production", help="Fully implemented")
    
    st.markdown("---")
    
    # Measure Definition
    with st.expander("📋 Measure Definition & Specifications", expanded=False):
        st.markdown("""
        ### HEDIS Specification: MY2025 Volume 2
        
        **Description:**  
        The percentage of members 18-85 years of age who had a diagnosis of hypertension (HTN)
        and whose blood pressure (BP) was adequately controlled during the measurement year
        based on the following criteria:
        
        **Control Target:** <140/90 mmHg
        
        **Eligible Population:**
        - Age 18-85 as of December 31 of the measurement year
        - Diagnosis of hypertension (essential hypertension or secondary hypertension)
        - Continuous enrollment during measurement year
        
        **Exclusions:**
        - Members in hospice
        - Members with ESRD or dialysis
        - Members with kidney transplant
        - Pregnancy during measurement year
        - Members 66+ with frailty and advanced illness
        
        **Clinical Rationale:**
        - Hypertension affects 1 in 3 American adults
        - Leading risk factor for heart disease, stroke, kidney disease
        - Blood pressure control reduces cardiovascular events by 20-30%
        - Annual monitoring and treatment adherence are key to control
        
        **Data Sources:** Claims + Medical Records (BP readings)
        
        **Star Rating Impact:** Triple-weighted measure (3x standard weight)
        
        **Recent Changes:** Control threshold remains <140/90 (NOT 130/80 from ACC/AHA guidelines)
        """)
    
    st.markdown("---")
    
    # Current Performance
    st.markdown("## 📈 Current Performance")
    
    # Simulated performance data
    control_rate = np.random.uniform(0.62, 0.72)
    eligible_members = np.random.randint(15000, 25000)  # Larger population (HTN more common)
    
    controlled_members = int(eligible_members * control_rate)
    has_bp_reading = int(eligible_members * 0.92)  # Most have BP readings
    no_bp_reading = eligible_members - has_bp_reading
    uncontrolled_members = has_bp_reading - controlled_members
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Eligible Members",
            f"{eligible_members:,}",
            help="Members 18-85 with hypertension diagnosis"
        )
        
        st.metric(
            "Members with BP Reading",
            f"{has_bp_reading:,}",
            f"{has_bp_reading/eligible_members*100:.1f}%",
            help="Members with BP reading in measurement year"
        )
    
    with col2:
        # Benchmark comparison
        benchmark = 68.0  # Industry average
        delta = (control_rate * 100) - benchmark
        
        st.metric(
            "BP Control Rate (<140/90)",
            f"{control_rate*100:.1f}%",
            f"{delta:+.1f}% vs benchmark",
            help="Percentage with BP <140/90 mmHg"
        )
        
        st.metric(
            "Controlled Members",
            f"{controlled_members:,}",
            help="Members with BP <140/90"
        )
    
    with col3:
        st.metric(
            "Uncontrolled Members",
            f"{uncontrolled_members:,}",
            f"{uncontrolled_members/eligible_members*100:.1f}%",
            help="Members with BP ≥140/90"
        )
        
        potential_revenue = max(0, 75 - control_rate*100) * 52500
        st.metric(
            "Gap to 75% Target",
            f"{max(0, 75 - control_rate*100):.1f}%",
            help="Points needed for top-tier performance"
        )
    
    # Performance gauge
    st.markdown("### BP Control Rate vs Benchmarks")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=control_rate * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "BP Control Rate (%)", 'font': {'size': 20}},
        delta={'reference': 68, 'suffix': '% (National Average)'},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 55], 'color': "lightgray"},
                {'range': [55, 65], 'color': "#ffdddd"},
                {'range': [65, 72], 'color': "#ffffdd"},
                {'range': [72, 100], 'color': "#ddffdd"}
            ],
            'threshold': {
                'line': {'color': "green", 'width': 4},
                'thickness': 0.75,
                'value': 75
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Interpretation
    if control_rate >= 0.72:
        st.success(f"""
        ✅ **Excellent Performance!**
        
        Your BP control rate of **{control_rate*100:.1f}%** exceeds industry benchmarks,
        placing you in the top tier for Medicare Advantage plans.
        """)
    elif control_rate >= 0.65:
        st.info(f"""
        ℹ️ **Good Performance - Room for Improvement**
        
        Your BP control rate of **{control_rate*100:.1f}%** is near the national average.
        Focus on medication adherence (PDC-RASA alignment) for improvement.
        """)
    else:
        st.warning(f"""
        ⚠️ **Below Average - Action Needed**
        
        Your BP control rate of **{control_rate*100:.1f}%** is below industry standards.
        Implement hypertension management programs and medication optimization.
        """)
    
    st.markdown("---")
    
    # Performance Trends
    st.markdown("## 📊 Performance Trends")
    
    # Simulated historical data
    months = pd.date_range(start='2024-01-01', end='2025-10-01', freq='M')
    trend_data = []
    
    base_rate = control_rate
    
    for i, month in enumerate(months):
        rate = base_rate + np.random.uniform(-0.03, 0.03) + (i * 0.0008)
        
        trend_data.append({
            'Month': month,
            'Control Rate (%)': rate * 100,
            'Uncontrolled (%)': (1 - rate) * 100
        })
    
    trend_df = pd.DataFrame(trend_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend_df['Month'],
        y=trend_df['Control Rate (%)'],
        name='BP Controlled (<140/90)',
        line=dict(color='green', width=3),
        mode='lines+markers',
        fill='tozeroy',
        fillcolor='rgba(0,255,0,0.1)'
    ))
    
    fig.add_hline(y=68, line_dash="dash", line_color="gray", annotation_text="National Average")
    fig.add_hline(y=75, line_dash="dash", line_color="green", annotation_text="Target (75%)")
    
    fig.update_layout(
        title="CBP Performance Trends (Last 22 Months)",
        xaxis_title="Month",
        yaxis_title="Percentage (%)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Gap Analysis by BP Range
    st.markdown("## 🎯 Gap Analysis by Blood Pressure Range")
    
    st.markdown("""
    Understanding the distribution of BP readings helps target interventions effectively.
    Members close to control (<150/95) are **quick wins** vs those far from control.
    """)
    
    # BP range breakdown
    bp_data = pd.DataFrame({
        'BP Range': [
            'Controlled (<140/90) ✅',
            'Near Control (140-149/90-94) ⚠️',
            'Stage 2 HTN (150-179/95-109) ⚠️',
            'Severe HTN (≥180/110) 🚨',
            'No BP Reading ⚠️'
        ],
        'Members': [
            controlled_members,
            int(uncontrolled_members * 0.45),  # Near control - quick wins
            int(uncontrolled_members * 0.40),  # Stage 2
            int(uncontrolled_members * 0.15),  # Severe
            no_bp_reading
        ],
        'Priority': ['LOW', 'HIGH', 'MEDIUM', 'URGENT', 'MEDIUM'],
        'Intervention': [
            'Maintain compliance',
            'Medication adjustment (QUICK WIN)',
            'Intensive management + PDC-RASA',
            'Urgent care referral',
            'Schedule BP check immediately'
        ]
    })
    
    bp_data['Percentage'] = bp_data['Members'] / eligible_members * 100
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Member Distribution by BP Range")
        
        fig = px.bar(
            bp_data,
            x='BP Range',
            y='Members',
            color='Priority',
            color_discrete_map={'URGENT': '#990000', 'HIGH': '#ff4444', 'MEDIUM': '#ffaa00', 'LOW': '#44ff44'},
            title='Members by Blood Pressure Control Status',
            text='Members'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_xaxis(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Priority Segments")
        
        quick_win_count = bp_data[bp_data['BP Range'].str.contains('Near Control')]['Members'].values[0]
        
        st.error(f"""
        **URGENT Priority**
        
        {bp_data[bp_data['Priority'] == 'URGENT']['Members'].values[0]:,} members
        Severe HTN (≥180/110)
        
        → Immediate intervention
        """)
        
        st.metric(
            "HIGH Priority (Quick Win)",
            f"{quick_win_count:,}",
            f"{quick_win_count/eligible_members*100:.1f}%",
            help="Near control - medication adjustment"
        )
        
        st.metric(
            "MEDIUM Priority",
            f"{bp_data[bp_data['Priority'] == 'MEDIUM']['Members'].sum():,}",
            help="Stage 2 HTN + No BP reading"
        )
    
    # Detailed BP breakdown
    st.markdown("### Detailed BP Status Analysis")
    st.dataframe(
        bp_data.style.background_gradient(subset=['Members'], cmap='Reds'),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Interventions
    st.markdown("## 💡 Recommended Interventions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### For Near Control Members (HIGH Priority - Quick Win)")
        st.error(f"""
        **Target:** {quick_win_count:,} members (BP 140-149/90-94)
        
        **Interventions:**
        1. 💊 **Medication Optimization**
           - Titrate current medication
           - Add second agent if on monotherapy
           - Switch to combo pill for adherence
           - Link to PDC-RASA (hypertension meds)
        
        2. 🩺 **Provider Engagement**
           - Alert PCP to near-control status
           - Standing orders for med adjustment
           - Pharmacy consult for optimization
        
        3. 📱 **Self-Monitoring**
           - Home BP monitor distribution
           - Text reminders for daily BP check
           - Telehealth BP monitoring programs
        
        4. 🧂 **Lifestyle Support**
           - DASH diet education
           - Sodium reduction counseling
           - Exercise program enrollment
        
        **Expected Impact:** 60-80% move to controlled
        **Financial Value:** ${int(quick_win_count * 0.70 * 45):,.0f}
        
        ⭐ **QUICK WIN:** Already engaged, just need optimization
        """)
    
    with col2:
        st.markdown("### For Uncontrolled/Severe HTN (URGENT/MEDIUM Priority)")
        st.warning(f"""
        **Target:** {bp_data[bp_data['Priority'].isin(['URGENT', 'MEDIUM'])]['Members'].sum():,} members
        
        **Interventions:**
        1. 🚨 **Severe HTN Protocol** (≥180/110)
           - Immediate PCP/urgent care referral
           - Nurse follow-up within 48 hours
           - Medication initiation/adjustment
           - Weekly BP monitoring until controlled
        
        2. 👨‍⚕️ **Intensive Care Management** (Stage 2)
           - Monthly nurse case management
           - Medication adherence tracking (PDC-RASA)
           - Quarterly provider visits
           - Home health referrals if appropriate
        
        3. 💰 **Financial Barriers**
           - Copay assistance programs
           - Generic medication alternatives
           - Medication samples if needed
           - Patient assistance programs
        
        4. 📚 **Education & Self-Management**
           - Hypertension education classes
           - Cardiovascular risk assessment
           - Complication prevention counseling
        
        **Expected Impact:** 40-50% move to controlled
        **Financial Value:** ${int(bp_data[bp_data['Priority'].isin(['URGENT', 'MEDIUM'])]['Members'].sum() * 0.45 * 45):,.0f}
        """)
    
    st.markdown("---")
    
    # Integration with PDC-RASA
    st.markdown("## 🔗 Integration with PDC-RASA (Hypertension Medication Adherence)")
    
    st.info("""
    **Critical Insight:** CBP performance is **highly correlated** with PDC-RASA (medication adherence).
    Members non-adherent to hypertension medications cannot achieve BP control.
    
    **Coordinated Strategy = Maximum Impact**
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### CBP + PDC-RASA Correlation")
        
        # Simulated correlation data
        adherence_groups = ['<40% PDC', '40-59% PDC', '60-79% PDC', '≥80% PDC']
        bp_control_by_adherence = [25, 45, 65, 78]  # BP control rates by adherence
        
        corr_data = pd.DataFrame({
            'PDC-RASA Level': adherence_groups,
            'BP Control Rate (%)': bp_control_by_adherence
        })
        
        fig = px.bar(
            corr_data,
            x='PDC-RASA Level',
            y='BP Control Rate (%)',
            title='BP Control Rate by Medication Adherence',
            color='BP Control Rate (%)',
            color_continuous_scale='Greens'
        )
        fig.add_hline(y=68, line_dash="dash", line_color="gray", annotation_text="Average CBP")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Coordinated Intervention Benefits")
        
        st.success("""
        **Members with PDC-RASA <80%:**
        - 2-3x less likely to achieve BP control
        - Higher hospitalization risk
        - Increased cardiovascular events
        
        **Intervention Strategy:**
        1. Identify CBP uncontrolled members
        2. Check PDC-RASA status
        3. If PDC <80%, prioritize adherence
        4. Use combo pills to improve adherence
        5. Address financial barriers
        
        **Expected Improvement:**
        - CBP: +8-12 percentage points
        - PDC-RASA: +10-15 percentage points
        - Combined value: $500K-$800K
        """)
        
        st.metric(
            "Members Needing Both Interventions",
            f"{int(uncontrolled_members * 0.60):,}",
            help="Uncontrolled BP + PDC <80%"
        )
    
    st.markdown("---")
    
    # Financial Impact
    st.markdown("## 💰 Financial Impact Model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Improvement Scenarios")
        
        improvement_points = st.slider(
            "BP Control Rate Improvement (percentage points)",
            min_value=0.0,
            max_value=12.0,
            value=5.0,
            step=0.5,
            help="Expected improvement from interventions"
        )
        
        new_control_rate = min(control_rate + (improvement_points / 100), 0.95)
        
        st.metric("Current Control Rate", f"{control_rate*100:.1f}%")
        st.metric("Projected Control Rate", f"{new_control_rate*100:.1f}%", f"+{improvement_points:.1f}%")
        
        # Improvement sources
        st.markdown("#### Improvement Breakdown")
        quick_win_contrib = min(improvement_points * 0.50, 6.0)
        medication_contrib = min(improvement_points * 0.30, 4.0)
        lifestyle_contrib = min(improvement_points * 0.20, 2.0)
        
        st.write(f"- Near control (quick wins): +{quick_win_contrib:.1f}%")
        st.write(f"- Medication adherence: +{medication_contrib:.1f}%")
        st.write(f"- Lifestyle interventions: +{lifestyle_contrib:.1f}%")
    
    with col2:
        st.markdown("### Financial Impact")
        
        # Triple-weighted value
        value_per_point = 52500
        total_value = improvement_points * value_per_point
        
        # Intervention costs
        med_optimization_cost = quick_win_count * 35
        intensive_mgmt_cost = int(uncontrolled_members * 0.55) * 60
        bp_monitors_cost = int(eligible_members * 0.30) * 25
        
        total_cost = med_optimization_cost + intensive_mgmt_cost + bp_monitors_cost
        net_value = total_value - total_cost
        roi = (net_value / total_cost * 100) if total_cost > 0 else 0
        
        st.metric("Gross Star Rating Value", f"${total_value:,.0f}")
        st.metric("Medication Optimization", f"${med_optimization_cost:,.0f}")
        st.metric("Intensive Management", f"${intensive_mgmt_cost:,.0f}")
        st.metric("BP Monitors", f"${bp_monitors_cost:,.0f}")
        st.metric("Total Intervention Cost", f"${total_cost:,.0f}")
        st.metric("Net Value", f"${net_value:,.0f}", f"ROI: {roi:.0f}%")
    
    if net_value > 0:
        st.success(f"""
        ✅ **Excellent ROI!**
        
        Investing ${total_cost:,.0f} to improve CBP by {improvement_points:.1f} percentage points
        generates **${total_value:,.0f}** in Star Rating value (triple-weighted),
        resulting in **${net_value:,.0f} net benefit** ({roi:.0f}% ROI).
        
        **Coordinated CBP + PDC-RASA approach recommended for maximum impact.**
        """)
    
    st.markdown("---")
    
    # Clinical Impact
    st.markdown("## 🫀 Clinical Impact: Preventing Cardiovascular Events")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Cardiovascular Risk by BP Control")
        
        risk_data = pd.DataFrame({
            'BP Status': ['Controlled (<140/90)', 'Uncontrolled (≥140/90)'],
            'MI Risk': [5, 12],
            'Stroke Risk': [3, 8],
            'Heart Failure Risk': [4, 10],
            'CKD Progression Risk': [6, 15]
        })
        
        risk_melted = risk_data.melt(id_vars=['BP Status'], var_name='Event Type', value_name='Annual Risk (%)')
        
        fig = px.bar(
            risk_melted,
            x='Event Type',
            y='Annual Risk (%)',
            color='BP Status',
            barmode='group',
            title='Annual Cardiovascular Event Risk by BP Control Status'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Events Prevented by BP Control")
        
        events_prevented = {
            'MI (Heart Attack)': int(uncontrolled_members * 0.07 * improvement_points/100),
            'Stroke': int(uncontrolled_members * 0.05 * improvement_points/100),
            'Heart Failure': int(uncontrolled_members * 0.06 * improvement_points/100),
            'CKD Progression': int(uncontrolled_members * 0.09 * improvement_points/100)
        }
        
        for event, count in events_prevented.items():
            st.metric(event, f"{count} prevented annually")
        
        total_prevented = sum(events_prevented.values())
        cost_per_event = 75000  # Average cost per CV event
        clinical_value = total_prevented * cost_per_event
        
        st.metric(
            "Total Clinical Value",
            f"${clinical_value:,.0f}",
            help="Cost savings from prevented events"
        )
    
    st.info(f"""
    **Population Health Impact:**
    
    Improving BP control by {improvement_points:.1f} percentage points in {uncontrolled_members:,} 
    uncontrolled members prevents approximately **{total_prevented} cardiovascular events** annually,
    generating **${clinical_value:,.0f}** in medical cost savings (beyond Star Rating value).
    
    **Total Value = Star Rating (${total_value:,.0f}) + Clinical Savings (${clinical_value:,.0f}) 
    = ${total_value + clinical_value:,.0f}**
    """)
    
    st.markdown("---")
    
    # Implementation Timeline
    st.markdown("## 📅 Implementation Timeline")
    
    timeline = pd.DataFrame({
        'Phase': ['Segmentation', 'Quick Win Launch', 'PDC-RASA Integration', 'Intensive Management', 'Scale & Monitor'],
        'Duration': ['Week 1', 'Weeks 2-4', 'Weeks 3-6', 'Weeks 5-12', 'Ongoing'],
        'Activities': [
            'Stratify members by BP range, identify quick wins',
            'Launch med optimization for near-control members',
            'Coordinate with PDC-RASA interventions',
            'Deploy intensive management for Stage 2 HTN',
            'Track progress weekly, adjust tactics monthly'
        ],
        'Target': [
            'All members categorized by priority',
            '70% of near-control achieve control',
            'PDC-RASA +10 points, CBP +5 points',
            '45% of Stage 2 achieve control',
            'Sustain 75%+ control rate'
        ]
    })
    
    st.table(timeline)
    
    st.markdown("---")
    
    # Key Takeaways
    st.markdown("## 🎯 Key Takeaways")
    
    st.info(f"""
    **Current Performance:**
    - BP Control Rate: **{control_rate*100:.1f}%** (Goal: 75%+)
    - Gap to Goal: **{max(0, 75 - control_rate*100):.1f} percentage points**
    - Industry Benchmark: **68%** (your position: {"ABOVE" if control_rate >= 0.68 else "BELOW"} average)
    
    **Quick Win Opportunity:**
    - **Near Control Members:** {quick_win_count:,} members (BP 140-149/90-94)
    - **Simple intervention:** Medication titration/optimization
    - **Expected conversion:** 60-80% to controlled status
    - **Value:** ${int(quick_win_count * 0.70 * 45):,.0f}
    
    **CBP + PDC-RASA Integration:**
    - Members with PDC <80% are **2-3x less likely** to achieve BP control
    - Coordinated intervention: CBP +8-12%, PDC-RASA +10-15%
    - Combined value: $500K-$800K
    - Target: {int(uncontrolled_members * 0.60):,} members needing both
    
    **Financial Impact:**
    - **Star Rating Value:** $360K-$615K per 1% improvement (triple-weighted)
    - **Total Opportunity:** ${(improvement_points if 'improvement_points' in locals() else 5.0) * 52500:,.0f} with {improvement_points if 'improvement_points' in locals() else 5.0}% improvement
    - **Clinical Savings:** ${clinical_value if 'clinical_value' in locals() else 500000:,.0f} from prevented CV events
    - **Total Value:** ${(total_value if 'total_value' in locals() else 262500) + (clinical_value if 'clinical_value' in locals() else 500000):,.0f}
    - **ROI:** {roi if 'roi' in locals() else 250:.0f}% on intervention investment
    
    **Priority Actions:**
    1. **URGENT:** Immediate intervention for severe HTN (≥180/110) members
    2. **HIGH:** Launch medication optimization for near-control members (quick win)
    3. Integrate with PDC-RASA (medication adherence) interventions
    4. Deploy home BP monitoring program (30% of members)
    5. Track BP control rates weekly by segment
    
    **Clinical Impact:**
    - Prevent ~{total_prevented if 'total_prevented' in locals() else 150} cardiovascular events annually
    - Reduce MI, stroke, heart failure, CKD progression risk
    - Improve quality of life and reduce healthcare costs
    
    **Timeline:** 2-week segmentation, 4-week quick win launch, 8-week scale-up, ongoing monitoring
    """)
    
    # Footer
    st.markdown("---")
    st.caption("""
    **CBP (Controlling High Blood Pressure)** | HEDIS MY2025 | Tier 1 Triple-Weighted ⭐⭐⭐  
    Last updated: {} | Model Version: v2.1 | Compliance: ✅
    """.format(datetime.now().strftime('%Y-%m-%d')))


# Run dashboard
if __name__ == "__main__":
    create_cbp_dashboard()

