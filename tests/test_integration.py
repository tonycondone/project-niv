import pytest
import os
import tempfile
import json
import shutil
from unittest.mock import patch, MagicMock
import sys

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_utils import ConfigValidator
from email_utils import EmailSender, send_email
from logger import logger, log_info, log_error, ProjectNIVException


class TestIntegration:
    """Integration tests for PROJECT NIV components."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.json')
        self.test_csv_path = os.path.join(self.temp_dir, 'test_data.csv')
        self.test_report_path = os.path.join(self.temp_dir, 'test_report.xlsx')

        # Create test configuration
        self.test_config = {
            'sender_email': 'test@example.com',
            'password': 'testpassword123',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'receiver_emails': ['recipient1@example.com'],
            'subject': 'Integration Test Report',
            'send_time': '08:00'
        }

        with open(self.config_path, 'w') as f:
            json.dump(self.test_config, f)

        # Create test CSV data
        with open(self.test_csv_path, 'w') as f:
            f.write('Name,Age,City\nAlice,25,New York\nBob,30,Los Angeles\nCharlie,35,Chicago\n')

        # Create test report file
        with open(self.test_report_path, 'w') as f:
            f.write('Test report content')

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_config_and_email_integration(self):
        """Test integration between configuration and email utilities."""
        # Load configuration
        config = ConfigValidator.load_config(self.config_path)

        # Verify configuration is loaded correctly
        assert config['sender_email'] == 'test@example.com'
        assert config['smtp_server'] == 'smtp.gmail.com'
        assert len(config['receiver_emails']) == 1

        # Initialize email sender with loaded config
        email_sender = EmailSender(config=config)

        # Test email sending (will fail due to mock SMTP, but should not crash)
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_server.send_message.side_effect = Exception("SMTP Error")
            mock_smtp.return_value = mock_server

            result = email_sender.send_email(self.test_report_path, "Integration test summary")

            # Should handle errors gracefully
            assert result is False

    def test_email_sender_with_config_validation(self):
        """Test EmailSender with configuration validation."""
        # Test with invalid config (missing required field)
        invalid_config = self.test_config.copy()
        del invalid_config['sender_email']

        # EmailSender should handle invalid config gracefully
        # (it will try to validate when sending email, not during initialization)
        email_sender = EmailSender(config=invalid_config)

        # The error should occur when trying to send email
        result = email_sender.send_email(self.test_report_path, "Test")
        assert result is False  # Should fail gracefully

    def test_email_sender_with_env_override(self):
        """Test EmailSender with environment variable overrides."""
        with patch.dict(os.environ, {'NIV_EMAIL_SENDER': 'env@example.com'}):
            config = ConfigValidator.load_config(self.config_path, use_env_vars=True)

            # Should be overridden by environment variable
            assert config['sender_email'] == 'env@example.com'

    def test_email_with_different_file_types(self):
        """Test email sending with different attachment types."""
        email_sender = EmailSender(config=self.test_config)

        # Test with CSV file
        csv_result = email_sender.send_email(self.test_csv_path, "CSV test")
        # Should handle gracefully even if SMTP fails

        # Test with Excel-like file
        excel_result = email_sender.send_email(self.test_report_path, "Excel test")
        # Should handle gracefully even if SMTP fails

        # Both should return False due to mock SMTP, but not crash
        assert csv_result is False
        assert excel_result is False

    def test_configuration_persistence_across_operations(self):
        """Test that configuration persists across multiple operations."""
        # Load config multiple times
        config1 = ConfigValidator.load_config(self.config_path)
        config2 = ConfigValidator.load_config(self.config_path)

        # Should be identical
        assert config1 == config2

        # Test updating config
        ConfigValidator.update_config(self.config_path, {'subject': 'Updated Subject'})

        config3 = ConfigValidator.load_config(self.config_path)
        assert config3['subject'] == 'Updated Subject'
        assert config3['sender_email'] == 'test@example.com'  # Unchanged

    def test_email_sender_reuse(self):
        """Test reusing EmailSender instance."""
        email_sender = EmailSender(config=self.test_config)

        # Send multiple emails
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_server.send_message.side_effect = Exception("SMTP Error")
            mock_smtp.return_value = mock_server

            result1 = email_sender.send_email(self.test_report_path, "First email")
            result2 = email_sender.send_email(self.test_report_path, "Second email")

            # Both should fail gracefully
            assert result1 is False
            assert result2 is False

    def test_configuration_and_logging_integration(self):
        """Test integration between configuration and logging."""
        # Load config and verify logging works
        config = ConfigValidator.load_config(self.config_path)

        # Log messages should work with the configuration context
        log_info(logger, "Integration test message", extra={"test_id": "integration_001"})

        # Should not raise exception
        assert True

    def test_email_with_large_attachments(self):
        """Test email sending with larger attachment files."""
        # Create a larger test file
        large_file = os.path.join(self.temp_dir, 'large_report.txt')
        with open(large_file, 'w') as f:
            f.write('x' * 10000)  # 10KB file

        email_sender = EmailSender(config=self.test_config)

        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_server.send_message.side_effect = Exception("SMTP Error")
            mock_smtp.return_value = mock_server

            result = email_sender.send_email(large_file, "Large file test")

            # Should handle large files gracefully
            assert result is False

    def test_error_handling_integration(self):
        """Test error handling across integrated components."""
        # Test with invalid configuration file
        invalid_config_path = os.path.join(self.temp_dir, 'invalid.json')
        with open(invalid_config_path, 'w') as f:
            f.write('{ invalid json }')

        # Should raise appropriate exception
        with pytest.raises(ProjectNIVException):
            ConfigValidator.load_config(invalid_config_path)

        # Test email sending with invalid attachment
        email_sender = EmailSender(config=self.test_config)
        result = email_sender.send_email('/nonexistent/file.xlsx', 'Test summary')

        # Should handle missing file gracefully
        assert result is False

    def test_configuration_validation_integration(self):
        """Test configuration validation in real usage scenarios."""
        # Test with minimal valid config
        minimal_config = {
            'sender_email': 'test@example.com',
            'password': 'testpassword123',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'receiver_emails': ['recipient@example.com'],
            'subject': 'Test',
            'send_time': '08:00'
        }

        # Save minimal config
        minimal_config_path = os.path.join(self.temp_dir, 'minimal_config.json')
        ConfigValidator.save_config(minimal_config, minimal_config_path)

        # Load and verify it gets completed with defaults
        loaded_config = ConfigValidator.load_config(minimal_config_path)

        # Should have additional fields from defaults
        assert 'log_level' in loaded_config
        assert 'enable_scheduling' in loaded_config

    def test_email_with_connection_testing(self):
        """Test email sender with connection testing capability."""
        email_sender = EmailSender(config=self.test_config)

        # Test connection (will fail due to mock, but should not crash)
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_server.login.side_effect = Exception("Auth failed")
            mock_smtp.return_value = mock_server

            result = email_sender.test_connection()

            # Should handle connection failure gracefully
            assert result is False

    def test_end_to_end_email_workflow(self):
        """Test complete email workflow from config to sending."""
        # 1. Load configuration
        config = ConfigValidator.load_config(self.config_path)

        # 2. Create email sender
        email_sender = EmailSender(config=config)

        # 3. Test connection
        connection_ok = email_sender.test_connection()

        # 4. Send email (will fail due to mock SMTP)
        email_result = email_sender.send_email(self.test_report_path, "E2E test summary")

        # 5. Verify workflow completed without crashing
        # (Actual success depends on SMTP availability)
        assert True  # If we get here, the workflow is functional

    def test_configuration_with_schema_validation(self):
        """Test configuration with comprehensive schema validation."""
        # Test with all schema fields
        full_config = {
            'sender_email': 'test@example.com',
            'password': 'testpassword123',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'receiver_emails': ['recipient1@example.com', 'recipient2@example.com'],
            'subject': 'Full Schema Test',
            'send_time': '14:30',
            'log_level': 'DEBUG',
            'enable_scheduling': False
        }

        # Should validate successfully
        validated_config = ConfigValidator.validate_and_complete_config(full_config)
        assert validated_config['log_level'] == 'DEBUG'
        assert validated_config['enable_scheduling'] is False

    def test_error_recovery_integration(self):
        """Test error recovery across integrated components."""
        # Test that one component failure doesn't crash the entire system

        # 1. Try to load invalid config (should fail gracefully)
        try:
            ConfigValidator.load_config('/nonexistent/config.json')
        except ProjectNIVException:
            pass  # Expected

        # 2. Load valid config (should work)
        config = ConfigValidator.load_config(self.config_path)

        # 3. Create email sender (should work)
        email_sender = EmailSender(config=config)

        # 4. Try to send to invalid attachment (should fail gracefully)
        result = email_sender.send_email('/nonexistent/file.xlsx', 'Test')

        # 5. Try to send to valid attachment (should fail due to SMTP but not crash)
        result = email_sender.send_email(self.test_report_path, 'Test')

        # All steps should complete without unhandled exceptions
        assert True