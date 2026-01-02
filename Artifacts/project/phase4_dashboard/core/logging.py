"""
Logging Configuration

Centralized logging setup with structured logging support.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler

from .config import get_settings


def setup_logging(
    name: str = "hedis_portfolio",
    level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up application logging
    
    Args:
        name: Logger name
        level: Log level (overrides config if provided)
        log_file: Log file path (overrides config if provided)
    
    Returns:
        Configured logger instance
    """
    settings = get_settings()
    log_config = settings.logging
    
    # Determine log level
    log_level = level or log_config.level
    numeric_level = getattr(logging, log_level, logging.INFO)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(log_config.format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if configured)
    log_file_path = log_file or log_config.file_path
    if log_file_path:
        log_path = Path(log_file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=log_config.max_bytes,
            backupCount=log_config.backup_count
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name (defaults to calling module name)
    
    Returns:
        Logger instance
    """
    if name is None:
        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            name = frame.f_back.f_globals.get('__name__', 'hedis_portfolio')
        else:
            name = 'hedis_portfolio'
    
    logger = logging.getLogger(name)
    
    # If logger has no handlers, set it up
    if not logger.handlers:
        setup_logging(name)
    
    return logger

