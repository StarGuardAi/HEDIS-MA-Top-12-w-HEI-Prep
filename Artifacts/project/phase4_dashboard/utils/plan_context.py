"""
Phase 4 Dashboard - Plan Context Utilities
Handles plan context data for consistent narrative storytelling
"""
from typing import Dict, Optional
from utils.database import execute_query


def get_plan_context() -> Optional[Dict]:
    """
    Get plan context information from database.
    Returns None if table doesn't exist or no data found.
    """
    try:
        query = """
            SELECT 
                plan_name,
                total_members,
                active_members,
                star_rating_2023,
                star_rating_2024,
                star_rating_projected_2025,
                bonus_revenue_at_risk,
                geographic_region,
                plan_type,
                year_established,
                member_growth_yoy
            FROM plan_context
            ORDER BY context_id DESC
            LIMIT 1;
        """
        df = execute_query(query)
        
        if df.empty:
            # Return defaults if table doesn't exist or is empty
            return {
                'plan_name': 'Mid-Atlantic Medicare Advantage',
                'total_members': 10000,
                'active_members': 10000,
                'star_rating_2023': 4.0,
                'star_rating_2024': 4.0,
                'star_rating_projected_2025': 4.5,
                'bonus_revenue_at_risk': 2500000.00,
                'geographic_region': 'Pittsburgh Metro Area',
                'plan_type': 'Regional Medicare Advantage',
                'year_established': 2015,
                'member_growth_yoy': -5.2
            }
        
        # Convert to dict, handling Decimal types
        row = df.iloc[0]
        return {
            'plan_name': str(row['plan_name']),
            'total_members': int(row['total_members']),
            'active_members': int(row['active_members']),
            'star_rating_2023': float(row['star_rating_2023']),
            'star_rating_2024': float(row['star_rating_2024']),
            'star_rating_projected_2025': float(row['star_rating_projected_2025']),
            'bonus_revenue_at_risk': float(row['bonus_revenue_at_risk']),
            'geographic_region': str(row['geographic_region']),
            'plan_type': str(row['plan_type']),
            'year_established': int(row['year_established']),
            'member_growth_yoy': float(row['member_growth_yoy'])
        }
    except Exception:
        # If table doesn't exist, return defaults
        return {
            'plan_name': 'Mid-Atlantic Medicare Advantage',
            'total_members': 10000,
            'active_members': 10000,
            'star_rating_2023': 4.0,
            'star_rating_2024': 4.0,
            'star_rating_projected_2025': 4.5,
            'bonus_revenue_at_risk': 2500000.00,
            'geographic_region': 'Pittsburgh Metro Area',
            'plan_type': 'Regional Medicare Advantage',
            'year_established': 2015,
            'member_growth_yoy': -5.2
        }


def get_plan_size_scenarios() -> Dict:
    """
    Get predefined plan size scenarios with characteristics.
    """
    return {
        10000: {
            'name': 'Small Plan',
            'label': '10K members',
            'description': 'Regional plan baseline - Current case study',
            'investment_range': '$50K-$150K',
            'implementation_complexity': 'Low',
            'typical_characteristics': 'Agile, quick decision-making, focused markets'
        },
        25000: {
            'name': 'Mid-Size Plan',
            'label': '25K members',
            'description': 'Expanded regional presence',
            'investment_range': '$125K-$375K',
            'implementation_complexity': 'Medium',
            'typical_characteristics': 'Multiple markets, structured operations'
        },
        50000: {
            'name': 'Large Plan',
            'label': '50K members',
            'description': 'Multi-state operations',
            'investment_range': '$250K-$750K',
            'implementation_complexity': 'High',
            'typical_characteristics': 'Enterprise processes, multiple departments'
        },
        100000: {
            'name': 'Enterprise Plan',
            'label': '100K+ members',
            'description': 'Major market player',
            'investment_range': '$500K-$1.5M',
            'implementation_complexity': 'Very High',
            'typical_characteristics': 'Complex operations, phased rollouts'
        }
    }


def get_industry_benchmarks() -> Dict:
    """
    Get industry benchmark comparison data.
    """
    return {
        'gap_closure_rate': {
            'display_name': 'Gap Closure Rate',
            'industry_avg': '28-35%',
            'this_plan': '42.4%',
            'status': 'Above',
            'icon': '✓'
        },
        'cost_per_closure': {
            'display_name': 'Cost Per Closure',
            'industry_avg': '$95-150',
            'this_plan': '$77.51',
            'status': 'Below',
            'icon': '✓'
        },
        'roi_first_quarter': {
            'display_name': 'ROI (First Quarter)',
            'industry_avg': '1.0-1.2x',
            'this_plan': '1.29x',
            'status': 'Above',
            'icon': '✓'
        },
        'digital_success_rate': {
            'display_name': 'Digital Success Rate',
            'industry_avg': '25-30%',
            'this_plan': '46.4%',
            'status': 'Above',
            'icon': '✓'
        }
    }

