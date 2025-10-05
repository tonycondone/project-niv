import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

def setup_logger(name: str = 'project_niv') -> logging.Logger:
    """Set up and configure logger for the application."""
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(name)s - %(message)s'
    )

    # File handler for persistent logging
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_handler = logging.FileHandler(f'logs/project_niv_{current_date}.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # Console handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

class ProjectNIVException(Exception):
    """Custom exception class for PROJECT NIV specific errors."""
    pass

def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """Log an error with context information."""
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)

def log_info(logger: logging.Logger, message: str):
    """Log an info message."""
    logger.info(message)

def log_warning(logger: logging.Logger, message: str):
    """Log a warning message."""
    logger.warning(message)

# Global logger instance
logger = setup_logger()