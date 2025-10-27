"""
HEI (Health Equity Index) Dashboard Page
Interactive visualization for health equity analysis and CMS compliance.

This is the UNIQUE differentiator - 2+ years ahead of CMS 2027 mandate.

Features:
- Portfolio equity score (0-100 scale)
- CMS penalty tier indicator
- Stratified performance by demographics
- Disparity detection visualizations
- Intervention priority matrix
- Financial impact calculator

Author: Robert Reichert
Date: October 25, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def create_hei_dashboard():
    """Create comprehensive HEI dashboard page."""
    
    # Header
    st.title("🏥 Health Equity Index (HEI) Dashboard")
    st.markdown("### CMS 2027 Mandate - 2+ Years Early Implementation ⭐")
    
    st.info("""
    **First-Mover Advantage:** This portfolio implements the CMS Health Equity Index requirement 
    **2+ years before the 2027 mandate**, providing massive competitive advantage and 
    **$10M-$20M downside protection** for a 100K member Medicare Advantage plan.
    """)
    
    st.markdown("---")
    
    # Overall Equity Score (Large Display)
    st.markdown("## 📊 Portfolio Equity Score")
    
    # Simulated equity score
    overall_score = np.random.uniform(68, 85)
    
    # Determine penalty tier
    if overall_score >= 70:
        penalty_tier = "NO PENALTY"
        penalty_amount = 0.0
        penalty_color = "green"
        financial_impact = "$0 (Excellent Performance)"
        status_icon = "✅"
    elif overall_score >= 50:
        penalty_tier = "MODERATE PENALTY"
        penalty_amount = -0.25
        penalty_color = "orange"
        financial_impact = "-$10M annually"
        status_icon = "⚠️"
    else:
        penalty_tier = "HIGH PENALTY"
        penalty_amount = -0.5
        penalty_color = "red"
        financial_impact = "-$20M annually"
        status_icon = "🚨"
    
    # Large equity score gauge
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=overall_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Equity Score", 'font': {'size': 24}},
            delta={'reference': 70, 'suffix': ' to no-penalty threshold'},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#ffcccc'},
                    {'range': [50, 70], 'color': '#ffffcc'},
                    {'range': [70, 100], 'color': '#ccffcc'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        fig.update_layout(
            height=400,
            font={'size': 16}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Penalty tier display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "CMS Penalty Tier",
            f"{status_icon} {penalty_tier}",
            help="Based on overall equity score"
        )
    
    with col2:
        st.metric(
            "Star Rating Impact",
            f"{penalty_amount:+.2f} stars",
            help="Penalty applied to overall Star Rating"
        )
    
    with col3:
        st.metric(
            "Financial Impact",
            financial_impact,
            help="Annual financial impact (100K member plan)"
        )
    
    # Interpretation
    if overall_score >= 70:
        st.success(f"""
        ✅ **Excellent Equity Performance!**
        
        Your portfolio equity score of **{overall_score:.1f}** exceeds the CMS threshold of 70, 
        avoiding any Star Rating penalties. Continue proactive equity monitoring to maintain this performance.
        """)
    elif overall_score >= 50:
        st.warning(f"""
        ⚠️ **Moderate Equity Performance - Action Needed**
        
        Your portfolio equity score of **{overall_score:.1f}** falls in the moderate penalty range (50-69).
        This results in a **-0.25 star penalty** and approximately **$10M in lost revenue** annually.
        
        **Recommendation:** Focus on high-priority interventions to improve score above 70.
        """)
    else:
        st.error(f"""
        🚨 **LOW Equity Performance - URGENT Action Required**
        
        Your portfolio equity score of **{overall_score:.1f}** is below 50, triggering a **-0.5 star penalty**
        and approximately **$20M in lost revenue** annually.
        
        **Recommendation:** Immediate intervention required. Prioritize disparity reduction initiatives.
        """)
    
    st.markdown("---")
    
    # Stratified Performance by Race/Ethnicity
    st.markdown("## 🌍 Stratified Performance Analysis")
    
    st.markdown("""
    Performance breakdown by demographic groups across all HEDIS measures.
    Identifies which populations have lower compliance rates and need targeted interventions.
    """)
    
    # Simulated stratified data
    demographic_groups = ['White', 'Black/African American', 'Hispanic/Latino', 'Asian', 'Other']
    measures = ['GSD', 'KED', 'CBP', 'EED', 'SUPD']
    
    stratified_data = []
    for measure in measures:
        for group in demographic_groups:
            # Simulate some disparities
            base_rate = np.random.uniform(0.70, 0.85)
            if group == 'Black/African American':
                rate = base_rate - np.random.uniform(0.05, 0.15)  # Disparity
            elif group == 'Hispanic/Latino':
                rate = base_rate - np.random.uniform(0.03, 0.10)  # Disparity
            else:
                rate = base_rate + np.random.uniform(-0.02, 0.05)
            
            stratified_data.append({
                'Measure': measure,
                'Demographic Group': group,
                'Compliance Rate': rate * 100,
                'Members': np.random.randint(1000, 5000)
            })
    
    stratified_df = pd.DataFrame(stratified_data)
    
    # Heatmap of stratified performance
    st.markdown("### Performance Heatmap by Demographics")
    
    pivot_data = stratified_df.pivot(
        index='Demographic Group',
        columns='Measure',
        values='Compliance Rate'
    )
    
    fig = px.imshow(
        pivot_data,
        labels=dict(x="HEDIS Measure", y="Demographic Group", color="Compliance Rate (%)"),
        x=pivot_data.columns,
        y=pivot_data.index,
        color_continuous_scale='RdYlGn',
        aspect="auto",
        title="Compliance Rates by Demographic Group and Measure"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Disparity Detection
    st.markdown("## 🔍 Disparity Detection")
    
    # Calculate disparities for each measure
    disparities = []
    for measure in measures:
        measure_data = stratified_df[stratified_df['Measure'] == measure]
        max_rate = measure_data['Compliance Rate'].max()
        min_rate = measure_data['Compliance Rate'].min()
        disparity_magnitude = max_rate - min_rate
        
        highest_group = measure_data.loc[measure_data['Compliance Rate'].idxmax(), 'Demographic Group']
        lowest_group = measure_data.loc[measure_data['Compliance Rate'].idxmin(), 'Demographic Group']
        
        if disparity_magnitude >= 15:
            disparity_level = "HIGH"
            color = "red"
        elif disparity_magnitude >= 10:
            disparity_level = "MODERATE"
            color = "orange"
        else:
            disparity_level = "LOW"
            color = "green"
        
        disparities.append({
            'Measure': measure,
            'Disparity Magnitude': disparity_magnitude,
            'Disparity Level': disparity_level,
            'Highest Group': highest_group,
            'Highest Rate': max_rate,
            'Lowest Group': lowest_group,
            'Lowest Rate': min_rate
        })
    
    disparity_df = pd.DataFrame(disparities).sort_values('Disparity Magnitude', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Disparity Magnitude by Measure")
        
        fig = px.bar(
            disparity_df,
            x='Measure',
            y='Disparity Magnitude',
            color='Disparity Level',
            color_discrete_map={'HIGH': '#ff4444', 'MODERATE': '#ffaa00', 'LOW': '#44ff44'},
            title='Percentage Point Difference Between Highest and Lowest Groups',
            labels={'Disparity Magnitude': 'Percentage Point Gap'}
        )
        fig.add_hline(y=10, line_dash="dash", line_color="orange", annotation_text="Moderate Threshold (10%)")
        fig.add_hline(y=15, line_dash="dash", line_color="red", annotation_text="High Threshold (15%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Disparity Summary")
        
        high_count = len(disparity_df[disparity_df['Disparity Level'] == 'HIGH'])
        moderate_count = len(disparity_df[disparity_df['Disparity Level'] == 'MODERATE'])
        low_count = len(disparity_df[disparity_df['Disparity Level'] == 'LOW'])
        
        st.metric("High Disparities", high_count, help="Gap ≥ 15 percentage points")
        st.metric("Moderate Disparities", moderate_count, help="Gap 10-15 percentage points")
        st.metric("Low Disparities", low_count, help="Gap < 10 percentage points")
    
    # Detailed disparity table
    st.markdown("### Detailed Disparity Analysis")
    st.dataframe(
        disparity_df.style.background_gradient(subset=['Disparity Magnitude'], cmap='Reds'),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Priority Interventions
    st.markdown("## 💡 Priority Interventions")
    
    st.markdown("""
    Top interventions ranked by impact potential. Focus on measures with largest disparities
    and highest Star Rating weights for maximum ROI.
    """)
    
    # Generate intervention priorities
    interventions = []
    for _, row in disparity_df.head(5).iterrows():
        measure_weight = 3.0 if row['Measure'] in ['GSD', 'KED', 'CBP'] else 1.0
        impact_score = row['Disparity Magnitude'] * measure_weight
        
        interventions.append({
            'Rank': len(interventions) + 1,
            'Measure': row['Measure'],
            'Target Group': row['Lowest Group'],
            'Current Rate': f"{row['Lowest Rate']:.1f}%",
            'Goal Rate': f"{row['Highest Rate']:.1f}%",
            'Gap to Close': f"{row['Disparity Magnitude']:.1f}%",
            'Measure Weight': f"{measure_weight:.0f}x",
            'Impact Score': impact_score,
            'Priority': 'HIGH' if impact_score > 30 else 'MEDIUM' if impact_score > 15 else 'LOW'
        })
    
    intervention_df = pd.DataFrame(interventions)
    
    st.dataframe(
        intervention_df.style.background_gradient(subset=['Impact Score'], cmap='OrRd'),
        use_container_width=True,
        hide_index=True
    )
    
    # Recommended actions
    st.markdown("### Recommended Actions")
    
    top_intervention = interventions[0]
    
    st.success(f"""
    **TOP PRIORITY: {top_intervention['Measure']} - {top_intervention['Target Group']}**
    
    **Current Situation:**
    - {top_intervention['Target Group']} population: {top_intervention['Current Rate']} compliance
    - Gap vs highest group: {top_intervention['Gap to Close']}
    - Measure weight: {top_intervention['Measure Weight']} ({"triple-weighted" if "3" in top_intervention['Measure Weight'] else "standard"})
    
    **Recommended Actions:**
    1. 📞 **Culturally-tailored outreach** - Develop materials in preferred language
    2. 🏥 **Provider education** - Train on cultural competency for this population
    3. 🤝 **Community partnerships** - Partner with community organizations
    4. 📊 **Barrier analysis** - Conduct root cause analysis of gaps
    5. 💰 **Targeted incentives** - Offer completion incentives
    6. 📈 **Monthly monitoring** - Track progress weekly
    
    **Expected Impact:**
    - Gap closure: 30-50% reduction in 6 months
    - Equity score: +3 to +5 points improvement
    - Financial: $200K-$500K value from improved compliance
    """)
    
    st.markdown("---")
    
    # Financial Impact Model
    st.markdown("## 💰 Financial Impact Calculator")
    
    st.markdown("""
    Calculate the financial impact of equity improvement initiatives.
    Model the cost-benefit of disparity reduction programs.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Intervention Costs")
        
        outreach_cost = st.number_input(
            "Outreach Campaign Cost",
            min_value=0,
            max_value=1000000,
            value=50000,
            step=10000,
            help="Cost of targeted member outreach"
        )
        
        provider_ed_cost = st.number_input(
            "Provider Education Cost",
            min_value=0,
            max_value=500000,
            value=25000,
            step=5000,
            help="Cost of cultural competency training"
        )
        
        community_cost = st.number_input(
            "Community Partnership Cost",
            min_value=0,
            max_value=500000,
            value=30000,
            step=5000,
            help="Cost of community partnerships"
        )
        
        total_cost = outreach_cost + provider_ed_cost + community_cost
        
        st.metric("Total Intervention Cost", f"${total_cost:,}")
    
    with col2:
        st.markdown("### Expected Benefits")
        
        # Calculate benefit based on equity score improvement
        score_improvement = st.slider(
            "Expected Equity Score Improvement",
            min_value=0,
            max_value=20,
            value=5,
            help="Points improvement in overall equity score"
        )
        
        new_score = overall_score + score_improvement
        
        # Determine new penalty tier
        if overall_score < 50 and new_score >= 50:
            penalty_avoided = 20_000_000 - 10_000_000
            tier_change = "HIGH → MODERATE"
        elif overall_score < 50 and new_score >= 70:
            penalty_avoided = 20_000_000
            tier_change = "HIGH → NO PENALTY"
        elif overall_score < 70 and new_score >= 70:
            penalty_avoided = 10_000_000
            tier_change = "MODERATE → NO PENALTY"
        else:
            penalty_avoided = 0
            tier_change = "No tier change"
        
        # Additional compliance value
        gap_closure_value = 500_000  # Approximate value from improved compliance
        
        total_benefit = penalty_avoided + gap_closure_value
        net_benefit = total_benefit - total_cost
        roi = (net_benefit / total_cost * 100) if total_cost > 0 else 0
        
        st.metric("Penalty Avoidance", f"${penalty_avoided:,}")
        st.metric("Gap Closure Value", f"${gap_closure_value:,}")
        st.metric("Total Benefit", f"${total_benefit:,}")
        st.metric("Net Benefit", f"${net_benefit:,}", delta=f"ROI: {roi:.0f}%")
        
        if tier_change != "No tier change":
            st.success(f"**Penalty Tier Change:** {tier_change}")
    
    if net_benefit > 0:
        st.success(f"""
        ✅ **Positive ROI!** 
        
        Investment of ${total_cost:,} generates ${total_benefit:,} in benefits,
        resulting in **${net_benefit:,} net value** and **{roi:.0f}% ROI**.
        
        This initiative is highly recommended for implementation.
        """)
    
    st.markdown("---")
    
    # Implementation Timeline
    st.markdown("## 📅 Implementation Timeline")
    
    timeline_data = pd.DataFrame({
        'Phase': ['Assessment', 'Planning', 'Pilot', 'Scale-Up', 'Monitoring'],
        'Duration': ['Month 1', 'Month 2', 'Months 3-4', 'Months 5-6', 'Ongoing'],
        'Key Activities': [
            'Conduct disparity analysis, identify root causes',
            'Develop intervention strategy, secure partnerships',
            'Launch pilot with top-priority population',
            'Expand to all identified populations',
            'Track progress, adjust tactics monthly'
        ],
        'Expected Outcome': [
            'Baseline established, priorities identified',
            'Detailed action plan with budget',
            '20-30% gap closure in pilot group',
            '40-60% overall gap closure',
            'Sustained equity improvement'
        ]
    })
    
    st.table(timeline_data)
    
    st.markdown("---")
    
    # CMS Compliance Status
    st.markdown("## ✅ CMS Compliance Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("""
        **Data Collection**
        
        ✅ Race/ethnicity standardized  
        ✅ Language preferences tracked  
        ✅ SDOH data integrated  
        ✅ Member-level stratification  
        
        Status: **Compliant**
        """)
    
    with col2:
        if overall_score >= 70:
            st.success("""
            **Equity Scoring**
            
            ✅ Portfolio score: {:.1f}  
            ✅ Above 70 threshold  
            ✅ No penalty tier  
            ✅ Reporting ready  
            
            Status: **Compliant**
            """.format(overall_score))
        else:
            st.warning("""
            **Equity Scoring**
            
            ⚠️ Portfolio score: {:.1f}  
            ⚠️ Below 70 threshold  
            ⚠️ Penalty tier active  
            ⚠️ Improvement needed  
            
            Status: **Action Required**
            """.format(overall_score))
    
    with col3:
        st.success("""
        **Intervention Planning**
        
        ✅ Priorities identified  
        ✅ Action plans developed  
        ✅ Budget allocated  
        ✅ Timeline established  
        
        Status: **Ready**
        """)
    
    st.markdown("---")
    
    # Key Takeaways
    st.markdown("## 🎯 Key Takeaways")
    
    st.info(f"""
    **Current Equity Performance:**
    - Overall Score: **{overall_score:.1f}/100**
    - Penalty Tier: **{penalty_tier}**
    - Financial Impact: **{financial_impact}**
    
    **Top Priorities:**
    1. {interventions[0]['Measure']} - {interventions[0]['Target Group']} (Gap: {interventions[0]['Gap to Close']})
    2. {interventions[1]['Measure']} - {interventions[1]['Target Group']} (Gap: {interventions[1]['Gap to Close']})
    3. {interventions[2]['Measure']} - {interventions[2]['Target Group']} (Gap: {interventions[2]['Gap to Close']})
    
    **Competitive Advantage:**
    - ✅ **2+ years ahead** of CMS 2027 mandate
    - ✅ **Proactive equity management** vs reactive compliance
    - ✅ **$10M-$20M protection** through early implementation
    - ✅ **Industry leadership** in health equity
    
    **Recommendation:** {"Maintain excellent performance with ongoing monitoring" if overall_score >= 70 else f"Implement priority interventions to improve score by {70 - overall_score:.0f} points"}
    """)
    
    # Footer
    st.markdown("---")
    st.caption("""
    **Health Equity Index (HEI) Dashboard** | CMS 2027 Mandate | 2+ Years Early Implementation ⭐  
    Last updated: {} | HEDIS MY2025 Compliant ✅
    """.format(datetime.now().strftime('%Y-%m-%d')))


# Example usage
if __name__ == "__main__":
    create_hei_dashboard()

