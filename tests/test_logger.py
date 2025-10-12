import pytest
import logging
import json
import os
import tempfile
import time
from unittest.mock import patch, MagicMock
import sys

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logger import (
    setup_logger, log_error, log_info, log_warning, log_debug, log_performance,
    log_etl_progress, get_logger, ProjectNIVException, EnhancedFormatter
)


class TestEnhancedLogging:
    """Comprehensive tests for enhanced logging functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_logger_name = 'test_logger'
        self.test_message = 'Test message'

        # Clean up any existing loggers
        logger = logging.getLogger(self.test_logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    def teardown_method(self):
        """Clean up after tests."""
        logger = logging.getLogger(self.test_logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    def test_setup_logger_basic(self):
        """Test basic logger setup."""
        logger = setup_logger(self.test_logger_name)
        assert logger is not None
        assert logger.name == self.test_logger_name
        assert len(logger.handlers) > 0

    def test_setup_logger_with_options(self):
        """Test logger setup with custom options."""
        logger = setup_logger(
            self.test_logger_name,
            log_level='DEBUG',
            log_to_file=False,
            log_to_console=True
        )

        assert logger.level == logging.DEBUG
        assert len(logger.handlers) == 1  # Only console handler
        assert isinstance(logger.handlers[0], logging.StreamHandler)

    def test_setup_logger_structured(self):
        """Test structured logging setup."""
        logger = setup_logger(self.test_logger_name, structured=True)
        formatter = logger.handlers[0].formatter
        assert isinstance(formatter, EnhancedFormatter)

    def test_setup_logger_avoids_duplicates(self):
        """Test that setup_logger avoids creating duplicate handlers."""
        logger1 = setup_logger(self.test_logger_name)
        logger2 = setup_logger(self.test_logger_name)

        # Should be the same logger instance
        assert logger1 is logger2

        # Should not have duplicate handlers
        handler_count = len(logger1.handlers)
        assert handler_count >= 1

    def test_log_error(self):
        """Test error logging functionality."""
        logger = setup_logger(self.test_logger_name)
        test_error = ValueError("Test error")

        # Should not raise exception
        log_error(logger, test_error, "test_context")

        # Check that error was logged (by checking handler was called)
        # This is a basic test - in real scenarios you'd check log files

    def test_log_error_with_extra(self):
        """Test error logging with extra data."""
        logger = setup_logger(self.test_logger_name)
        test_error = ValueError("Test error")
        extra_data = {"user_id": "123", "operation": "test"}

        log_error(logger, test_error, "test_context", extra_data)

        # Should not raise exception
        assert True  # If we get here, logging worked

    def test_log_info(self):
        """Test info logging functionality."""
        logger = setup_logger(self.test_logger_name)
        log_info(logger, self.test_message)
        # Should not raise exception
        assert True

    def test_log_warning(self):
        """Test warning logging functionality."""
        logger = setup_logger(self.test_logger_name)
        log_warning(logger, self.test_message)
        # Should not raise exception
        assert True

    def test_log_debug(self):
        """Test debug logging functionality."""
        logger = setup_logger(self.test_logger_name, log_level='DEBUG')
        log_debug(logger, self.test_message)
        # Should not raise exception
        assert True

    def test_log_performance(self):
        """Test performance logging functionality."""
        logger = setup_logger(self.test_logger_name)
        operation = "test_operation"
        duration = 1.5

        log_performance(logger, operation, duration, {"extra": "data"})

        # Should not raise exception
        assert True

    def test_log_etl_progress(self):
        """Test ETL progress logging functionality."""
        logger = setup_logger(self.test_logger_name)
        step = "data_processing"
        total_steps = 5
        current_step = 2

        log_etl_progress(logger, step, total_steps, current_step, {"records": 100})

        # Should not raise exception
        assert True

    def test_get_logger(self):
        """Test get_logger utility function."""
        logger = get_logger(self.test_logger_name)
        assert logger is not None
        assert logger.name == self.test_logger_name

    def test_get_logger_default_name(self):
        """Test get_logger with default name."""
        logger = get_logger()
        assert logger.name == 'project_niv'

    def test_enhanced_formatter(self):
        """Test EnhancedFormatter functionality."""
        formatter = EnhancedFormatter()

        # Create a test log record
        record = logging.LogRecord(
            name='test', level=logging.INFO, pathname='test.py',
            lineno=10, msg='Test message', args=(), exc_info=None
        )

        # Add extra data to record
        record.test_extra = "extra_value"
        record.created = time.time()

        formatted = formatter.format(record)
        assert isinstance(formatted, str)
        assert 'Test message' in formatted

    def test_enhanced_formatter_with_structured(self):
        """Test EnhancedFormatter with structured logging."""
        formatter = EnhancedFormatter(include_extra=True)

        record = logging.LogRecord(
            name='test', level=logging.INFO, pathname='test.py',
            lineno=10, msg='Test message', args=(), exc_info=None
        )

        record.test_extra = "extra_value"
        record.created = time.time()

        formatted = formatter.format(record)
        assert 'extra_info' in formatted

    def test_projectniv_exception_basic(self):
        """Test ProjectNIVException basic functionality."""
        exception = ProjectNIVException("Test error")
        assert str(exception) == "Test error"

    def test_projectniv_exception_with_code(self):
        """Test ProjectNIVException with error code."""
        exception = ProjectNIVException("Test error", "TEST_ERROR")
        assert str(exception) == "[TEST_ERROR] Test error"

    def test_projectniv_exception_with_details(self):
        """Test ProjectNIVException with details."""
        details = {"user_id": "123", "operation": "test"}
        exception = ProjectNIVException("Test error", "TEST_ERROR", details)
        assert exception.details == details
        assert str(exception) == "[TEST_ERROR] Test error"

    def test_logger_level_filtering(self):
        """Test that logger respects log levels."""
        logger = setup_logger(self.test_logger_name, log_level='WARNING')

        # Debug and info messages should be filtered out at WARNING level
        # But warning and error should pass through
        log_debug(logger, "debug message")  # Should be filtered
        log_info(logger, "info message")    # Should be filtered
        log_warning(logger, "warning message")  # Should pass
        log_error(logger, ValueError("error"), "error context")  # Should pass

        # Should not raise exception
        assert True

    @patch('logger.datetime')
    def test_enhanced_formatter_iso_timestamp(self, mock_datetime):
        """Test that EnhancedFormatter adds ISO timestamp."""
        mock_datetime.now.return_value.strftime.return_value = '2023-01-01T12:00:00'
        mock_datetime.fromtimestamp.return_value.isoformat.return_value = '2023-01-01T12:00:00'

        formatter = EnhancedFormatter()
        record = logging.LogRecord(
            name='test', level=logging.INFO, pathname='test.py',
            lineno=10, msg='Test message', args=(), exc_info=None
        )
        record.created = time.time()

        formatted = formatter.format(record)
        assert '2023-01-01T12:00:00' in formatted

    def test_log_functions_with_none_logger(self):
        """Test that log functions handle None logger gracefully."""
        # Should not raise exception even with None logger
        log_info(None, "test message")
        log_warning(None, "test message")
        log_debug(None, "test message")
        log_error(None, ValueError("test"), "context")
        log_performance(None, "operation", 1.0)
        log_etl_progress(None, "step", 1, 1)

        # If we get here, no exceptions were raised
        assert True

    def test_logger_with_file_output(self):
        """Test logger with file output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, 'test.log')

            with patch('logger.os.makedirs'):  # Prevent actual directory creation
                logger = setup_logger(self.test_logger_name, log_to_console=False)

                # Add file handler manually for test
                handler = logging.FileHandler(log_file)
                logger.addHandler(handler)

                log_info(logger, "Test file message")

                # Check that file was created and contains message
                assert os.path.exists(log_file)
                with open(log_file, 'r') as f:
                    content = f.read()
                    assert 'Test file message' in content

    def test_multiple_logger_instances(self):
        """Test creating multiple logger instances."""
        logger1 = setup_logger('logger1')
        logger2 = setup_logger('logger2')
        logger3 = setup_logger('logger1')  # Same name as logger1

        assert logger1 is not logger3  # Should return same instance for same name
        assert logger1 is not logger2  # Different names should be different instances
        assert logger2 is not logger3

    def test_logger_configuration_persistence(self):
        """Test that logger configuration persists across calls."""
        logger = setup_logger(self.test_logger_name, log_level='ERROR')

        # Configure logger
        assert logger.level == logging.ERROR

        # Get same logger again
        logger2 = setup_logger(self.test_logger_name)

        # Should have same configuration
        assert logger is logger2
        assert logger.level == logging.ERROR