"""
Date and number formatting utilities
"""
from datetime import datetime, date
from typing import Union


def format_date_mmddyyyy(input_date: Union[datetime, date]) -> str:
    """
    Format date as MM/DD/YYYY
    
    Args:
        input_date: datetime or date object
    
    Returns:
        Formatted string: MM/DD/YYYY
    """
    if isinstance(input_date, datetime):
        return input_date.strftime("%m/%d/%Y")
    elif isinstance(input_date, date):
        return input_date.strftime("%m/%d/%Y")
    else:
        return str(input_date)


def format_date_range(start: Union[datetime, date], end: Union[datetime, date]) -> str:
    """
    Format date range as MM/DD/YYYY - MM/DD/YYYY
    
    Args:
        start: Start date
        end: End date
    
    Returns:
        Formatted string
    """
    return f"{format_date_mmddyyyy(start)} - {format_date_mmddyyyy(end)}"


def format_date_with_duration(start: Union[datetime, date], end: Union[datetime, date]) -> str:
    """
    Format date range with duration
    
    Args:
        start: Start date
        end: End date
    
    Returns:
        Formatted string with duration
    """
    if isinstance(start, date) and isinstance(end, date):
        days = (end - start).days
        return f"{format_date_mmddyyyy(start)} - {format_date_mmddyyyy(end)} ({days} days)"
    return format_date_range(start, end)

