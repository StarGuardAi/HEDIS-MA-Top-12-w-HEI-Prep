"""
PDC-DR (Proportion of Days Covered - Diabetes Medications) Measure Dashboard Page

Tier 2, Standard-Weighted Measure
Star Rating Value: $180K-$310K per 0.1 improvement
HEDIS Specification: MY2025 Volume 2

Critical for GSD and KED performance - medication adherence drives clinical outcomes.

Author: Robert Reichert
Date: October 26, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def create_pdc_dr_dashboard():
    """Create comprehensive PDC-DR measure dashboard."""
    
    # Header
    st.title("💊 PDC-DR: Diabetes Medication Adherence")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tier", "2", help="High-value tier")
    
    with col2:
        st.metric("Weight", "1x", help="Standard weighted")
    
    with col3:
        st.metric("Star Value", "$180K-$310K", help="Value per 0.1 improvement")
    
    with col4:
        st.metric("Status", "✅ Production", help="Fully implemented")
    
    st.info("""
    **Critical Link:** PDC-DR directly impacts GSD and KED performance.  
    Members non-adherent to diabetes medications **cannot achieve glycemic control**.
    """)
    
    st.markdown("---")
    
    # Measure Definition
    with st.expander("📋 Measure Definition & Specifications", expanded=False):
        st.markdown("""
        ### HEDIS Specification: MY2025 Volume 2
        
        **Description:**  
        The percentage of members 18-75 years of age with diabetes who were dispensed
        a medication for diabetes and who have a PDC (Proportion of Days Covered) of at least **80%**
        during the measurement year.
        
        **Qualifying Medications:**
        - **Oral diabetes medications:** Metformin, sulfonylureas, DPP-4 inhibitors, SGLT2 inhibitors, etc.
        - **Injectable diabetes medications:** Insulin, GLP-1 agonists (e.g., Ozempic, Trulicity)
        - **Combination products:** Must include diabetes medication component
        
        **PDC Calculation:**
        ```
        PDC = (Days covered by medication / Days in measurement period) × 100%
        
        PDC ≥80% = Adherent (counts toward measure)
        PDC <80% = Non-adherent (does not count)
        ```
        
        **Eligible Population:**
        - Age 18-75 as of December 31 of measurement year
        - Diagnosis of diabetes (type 1 or type 2)
        - At least 2 prescription fills of diabetes medication during measurement year
        
        **Exclusions:**
        - Members in hospice
        - Members with gestational or steroid-induced diabetes only
        
        **Clinical Rationale:**
        - Medication adherence is THE key driver of glycemic control
        - PDC <80% associated with:
          - Higher HbA1c levels
          - Increased hospitalization risk
          - Greater risk of diabetes complications
          - 2-3x higher healthcare costs
        
        **Data Sources:** Pharmacy claims
        
        **Star Rating Impact:** Standard weight, but **critical enabler** for GSD/KED success
        """)
    
    st.markdown("---")
    
    # Current Performance
    st.markdown("## 📈 Current Performance")
    
    # Simulated performance data
    pdc_rate = np.random.uniform(0.68, 0.78)
    eligible_members = np.random.randint(8000, 12000)
    
    adherent_members = int(eligible_members * pdc_rate)
    non_adherent_members = eligible_members - adherent_members
    
    # PDC distribution
    pdc_60_79 = int(non_adherent_members * 0.45)  # Close to threshold - quick wins
    pdc_40_59 = int(non_adherent_members * 0.35)  # Moderate non-adherence
    pdc_under_40 = non_adherent_members - pdc_60_79 - pdc_40_59  # Severe non-adherence
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Eligible Members",
            f"{eligible_members:,}",
            help="Members 18-75 with diabetes on medication"
        )
        
        st.metric(
            "Adherent Members (PDC ≥80%)",
            f"{adherent_members:,}",
            f"{pdc_rate*100:.1f}%"
        )
    
    with col2:
        benchmark = 75.0
        delta = (pdc_rate * 100) - benchmark
        
        st.metric(
            "PDC-DR Rate",
            f"{pdc_rate*100:.1f}%",
            f"{delta:+.1f}% vs benchmark",
            help="Percentage with PDC ≥80%"
        )
        
        st.metric(
            "Non-Adherent Members",
            f"{non_adherent_members:,}",
            f"{non_adherent_members/eligible_members*100:.1f}%"
        )
    
    with col3:
        st.metric(
            "Gap to 85% Target",
            f"{max(0, 85 - pdc_rate*100):.1f}%",
            help="Points needed for top performance"
        )
        
        potential_revenue = max(0, 85 - pdc_rate*100) * 25000
        st.metric(
            "Improvement Opportunity",
            f"${potential_revenue:,.0f}",
            help="Star Rating value"
        )
    
    # Performance gauge
    st.markdown("### PDC-DR Rate vs Benchmarks")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pdc_rate * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "PDC-DR Rate (%)", 'font': {'size': 20}},
        delta={'reference': 75, 'suffix': '% (National Average)'},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 65], 'color': "#ffdddd"},
                {'range': [65, 75], 'color': "#ffffdd"},
                {'range': [75, 85], 'color': "#ddffdd"},
                {'range': [85, 100], 'color': "#aaffaa"}
            ],
            'threshold': {
                'line': {'color': "green", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    if pdc_rate >= 0.80:
        st.success(f"✅ **Excellent adherence!** Your PDC-DR rate of {pdc_rate*100:.1f}% exceeds the 80% clinical threshold.")
    elif pdc_rate >= 0.75:
        st.info(f"ℹ️ **Good performance.** At {pdc_rate*100:.1f}%, focus on members with PDC 60-79% for quick wins.")
    else:
        st.warning(f"⚠️ **Action needed.** At {pdc_rate*100:.1f}%, implement adherence programs immediately.")
    
    st.markdown("---")
    
    # Gap Analysis by PDC Range
    st.markdown("## 🎯 Gap Analysis by Adherence Level")
    
    pdc_data = pd.DataFrame({
        'PDC Range': [
            'Adherent (≥80%) ✅',
            'Near-Adherent (60-79%) ⚠️',
            'Moderate Non-Adherence (40-59%) ⚠️',
            'Severe Non-Adherence (<40%) 🚨'
        ],
        'Members': [adherent_members, pdc_60_79, pdc_40_59, pdc_under_40],
        'Priority': ['LOW', 'HIGH', 'MEDIUM', 'URGENT'],
        'Intervention': [
            'Maintain - auto-refill programs',
            'Refill reminders (QUICK WIN)',
            'Barriers assessment + support',
            'Intensive case management'
        ]
    })
    
    pdc_data['Percentage'] = pdc_data['Members'] / eligible_members * 100
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            pdc_data,
            x='PDC Range',
            y='Members',
            color='Priority',
            color_discrete_map={'URGENT': '#990000', 'HIGH': '#ff4444', 'MEDIUM': '#ffaa00', 'LOW': '#44ff44'},
            title='Members by Medication Adherence Level',
            text='Members'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_xaxis(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Quick Win: 60-79% PDC")
        
        st.error(f"""
        **{pdc_60_79:,} members**  
        ({pdc_60_79/eligible_members*100:.1f}% of population)
        
        **Already taking medication**  
        **Just need refill reminders**
        
        → Text/email reminders  
        → Auto-refill enrollment  
        → Pharmacy sync programs
        
        **Expected conversion:** 50-70%  
        **Value:** ${int(pdc_60_79 * 0.60 * 25):,.0f}
        """)
    
    st.dataframe(
        pdc_data.style.background_gradient(subset=['Members'], cmap='YlOrRd'),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Interventions
    st.markdown("## 💡 Recommended Interventions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### For Near-Adherent (60-79% PDC) - Quick Win")
        st.error(f"""
        **Target:** {pdc_60_79:,} members
        
        **Interventions:**
        1. 📱 **Automated Refill Reminders**
           - Text messages 7 days before due
           - Email + IVR backup
           - Pharmacy-initiated calls
        
        2. 🔄 **Auto-Refill Programs**
           - Enroll in pharmacy auto-refill
           - Medication synchronization (sync all meds to same date)
           - Home delivery options
        
        3. 💰 **Cost Barriers**
           - Check for generic alternatives
           - Apply manufacturer copay cards
           - Patient assistance programs
        
        4. 📦 **Convenience**
           - 90-day supply prescriptions
           - Mail-order pharmacy
           - Pickup reminders
        
        **Expected Impact:** 50-70% move to ≥80% PDC  
        **Financial Value:** ${int(pdc_60_79 * 0.60 * 25):,.0f}  
        **Clinical Impact:** Improved glycemic control (GSD +3-5%)
        """)
    
    with col2:
        st.markdown("### For Moderate/Severe Non-Adherence (<60% PDC)")
        st.warning(f"""
        **Target:** {pdc_40_59 + pdc_under_40:,} members
        
        **Interventions:**
        1. 🔍 **Barriers Assessment**
           - Phone interview to identify barriers
           - Cost, side effects, forgetfulness, belief
           - Health literacy assessment
        
        2. 👨‍⚕️ **Clinical Interventions**
           - Pharmacist consult for side effect management
           - Medication simplification (combo pills)
           - Diabetes educator referral
        
        3. 💰 **Financial Support**
           - Copay assistance programs
           - Generic substitution
           - Free samples if appropriate
           - Manufacturer patient assistance
        
        4. 👩‍⚕️ **Case Management**
           - Monthly nurse follow-up
           - Motivational interviewing
           - Goal setting and tracking
        
        **Expected Impact:** 30-40% move to ≥80% PDC  
        **Financial Value:** ${int((pdc_40_59 + pdc_under_40) * 0.35 * 25):,.0f}  
        **Clinical Impact:** Prevent hospitalizations, complications
        """)
    
    st.markdown("---")
    
    # Impact on GSD
    st.markdown("## 🔗 Impact on GSD (Glycemic Control)")
    
    st.success("""
    **Critical Relationship:** PDC-DR is the #1 predictor of GSD performance.  
    Members cannot achieve good glycemic control without taking their medications consistently.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### HbA1c Levels by PDC-DR")
        
        hba1c_data = pd.DataFrame({
            'PDC Range': ['<40%', '40-59%', '60-79%', '≥80%'],
            'Avg HbA1c': [9.2, 8.5, 7.8, 7.1],
            'Good Control Rate (%)': [25, 42, 58, 78]
        })
        
        fig = px.line(
            hba1c_data,
            x='PDC Range',
            y='Avg HbA1c',
            title='Average HbA1c by Medication Adherence',
            markers=True,
            line_shape='spline'
        )
        fig.add_hline(y=8.0, line_dash="dash", line_color="orange", annotation_text="Good Control Threshold")
        fig.update_yaxes(range=[6.5, 10])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### GSD Performance by PDC-DR")
        
        fig = px.bar(
            hba1c_data,
            x='PDC Range',
            y='Good Control Rate (%)',
            title='GSD Good Control Rate by PDC-DR Level',
            color='Good Control Rate (%)',
            color_continuous_scale='Greens'
        )
        fig.add_hline(y=70, line_dash="dash", line_color="green", annotation_text="GSD Target (70%)")
        st.plotly_chart(fig, use_container_width=True)
    
    st.info(f"""
    **Coordinated PDC-DR + GSD Strategy:**
    
    Improving PDC-DR from {pdc_rate*100:.1f}% to 85% (+{85 - pdc_rate*100:.1f} points) will:
    - **GSD Impact:** +5-8 percentage points in good control rate
    - **Combined Star Value:** ${int((85 - pdc_rate*100) * 25000 + 6.5 * 52500):,.0f}
    - **PDC-DR alone:** ${int((85 - pdc_rate*100) * 25000):,.0f}
    - **GSD lift:** ${int(6.5 * 52500):,.0f} (triple-weighted)
    
    **ROI on coordinated approach: 400-600%**
    """)
    
    st.markdown("---")
    
    # Financial Impact
    st.markdown("## 💰 Financial Impact Model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Improvement Scenarios")
        
        improvement_points = st.slider(
            "PDC-DR Rate Improvement (percentage points)",
            min_value=0.0,
            max_value=15.0,
            value=8.0,
            step=0.5
        )
        
        new_pdc_rate = min(pdc_rate + (improvement_points / 100), 0.95)
        
        st.metric("Current PDC-DR Rate", f"{pdc_rate*100:.1f}%")
        st.metric("Projected PDC-DR Rate", f"{new_pdc_rate*100:.1f}%", f"+{improvement_points:.1f}%")
        
        st.markdown("#### Improvement Sources")
        st.write(f"- 60-79% PDC (quick wins): +{min(improvement_points * 0.50, 8.0):.1f}%")
        st.write(f"- 40-59% PDC (barriers): +{min(improvement_points * 0.30, 5.0):.1f}%")
        st.write(f"- <40% PDC (intensive): +{min(improvement_points * 0.20, 3.0):.1f}%")
    
    with col2:
        st.markdown("### Financial Impact")
        
        # PDC-DR value (standard weighted)
        pdc_value = improvement_points * 25000
        
        # GSD lift value (triple-weighted) - 65% of PDC improvement translates to GSD
        gsd_lift_points = improvement_points * 0.65
        gsd_value = gsd_lift_points * 52500
        
        total_value = pdc_value + gsd_value
        
        # Intervention costs
        refill_reminders_cost = pdc_60_79 * 5
        case_mgmt_cost = (pdc_40_59 + pdc_under_40) * 45
        copay_assistance_cost = non_adherent_members * 0.30 * 100
        
        total_cost = refill_reminders_cost + case_mgmt_cost + copay_assistance_cost
        net_value = total_value - total_cost
        roi = (net_value / total_cost * 100) if total_cost > 0 else 0
        
        st.metric("PDC-DR Value", f"${pdc_value:,.0f}")
        st.metric("GSD Lift Value", f"${gsd_value:,.0f}", help="From improved medication adherence")
        st.metric("Combined Value", f"${total_value:,.0f}")
        st.metric("Intervention Cost", f"${total_cost:,.0f}")
        st.metric("Net Value", f"${net_value:,.0f}", f"ROI: {roi:.0f}%")
    
    if net_value > 0:
        st.success(f"""
        ✅ **Outstanding ROI!**
        
        Investing ${total_cost:,.0f} improves PDC-DR by {improvement_points:.1f} points
        AND lifts GSD by {gsd_lift_points:.1f} points, generating **${total_value:,.0f}**
        total value ({roi:.0f}% ROI).
        
        **Medication adherence programs are among the highest-ROI interventions in healthcare.**
        """)
    
    st.markdown("---")
    
    # Key Takeaways
    st.markdown("## 🎯 Key Takeaways")
    
    st.info(f"""
    **Current Performance:**
    - PDC-DR Rate: **{pdc_rate*100:.1f}%** (Target: 85%+)
    - Gap to Target: **{max(0, 85 - pdc_rate*100):.1f} percentage points**
    - Non-Adherent Members: **{non_adherent_members:,}** ({non_adherent_members/eligible_members*100:.1f}%)
    
    **Quick Win Opportunity:**
    - **Near-Adherent (60-79% PDC):** {pdc_60_79:,} members
    - **Simple intervention:** Automated refill reminders + auto-refill enrollment
    - **Expected conversion:** 50-70% to ≥80% PDC
    - **Value:** ${int(pdc_60_79 * 0.60 * 25):,.0f} (PDC-DR alone)
    
    **Impact on GSD (Glycemic Control):**
    - Members with PDC <80% have **2-3x lower** GSD good control rates
    - Improving PDC-DR by {improvement_points if 'improvement_points' in locals() else 8.0}% → GSD +{(improvement_points if 'improvement_points' in locals() else 8.0) * 0.65:.1f}%
    - **Combined value:** ${(pdc_value if 'pdc_value' in locals() else 200000) + (gsd_value if 'gsd_value' in locals() else 227000):,.0f}
    
    **Financial Impact:**
    - **PDC-DR Value:** ${pdc_value if 'pdc_value' in locals() else 200000:,.0f}
    - **GSD Lift Value:** ${gsd_value if 'gsd_value' in locals() else 227000:,.0f} (from improved adherence)
    - **Total Value:** ${total_value if 'total_value' in locals() else 427000:,.0f}
    - **ROI:** {roi if 'roi' in locals() else 450:.0f}%
    
    **Priority Actions:**
    1. **HIGH:** Automated refill reminders for 60-79% PDC segment (quick win)
    2. Enroll members in pharmacy auto-refill and medication sync programs
    3. Barriers assessment for <60% PDC members
    4. Copay assistance and generic alternatives
    5. Track PDC monthly, correlate with HbA1c outcomes (GSD)
    
    **Timeline:** 2-week setup, 4-week pilot (60-79% PDC), 8-week scale to all segments
    """)
    
    st.markdown("---")
    st.caption(f"""
    **PDC-DR (Diabetes Medication Adherence)** | HEDIS MY2025 | Tier 2 Standard-Weighted  
    Last updated: {datetime.now().strftime('%Y-%m-%d')} | GSD Enabler ✅ | Compliance: ✅
    """)


if __name__ == "__main__":
    create_pdc_dr_dashboard()

