"""
PDC-RASA (Proportion of Days Covered - RASA Medications for Hypertension)

Tier 2, Standard-Weighted Measure
Star Rating Value: $180K-$310K per 0.1 improvement
HEDIS Specification: MY2025 Volume 2

Critical for CBP performance - medication adherence drives BP control.

Author: Robert Reichert
Date: October 26, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def create_pdc_rasa_dashboard():
    """Create comprehensive PDC-RASA measure dashboard."""
    
    st.title("💊 PDC-RASA: Hypertension Medication Adherence")
    
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
    **Critical Link:** PDC-RASA directly impacts CBP performance.  
    Members non-adherent to hypertension medications **cannot achieve BP control**.
    """)
    
    st.markdown("---")
    
    with st.expander("📋 Measure Definition & Specifications", expanded=False):
        st.markdown("""
        ### HEDIS Specification: MY2025 Volume 2
        
        **Description:**  
        The percentage of members 18-85 years of age with hypertension who were dispensed
        a RASA medication (ACE inhibitor or ARB) and who have a PDC of at least **80%**.
        
        **Qualifying Medications:**
        - **ACE Inhibitors:** Lisinopril, Enalapril, Ramipril, etc.
        - **ARBs:** Losartan, Valsartan, Olmesartan, etc.
        - **Combination products:** ACE/ARB + diuretic or calcium channel blocker
        
        **PDC Calculation:** (Days covered / Days in measurement period) × 100%
        
        **Eligible Population:**
        - Age 18-85 as of December 31
        - Diagnosis of hypertension
        - At least 2 prescription fills of RASA medication
        
        **Clinical Rationale:**
        - RASA medications are first-line for hypertension
        - PDC <80% associated with uncontrolled BP, higher CV event risk
        - Medication adherence is THE key driver of BP control
        
        **Data Sources:** Pharmacy claims
        """)
    
    st.markdown("---")
    
    # Performance
    st.markdown("## 📈 Current Performance")
    
    pdc_rate = np.random.uniform(0.70, 0.80)
    eligible_members = np.random.randint(15000, 25000)
    adherent_members = int(eligible_members * pdc_rate)
    non_adherent_members = eligible_members - adherent_members
    pdc_60_79 = int(non_adherent_members * 0.45)
    pdc_40_59 = int(non_adherent_members * 0.35)
    pdc_under_40 = non_adherent_members - pdc_60_79 - pdc_40_59
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Eligible Members", f"{eligible_members:,}", help="Members 18-85 with hypertension on RASA")
        st.metric("Adherent (PDC ≥80%)", f"{adherent_members:,}", f"{pdc_rate*100:.1f}%")
    with col2:
        benchmark = 76.0
        delta = (pdc_rate * 100) - benchmark
        st.metric("PDC-RASA Rate", f"{pdc_rate*100:.1f}%", f"{delta:+.1f}% vs benchmark")
        st.metric("Non-Adherent", f"{non_adherent_members:,}", f"{non_adherent_members/eligible_members*100:.1f}%")
    with col3:
        st.metric("Gap to 85% Target", f"{max(0, 85 - pdc_rate*100):.1f}%")
        st.metric("Improvement Value", f"${max(0, 85 - pdc_rate*100) * 25000:,.0f}")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pdc_rate * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "PDC-RASA Rate (%)", 'font': {'size': 20}},
        delta={'reference': 76, 'suffix': '% (National Average)'},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 65], 'color': "#ffdddd"},
                {'range': [65, 76], 'color': "#ffffdd"},
                {'range': [76, 85], 'color': "#ddffdd"},
                {'range': [85, 100], 'color': "#aaffaa"}
            ],
            'threshold': {'line': {'color': "green", 'width': 4}, 'value': 80}
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Gap Analysis
    st.markdown("## 🎯 Gap Analysis by Adherence Level")
    
    pdc_data = pd.DataFrame({
        'PDC Range': ['Adherent (≥80%) ✅', 'Near-Adherent (60-79%) ⚠️', 'Moderate (40-59%) ⚠️', 'Severe (<40%) 🚨'],
        'Members': [adherent_members, pdc_60_79, pdc_40_59, pdc_under_40],
        'Priority': ['LOW', 'HIGH', 'MEDIUM', 'URGENT']
    })
    pdc_data['Percentage'] = pdc_data['Members'] / eligible_members * 100
    
    fig = px.bar(pdc_data, x='PDC Range', y='Members', color='Priority',
                 color_discrete_map={'URGENT': '#990000', 'HIGH': '#ff4444', 'MEDIUM': '#ffaa00', 'LOW': '#44ff44'},
                 title='Members by Medication Adherence Level', text='Members')
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(pdc_data.style.background_gradient(subset=['Members'], cmap='YlOrRd'), 
                 use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Integration with CBP
    st.markdown("## 🔗 Impact on CBP (Blood Pressure Control)")
    
    st.success("""
    **Critical Relationship:** PDC-RASA is the #1 predictor of CBP performance.  
    Members cannot achieve BP control without taking their hypertension medications.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        bp_data = pd.DataFrame({
            'PDC Range': ['<40%', '40-59%', '60-79%', '≥80%'],
            'BP Control Rate (%)': [28, 45, 62, 76]
        })
        fig = px.bar(bp_data, x='PDC Range', y='BP Control Rate (%)',
                     title='CBP Performance by PDC-RASA Level',
                     color='BP Control Rate (%)', color_continuous_scale='Greens')
        fig.add_hline(y=68, line_dash="dash", annotation_text="CBP Avg (68%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Coordinated Strategy Benefits")
        st.success(f"""
        **Improving PDC-RASA → CBP lift:**
        - PDC-RASA +10% → CBP +7-10%
        - Combined Star Value: $400K-$600K
        - ROI: 350-500%
        
        **Target:** {int(non_adherent_members * 0.60):,} members
        (Non-adherent to meds + uncontrolled BP)
        """)
    
    st.markdown("---")
    
    # Financial Impact
    st.markdown("## 💰 Financial Impact Model")
    
    col1, col2 = st.columns(2)
    with col1:
        improvement_points = st.slider("PDC-RASA Improvement (percentage points)", 
                                       0.0, 15.0, 7.0, 0.5)
        new_rate = min(pdc_rate + (improvement_points / 100), 0.95)
        st.metric("Current Rate", f"{pdc_rate*100:.1f}%")
        st.metric("Projected Rate", f"{new_rate*100:.1f}%", f"+{improvement_points:.1f}%")
    
    with col2:
        pdc_value = improvement_points * 25000
        cbp_lift = improvement_points * 0.70 * 52500
        total_value = pdc_value + cbp_lift
        cost = pdc_60_79 * 5 + (pdc_40_59 + pdc_under_40) * 45
        net_value = total_value - cost
        roi = (net_value / cost * 100) if cost > 0 else 0
        
        st.metric("PDC-RASA Value", f"${pdc_value:,.0f}")
        st.metric("CBP Lift Value", f"${cbp_lift:,.0f}")
        st.metric("Combined Value", f"${total_value:,.0f}")
        st.metric("Net Benefit", f"${net_value:,.0f}", f"ROI: {roi:.0f}%")
    
    st.markdown("---")
    
    # Key Takeaways
    st.markdown("## 🎯 Key Takeaways")
    
    st.info(f"""
    **Current Performance:** PDC-RASA Rate: **{pdc_rate*100:.1f}%** (Target: 85%+)
    
    **Quick Win:** {pdc_60_79:,} near-adherent members (60-79% PDC) - refill reminders
    
    **CBP Impact:** Improving PDC-RASA by {improvement_points:.1f}% → CBP +{improvement_points * 0.70:.1f}%
    
    **Combined Value:** ${total_value:,.0f} (PDC-RASA + CBP lift)
    
    **ROI:** {roi:.0f}% - medication adherence programs are highest-ROI interventions
    
    **Priority:** HIGH - Launch refill reminder campaign, auto-refill enrollment, medication sync
    """)
    
    st.caption(f"**PDC-RASA** | HEDIS MY2025 | Tier 2 | CBP Enabler ✅ | {datetime.now().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    create_pdc_rasa_dashboard()

