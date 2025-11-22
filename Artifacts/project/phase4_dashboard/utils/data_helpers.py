"""
Phase 4 Dashboard - Data Helper Functions
Helper functions for data validation and feedback
"""
import streamlit as st
from datetime import datetime
from typing import Tuple, Optional, Union
from .database import get_connection


def format_date_display(date: Union[datetime, str]) -> str:
    """
    Format a date for display as MM/DD/YYYY.
    
    Args:
        date: datetime object or date string
        
    Returns:
        Formatted date string as MM/DD/YYYY
    """
    if isinstance(date, str):
        try:
            # Try to parse YYYY-MM-DD format
            date = datetime.strptime(date, "%Y-%m-%d")
        except:
            # Try to parse YYYY-MM format (for monthly data)
            try:
                date = datetime.strptime(date, "%Y-%m")
                return date.strftime("%m/%Y")
            except:
                return date  # Return as-is if can't parse
    
    if hasattr(date, 'strftime'):
        return date.strftime("%m/%d/%Y")
    return str(date)


def format_month_display(month_str: str) -> str:
    """
    Format a month string (YYYY-MM) for display as MM/YYYY.
    
    Args:
        month_str: Month string in YYYY-MM format (e.g., "2024-10")
        
    Returns:
        Formatted month string as MM/YYYY (e.g., "10/2024")
    """
    try:
        # Parse YYYY-MM format
        date = datetime.strptime(month_str, "%Y-%m")
        return date.strftime("%m/%Y")
    except:
        return month_str  # Return as-is if can't parse


def get_data_date_range() -> Optional[Tuple[datetime, datetime]]:
    """
    Get the available date range from the database.
    Returns: (min_date, max_date) tuple or None if no data
    """
    try:
        conn, _ = get_connection()  # Unpack connection and count
        if conn is None:
            return None, None
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(intervention_date) as min_date, MAX(intervention_date) as max_date FROM member_interventions")
        date_range = cursor.fetchone()
        cursor.close()
        # Don't close cached connection - it's managed by st.cache_resource
        
        if date_range and date_range[0] and date_range[1]:
            return (date_range[0], date_range[1])
        return None
    except:
        return None


def show_data_availability_warning(selected_start: datetime, selected_end: datetime):
    """
    Show a warning if the selected date range is outside available data.
    """
    date_range = get_data_date_range()
    
    if date_range:
        available_start, available_end = date_range
        
        # Format dates for display as MM/DD/YYYY
        available_start_str = format_date_display(available_start)
        available_end_str = format_date_display(available_end)
        selected_start_str = format_date_display(selected_start)
        selected_end_str = format_date_display(selected_end)
        
        # Check if selected range is outside available data (use YYYY-MM-DD for comparison)
        available_start_db = available_start.strftime("%Y-%m-%d") if hasattr(available_start, 'strftime') else str(available_start)
        available_end_db = available_end.strftime("%Y-%m-%d") if hasattr(available_end, 'strftime') else str(available_end)
        selected_start_db = selected_start.strftime("%Y-%m-%d")
        selected_end_db = selected_end.strftime("%Y-%m-%d")
        
        if selected_start_db < available_start_db or selected_end_db > available_end_db:
            st.warning(
                f"⚠️ **Date Range Notice:** Data is available from **{available_start_str}** to **{available_end_str}**. "
                f"Your selected range ({selected_start_str} to {selected_end_str}) may have limited or no data."
            )

