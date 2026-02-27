"""
COL (Colorectal Cancer Screening)

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

def create_col_dashboard():
    """Create COL measure dashboard."""
    
    st.title("🔬 COL: Colorectal Cancer Screening")
    
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
        
        **Description:** Percentage of members 45-75 years who had appropriate
        screening for colorectal cancer.
        
        **Qualifying Screens:**
        - **Colonoscopy** (10-year lookback)
        - **Flexible sigmoidoscopy** (5-year lookback)
        - **CT colonography** (5-year lookback)
        - **FIT-DNA test** (3-year lookback)
        - **FIT test** (annual)
        
        **Eligible Population:**
        - Age 45-75 (expanded from 50-75 in 2021)
        - Continuous enrollment
        
        **Exclusions:**
        - Total colectomy
        - Hospice
        """)
    
    st.markdown("---")
    
    st.markdown("## 📈 Current Performance")
    
    screening_rate = np.random.uniform(0.66, 0.76)
    eligible = np.random.randint(12000, 18000)
    screened = int(eligible * screening_rate)
    not_screened = eligible - screened
    never_screened = int(not_screened * 0.40)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Eligible Members", f"{eligible:,}")
        st.metric("Appropriately Screened", f"{screened:,}", f"{screening_rate*100:.1f}%")
    with col2:
        benchmark = 72.0
        st.metric("COL Rate", f"{screening_rate*100:.1f}%", f"{(screening_rate*100 - benchmark):+.1f}%")
    with col3:
        st.metric("Gap to 80%", f"{max(0, 80 - screening_rate*100):.1f}%")
        st.metric("Value", f"${max(0, 80 - screening_rate*100) * 25000:,.0f}")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=screening_rate * 100,
        title={'text': "COL Screening Rate (%)"},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "darkgreen"},
               'steps': [{'range': [0, 68], 'color': "#ffdddd"},
                        {'range': [68, 78], 'color': "#ffffdd"},
                        {'range': [78, 100], 'color': "#ddffdd"}]}
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Gap Analysis by Screening Modality")
    
    modality_data = pd.DataFrame({
        'Screening Type': ['Colonoscopy', 'FIT (annual)', 'FIT-DNA', 'Other', 'Not Screened'],
        'Members': [
            int(screened * 0.75),  # Most common
            int(screened * 0.18),
            int(screened * 0.05),
            int(screened * 0.02),
            not_screened
        ]
    })
    
    fig = px.pie(modality_data, values='Members', names='Screening Type',
                 title='Screening Distribution by Modality')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("## 💡 Interventions & Financial Impact")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Multi-Modal Approach")
        st.error(f"""
        **Not Screened: {not_screened:,} members**
        
        **Barrier-Specific Interventions:**
        
        **For colonoscopy-hesitant:**
        - FIT kit mailing (annual, non-invasive)
        - Home-based screening option
        - $0 copay
        
        **For access-limited:**
        - Mobile screening units
        - Transportation assistance
        - Scheduling support
        
        **For never-screened:**
        - Education on colon cancer risk
        - Provider referrals
        - Navigator programs
        
        **Expected:** 50-65% complete screening
        """)
    
    with col2:
        improvement = st.slider("COL Improvement (pp)", 0.0, 12.0, 6.0, 0.5)
        value = improvement * 25000
        fit_kit_cost = not_screened * 8  # FIT kits cheap
        outreach_cost = not_screened * 12
        cost = fit_kit_cost + outreach_cost
        net = value - cost
        roi = (net / cost * 100) if cost > 0 else 0
        
        st.metric("Star Value", f"${value:,.0f}")
        st.metric("Intervention Cost", f"${cost:,.0f}")
        st.metric("Net Benefit", f"${net:,.0f}", f"ROI: {roi:.0f}%")
        
        st.success("""
        **FIT Kit Strategy:**
        - Mail FIT kits to all unscreened
        - Low cost ($8/kit)
        - High completion (35-50%)
        - Quick win for annual screening
        """)
    
    st.markdown("---")
    
    st.markdown("## 🔬 Clinical Impact")
    
    st.success("""
    **Early Detection Saves Lives:**
    - Colorectal cancer is 3rd most common cancer
    - Screening reduces mortality by 30-50%
    - Stage 1 detection: 92% 5-year survival
    - Stage 4 detection: 14% 5-year survival
    - Colonoscopy can remove precancerous polyps → prevent cancer
    """)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Key Takeaways")
    st.info(f"""
    **Rate:** {screening_rate*100:.1f}% (Target: 80%+)  
    **Not Screened:** {not_screened:,} members  
    **Never Screened:** {never_screened:,} members (HIGH priority)  
    **Value:** ${value:,.0f} with {improvement:.1f}% improvement  
    **Strategy:** FIT kit mailing program (low cost, high impact) + colonoscopy access  
    **Clinical Impact:** Early detection, lives saved, cancer prevention
    """)
    
    st.caption(f"**COL** | MY2025 | Tier 2 | {datetime.now().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    create_col_dashboard()

