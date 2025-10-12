import pytest
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
import sys

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_utils import ConfigValidator, ProjectNIVException


class TestConfigValidator:
    """Comprehensive tests for ConfigValidator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.valid_config = {
            'sender_email': 'test@example.com',
            'password': 'testpassword123',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'receiver_emails': ['recipient1@example.com', 'recipient2@example.com'],
            'subject': 'Test Report',
            'send_time': '08:00',
            'log_level': 'INFO',
            'enable_scheduling': True
        }

        self.invalid_config = {
            'sender_email': 'invalid-email',
            'password': 'short',
            'smtp_server': 'invalid.smtp.com',
            'smtp_port': 99999,
            'receiver_emails': ['invalid-email'],
            'subject': '',
            'send_time': '25:00'
        }

    def test_load_config_from_file(self):
        """Test loading configuration from existing file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_config, f)
            temp_path = f.name

        try:
            config = ConfigValidator.load_config(temp_path)
            assert config == self.valid_config
        finally:
            os.unlink(temp_path)

    def test_load_config_from_nonexistent_file(self):
        """Test loading configuration from non-existent file creates default."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, 'nonexistent.json')
            config = ConfigValidator.load_config(config_path)

            # Should return default config with some fields
            assert 'sender_email' in config
            assert 'smtp_server' in config

    def test_load_config_invalid_json(self):
        """Test loading configuration with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{ invalid json content }')
            temp_path = f.name

        try:
            with pytest.raises(ProjectNIVException) as exc_info:
                ConfigValidator.load_config(temp_path)
            assert 'Invalid JSON' in str(exc_info.value)
        finally:
            os.unlink(temp_path)

    @patch.dict(os.environ, {'NIV_EMAIL_SENDER': 'env@example.com'})
    def test_load_config_with_env_vars(self):
        """Test loading configuration with environment variable overrides."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_config, f)
            temp_path = f.name

        try:
            config = ConfigValidator.load_config(temp_path, use_env_vars=True)
            assert config['sender_email'] == 'env@example.com'  # Overridden by env var
            assert config['smtp_server'] == 'smtp.gmail.com'  # Not overridden
        finally:
            os.unlink(temp_path)

    def test_validate_and_complete_config_valid(self):
        """Test validation of valid configuration."""
        config = ConfigValidator.validate_and_complete_config(self.valid_config)
        assert config == self.valid_config
        assert len(config) >= len(self.valid_config)  # May have added defaults

    def test_validate_and_complete_config_missing_required(self):
        """Test validation fails with missing required fields."""
        incomplete_config = {k: v for k, v in self.valid_config.items() if k != 'sender_email'}

        with pytest.raises(ProjectNIVException) as exc_info:
            ConfigValidator.validate_and_complete_config(incomplete_config)
        assert 'required' in str(exc_info.value).lower()

    def test_validate_and_complete_config_invalid_type(self):
        """Test validation fails with wrong types."""
        invalid_config = self.valid_config.copy()
        invalid_config['smtp_port'] = 'not_a_number'

        with pytest.raises(ProjectNIVException) as exc_info:
            ConfigValidator.validate_and_complete_config(invalid_config)
        assert 'type' in str(exc_info.value).lower()

    def test_validate_and_complete_config_invalid_email(self):
        """Test validation fails with invalid email format."""
        invalid_config = self.valid_config.copy()
        invalid_config['sender_email'] = 'not-an-email'

        with pytest.raises(ProjectNIVException) as exc_info:
            ConfigValidator.validate_and_complete_config(invalid_config)
        assert 'email' in str(exc_info.value).lower()

    def test_validate_and_complete_config_invalid_time(self):
        """Test validation fails with invalid time format."""
        invalid_config = self.valid_config.copy()
        invalid_config['send_time'] = '25:00'

        with pytest.raises(ProjectNIVException) as exc_info:
            ConfigValidator.validate_and_complete_config(invalid_config)
        assert 'format is invalid' in str(exc_info.value)

    def test_validate_and_complete_config_adds_defaults(self):
        """Test that optional fields get default values."""
        minimal_config = {
            'sender_email': 'test@example.com',
            'password': 'testpassword123',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'receiver_emails': ['recipient@example.com'],
            'subject': 'Test',
            'send_time': '08:00'
        }

        config = ConfigValidator.validate_and_complete_config(minimal_config)
        assert 'log_level' in config
        assert 'enable_scheduling' in config

    def test_create_default_config(self):
        """Test creating default configuration file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, 'default_config.json')

            ConfigValidator.create_default_config(config_path)

            assert os.path.exists(config_path)
            with open(config_path, 'r') as f:
                config = json.load(f)

            assert 'sender_email' in config
            assert 'smtp_server' in config

    def test_update_config(self):
        """Test updating configuration file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_config, f)
            temp_path = f.name

        try:
            updates = {'subject': 'Updated Subject', 'log_level': 'DEBUG'}
            ConfigValidator.update_config(temp_path, updates)

            with open(temp_path, 'r') as f:
                updated_config = json.load(f)

            assert updated_config['subject'] == 'Updated Subject'
            assert updated_config['log_level'] == 'DEBUG'
            assert updated_config['sender_email'] == 'test@example.com'  # Unchanged
        finally:
            os.unlink(temp_path)

    def test_save_config(self):
        """Test saving configuration to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, 'saved_config.json')

            ConfigValidator.save_config(self.valid_config, config_path)

            assert os.path.exists(config_path)
            with open(config_path, 'r') as f:
                saved_config = json.load(f)

            assert saved_config == self.valid_config

    def test_get_config_value(self):
        """Test getting configuration values with defaults."""
        assert ConfigValidator.get_config_value(self.valid_config, 'sender_email') == 'test@example.com'
        assert ConfigValidator.get_config_value(self.valid_config, 'nonexistent', 'default') == 'default'
        assert ConfigValidator.get_config_value(self.valid_config, 'nonexistent') is None

    def test_validate_config_path_valid(self):
        """Test validating valid configuration paths."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_config, f)
            temp_path = f.name

        try:
            assert ConfigValidator.validate_config_path(temp_path) is True
        finally:
            os.unlink(temp_path)

    def test_validate_config_path_invalid(self):
        """Test validating invalid configuration paths."""
        assert ConfigValidator.validate_config_path('/nonexistent/path/config.json') is False

    def test_get_config_schema(self):
        """Test getting configuration schema."""
        schema = ConfigValidator.get_config_schema()
        assert isinstance(schema, dict)
        assert 'sender_email' in schema
        assert 'smtp_server' in schema
        assert schema['sender_email']['type'] == str
        assert schema['smtp_port']['type'] == int

    def test_cross_field_validation_email_format(self):
        """Test cross-field validation for email formats."""
        invalid_config = self.valid_config.copy()
        invalid_config['receiver_emails'] = ['invalid-email']

        with pytest.raises(ProjectNIVException) as exc_info:
            ConfigValidator.validate_and_complete_config(invalid_config)
        assert 'email format' in str(exc_info.value).lower()

    def test_cross_field_validation_smtp_warnings(self):
        """Test SMTP configuration warnings are logged."""
        config = self.valid_config.copy()
        config['smtp_server'] = 'smtp.gmail.com'
        config['smtp_port'] = 25  # Wrong port for Gmail

        # Should not raise exception, but may log warnings
        result = ConfigValidator.validate_and_complete_config(config)
        assert result is not None

    def test_config_with_env_var_parsing_errors(self):
        """Test handling of environment variable parsing errors."""
        with patch.dict(os.environ, {'NIV_EMAIL_RECIPIENTS': 'invalid-json'}):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(self.valid_config, f)
                temp_path = f.name

            try:
                # Should not crash, just use default value
                config = ConfigValidator.load_config(temp_path, use_env_vars=True)
                assert config['receiver_emails'] == self.valid_config['receiver_emails']
            finally:
                os.unlink(temp_path)

    @pytest.mark.parametrize("field,value,expected_valid", [
        ('sender_email', 'valid@example.com', True),
        ('sender_email', 'invalid-email', False),
        ('smtp_port', 587, True),
        ('smtp_port', 99999, False),
        ('send_time', '08:00', True),
        ('send_time', '25:00', False),
        ('log_level', 'INFO', True),
        ('log_level', 'INVALID', False),
    ])
    def test_field_validation(self, field, value, expected_valid):
        """Test individual field validation."""
        config = self.valid_config.copy()
        config[field] = value

        if expected_valid:
            # Should not raise exception
            result = ConfigValidator.validate_and_complete_config(config)
            assert result[field] == value
        else:
            # Should raise exception
            with pytest.raises(ProjectNIVException):
                ConfigValidator.validate_and_complete_config(config)