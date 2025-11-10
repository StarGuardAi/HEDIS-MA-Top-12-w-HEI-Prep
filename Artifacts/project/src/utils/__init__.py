"""
HEDIS Star Rating Portfolio Optimizer - Utilities Package

Provides utilities for:
- HEDIS measure specifications (hedis_specs.py)
- Star rating calculations (star_calculator.py)
- Data validation (data_validation.py)

Version: 2.0.0
"""

# Lazy imports - only load when explicitly requested
# This avoids loading pandas/numpy unless actually needed

__all__ = [
    'hedis_specs',
    'star_calculator',
    'data_validation',
]
