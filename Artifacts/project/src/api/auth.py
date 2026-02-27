"""
Authentication & Rate Limiting
API key authentication and rate limiting middleware.
"""

import time
import hashlib
import secrets
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from fastapi import Header, HTTPException, status, Request
from pydantic import BaseModel, Field

from .config import settings


# ===== API Key Models =====

class APIKey(BaseModel):
    """API Key model."""
    key_id: str = Field(..., description="Unique key identifier")
    hashed_key: str = Field(..., description="Hashed API key (SHA-256)")
    name: str = Field(..., description="Key name/description")
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    is_active: bool = Field(default=True)


# ===== API Key Management =====

class APIKeyManager:
    """
    Manage API keys with secure hashing and validation.
    
    Keys are stored as SHA-256 hashes for security.
    """
    
    def __init__(self):
        self._keys: Dict[str, APIKey] = {}
        
        # Add default development key
        if settings.default_api_key and settings.environment == "development":
            self.add_key(
                key=settings.default_api_key,
                name="Development Key",
                key_id="dev-key-001"
            )
    
    def generate_api_key(self) -> str:
        """
        Generate a new secure API key (32 bytes, hex encoded).
        
        Returns:
            str: New API key (64 characters hex)
        """
        return secrets.token_hex(32)
    
    def hash_key(self, key: str) -> str:
        """
        Hash API key using SHA-256.
        
        Args:
            key: Raw API key
            
        Returns:
            str: SHA-256 hash (hex)
        """
        return hashlib.sha256(key.encode()).hexdigest()
    
    def add_key(
        self,
        key: str,
        name: str,
        key_id: Optional[str] = None,
        expires_at: Optional[datetime] = None
    ) -> APIKey:
        """
        Add a new API key to the manager.
        
        Args:
            key: Raw API key (will be hashed)
            name: Key name/description
            key_id: Optional key ID (generated if not provided)
            expires_at: Optional expiration date
            
        Returns:
            APIKey: The created API key object
        """
        if not key_id:
            key_id = f"key-{secrets.token_hex(8)}"
        
        hashed = self.hash_key(key)
        
        api_key = APIKey(
            key_id=key_id,
            hashed_key=hashed,
            name=name,
            expires_at=expires_at
        )
        
        self._keys[hashed] = api_key
        
        return api_key
    
    def verify_key(self, key: str) -> Optional[APIKey]:
        """
        Verify an API key.
        
        Args:
            key: Raw API key to verify
            
        Returns:
            APIKey if valid, None otherwise
        """
        hashed = self.hash_key(key)
        api_key = self._keys.get(hashed)
        
        if not api_key:
            return None
        
        # Check if active
        if not api_key.is_active:
            return None
        
        # Check expiration
        if api_key.expires_at and datetime.now() > api_key.expires_at:
            return None
        
        return api_key
    
    def revoke_key(self, key: str) -> bool:
        """
        Revoke an API key.
        
        Args:
            key: Raw API key to revoke
            
        Returns:
            bool: True if revoked, False if not found
        """
        hashed = self.hash_key(key)
        api_key = self._keys.get(hashed)
        
        if api_key:
            api_key.is_active = False
            return True
        
        return False


# Global API key manager
api_key_manager = APIKeyManager()


# ===== Rate Limiting =====

class RateLimiter:
    """
    Simple in-memory rate limiter.
    
    Tracks requests per API key per time window.
    """
    
    def __init__(self, requests_per_window: int = 100, window_seconds: int = 60):
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self._requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, key_hash: str) -> tuple[bool, int]:
        """
        Check if request is allowed for this key.
        
        Args:
            key_hash: Hashed API key
            
        Returns:
            tuple: (allowed, remaining_requests)
        """
        now = time.time()
        window_start = now - self.window_seconds
        
        # Get requests for this key
        requests = self._requests[key_hash]
        
        # Remove old requests outside the window
        requests = [req_time for req_time in requests if req_time > window_start]
        self._requests[key_hash] = requests
        
        # Check if under limit
        if len(requests) < self.requests_per_window:
            # Add this request
            requests.append(now)
            remaining = self.requests_per_window - len(requests)
            return True, remaining
        else:
            remaining = 0
            return False, remaining
    
    def get_retry_after(self, key_hash: str) -> int:
        """
        Get seconds until rate limit resets.
        
        Args:
            key_hash: Hashed API key
            
        Returns:
            int: Seconds until reset
        """
        requests = self._requests[key_hash]
        if not requests:
            return 0
        
        oldest_request = min(requests)
        reset_time = oldest_request + self.window_seconds
        retry_after = max(0, int(reset_time - time.time()))
        
        return retry_after


# Global rate limiter
rate_limiter = RateLimiter(
    requests_per_window=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window
)


# ===== Authentication Dependency =====

async def verify_api_key(
    request: Request,
    x_api_key: Optional[str] = Header(None, description="API Key for authentication")
) -> str:
    """
    Verify API key from X-API-Key header.
    
    Args:
        x_api_key: API key from header
        request: Request object
        
    Returns:
        str: Key hash if valid
        
    Raises:
        HTTPException: 401 if invalid or missing
    """
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    # Check if key provided
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Provide X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    # Verify key
    api_key = api_key_manager.verify_key(x_api_key)
    
    if not api_key:
        # Log failed attempt (PHI-safe)
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Invalid API key attempt | Request-ID: {request_id}")
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    # Get key hash for rate limiting
    key_hash = api_key.hashed_key
    
    # Check rate limit if enabled
    if settings.rate_limit_enabled:
        allowed, remaining = rate_limiter.is_allowed(key_hash)
        
        # Add rate limit headers to response (will be added by middleware)
        request.state.rate_limit_remaining = remaining
        request.state.rate_limit_limit = settings.rate_limit_requests
        request.state.rate_limit_reset = rate_limiter.window_seconds
        
        if not allowed:
            retry_after = rate_limiter.get_retry_after(key_hash)
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(settings.rate_limit_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after)
                }
            )
    
    return key_hash


# ===== Rate Limit Middleware =====

@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    """
    Add rate limit headers to responses.
    """
    response = await call_next(request)
    
    # Add rate limit headers if available
    if hasattr(request.state, 'rate_limit_remaining'):
        response.headers["X-RateLimit-Limit"] = str(request.state.rate_limit_limit)
        response.headers["X-RateLimit-Remaining"] = str(request.state.rate_limit_remaining)
        response.headers["X-RateLimit-Reset"] = str(request.state.rate_limit_reset)
    
    return response

