import logging
import os
import sys
from datetime import datetime
from typing import Dict, Optional, Any
import json
import traceback

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

class EnhancedFormatter(logging.Formatter):
    """Enhanced formatter with structured logging support."""

    def __init__(self, *args, **kwargs):
        # Extract include_extra from kwargs if present, otherwise default to True
        self.include_extra = kwargs.pop('include_extra', True)
        super().__init__(*args, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        # Add timestamp in ISO format for better parsing
        record.iso_time = datetime.fromtimestamp(record.created).isoformat()

        # Include extra fields if present
        if self.include_extra and hasattr(record, '__dict__'):
            extra_info = {k: v for k, v in record.__dict__.items()
                         if k not in ['name', 'msg', 'args', 'levelname', 'levelno',
                                    'pathname', 'filename', 'module', 'exc_info',
                                    'exc_text', 'stack_info', 'lineno', 'funcName',
                                    'created', 'msecs', 'relativeCreated', 'thread',
                                    'threadName', 'processName', 'process', 'getMessage', 'iso_time']}
            if extra_info:
                record.extra_info = json.dumps(extra_info, default=str)
            else:
                record.extra_info = None

        return super().format(record)

class ProjectNIVException(Exception):
    """Custom exception class for PROJECT NIV specific errors."""

    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}

    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {super().__str__()}"
        return super().__str__()

def setup_logger(name: str = 'project_niv',
                log_level: str = 'INFO',
                log_to_file: bool = True,
                log_to_console: bool = True,
                structured: bool = False) -> logging.Logger:
    """Set up and configure logger for the application with enhanced features."""

    logger = logging.getLogger(name)

    # Avoid duplicate handlers - check if we already set up this logger
    if hasattr(logger, '_niv_configured') and logger._niv_configured:
        return logger

    # Parse log level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # Create formatters
    if structured:
        file_formatter = EnhancedFormatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s | %(extra_info)s',
            include_extra=True
        )
        console_formatter = EnhancedFormatter(
            '%(levelname)s | %(name)s | %(message)s',
            include_extra=False
        )
    else:
        file_formatter = EnhancedFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        console_formatter = EnhancedFormatter(
            '%(levelname)s - %(name)s - %(message)s'
        )

    handlers = []

    # File handler for persistent logging
    if log_to_file:
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_handler = logging.FileHandler(f'logs/project_niv_{current_date}.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)

    # Console handler for immediate feedback
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(console_formatter)
        handlers.append(console_handler)

    # Add handlers to logger
    for handler in handlers:
        logger.addHandler(handler)

    # Mark logger as configured to avoid duplicates
    logger._niv_configured = True

    return logger

def log_error(logger: logging.Logger, error: Exception, context: str = "",
              extra: Optional[Dict[str, Any]] = None):
    """Log an error with context information and optional extra data."""
    if logger is None:
        return
    if extra:
        logger.error(f"Error in {context}: {str(error)}",
                    extra={"context": context, "error_type": type(error).__name__, **extra},
                    exc_info=True)
    else:
        logger.error(f"Error in {context}: {str(error)}", exc_info=True)

def log_info(logger: logging.Logger, message: str, extra: Optional[Dict[str, Any]] = None):
    """Log an info message with optional extra data."""
    if logger is None:
        return
    if extra:
        logger.info(message, extra=extra)
    else:
        logger.info(message)

def log_warning(logger: logging.Logger, message: str, extra: Optional[Dict[str, Any]] = None):
    """Log a warning message with optional extra data."""
    if logger is None:
        return
    if extra:
        logger.warning(message, extra=extra)
    else:
        logger.warning(message)

def log_debug(logger: logging.Logger, message: str, extra: Optional[Dict[str, Any]] = None):
    """Log a debug message with optional extra data."""
    if logger is None:
        return
    if extra:
        logger.debug(message, extra=extra)
    else:
        logger.debug(message)

def log_performance(logger: logging.Logger, operation: str, duration: float,
                   extra: Optional[Dict[str, Any]] = None):
    """Log performance metrics for operations."""
    if logger is None:
        return
    perf_data = {"operation": operation, "duration_seconds": duration, **(extra or {})}
    logger.info(f"Performance: {operation} completed in {duration:.3f}s", extra=perf_data)

def log_etl_progress(logger: logging.Logger, step: str, total_steps: int, current_step: int,
                    extra: Optional[Dict[str, Any]] = None):
    """Log ETL processing progress."""
    if logger is None:
        return
    progress = (current_step / total_steps) * 100
    progress_data = {
        "etl_step": step,
        "progress_percent": progress,
        "current_step": current_step,
        "total_steps": total_steps,
        **(extra or {})
    }
    logger.info(f"ETL Progress: {step} ({current_step}/{total_steps} - {progress:.1f}%)",
                extra=progress_data)

def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance, creating one if it doesn't exist."""
    return setup_logger(name or 'project_niv')

# Global logger instance with enhanced features
logger = setup_logger()