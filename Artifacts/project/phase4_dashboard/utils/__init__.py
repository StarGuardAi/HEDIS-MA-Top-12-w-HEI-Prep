"""Phase 4 Dashboard Utilities"""
# Import only essential functions - direct imports for reliability
# These are imported directly by app.py and pages, so they must work
from .database import execute_query, get_connection, show_db_status

# Import query functions
from .queries import (
    get_budget_variance_by_measure_query,
    get_cost_per_closure_by_activity_query,
    get_cost_tier_comparison_query,
    get_monthly_intervention_trend_query,
    get_portfolio_summary_query,
    get_roi_by_measure_query,
)

# Import data helper functions
from .data_helpers import (
    format_date_display,
    format_month_display,
    get_data_date_range,
    show_data_availability_warning,
)

__all__ = [
    "execute_query",
    "get_connection",
    "show_db_status",
    "get_roi_by_measure_query",
    "get_cost_per_closure_by_activity_query",
    "get_monthly_intervention_trend_query",
    "get_budget_variance_by_measure_query",
    "get_cost_tier_comparison_query",
    "get_portfolio_summary_query",
    "format_date_display",
    "format_month_display",
    "get_data_date_range",
    "show_data_availability_warning",
]

