"""
PDC-STA (Proportion of Days Covered - Statin Medications)

Tier 2, Standard-Weighted Measure
Star Rating Value: $180K-$310K per 0.1 improvement
HEDIS Specification: MY2025 Volume 2

Critical for SUPD and cardiovascular risk reduction.

Author: Robert Reichert
Date: October 26, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def create_pdc_sta_dashboard():
    """Create comprehensive PDC-STA measure dashboard."""
    
    st.title("💊 PDC-STA: Statin Medication Adherence")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tier", "2")
    with col2:
        st.metric("Weight", "1x")
    with col3:
        st.metric("Star Value", "$180K-$310K")
    with col4:
        st.metric("Status", "✅ Production")
    
    st.info("**Critical Link:** PDC-STA enables SUPD performance and reduces cardiovascular risk.")
    
    st.markdown("---")
    
    with st.expander("📋 Measure Definition", expanded=False):
        st.markdown("""
        ### HEDIS Specification: MY2025 Volume 2
        
        **Description:** Percentage of members 18-85 with cardiovascular disease or diabetes
        who were dispensed a statin medication and have PDC ≥80%.
        
        **Qualifying Medications:**
        - Atorvastatin (Lipitor), Simvastatin, Rosuvastatin (Crestor), Pravastatin, etc.
        - Combination products (e.g., statin + ezetimibe)
        
        **Eligible Population:**
        - Age 18-85
        - Cardiovascular disease OR diabetes diagnosis
        - At least 2 statin prescription fills
        
        **Clinical Rationale:**
        - Statins reduce LDL cholesterol, CV events, stroke risk
        - Adherence critical for benefit (effects reverse if stopped)
        """)
    
    st.markdown("---")
    
    st.markdown("## 📈 Current Performance")
    
    pdc_rate = np.random.uniform(0.72, 0.82)
    eligible_members = np.random.randint(18000, 28000)
    adherent_members = int(eligible_members * pdc_rate)
    non_adherent = eligible_members - adherent_members
    pdc_60_79 = int(non_adherent * 0.50)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Eligible Members", f"{eligible_members:,}")
        st.metric("Adherent (≥80%)", f"{adherent_members:,}", f"{pdc_rate*100:.1f}%")
    with col2:
        benchmark = 77.0
        delta = (pdc_rate * 100) - benchmark
        st.metric("PDC-STA Rate", f"{pdc_rate*100:.1f}%", f"{delta:+.1f}% vs benchmark")
    with col3:
        st.metric("Gap to 85%", f"{max(0, 85 - pdc_rate*100):.1f}%")
        st.metric("Value", f"${max(0, 85 - pdc_rate*100) * 25000:,.0f}")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta", value=pdc_rate * 100,
        title={'text': "PDC-STA Rate (%)"}, delta={'reference': 77},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "darkblue"},
               'steps': [{'range': [0, 70], 'color': "#ffdddd"}, 
                        {'range': [70, 80], 'color': "#ffffdd"},
                        {'range': [80, 100], 'color': "#ddffdd"}]}
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Gap Analysis")
    
    pdc_data = pd.DataFrame({
        'PDC Range': ['Adherent (≥80%)', 'Near (60-79%)', 'Low (<60%)'],
        'Members': [adherent_members, pdc_60_79, non_adherent - pdc_60_79],
        'Priority': ['LOW', 'HIGH', 'URGENT']
    })
    
    fig = px.bar(pdc_data, x='PDC Range', y='Members', color='Priority',
                 color_discrete_map={'URGENT': '#990000', 'HIGH': '#ff4444', 'LOW': '#44ff44'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 🔗 Impact on SUPD & Cardiovascular Health")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### SUPD Performance by PDC-STA")
        supd_data = pd.DataFrame({
            'PDC Range': ['<60%', '60-79%', '≥80%'],
            'SUPD Rate (%)': [35, 62, 88]
        })
        fig = px.bar(supd_data, x='PDC Range', y='SUPD Rate (%)', color='SUPD Rate (%)',
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.success("""
        **Coordinated PDC-STA + SUPD:**
        - PDC-STA +8% → SUPD +10-12%
        - Combined value: $400K-$500K
        - ROI: 400%+
        
        **Plus CV Risk Reduction:**
        - Fewer MI, stroke events
        - Clinical savings: $300K-$500K
        """)
    
    st.markdown("---")
    
    st.markdown("## 💰 Financial Impact")
    
    col1, col2 = st.columns(2)
    with col1:
        improvement = st.slider("PDC-STA Improvement (pp)", 0.0, 12.0, 6.0, 0.5)
        st.metric("Projected Rate", f"{min(pdc_rate*100 + improvement, 95):.1f}%", f"+{improvement:.1f}%")
    
    with col2:
        pdc_value = improvement * 25000
        supd_value = improvement * 0.75 * 25000
        total = pdc_value + supd_value
        cost = pdc_60_79 * 4 + (non_adherent - pdc_60_79) * 35
        net = total - cost
        roi = (net / cost * 100) if cost > 0 else 0
        
        st.metric("Combined Value", f"${total:,.0f}")
        st.metric("Net Benefit", f"${net:,.0f}", f"ROI: {roi:.0f}%")
    
    st.markdown("---")
    
    st.markdown("## 🎯 Key Takeaways")
    st.info(f"""
    **Rate:** {pdc_rate*100:.1f}% (Target: 85%+)  
    **Quick Win:** {pdc_60_79:,} near-adherent members - refill reminders  
    **SUPD Impact:** +{improvement * 0.75:.1f}% with PDC-STA improvement  
    **Value:** ${total:,.0f} combined (PDC-STA + SUPD lift)  
    **ROI:** {roi:.0f}%
    """)
    
    st.caption(f"**PDC-STA** | MY2025 | Tier 2 | SUPD Enabler | {datetime.now().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    create_pdc_sta_dashboard()

