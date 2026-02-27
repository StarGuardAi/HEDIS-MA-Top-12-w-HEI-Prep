"""
Members page
"""
import streamlit as st
from src.data.loaders import load_member_data
from src.models.calculator import ROICalculator


def render():
    """Render members page"""
    st.header("👥 Members")
    
    # Filters
    col1, col2 = st.columns(2, gap="small")
    with col1:
        selected_measures = st.multiselect(
            "Select Measures",
            options=['HbA1c_Testing', 'BP_Control', 'Breast_Cancer_Screening'],
            default=[]
        )
    with col2:
        show_high_priority = st.checkbox("Show High Priority Only", value=False)
    
    # Load member data
    members_df = load_member_data()
    
    # Filter by priority if requested
    if show_high_priority and not members_df.empty:
        if 'predicted_closure_probability' in members_df.columns:
            members_df = members_df[members_df['predicted_closure_probability'] >= 0.7]
    
    # Display members
    if not members_df.empty:
        st.subheader(f"Members ({len(members_df)})")
        st.dataframe(members_df, use_container_width=True)
        
        # Calculate ROI
        calculator = ROICalculator()
        roi_result = calculator.calculate_intervention_roi(members_df)
        
        st.subheader("ROI Analysis")
        col1, col2, col3 = st.columns(3, gap="small")
        with col1:
            st.metric("Total Members", roi_result['total_members'])
        with col2:
            st.metric("Predicted Value", f"${roi_result['predicted_value']:,.0f}")
        with col3:
            st.metric("ROI", f"{roi_result['roi_percentage']:.0f}%")
    else:
        st.info("No member data available")

