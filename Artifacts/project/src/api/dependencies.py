"""
API Dependencies
Reusable dependency injection functions for FastAPI endpoints.
"""

import time
from typing import Dict, Any
from fastapi import Depends, Header, HTTPException, status
from .config import get_settings, APISettings
import hashlib


# ===== Configuration Dependency =====

async def get_config() -> APISettings:
    """Get API configuration settings."""
    return get_settings()


# ===== Request Tracking =====

_request_start_times: Dict[str, float] = {}


async def track_request_start(request_id: str = Header(default=None)) -> Dict[str, Any]:
    """
    Track request start time for performance monitoring.
    
    Returns:
        Dict with request_id and start_time
    """
    import uuid
    
    if not request_id:
        request_id = str(uuid.uuid4())
    
    start_time = time.time()
    _request_start_times[request_id] = start_time
    
    return {
        "request_id": request_id,
        "start_time": start_time
    }


async def get_request_duration(request_info: Dict = Depends(track_request_start)) -> float:
    """Calculate request duration in milliseconds."""
    start_time = request_info["start_time"]
    duration_ms = (time.time() - start_time) * 1000
    return duration_ms


# ===== PHI Protection =====

def hash_member_id(member_id: str) -> str:
    """
    Hash member ID using SHA-256 for PHI protection.
    
    Args:
        member_id: Raw member identifier
        
    Returns:
        SHA-256 hash (first 16 characters for readability)
    """
    hash_obj = hashlib.sha256(member_id.encode())
    return hash_obj.hexdigest()[:16]


# ===== Model Loading =====

class ModelCache:
    """
    Singleton cache for loaded ML models.
    Models are loaded once at startup and reused.
    """
    _instance = None
    _models: Dict[str, Any] = {}
    _scalers: Dict[str, Any] = {}
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_all_models(self):
        """Load all 12 measure models at startup."""
        # This will be implemented in prediction endpoints
        # For now, just mark as initialized
        self._initialized = True
    
    def get_model(self, measure_code: str):
        """Get cached model for measure."""
        return self._models.get(measure_code)
    
    def get_scaler(self, measure_code: str):
        """Get cached scaler for measure."""
        return self._scalers.get(measure_code)
    
    def set_model(self, measure_code: str, model: Any):
        """Cache model for measure."""
        self._models[measure_code] = model
    
    def set_scaler(self, measure_code: str, scaler: Any):
        """Cache scaler for measure."""
        self._scalers[measure_code] = scaler
    
    @property
    def is_initialized(self) -> bool:
        """Check if models are loaded."""
        return self._initialized


# Global model cache instance
model_cache = ModelCache()


async def get_model_cache() -> ModelCache:
    """Dependency to get model cache."""
    return model_cache

