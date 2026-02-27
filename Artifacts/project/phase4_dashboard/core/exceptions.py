"""
Custom Exception Classes

Hierarchical exception structure for better error handling and debugging.
"""

from typing import Optional, Dict, Any


class HEDISError(Exception):
    """Base exception for all HEDIS Portfolio Optimizer errors"""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses"""
        return {
            'error': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code,
            'details': self.details
        }


class DatabaseError(HEDISError):
    """Database-related errors"""
    pass


class ValidationError(HEDISError):
    """Data validation errors"""
    pass


class BusinessLogicError(HEDISError):
    """Business logic violation errors"""
    pass


class ConfigurationError(HEDISError):
    """Configuration errors"""
    pass


class ExternalServiceError(HEDISError):
    """External service integration errors"""
    pass


class AuthenticationError(HEDISError):
    """Authentication/authorization errors"""
    pass


class NotFoundError(HEDISError):
    """Resource not found errors"""
    pass

