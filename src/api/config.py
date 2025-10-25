"""
API Configuration Settings
Manages environment-specific configuration for the HEDIS API.
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class APISettings(BaseSettings):
    """
    API Configuration with environment variable support.
    
    Environment variables can override these defaults:
    - API_TITLE, API_VERSION, API_ENV, etc.
    """
    
    # API Metadata
    api_title: str = Field(
        default="HEDIS Star Rating Portfolio Optimizer API",
        description="API title displayed in OpenAPI docs"
    )
    api_version: str = Field(default="2.0.0", description="API version")
    api_description: str = Field(
        default="Production-ready API for 12 HEDIS measures prediction and portfolio optimization",
        description="API description"
    )
    
    # Environment
    environment: str = Field(
        default="development",
        description="Environment: development, staging, production"
    )
    debug: bool = Field(default=True, description="Debug mode")
    
    # Server
    host: str = Field(default="0.0.0.0", description="API host")
    port: int = Field(default=8000, description="API port")
    reload: bool = Field(default=True, description="Auto-reload on code changes")
    
    # CORS
    cors_enabled: bool = Field(default=True, description="Enable CORS")
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000", "http://localhost:8501"],
        description="Allowed CORS origins"
    )
    
    # Authentication
    api_key_header: str = Field(
        default="X-API-Key",
        description="API key header name"
    )
    default_api_key: Optional[str] = Field(
        default="dev-key-12345",
        description="Default API key for development"
    )
    
    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_requests: int = Field(
        default=100,
        description="Max requests per minute per API key"
    )
    rate_limit_window: int = Field(
        default=60,
        description="Rate limit window in seconds"
    )
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or text")
    log_requests: bool = Field(default=True, description="Log all requests")
    
    # Model Configuration
    models_dir: str = Field(default="models", description="Directory containing trained models")
    load_models_on_startup: bool = Field(
        default=True,
        description="Load all models at startup (vs lazy loading)"
    )
    
    # Caching
    cache_enabled: bool = Field(default=True, description="Enable in-memory caching")
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds")
    
    # Performance
    max_batch_size: int = Field(
        default=1000,
        description="Maximum batch prediction size"
    )
    enable_shap: bool = Field(
        default=True,
        description="Enable SHAP value calculation"
    )
    
    # Security
    hash_member_ids: bool = Field(
        default=True,
        description="Hash member IDs for PHI protection"
    )
    
    class Config:
        env_prefix = "API_"
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = APISettings()


def get_settings() -> APISettings:
    """Dependency to get settings in FastAPI endpoints."""
    return settings

