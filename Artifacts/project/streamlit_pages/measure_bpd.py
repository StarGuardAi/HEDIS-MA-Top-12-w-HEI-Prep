"""
BPD (Blood Pressure Control for Patients with Diabetes)

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

def create_bpd_dashboard():
    """Create BPD measure dashboard."""
    
    st.title("🩺 BPD: Blood Pressure Control for Patients with Diabetes")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tier", "2")
    with col2:
        st.metric("Weight", "1x")
    with col3:
        st.metric("Star Value", "$180K-$310K")
    with col4:
        st.metric("Status", "✅ Production")
    
    st.info("**Note:** Similar to CBP but specifically for diabetes population (overlaps with GSD cohort).")
    
    st.markdown("---")
    
    with st.expander("📋 Measure Definition", expanded=False):
        st.markdown("""
        ### HEDIS Specification: MY2025 Volume 2
        
        **Description:** Percentage of members 18-75 with diabetes whose BP was <140/90 mmHg.
        
        **Eligible Population:**
        - Age 18-75
        - Diabetes diagnosis (same as GSD/KED/EED)
        - BP reading in measurement year
        
        **Target:** <140/90 mmHg
        """)
    
    st.markdown("---")
    
    st.markdown("## 📈 Current Performance")
    
    control_rate = np.random.uniform(0.64, 0.74)
    eligible = np.random.randint(8000, 12000)
    controlled = int(eligible * control_rate)
    uncontrolled = eligible - controlled
    near_control = int(uncontrolled * 0.45)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Eligible Members", f"{eligible:,}")
        st.metric("Controlled (<140/90)", f"{controlled:,}", f"{control_rate*100:.1f}%")
    with col2:
        benchmark = 70.0
        st.metric("BPD Rate", f"{control_rate*100:.1f}%", f"{(control_rate*100 - benchmark):+.1f}%")
    with col3:
        st.metric("Gap to 75%", f"{max(0, 75 - control_rate*100):.1f}%")
        st.metric("Value", f"${max(0, 75 - control_rate*100) * 25000:,.0f}")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=control_rate * 100,
        title={'text': "BPD Control Rate (%)"},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "darkred"},
               'steps': [{'range': [0, 65], 'color': "#ffdddd"},
                        {'range': [65, 75], 'color': "#ffffdd"},
                        {'range': [75, 100], 'color': "#ddffdd"}]}
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Gap Analysis")
    
    bp_data = pd.DataFrame({
        'BP Status': ['Controlled (<140/90)', 'Near Control (140-149/90-94)', 'Uncontrolled (≥150/95)'],
        'Members': [controlled, near_control, uncontrolled - near_control],
        'Priority': ['LOW', 'HIGH', 'MEDIUM']
    })
    
    fig = px.bar(bp_data, x='BP Status', y='Members', color='Priority',
                 color_discrete_map={'HIGH': '#ff4444', 'MEDIUM': '#ffaa00', 'LOW': '#44ff44'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 💡 Interventions & Financial Impact")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Priority Actions")
        st.error(f"""
        **Near Control - Quick Win**  
        {near_control:,} members
        
        - Medication titration
        - PDC-RASA alignment
        - Home BP monitoring
        
        **Expected:** 60-70% achieve control
        """)
    
    with col2:
        improvement = st.slider("BPD Improvement (pp)", 0.0, 10.0, 4.0, 0.5)
        value = improvement * 25000
        cost = near_control * 30 + (uncontrolled - near_control) * 55
        net = value - cost
        roi = (net / cost * 100) if cost > 0 else 0
        
        st.metric("Star Value", f"${value:,.0f}")
        st.metric("Net Benefit", f"${net:,.0f}", f"ROI: {roi:.0f}%")
    
    st.markdown("---")
    
    st.markdown("## 🎯 Key Takeaways")
    st.info(f"""
    **Rate:** {control_rate*100:.1f}% (Target: 75%+)  
    **Quick Win:** {near_control:,} near-control members  
    **Value:** ${value:,.0f} with {improvement:.1f}% improvement  
    **Strategy:** Coordinate with PDC-RASA and GSD interventions (same population)
    """)
    
    st.caption(f"**BPD** | MY2025 | Tier 2 | {datetime.now().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    create_bpd_dashboard()

