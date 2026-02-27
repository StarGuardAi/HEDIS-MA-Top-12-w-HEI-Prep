"""
Data Validation Utilities
Ensures no zero data points across all pages for better user experience
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional


def ensure_no_zero_data(df: pd.DataFrame, columns: Optional[list] = None, replacement_method: str = "median") -> pd.DataFrame:
    """
    Ensure no zero values in critical columns by replacing with reasonable defaults.
    
    Args:
        df: DataFrame to process
        columns: List of column names to check. If None, checks common numeric columns
        replacement_method: Method to use for replacement ('median', 'mean', 'min_nonzero', 'default')
    
    Returns:
        DataFrame with zero values replaced
    """
    df_clean = df.copy()
    
    # Default columns to check if not specified
    if columns is None:
        columns = [col for col in df_clean.columns if df_clean[col].dtype in [np.float64, np.int64, float, int]]
    
    for col in columns:
        if col not in df_clean.columns:
            continue
            
        # Check for zeros and negative values
        zero_mask = (df_clean[col] == 0) | (df_clean[col] < 0) | df_clean[col].isna()
        
        if zero_mask.any():
            if replacement_method == "median":
                replacement_value = df_clean[col].replace(0, np.nan).median()
            elif replacement_method == "mean":
                replacement_value = df_clean[col].replace(0, np.nan).mean()
            elif replacement_method == "min_nonzero":
                replacement_value = df_clean[col][df_clean[col] > 0].min()
            else:  # default
                replacement_value = 1.0
            
            # Use column-specific defaults if median/mean is still zero or NaN
            if pd.isna(replacement_value) or replacement_value == 0:
                if 'investment' in col.lower() or 'cost' in col.lower():
                    replacement_value = 1000.0
                elif 'revenue' in col.lower() or 'impact' in col.lower():
                    replacement_value = 1000.0
                elif 'rate' in col.lower() or 'ratio' in col.lower():
                    replacement_value = 0.1
                elif 'success' in col.lower() or 'closure' in col.lower():
                    replacement_value = 10.0
                else:
                    replacement_value = 1.0
            
            df_clean.loc[zero_mask, col] = replacement_value
    
    return df_clean


def ensure_minimum_values(df: pd.DataFrame, min_values: Dict[str, float]) -> pd.DataFrame:
    """
    Ensure columns meet minimum threshold values.
    
    Args:
        df: DataFrame to process
        min_values: Dictionary mapping column names to minimum values
    
    Returns:
        DataFrame with values below minimum replaced
    """
    df_clean = df.copy()
    
    for col, min_val in min_values.items():
        if col in df_clean.columns:
            df_clean.loc[df_clean[col] < min_val, col] = min_val
    
    return df_clean


def validate_scenario_data(scenario_result: dict) -> dict:
    """
    Validate scenario result data to ensure no zero values.
    
    Args:
        scenario_result: Dictionary containing scenario results
    
    Returns:
        Validated scenario result dictionary
    """
    validated = scenario_result.copy()
    
    # Ensure minimum values
    validated['total_investment'] = max(validated.get('total_investment', 0), 1000)
    validated['total_revenue'] = max(validated.get('total_revenue', 0), 1000)
    validated['net_benefit'] = validated['total_revenue'] - validated['total_investment']
    validated['roi_ratio'] = max(validated.get('roi_ratio', 0), 0.1)
    validated['success_rate_boost'] = max(validated.get('success_rate_boost', 0), 0)
    validated['investment_multiplier'] = max(validated.get('investment_multiplier', 0), 0.1)
    
    return validated


