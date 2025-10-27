"""
BCS (Breast Cancer Screening)

Tier 2, Standard-Weighted Measure
Star Rating Value: $180K-$310K per 0.1 improvement

Author: Robert Reichert
Date: October 26, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def create_bcs_dashboard():
    """Create BCS measure dashboard."""
    
    st.title("🎗️ BCS: Breast Cancer Screening")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tier", "2")
    with col2:
        st.metric("Weight", "1x")
    with col3:
        st.metric("Star Value", "$180K-$310K")
    with col4:
        st.metric("Status", "✅ Production")
    
    st.markdown("---")
    
    with st.expander("📋 Measure Definition", expanded=False):
        st.markdown("""
        ### HEDIS Specification: MY2025 Volume 2
        
        **Description:** Percentage of women 50-74 years who had a mammogram
        to screen for breast cancer in the past 2 years.
        
        **Eligible Population:**
        - Women only
        - Age 50-74
        - Continuous enrollment
        
        **Lookback:** 2-year window (24 months)
        
        **Exclusions:**
        - Bilateral mastectomy
        - Hospice
        """)
    
    st.markdown("---")
    
    st.markdown("## 📈 Current Performance")
    
    screening_rate = np.random.uniform(0.68, 0.78)
    eligible = np.random.randint(6000, 10000)
    screened = int(eligible * screening_rate)
    not_screened = eligible - screened
    overdue = int(not_screened * 0.60)  # Overdue by >2 years
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Eligible Women", f"{eligible:,}")
        st.metric("Screened (2 years)", f"{screened:,}", f"{screening_rate*100:.1f}%")
    with col2:
        benchmark = 74.0
        st.metric("BCS Rate", f"{screening_rate*100:.1f}%", f"{(screening_rate*100 - benchmark):+.1f}%")
    with col3:
        st.metric("Gap to 80%", f"{max(0, 80 - screening_rate*100):.1f}%")
        st.metric("Value", f"${max(0, 80 - screening_rate*100) * 25000:,.0f}")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=screening_rate * 100,
        title={'text': "BCS Screening Rate (%)"},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "pink"},
               'steps': [{'range': [0, 70], 'color': "#ffdddd"},
                        {'range': [70, 80], 'color': "#ffffdd"},
                        {'range': [80, 100], 'color': "#ddffdd"}]}
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Gap Analysis")
    
    gap_data = pd.DataFrame({
        'Screening Status': ['Screened (past 2 yrs) ✅', 'Overdue (>2 yrs) ⚠️', 'Due Soon ⚠️'],
        'Members': [screened, overdue, not_screened - overdue],
        'Priority': ['LOW', 'HIGH', 'MEDIUM']
    })
    
    fig = px.bar(gap_data, x='Screening Status', y='Members', color='Priority',
                 color_discrete_map={'HIGH': '#ff4444', 'MEDIUM': '#ffaa00', 'LOW': '#44ff44'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 💡 Interventions & Financial Impact")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Priority Actions")
        st.error(f"""
        **Overdue Members: {overdue:,}**
        
        **Interventions:**
        - Proactive outreach (phone/text)
        - Mobile mammography units
        - Transportation assistance
        - Evening/weekend appointments
        - $0 copay screening
        
        **Expected:** 50-60% complete screening
        """)
    
    with col2:
        improvement = st.slider("BCS Improvement (pp)", 0.0, 10.0, 5.0, 0.5)
        value = improvement * 25000
        cost = overdue * 35 + (not_screened - overdue) * 15
        net = value - cost
        roi = (net / cost * 100) if cost > 0 else 0
        
        st.metric("Star Value", f"${value:,.0f}")
        st.metric("Net Benefit", f"${net:,.0f}", f"ROI: {roi:.0f}%")
    
    st.markdown("---")
    
    st.markdown("## 🎗️ Clinical Impact")
    
    st.success("""
    **Early Detection Saves Lives:**
    - Mammography reduces breast cancer mortality by 20-30%
    - Stage 1 detection: 99% 5-year survival
    - Stage 4 detection: 27% 5-year survival
    - Every 1,000 women screened → prevent 1-2 deaths over 10 years
    """)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Key Takeaways")
    st.info(f"""
    **Rate:** {screening_rate*100:.1f}% (Target: 80%+)  
    **Overdue:** {overdue:,} women >2 years since last screening  
    **Value:** ${value:,.0f} with {improvement:.1f}% improvement  
    **Strategy:** Mobile mammography + proactive outreach + access barriers removal  
    **Clinical Impact:** Early detection, lives saved
    """)
    
    st.caption(f"**BCS** | MY2025 | Tier 2 | {datetime.now().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    create_bcs_dashboard()

