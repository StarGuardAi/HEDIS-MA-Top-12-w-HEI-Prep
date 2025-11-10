"""
Common Schema Definitions
Shared Pydantic models used across multiple endpoints.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """
    Standard error response format.
    Used for all API errors with PHI-safe messages.
    """
    error: str = Field(..., description="Error type or title")
    detail: str = Field(..., description="Detailed error message")
    status_code: int = Field(..., description="HTTP status code")
    request_id: str = Field(..., description="Unique request identifier")
    timestamp: float = Field(..., description="Unix timestamp of error")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Validation Error",
                "detail": "Invalid measure code",
                "status_code": 422,
                "request_id": "abc123def456",
                "timestamp": 1698172800.0
            }
        }


class HealthResponse(BaseModel):
    """
    Health check response.
    """
    status: str = Field(..., description="Health status: healthy, unhealthy, degraded")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment: development, staging, production")
    models_loaded: Optional[bool] = Field(None, description="Whether ML models are loaded")
    uptime_seconds: Optional[float] = Field(None, description="API uptime in seconds")
    timestamp: float = Field(..., description="Current timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "2.0.0",
                "environment": "production",
                "models_loaded": True,
                "uptime_seconds": 3600.5,
                "timestamp": 1698172800.0
            }
        }


class MessageResponse(BaseModel):
    """
    Simple message response.
    """
    message: str = Field(..., description="Response message")
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp())
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation successful",
                "timestamp": 1698172800.0
            }
        }

