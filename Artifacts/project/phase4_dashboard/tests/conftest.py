"""
Pytest configuration and fixtures
"""
import pytest
import pandas as pd


@pytest.fixture
def sample_member_data():
    """Sample member data for testing"""
    return pd.DataFrame({
        'member_id': ['M001', 'M002', 'M003'],
        'member_name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'measure_name': ['HbA1c_Testing', 'BP_Control', 'HbA1c_Testing'],
        'gap_status': ['Open', 'Open', 'Closed'],
        'predicted_closure_probability': [0.85, 0.72, 0.95],
        'financial_value': [300, 250, 300],
        'risk_score': [0.75, 0.68, 0.82],
        'state': ['CA', 'TX', 'FL'],
        'zip_code': ['90210', '75001', '33101']
    })


@pytest.fixture
def sample_measures_data():
    """Sample measure data for testing"""
    return pd.DataFrame({
        'measure_name': ['HbA1c_Testing', 'BP_Control'],
        'current_rate': [85.0, 78.5],
        'benchmark_rate': [90.0, 82.0],
        'gap_count': [150, 220],
        'total_value': [45000, 55000]
    })


@pytest.fixture
def sample_portfolio_summary():
    """Sample portfolio summary data for testing"""
    return pd.DataFrame({
        'roi_percentage': [498],
        'star_rating': [4.5],
        'member_count': [10000],
        'compliance_rate': [85]
    })
