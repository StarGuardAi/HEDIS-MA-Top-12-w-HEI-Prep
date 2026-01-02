"""
Core module for HEDIS Portfolio Optimizer

Provides foundational components:
- Configuration management
- Logging
- Exception handling
- Type definitions
"""

from .config import Settings, get_settings
from .logging import setup_logging, get_logger
from .exceptions import (
    HEDISError,
    DatabaseError,
    ValidationError,
    BusinessLogicError
)

__all__ = [
    'Settings',
    'get_settings',
    'setup_logging',
    'get_logger',
    'HEDISError',
    'DatabaseError',
    'ValidationError',
    'BusinessLogicError',
]

