"""
Measure Analysis Utilities
Functions for analyzing HEDIS measure performance and gaps
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from utils.database import execute_query
from utils.measure_definitions import get_measure_definition


def get_measure_performance(measure_id: str, start_date: str, end_date: str) -> Dict:
    """
    Get comprehensive performance data for a measure.
    
    Returns:
        Dictionary with performance metrics, rates, and trends
    """
    # This would query actual database - placeholder structure
    return {
        "current_rate": 85.5,
        "benchmark_rate": 85.0,
        "numerator": 850,
        "denominator": 1000,
        "exclusions": 50,
        "rate_by_age": {
            "18-44": 88.2,
            "45-64": 85.1,
            "65-75": 83.5
        },
        "rate_by_gender": {
            "Male": 84.2,
            "Female": 86.8
        },
        "rate_by_risk_score": {
            "Low": 90.1,
            "Medium": 85.3,
            "High": 78.2
        },
        "trend_24_months": [
            {"month": "2023-01", "rate": 82.1},
            {"month": "2023-02", "rate": 82.5},
            # ... 24 months of data
        ]
    }


def get_gap_analysis(measure_id: str, start_date: str, end_date: str) -> Dict:
    """
    Get gap analysis for a measure.
    
    Returns:
        Dictionary with gap details, reasons, and closure metrics
    """
    return {
        "total_gaps": 150,
        "gaps_by_reason": {
            "Not Scheduled": 60,
            "Missed Appointment": 45,
            "Lab Pending": 30,
            "Provider Delay": 15
        },
        "average_days_to_close": 12.5,
        "closure_rate_by_intervention": {
            "Phone Call": 0.75,
            "Text Message": 0.60,
            "Mail": 0.45,
            "Provider Outreach": 0.85
        },
        "cost_per_closed_gap": 45.50,
        "gaps_by_priority": {
            "High": 50,
            "Medium": 70,
            "Low": 30
        }
    }


def get_members_with_gaps(
    measure_id: str,
    start_date: str,
    end_date: str,
    limit: int = 100
) -> pd.DataFrame:
    """
    Get members with gaps, prioritized by closure probability.
    
    Returns:
        DataFrame with member details and prioritization scores
    """
    # Placeholder - would query actual database
    data = {
        "member_id": [f"MEM{i:04d}" for i in range(1, limit + 1)],
        "member_name": [f"Member {i}" for i in range(1, limit + 1)],
        "age": np.random.randint(45, 75, limit),
        "gender": np.random.choice(["Male", "Female"], limit),
        "risk_score": np.random.choice(["Low", "Medium", "High"], limit),
        "gap_reason": np.random.choice(
            ["Not Scheduled", "Missed Appointment", "Lab Pending", "Provider Delay"],
            limit
        ),
        "days_since_gap": np.random.randint(1, 90, limit),
        "closure_probability": np.random.uniform(0.3, 0.95, limit),
        "priority": np.random.choice(["High", "Medium", "Low"], limit),
        "assigned_coordinator": [None] * limit,
        "last_contact_date": [None] * limit,
        "next_action": np.random.choice(
            ["Schedule Appointment", "Order Lab", "Follow Up", "Provider Outreach"],
            limit
        )
    }
    
    df = pd.DataFrame(data)
    
    # Sort by closure probability (descending)
    df = df.sort_values("closure_probability", ascending=False)
    
    return df


def calculate_closure_probability(
    member_data: Dict,
    historical_data: Optional[pd.DataFrame] = None
) -> float:
    """
    Calculate closure probability for a member based on various factors.
    
    Factors:
    - Age
    - Risk score
    - Gap reason
    - Days since gap
    - Historical closure rate
    """
    base_probability = 0.5
    
    # Age factor (younger members more likely to close)
    age = member_data.get("age", 60)
    if age < 50:
        base_probability += 0.15
    elif age > 70:
        base_probability -= 0.10
    
    # Risk score factor
    risk_score = member_data.get("risk_score", "Medium")
    if risk_score == "Low":
        base_probability += 0.10
    elif risk_score == "High":
        base_probability -= 0.15
    
    # Gap reason factor
    gap_reason = member_data.get("gap_reason", "Not Scheduled")
    reason_factors = {
        "Lab Pending": 0.20,  # Lab pending is easier to close
        "Not Scheduled": 0.10,
        "Missed Appointment": -0.05,
        "Provider Delay": -0.10
    }
    base_probability += reason_factors.get(gap_reason, 0)
    
    # Days since gap (recent gaps more likely to close)
    days_since = member_data.get("days_since_gap", 30)
    if days_since < 7:
        base_probability += 0.10
    elif days_since > 60:
        base_probability -= 0.15
    
    # Clamp between 0 and 1
    return max(0.0, min(1.0, base_probability))


def get_provider_performance(measure_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Get provider performance comparison for a measure."""
    # Placeholder - would query actual database
    data = {
        "provider_id": [f"PROV{i:03d}" for i in range(1, 21)],
        "provider_name": [f"Provider {i}" for i in range(1, 21)],
        "member_count": np.random.randint(10, 100, 20),
        "completion_rate": np.random.uniform(70.0, 95.0, 20),
        "average_days_to_complete": np.random.uniform(5.0, 25.0, 20),
        "quality_score": np.random.uniform(3.0, 5.0, 20)
    }
    
    df = pd.DataFrame(data)
    df = df.sort_values("completion_rate", ascending=False)
    
    return df


def get_geographic_performance(measure_id: str, start_date: str, end_date: str) -> Dict:
    """Get geographic performance map data."""
    return {
        "regions": [
            {"region": "Northeast", "rate": 87.2, "member_count": 250},
            {"region": "Southeast", "rate": 84.5, "member_count": 300},
            {"region": "Midwest", "rate": 86.1, "member_count": 200},
            {"region": "West", "rate": 85.8, "member_count": 250}
        ],
        "states": [
            {"state": "CA", "rate": 86.5, "member_count": 150},
            {"state": "NY", "rate": 88.1, "member_count": 120},
            {"state": "TX", "rate": 84.2, "member_count": 180}
        ]
    }


def get_best_practices(measure_id: str) -> Dict:
    """Get evidence-based best practices for a measure."""
    definition = get_measure_definition(measure_id)
    if not definition:
        return {}
    
    # Measure-specific best practices
    practices = {
        "HBA1C": {
            "interventions": [
                "Automated lab order reminders",
                "Provider education on testing frequency",
                "Member education on diabetes management",
                "Pharmacy-based testing programs"
            ],
            "success_stories": [
                "Plan A increased rate from 82% to 89% using automated reminders",
                "Plan B achieved 92% rate with pharmacy partnerships"
            ],
            "recommended_cadence": "Quarterly outreach, monthly for high-risk members"
        },
        "BP": {
            "interventions": [
                "Home blood pressure monitoring programs",
                "Pharmacist-led medication management",
                "Provider alerts for uncontrolled BP",
                "Member self-management support"
            ],
            "success_stories": [
                "Plan C improved control rate by 8% with home monitoring",
                "Plan D achieved 85% control with pharmacist partnerships"
            ],
            "recommended_cadence": "Monthly outreach for uncontrolled members"
        }
    }
    
    return practices.get(measure_id, {
        "interventions": ["Standard outreach protocols"],
        "success_stories": ["Industry best practices apply"],
        "recommended_cadence": "Quarterly outreach"
    })


def export_call_list(members_df: pd.DataFrame, format: str = "csv") -> str:
    """Export member list for calling."""
    if format == "csv":
        return members_df.to_csv(index=False)
    elif format == "excel":
        # Would use openpyxl for Excel export
        return members_df.to_csv(index=False)  # Placeholder
    return ""

