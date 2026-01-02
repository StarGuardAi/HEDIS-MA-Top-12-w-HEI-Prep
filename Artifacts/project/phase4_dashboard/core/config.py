"""
Configuration Management

Centralized configuration using Pydantic Settings for type safety and validation.
Supports environment variables, secrets, and default values.
"""

import os
from typing import Optional, List
from functools import lru_cache

try:
    from pydantic_settings import BaseSettings
    from pydantic import Field, validator
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings, Field, validator


class DatabaseConfig(BaseSettings):
    """Database configuration"""
    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    name: str = Field(default="hedis_portfolio", env="DB_NAME")
    user: str = Field(default="hedis_api", env="DB_USER")
    password: str = Field(default="hedis_password", env="DB_PASSWORD")
    pool_size: int = Field(default=5, env="DB_POOL_SIZE")
    max_overflow: int = Field(default=10, env="DB_MAX_OVERFLOW")
    
    class Config:
        env_prefix = "DB_"
        case_sensitive = False


class APIConfig(BaseSettings):
    """External API configuration"""
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    anthropic_model: str = Field(default="claude-3-opus-20240229", env="ANTHROPIC_MODEL")
    api_timeout: int = Field(default=30, env="API_TIMEOUT")
    
    class Config:
        env_prefix = "API_"
        case_sensitive = False


class CacheConfig(BaseSettings):
    """Caching configuration"""
    enabled: bool = Field(default=True, env="CACHE_ENABLED")
    ttl: int = Field(default=3600, env="CACHE_TTL")
    max_size: int = Field(default=1000, env="CACHE_MAX_SIZE")
    
    class Config:
        env_prefix = "CACHE_"
        case_sensitive = False


class LoggingConfig(BaseSettings):
    """Logging configuration"""
    level: str = Field(default="INFO", env="LOG_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    file_path: Optional[str] = Field(default=None, env="LOG_FILE_PATH")
    max_bytes: int = Field(default=10485760, env="LOG_MAX_BYTES")  # 10MB
    backup_count: int = Field(default=5, env="LOG_BACKUP_COUNT")
    
    @validator('level')
    def validate_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()
    
    class Config:
        env_prefix = "LOG_"
        case_sensitive = False


class SecurityConfig(BaseSettings):
    """Security configuration"""
    secret_key: str = Field(default="change-me-in-production", env="SECRET_KEY")
    allowed_hosts: List[str] = Field(default=["*"], env="ALLOWED_HOSTS")
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")
    
    class Config:
        env_prefix = "SECRET_"
        case_sensitive = False


class Settings(BaseSettings):
    """Application settings"""
    
    # Application metadata
    app_name: str = "HEDIS Portfolio Optimizer"
    app_version: str = "4.0.0"
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Component configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    
    # Streamlit specific
    streamlit_port: int = Field(default=8501, env="STREAMLIT_PORT")
    streamlit_host: str = Field(default="localhost", env="STREAMLIT_HOST")
    
    # Feature flags
    enable_ai_insights: bool = Field(default=True, env="ENABLE_AI_INSIGHTS")
    enable_ml_predictions: bool = Field(default=True, env="ENABLE_ML_PREDICTIONS")
    enable_audit_logging: bool = Field(default=True, env="ENABLE_AUDIT_LOGGING")
    
    @validator('environment')
    def validate_environment(cls, v):
        valid_envs = ['development', 'staging', 'production']
        if v.lower() not in valid_envs:
            raise ValueError(f"Environment must be one of {valid_envs}")
        return v.lower()
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Allow reading from Streamlit secrets
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            # Try to get settings from Streamlit secrets if available
            try:
                import streamlit as st
                if hasattr(st, 'secrets'):
                    return (
                        init_settings,
                        env_settings,
                        file_secret_settings,
                        StreamlitSecretsSettingsSource(),
                    )
            except ImportError:
                pass
            return (init_settings, env_settings, file_secret_settings)


class StreamlitSecretsSettingsSource:
    """Custom settings source for Streamlit secrets"""
    def __call__(self, settings: BaseSettings) -> dict:
        try:
            import streamlit as st
            if hasattr(st, 'secrets'):
                return dict(st.secrets)
        except (ImportError, AttributeError):
            pass
        return {}


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached)
    
    Returns:
        Settings: Application configuration object
    """
    return Settings()

