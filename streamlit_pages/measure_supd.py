"""
SUPD (Statin Use in Persons with Diabetes)

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

def create_supd_dashboard():
    """Create SUPD measure dashboard."""
    
    st.title("💊 SUPD: Statin Use in Persons with Diabetes")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tier", "2")
    with col2:
        st.metric("Weight", "1x")
    with col3:
        st.metric("Star Value", "$180K-$310K")
    with col4:
        st.metric("Status", "✅ Production")
    
    st.info("**Critical Link:** Enabled by PDC-STA (statin medication adherence).")
    
    st.markdown("---")
    
    with st.expander("📋 Measure Definition", expanded=False):
        st.markdown("""
        ### HEDIS Specification: MY2025 Volume 2
        
        **Description:** Percentage of members 40-75 with diabetes who received a statin medication
        during the measurement year.
        
        **Eligible Population:**
        - Age 40-75
        - Diabetes diagnosis (overlaps with GSD)
        - No contraindications to statins
        
        **Qualifying:** At least 1 statin prescription fill
        """)
    
    st.markdown("---")
    
    st.markdown("## 📈 Current Performance")
    
    statin_rate = np.random.uniform(0.72, 0.82)
    eligible = np.random.randint(7000, 11000)
    on_statin = int(eligible * statin_rate)
    not_on_statin = eligible - on_statin
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Eligible Members", f"{eligible:,}")
        st.metric("On Statin", f"{on_statin:,}", f"{statin_rate*100:.1f}%")
    with col2:
        benchmark = 78.0
        st.metric("SUPD Rate", f"{statin_rate*100:.1f}%", f"{(statin_rate*100 - benchmark):+.1f}%")
    with col3:
        st.metric("Gap to 85%", f"{max(0, 85 - statin_rate*100):.1f}%")
        st.metric("Value", f"${max(0, 85 - statin_rate*100) * 25000:,.0f}")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=statin_rate * 100,
        title={'text': "SUPD Rate (%)"},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "darkblue"},
               'steps': [{'range': [0, 75], 'color': "#ffdddd"},
                        {'range': [75, 85], 'color': "#ffffdd"},
                        {'range': [85, 100], 'color': "#ddffdd"}]}
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Gap Analysis")
    
    gap_data = pd.DataFrame({
        'Status': ['On Statin ✅', 'Not on Statin ⚠️'],
        'Members': [on_statin, not_on_statin],
        'Priority': ['LOW', 'HIGH']
    })
    
    fig = px.bar(gap_data, x='Status', y='Members', color='Priority',
                 color_discrete_map={'HIGH': '#ff4444', 'LOW': '#44ff44'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 💡 Interventions")
    
    col1, col2 = st.columns(2)
    with col1:
        st.error(f"""
        **Not on Statin: {not_on_statin:,} members**
        
        **Interventions:**
        - Provider alerts (statin initiation)
        - Patient education (CV risk)
        - Address barriers (side effects, cost)
        - Generic alternatives
        
        **Expected:** 70-80% initiate statin
        """)
    
    with col2:
        st.success(f"""
        **PDC-STA Alignment Critical**
        
        Members on statin but non-adherent
        (PDC <80%) don't get CV benefit.
        
        **Dual Strategy:**
        1. SUPD: Get members on statin
        2. PDC-STA: Keep them adherent
        
        **Combined value: $400K-$500K**
        """)
    
    st.markdown("---")
    
    st.markdown("## 💰 Financial Impact")
    
    improvement = st.slider("SUPD Improvement (pp)", 0.0, 10.0, 5.0, 0.5)
    value = improvement * 25000
    cost = not_on_statin * 40
    net = value - cost
    roi = (net / cost * 100) if cost > 0 else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Star Value", f"${value:,.0f}")
        st.metric("Intervention Cost", f"${cost:,.0f}")
    with col2:
        st.metric("Net Benefit", f"${net:,.0f}")
        st.metric("ROI", f"{roi:.0f}%")
    
    st.markdown("---")
    
    st.markdown("## 🎯 Key Takeaways")
    st.info(f"""
    **Rate:** {statin_rate*100:.1f}% (Target: 85%+)  
    **Gap:** {not_on_statin:,} members not on statin  
    **Value:** ${value:,.0f} with {improvement:.1f}% improvement  
    **Strategy:** Provider alerts + patient education + PDC-STA coordination
    """)
    
    st.caption(f"**SUPD** | MY2025 | Tier 2 | {datetime.now().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    create_supd_dashboard()

