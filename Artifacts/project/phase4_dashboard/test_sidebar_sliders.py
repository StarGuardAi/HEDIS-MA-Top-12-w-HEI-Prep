import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sidebar Slider Test", layout="wide")

# Initialize session state
if 'membership_slider_widget' not in st.session_state:
    st.session_state.membership_slider_widget = 10000

if 'min_members_widget' not in st.session_state:
    st.session_state.min_members_widget = 0

# SIDEBAR
with st.sidebar:
    st.title("🎛️ Test Filters")
    
    # Membership slider
    st.markdown("### 🏥 Plan Membership Size")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("10K", key="btn_10k"):
            st.session_state.membership_slider_widget = 10000
            st.rerun()
    with col2:
        if st.button("50K", key="btn_50k"):
            st.session_state.membership_slider_widget = 50000
            st.rerun()
    
    st.slider(
        "Total Membership",
        5000, 250000,
        st.session_state.membership_slider_widget,
        5000,
        key="membership_slider_widget"
    )
    st.write(f"Value: {st.session_state.membership_slider_widget}")
    
    st.markdown("---")
    
    # Threshold slider
    st.markdown("### 🎯 Threshold")
    st.slider(
        "Min Members",
        0, 1000,
        st.session_state.min_members_widget,
        25,
        key="min_members_widget"
    )
    st.write(f"Value: {st.session_state.min_members_widget}")
    
    # Debug panel
    with st.expander("🐛 DEBUG", expanded=True):
        st.write(st.session_state)

# MAIN CONTENT
st.title("Main Content Area")
st.write(f"Membership from sidebar: {st.session_state.membership_slider_widget}")
st.write(f"Min members from sidebar: {st.session_state.min_members_widget}")

st.markdown("---")
st.write("**Test Instructions:**")
st.write("1. Try dragging the sliders in the sidebar")
st.write("2. Watch the debug panel - do values change?")
st.write("3. Try clicking the 10K/50K buttons")
st.write("4. Do the values in the main content update?")

