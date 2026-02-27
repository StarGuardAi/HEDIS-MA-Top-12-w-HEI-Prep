"""
Measures page
"""
import streamlit as st
from src.data.loaders import load_measures_data
from config.settings import HEDIS_MEASURES


def render():
    """Render measures page"""
    st.header("📋 HEDIS Measures")
    
    # Load measures data
    measures_df = load_measures_data()
    
    # Display measure definitions
    st.subheader("Measure Definitions")
    
    for measure_key, measure_info in HEDIS_MEASURES.items():
        with st.expander(f"{measure_info['name']} - {measure_info['category']}"):
            st.write(f"**Description**: {measure_info['description']}")
            st.write(f"**Star Rating Weight**: {measure_info['star_weight']}")
            st.write(f"**Category**: {measure_info['category']}")
    
    # Display measures data
    if not measures_df.empty:
        st.subheader("Measure Performance")
        st.dataframe(measures_df, use_container_width=True)
    else:
        st.info("No measures performance data available")

