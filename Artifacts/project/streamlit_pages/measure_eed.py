"""
EED (Eye Exam for Patients with Diabetes) Measure Dashboard Page

NEW 2025 Measure - Tier 1, Triple-Weighted
Star Rating Value: $360K-$615K per 0.1 improvement
HEDIS Specification: MY2025 Volume 2

This is a **NEW** measure for 2025, replacing the older retinal eye exam measure.

Author: Robert Reichert
Date: October 25, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def create_eed_dashboard():
    """Create comprehensive EED measure dashboard."""
    
    # Header
    st.title("👁️ EED: Eye Exam for Patients with Diabetes")
    st.markdown("### **NEW 2025 MEASURE** - Enhanced Specifications ⚠️")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Tier", "1", help="Highest priority tier")
    
    with col2:
        st.metric("Weight", "3x", help="Triple-weighted measure")
    
    with col3:
        st.metric("Star Value", "$360K-$615K", help="Value per 0.1 improvement")
    
    with col4:
        st.metric("Status", "🆕 NEW 2025", help="Enhanced specifications")
    
    with col5:
        st.metric("Implementation", "✅ Ready", help="Fully implemented")
    
    st.warning("""
    ⚠️ **Specification Change Alert:**  
    This measure has **enhanced specifications for 2025**, expanding beyond traditional retinal exams
    to include advanced imaging and AI-assisted screening. Update workflows accordingly.
    """)
    
    st.markdown("---")
    
    # Measure Definition
    with st.expander("📋 Measure Definition & Specifications", expanded=False):
        st.markdown("""
        ### HEDIS Specification: MY2025 Volume 2 (ENHANCED)
        
        **Description:**  
        The percentage of members 18-75 years of age with diabetes (type 1 or type 2)
        who had a **retinal or dilated eye exam** by an eye care professional during
        the measurement year or a negative retinal exam in the year prior to the measurement year.
        
        **Qualifying Exams (2025 Enhanced):**
        1. **Retinal or dilated eye exam** by optometrist or ophthalmologist
        2. **Fundus photography** with interpretation
        3. **OCT (Optical Coherence Tomography)** imaging
        4. **AI-assisted diabetic retinopathy screening** (NEW for 2025)
        
        **Eligible Population:**
        - Age 18-75 as of December 31 of the measurement year
        - Diagnosis of diabetes (type 1 or type 2) - **Same as GSD, KED**
        - Continuous enrollment during measurement year
        
        **Exclusions:**
        - Members in hospice
        - Members with bilateral eye enucleation (both eyes removed)
        - Members with gestational or steroid-induced diabetes only
        
        **Clinical Rationale:**
        - Diabetic retinopathy is the leading cause of preventable blindness
        - Early detection allows laser treatment to prevent vision loss
        - 1 in 3 adults with diabetes has some stage of diabetic retinopathy
        - Annual screening recommended by ADA and AAO
        
        **Data Sources:** Claims + Medical Records
        
        **Star Rating Impact:** Triple-weighted measure (3x standard weight)
        
        **2025 Enhancement:** AI-assisted screening now qualifies, enabling pharmacy/retail clinic exams.
        """)
    
    st.markdown("---")
    
    # Current Performance
    st.markdown("## 📈 Current Performance")
    
    # Simulated performance data
    completion_rate = np.random.uniform(0.58, 0.68)
    eligible_members = np.random.randint(8000, 12000)
    
    completed_members = int(eligible_members * completion_rate)
    last_year_exam = int(completed_members * 0.35)  # Had exam in prior year (still counts)
    current_year_exam = completed_members - last_year_exam
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Eligible Members",
            f"{eligible_members:,}",
            help="Same population as GSD/KED (diabetes 18-75)"
        )
        
        st.metric(
            "Members with Eye Exam",
            f"{completed_members:,}",
            f"{completion_rate*100:.1f}%",
            help="Eye exam this year OR prior year"
        )
    
    with col2:
        st.metric(
            "Overall Completion Rate",
            f"{completion_rate*100:.1f}%",
            help="Percentage with qualifying eye exam"
        )
        
        # Benchmark comparison
        benchmark = 65.0  # Typical industry benchmark
        delta = (completion_rate * 100) - benchmark
        
        st.metric(
            "vs Industry Benchmark",
            f"{benchmark:.1f}%",
            f"{delta:+.1f}%",
            help="Industry average for eye exams"
        )
    
    with col3:
        st.metric(
            "Gap to 75% Target",
            f"{max(0, 75 - completion_rate*100):.1f}%",
            help="Points needed for top-tier performance"
        )
        
        potential_revenue = max(0, 75 - completion_rate*100) * 52500
        st.metric(
            "Improvement Opportunity",
            f"${potential_revenue:,.0f}",
            help="Value of closing gap to 75%"
        )
    
    # Performance gauge
    st.markdown("### Eye Exam Completion Rate")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=completion_rate * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "EED Completion Rate (%)", 'font': {'size': 20}},
        delta={'reference': 65, 'suffix': '% (Industry Benchmark)'},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 60], 'color': "#ffdddd"},
                {'range': [60, 70], 'color': "#ffffdd"},
                {'range': [70, 100], 'color': "#ddffdd"}
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
    if completion_rate >= 0.70:
        st.success(f"""
        ✅ **Excellent Performance!**
        
        Your eye exam completion rate of **{completion_rate*100:.1f}%** exceeds the industry average,
        positioning you well for high Star Ratings.
        """)
    elif completion_rate >= 0.60:
        st.info(f"""
        ℹ️ **Good Performance - Continue Building**
        
        Your completion rate of **{completion_rate*100:.1f}%** is near the industry average.
        Focus on members overdue for their annual exam.
        """)
    else:
        st.warning(f"""
        ⚠️ **Below Average - Urgent Action Needed**
        
        Your completion rate of **{completion_rate*100:.1f}%** is below industry standards.
        Implement vision care access initiatives and provider partnerships.
        """)
    
    st.markdown("---")
    
    # Gap Analysis
    st.markdown("## 🎯 Gap Analysis & Exam History")
    
    # Exam timing breakdown
    never_had_exam = eligible_members - completed_members
    exam_2plus_years_ago = int(never_had_exam * 0.40)  # Had exam >2 years ago (doesn't count)
    truly_never = never_had_exam - exam_2plus_years_ago
    
    exam_data = pd.DataFrame({
        'Exam Status': [
            'Current Year Exam ✅',
            'Prior Year Exam (Still Counts) ✅',
            'Exam 2+ Years Ago ⚠️',
            'Never Had Exam ⚠️'
        ],
        'Members': [current_year_exam, last_year_exam, exam_2plus_years_ago, truly_never],
        'Priority': ['LOW', 'MEDIUM', 'HIGH', 'HIGH'],
        'Intervention': [
            'Maintain - schedule next year',
            'Encourage annual exam this year',
            'Overdue - schedule immediately',
            'Education + access support'
        ]
    })
    
    exam_data['Percentage'] = exam_data['Members'] / eligible_members * 100
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Member Distribution by Exam Timing")
        
        fig = px.bar(
            exam_data,
            x='Exam Status',
            y='Members',
            color='Priority',
            color_discrete_map={'HIGH': '#ff4444', 'MEDIUM': '#ffaa00', 'LOW': '#44ff44'},
            title='Members by Eye Exam Recency',
            text='Members'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_xaxis(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Priority Segments")
        
        high_priority = exam_2plus_years_ago + truly_never
        
        st.metric(
            "HIGH Priority (Overdue)",
            f"{high_priority:,}",
            f"{high_priority/eligible_members*100:.1f}%"
        )
        
        st.metric(
            "MEDIUM Priority (Prior Year)",
            f"{last_year_exam:,}",
            f"{last_year_exam/eligible_members*100:.1f}%"
        )
        
        st.metric(
            "LOW Priority (Current)",
            f"{current_year_exam:,}",
            f"{current_year_exam/eligible_members*100:.1f}%"
        )
    
    # Detailed exam status
    st.markdown("### Detailed Exam Status")
    st.dataframe(
        exam_data.style.background_gradient(subset=['Members'], cmap='YlOrRd'),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Interventions
    st.markdown("## 💡 Recommended Interventions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### For Overdue Members (HIGH Priority)")
        st.error(f"""
        **Target:** {high_priority:,} members
        
        **Interventions:**
        1. 👁️ **Vision Care Access**
           - Partner with optometry networks
           - In-network provider expansion
           - Transportation assistance
           - Evening/weekend appointments
        
        2. 📞 **Proactive Outreach**
           - Personalized reminder calls
           - Text/email appointment scheduling
           - IVR campaigns with urgency messaging
        
        3. 🏪 **Retail Clinic Partnerships (NEW 2025)**
           - AI-assisted retinopathy screening
           - Walmart Vision, CVS, Target Optical
           - No-cost screening events
           - Same-day appointments
        
        4. 💰 **Financial Incentives**
           - Waive copays for overdue members
           - Gift cards for completion
           - Bundled incentives (EED + KED + GSD)
        
        **Expected Impact:** 40-50% completion rate
        **Financial Value:** ${int(high_priority * 0.45 * 45):,.0f}
        """)
    
    with col2:
        st.markdown("### For Prior Year Exam Members (MEDIUM Priority)")
        st.warning(f"""
        **Target:** {last_year_exam:,} members
        
        **Interventions:**
        1. 📅 **Annual Reminder Campaign**
           - "Time for your annual eye exam" messaging
           - Appointment scheduling assistance
           - Provider recommendations
        
        2. 🤝 **Provider Engagement**
           - Automatic scheduling at prior clinic
           - Provider recall systems
           - Standing appointments
        
        3. 📚 **Education on Annual Screening**
           - Why annual exams matter
           - Diabetic retinopathy progression
           - Vision loss prevention
        
        **Expected Impact:** 60-70% complete exam this year
        **Financial Value:** ${int(last_year_exam * 0.65 * 45):,.0f}
        
        **Note:** These members already understand importance
        (completed exam before), so conversion rates are higher.
        """)
    
    st.markdown("---")
    
    # 2025 Enhancement - AI Screening
    st.markdown("## 🤖 2025 Enhancement: AI-Assisted Screening")
    
    st.success("""
    **MAJOR OPPORTUNITY:** New for 2025, AI-assisted diabetic retinopathy screening
    now qualifies for EED credit. This enables **retail clinic partnerships** and
    significantly **reduces access barriers**.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Traditional Eye Exam Model")
        st.info("""
        **Location:** Ophthalmologist/optometrist office
        **Wait Time:** 2-4 weeks for appointment
        **Duration:** 60-90 minutes (including dilation)
        **Cost:** $100-$200
        **Barriers:**
        - Limited appointments
        - Transportation required
        - Time off work needed
        - Post-dilation vision impairment
        
        **Typical Completion:** 60-65%
        """)
    
    with col2:
        st.markdown("### AI-Assisted Screening (NEW 2025)")
        st.success("""
        **Location:** Pharmacy, retail clinic, PCP office
        **Wait Time:** Same-day or walk-in
        **Duration:** 10-15 minutes (no dilation)
        **Cost:** $0-$30
        **Benefits:**
        - Immediate availability
        - Convenient locations
        - No time off work
        - No vision impairment
        - Results in 48 hours
        
        **Projected Completion:** 75-80%
        """)
    
    st.markdown("### AI Screening Partner Options")
    
    partners = pd.DataFrame({
        'Partner': ['CVS MinuteClinic', 'Walmart Vision Center', 'Walgreens', 'IDx-DR (Mobile)', 'EyeQue (Home Kit)'],
        'Locations': ['1,100+ clinics', '2,500+ centers', '8,000+ pharmacies', 'Mobile units', 'Ship to home'],
        'Cost': ['$0 copay', '$25', '$30', '$0 (sponsored)', '$49'],
        'AI Technology': ['IDx-DR', 'Optos', 'Digital Health', 'IDx-DR', 'Telehealth'],
        'Turnaround': ['48 hours', 'Same day', '72 hours', '24 hours', '48 hours'],
        'Priority': ['HIGH', 'HIGH', 'MEDIUM', 'HIGH', 'LOW']
    })
    
    st.dataframe(partners, use_container_width=True, hide_index=True)
    
    st.info(f"""
    **Implementation Recommendation:**
    
    Partner with **CVS MinuteClinic** and **Walmart Vision Centers** for immediate access.
    Target **{high_priority:,} overdue members** with AI-assisted screening option.
    
    **Projected Impact:**
    - Traditional model: 45% completion → **Revenue: ${int(high_priority * 0.45 * 45):,.0f}**
    - AI-assisted model: 65% completion → **Revenue: ${int(high_priority * 0.65 * 45):,.0f}**
    - **Additional Value: ${int(high_priority * (0.65 - 0.45) * 45):,.0f}**
    """)
    
    st.markdown("---")
    
    # Financial Impact
    st.markdown("## 💰 Financial Impact Model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Improvement Scenarios")
        
        improvement_points = st.slider(
            "Completion Rate Improvement (percentage points)",
            min_value=0.0,
            max_value=15.0,
            value=7.0,
            step=0.5,
            help="Improvement from AI-assisted screening + outreach"
        )
        
        new_completion_rate = min(completion_rate + (improvement_points / 100), 0.95)
        
        st.metric("Current Rate", f"{completion_rate*100:.1f}%")
        st.metric("Projected Rate", f"{new_completion_rate*100:.1f}%", f"+{improvement_points:.1f}%")
        
        # Breakdown by intervention
        ai_contribution = min(improvement_points * 0.50, 8.0)
        outreach_contribution = min(improvement_points * 0.30, 4.0)
        incentive_contribution = min(improvement_points * 0.20, 3.0)
        
        st.markdown("#### Improvement Sources")
        st.write(f"- AI-assisted screening: +{ai_contribution:.1f}%")
        st.write(f"- Proactive outreach: +{outreach_contribution:.1f}%")
        st.write(f"- Financial incentives: +{incentive_contribution:.1f}%")
    
    with col2:
        st.markdown("### Financial Impact")
        
        value_per_point = 52500  # Triple-weighted
        total_value = improvement_points * value_per_point
        
        # Intervention costs
        ai_setup_cost = 50000  # One-time partnership setup
        screening_cost = high_priority * 25  # $25 per AI screening
        outreach_cost = eligible_members * 8  # $8 per member outreach
        incentive_cost = high_priority * 0.50 * 30  # 50% take incentive
        
        total_cost = ai_setup_cost + screening_cost + outreach_cost + incentive_cost
        net_value = total_value - total_cost
        roi = (net_value / total_cost * 100) if total_cost > 0 else 0
        
        st.metric("Gross Star Rating Value", f"${total_value:,.0f}")
        st.metric("AI Partnership Setup", f"${ai_setup_cost:,.0f}")
        st.metric("Screening + Outreach", f"${screening_cost + outreach_cost:,.0f}")
        st.metric("Incentives", f"${incentive_cost:,.0f}")
        st.metric("Total Cost", f"${total_cost:,.0f}")
        st.metric("Net Value", f"${net_value:,.0f}", f"ROI: {roi:.0f}%")
    
    if net_value > 0:
        st.success(f"""
        ✅ **Excellent ROI!**
        
        Investing ${total_cost:,.0f} (including AI screening partnership) generates
        **${total_value:,.0f}** in Star Rating value, resulting in **${net_value:,.0f} net benefit**
        ({roi:.0f}% ROI).
        
        The AI-assisted screening partnership is highly recommended.
        """)
    
    st.markdown("---")
    
    # Clinical Impact
    st.markdown("## 👁️ Clinical Impact: Preventing Blindness")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Diabetic Retinopathy Stages")
        
        retinopathy_data = pd.DataFrame({
            'Stage': ['No DR', 'Mild NPDR', 'Moderate NPDR', 'Severe NPDR', 'PDR'],
            'Prevalence': [70, 15, 10, 3, 2],
            'Treatment': ['Monitor annually', 'Monitor q6mo', 'Monitor q3-4mo', 'Laser/injection', 'Urgent laser']
        })
        
        fig = px.pie(
            retinopathy_data,
            values='Prevalence',
            names='Stage',
            title='Diabetic Retinopathy Prevalence in Diabetes Population'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Vision Loss Prevention")
        
        unscreened = never_had_exam
        estimated_dr = int(unscreened * 0.30)  # 30% have DR
        estimated_severe = int(estimated_dr * 0.15)  # 15% of DR is severe/PDR
        
        st.error(f"""
        **Unscreened Population Risk:**
        
        - **{unscreened:,} members** unscreened
        - **~{estimated_dr:,} members** (~30%) likely have diabetic retinopathy
        - **~{estimated_severe} members** likely have severe DR/PDR
        
        **Without screening:**
        - Risk of preventable vision loss
        - Progression to blindness
        - Reduced quality of life
        - Increased healthcare costs
        
        **With annual screening:**
        - Early detection and treatment
        - 95% reduction in severe vision loss
        - Improved member outcomes
        - Lower long-term costs
        """)
        
        st.metric(
            "Vision Loss Prevention Value",
            f"${estimated_severe * 50000:,.0f}",
            help="Estimated cost savings from preventing severe vision loss"
        )
    
    st.markdown("---")
    
    # Implementation Timeline
    st.markdown("## 📅 Implementation Timeline")
    
    timeline = pd.DataFrame({
        'Phase': ['Partner Selection', 'Contract & Setup', 'Provider Training', 'Member Outreach', 'Scale & Monitor'],
        'Duration': ['Week 1', 'Weeks 2-3', 'Week 4', 'Weeks 5-8', 'Weeks 9-16'],
        'Activities': [
            'Evaluate AI screening partners (CVS, Walmart, etc.)',
            'Negotiate contracts, integrate systems, test workflows',
            'Train PCPs on AI screening referrals',
            'Launch targeted outreach to overdue members',
            'Scale to all segments, track weekly, optimize'
        ],
        'Target': [
            'Partner selected (CVS or Walmart recommended)',
            'AI screening available in 50+ locations',
            '100% PCP awareness and referral capability',
            '60%+ of overdue members complete screening',
            '75%+ overall completion rate'
        ]
    })
    
    st.table(timeline)
    
    st.markdown("---")
    
    # Key Takeaways
    st.markdown("## 🎯 Key Takeaways")
    
    st.info(f"""
    **Current Performance:**
    - Eye Exam Completion Rate: **{completion_rate*100:.1f}%** (Goal: 75%+)
    - Gap to Goal: **{max(0, 75 - completion_rate*100):.1f} percentage points**
    - Industry Benchmark: **65%** (your position: {"ABOVE" if completion_rate >= 0.65 else "AT/BELOW"} average)
    
    **2025 Game-Changer: AI-Assisted Screening**
    - ✅ **NEW** HEDIS-qualifying option for 2025
    - ✅ **Retail clinic access** (CVS, Walmart, Walgreens)
    - ✅ **10-15 minute** no-dilation screening
    - ✅ **65-80% completion rates** (vs 60-65% traditional)
    - ✅ **20% higher** expected completion vs traditional model
    
    **Top Opportunities:**
    1. **Overdue Members:** {high_priority:,} members (${int(high_priority * 0.45 * 45):,.0f} base value)
    2. **AI Screening Boost:** +{high_priority * 0.20 / eligible_members * 100:.1f}% completion → +${int(high_priority * 0.20 * 45):,.0f}
    3. **Prior Year Members:** {last_year_exam:,} members (${int(last_year_exam * 0.65 * 45):,.0f} value)
    
    **Financial Impact:**
    - **Star Rating Value:** $360K-$615K per 1% improvement (triple-weighted)
    - **Total Opportunity:** ${(improvement_points if 'improvement_points' in locals() else 7.0) * 52500:,.0f} with {improvement_points if 'improvement_points' in locals() else 7.0}% improvement
    - **ROI:** {roi if 'roi' in locals() else 250:.0f}% including AI screening partnership
    
    **Priority Actions:**
    1. **URGENT:** Partner with CVS MinuteClinic or Walmart Vision (AI screening)
    2. Launch targeted outreach to {high_priority:,} overdue members
    3. Promote AI screening as fast, convenient alternative
    4. Train PCPs on AI screening referral workflows
    5. Track completion rates weekly by screening modality
    
    **Clinical Impact:**
    - Prevent vision loss in ~{estimated_severe if 'estimated_severe' in locals() else 150} high-risk members
    - Early detection and treatment for ~{estimated_dr if 'estimated_dr' in locals() else 1200} members with DR
    - Long-term cost savings: ${(estimated_severe if 'estimated_severe' in locals() else 150) * 50000:,.0f}
    
    **Timeline:** 4-week partnership setup, 4-week outreach launch, 8-week scale-up, ongoing monitoring
    """)
    
    # Footer
    st.markdown("---")
    st.caption("""
    **EED (Eye Exam for Patients with Diabetes)** | 🆕 ENHANCED HEDIS MY2025 | Tier 1 Triple-Weighted ⭐⭐⭐  
    Last updated: {} | AI-Assisted Screening Qualified ✅ | Compliance: ✅
    """.format(datetime.now().strftime('%Y-%m-%d')))


# Run dashboard
if __name__ == "__main__":
    create_eed_dashboard()

