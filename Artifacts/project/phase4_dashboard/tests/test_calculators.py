"""
Tests for calculator logic
"""
import pytest
from src.models.calculator import ROICalculator, StarRatingCalculator


def test_roi_calculation(sample_member_data):
    """Test ROI calculator with sample data"""
    calculator = ROICalculator()
    result = calculator.calculate_intervention_roi(sample_member_data, intervention_cost_per_member=50)
    
    assert 'roi_percentage' in result
    assert result['roi_percentage'] > 0
    assert result['net_value'] > 0
    assert result['total_members'] == 3


def test_roi_calculation_empty_data():
    """Test ROI calculator with empty data"""
    import pandas as pd
    calculator = ROICalculator()
    result = calculator.calculate_intervention_roi(pd.DataFrame(), intervention_cost_per_member=50)
    
    assert result['total_members'] == 0
    assert result['roi_percentage'] == 0


def test_star_rating_impact():
    """Test Star Rating impact calculation"""
    impact = StarRatingCalculator.calculate_measure_impact(
        current_rate=85.0,
        predicted_rate=90.0,
        measure_weight=3.0
    )
    
    assert impact > 0
    assert impact < 1


def test_star_rating_overall_rating():
    """Test overall star rating calculation"""
    measure_impacts = {
        'HbA1c_Testing': 0.1,
        'BP_Control': 0.15,
        'Breast_Cancer_Screening': 0.05
    }
    
    rating = StarRatingCalculator.calculate_overall_rating(
        measure_impacts=measure_impacts,
        base_rating=4.0
    )
    
    assert 1.0 <= rating <= 5.0
    assert rating > 4.0  # Should improve from base


def test_star_rating_clamping():
    """Test that star rating is clamped between 1 and 5"""
    # Test upper bound
    measure_impacts = {'Measure1': 10.0}  # Very large impact
    rating = StarRatingCalculator.calculate_overall_rating(
        measure_impacts=measure_impacts,
        base_rating=4.0
    )
    assert rating == 5.0
    
    # Test lower bound
    measure_impacts = {'Measure1': -10.0}  # Very negative impact
    rating = StarRatingCalculator.calculate_overall_rating(
        measure_impacts=measure_impacts,
        base_rating=2.0
    )
    assert rating == 1.0

