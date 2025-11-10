"""
HEDIS Star Rating Portfolio Optimizer - Main API Application

Production-ready FastAPI application serving 12 HEDIS measures.

Author: Robert Reichert
GitHub: github.com/StarGuardAi
"""

import time
import uuid
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import settings
from .dependencies import model_cache

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ===== Lifespan Events =====

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for startup and shutdown.
    Load models at startup, cleanup at shutdown.
    """
    # Startup
    logger.info("🚀 HEDIS API Starting Up...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Version: {settings.api_version}")
    
    if settings.load_models_on_startup:
        logger.info("Loading ML models...")
        try:
            model_cache.load_all_models()
            logger.info("✅ Models loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load models: {e}")
    
    logger.info("✅ API Ready!")
    
    yield
    
    # Shutdown
    logger.info("🛑 HEDIS API Shutting Down...")
    logger.info("✅ Cleanup Complete")


# ===== FastAPI Application =====

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan,
)


# ===== Middleware =====

# CORS Middleware
if settings.cors_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS enabled for origins: {settings.cors_origins}")


# Request ID Middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """
    Add unique request ID to each request for tracking.
    """
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    
    return response


# Request Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Track and log request processing time.
    """
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    response.headers["X-Process-Time-Ms"] = str(round(process_time, 2))
    
    # Log request if enabled
    if settings.log_requests:
        logger.info(
            f"Request: {request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time:.2f}ms | "
            f"Request-ID: {getattr(request.state, 'request_id', 'unknown')}"
        )
    
    return response


# Logging Middleware (PHI-safe)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log requests with PHI-safe information.
    Never logs member IDs or other PII.
    """
    request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
    
    # Log incoming request (PHI-safe)
    logger.debug(
        f"Incoming request: {request.method} {request.url.path} | "
        f"Request-ID: {request_id}"
    )
    
    response = await call_next(request)
    
    return response


# ===== Exception Handlers =====

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions with PHI-safe error messages.
    """
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.error(
        f"HTTP Exception: {exc.status_code} | "
        f"Detail: {exc.detail} | "
        f"Request-ID: {request_id}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "request_id": request_id,
            "timestamp": time.time()
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors with clear messages.
    """
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.warning(
        f"Validation Error: {exc.errors()} | "
        f"Request-ID: {request_id}"
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": exc.errors(),
            "request_id": request_id,
            "timestamp": time.time()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions safely (PHI-protected).
    """
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.error(
        f"Unexpected Error: {type(exc).__name__}: {str(exc)} | "
        f"Request-ID: {request_id}",
        exc_info=True
    )
    
    # Don't expose internal error details in production
    error_message = str(exc) if settings.debug else "Internal server error"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": error_message,
            "request_id": request_id,
            "timestamp": time.time()
        }
    )


# ===== Root Endpoints =====

@app.get("/", tags=["Root"])
async def root() -> Dict[str, Any]:
    """
    API root endpoint with basic information.
    """
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "status": "operational",
        "environment": settings.environment,
        "docs_url": "/docs" if settings.debug else None,
        "health_check": "/health",
        "measures_endpoint": "/api/v1/measures",
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint.
    Returns API status and version.
    """
    return {
        "status": "healthy",
        "version": settings.api_version,
        "environment": settings.environment,
        "timestamp": time.time()
    }


@app.get("/health/ready", tags=["Health"])
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness check for Kubernetes.
    Returns ready status if models are loaded.
    """
    models_ready = model_cache.is_initialized
    
    if not models_ready and settings.load_models_on_startup:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "reason": "Models not loaded",
                "timestamp": time.time()
            }
        )
    
    return {
        "status": "ready",
        "models_loaded": models_ready,
        "timestamp": time.time()
    }


@app.get("/health/live", tags=["Health"])
async def liveness_check() -> Dict[str, Any]:
    """
    Liveness check for Kubernetes.
    Simple ping to verify API is alive.
    """
    return {
        "status": "alive",
        "timestamp": time.time()
    }


# ===== Router Registration =====
from .routers import prediction, portfolio, analytics, measures
app.include_router(prediction.router, prefix="/api/v1", tags=["Predictions"])
app.include_router(portfolio.router, prefix="/api/v1", tags=["Portfolio"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(measures.router, prefix="/api/v1", tags=["Measures"])


# ===== Main Entry Point =====

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )

