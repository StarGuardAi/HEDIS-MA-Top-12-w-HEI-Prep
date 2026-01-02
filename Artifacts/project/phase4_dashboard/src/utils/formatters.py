"""
Date and number formatting utilities
"""
from datetime import datetime, date
from typing import Union, Optional


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


# ============================================================================
# SAFE DATA CONVERSION UTILITIES
# ============================================================================

def safe_float(value, default=0.0):
    """
    Safely convert value to float, return default if None or invalid
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Float value or default
    """
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value, default=0):
    """Safely convert to int"""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_percent(value, default=0.0):
    """Safely convert to percentage (0-100)"""
    float_val = safe_float(value, default)
    return float_val * 100 if float_val <= 1.0 else float_val


# ============================================================================
# MEASURE NAME MAPPING
# ============================================================================

MEASURE_NAME_MAP = {
    # Map various formats to standard names
    "HbA1c Testing": "HbA1c Testing (CDC)",
    "CDC": "HbA1c Testing (CDC)",
    "Blood Pressure Control": "Blood Pressure Control (CBP)",
    "CBP": "Blood Pressure Control (CBP)",
    "Colorectal Cancer Screening": "Colorectal Cancer Screening (COL)",
    "COL": "Colorectal Cancer Screening (COL)",
    "Breast Cancer Screening": "Breast Cancer Screening (BCS)",
    "BCS": "Breast Cancer Screening (BCS)",
    "Controlling High Blood Pressure": "Controlling High Blood Pressure (CBP)",
    "Diabetes Care - Eye Exam": "Diabetes Eye Exam (EED)",
    "Diabetes Eye Exam": "Diabetes Eye Exam (EED)",
    "EED": "Diabetes Eye Exam (EED)",
    "Diabetes Kidney Disease Monitoring": "Diabetes Kidney Disease Monitoring (KED)",
    "KED": "Diabetes Kidney Disease Monitoring (KED)",
    "Statin Therapy for CVD": "Statin Therapy for CVD (SPC)",
    "Statin Therapy - Cardiovascular Disease": "Statin Therapy for CVD (SPC)",
    "SPC": "Statin Therapy for CVD (SPC)",
    "Follow-Up After ED - Mental Health": "Follow-Up After ED - Mental Health (FUM)",
    "FUM": "Follow-Up After ED - Mental Health (FUM)",
    "Antidepressant Medication Management": "Antidepressant Medication Management (AMM)",
    "AMM": "Antidepressant Medication Management (AMM)",
    "Plan All-Cause Readmissions": "Plan All-Cause Readmissions (PCR)",
    "PCR": "Plan All-Cause Readmissions (PCR)",
    "Medication Adherence - Diabetes": "Medication Adherence - Diabetes (MAD)",
    "MAD": "Medication Adherence - Diabetes (MAD)",
    # Add more mappings as needed
}


def standardize_measure_names(df):
    """
    Standardize measure names in DataFrame to match filter names
    
    Args:
        df: DataFrame with 'measure_name' column (or similar)
    
    Returns:
        DataFrame with standardized measure names
    """
    import pandas as pd
    
    if not isinstance(df, pd.DataFrame) or df.empty:
        return df
    
    # Try different possible column names for measures
    measure_col = None
    for col in ['measure_name', 'measure', 'measure_code', 'hedis_measure', 'Measure']:
        if col in df.columns:
            measure_col = col
            break
    
    if measure_col:
        df = df.copy()
        df[measure_col] = df[measure_col].map(
            lambda x: MEASURE_NAME_MAP.get(str(x).strip(), str(x).strip()) if pd.notna(x) else x
        )
    
    return df

