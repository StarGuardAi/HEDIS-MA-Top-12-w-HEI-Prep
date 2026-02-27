"""
HEDIS Portfolio Optimizer - Main Application Entry Point

This is the main entry point for the Streamlit application.
All business logic should be in src/ modules.
"""
import streamlit as st

from config.settings import APP_CONFIG
from src.utils.state import init_session_state
from src.ui.layout import setup_page_config, render_header
from src.ui.pages import dashboard, measures, members, analytics


def main():
    """Main application entry point"""
    # Setup
    setup_page_config()
    init_session_state()
    
    # Render
    render_header()
    
    # Navigation
    page = st.sidebar.selectbox("Navigate", ["Dashboard", "Measures", "Members", "Analytics"])
    
    if page == "Dashboard":
        dashboard.render()
    elif page == "Measures":
        measures.render()
    elif page == "Members":
        members.render()
    else:
        analytics.render()


if __name__ == "__main__":
    main()

