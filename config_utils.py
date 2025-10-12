import json
import os
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from logger import logger, ProjectNIVException, log_error, log_info, log_warning, log_debug

class ConfigValidator:
    """Validates and manages configuration settings with enhanced features."""

    # Configuration schema with validation rules
    CONFIG_SCHEMA = {
        'sender_email': {
            'type': str,
            'required': True,
            'regex': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'description': 'Email address for sending reports'
        },
        'password': {
            'type': str,
            'required': True,
            'min_length': 8,
            'description': 'App password for email authentication'
        },
        'smtp_server': {
            'type': str,
            'required': True,
            'allowed_values': ['smtp.gmail.com', 'smtp.outlook.com', 'smtp.mail.yahoo.com'],
            'description': 'SMTP server hostname'
        },
        'smtp_port': {
            'type': int,
            'required': True,
            'min': 1,
            'max': 65535,
            'description': 'SMTP server port'
        },
        'receiver_emails': {
            'type': list,
            'required': True,
            'min_items': 1,
            'description': 'List of recipient email addresses'
        },
        'subject': {
            'type': str,
            'required': True,
            'min_length': 1,
            'max_length': 255,
            'description': 'Email subject line'
        },
        'send_time': {
            'type': str,
            'required': True,
            'regex': r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$',
            'description': 'Time to send emails (HH:MM format)'
        },
        'log_level': {
            'type': str,
            'required': False,
            'allowed_values': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            'default': 'INFO',
            'description': 'Logging level'
        },
        'enable_scheduling': {
            'type': bool,
            'required': False,
            'default': True,
            'description': 'Enable scheduled email sending'
        }
    }

    DEFAULT_CONFIG = {
        'sender_email': 'youremail@example.com',
        'password': 'yourapppassword',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'receiver_emails': ['recipient1@example.com'],
        'subject': 'Weekly Data Report',
        'send_time': '08:00',
        'log_level': 'INFO',
        'enable_scheduling': True
    }

    @staticmethod
    def load_config(config_path: str = 'config.json', use_env_vars: bool = True) -> Dict[str, Any]:
        """
        Load and validate configuration from JSON file with environment variable support.

        Args:
            config_path: Path to configuration file
            use_env_vars: Whether to override config with environment variables

        Returns:
            Validated configuration dictionary

        Raises:
            ProjectNIVException: If configuration is invalid or missing
        """
        try:
            config = {}

            # Load from file if it exists
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
                log_info(logger, f"Configuration loaded from {config_path}")
            else:
                log_warning(logger, f"Config file {config_path} not found. Using defaults and environment variables.")
                config.update(ConfigValidator.DEFAULT_CONFIG.copy())

            # Override with environment variables if enabled
            if use_env_vars:
                config = ConfigValidator._merge_env_vars(config)

            # Validate and complete configuration
            config = ConfigValidator.validate_and_complete_config(config)

            log_info(logger, "Configuration loaded and validated successfully",
                    extra={"config_fields": len(config)})
            return config

        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in config file {config_path}: {e}"
            log_error(logger, e, "load_config", {"config_path": config_path})
            raise ProjectNIVException(error_msg, "CONFIG_INVALID_JSON")
        except Exception as e:
            error_msg = f"Error loading config from {config_path}: {e}"
            log_error(logger, e, "load_config", {"config_path": config_path})
            raise ProjectNIVException(error_msg, "CONFIG_LOAD_ERROR")

    @staticmethod
    def _merge_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge environment variables into configuration."""
        env_mappings = {
            'NIV_EMAIL_SENDER': 'sender_email',
            'NIV_EMAIL_PASSWORD': 'password',
            'NIV_SMTP_SERVER': 'smtp_server',
            'NIV_SMTP_PORT': 'smtp_port',
            'NIV_EMAIL_RECIPIENTS': 'receiver_emails',  # JSON array as string
            'NIV_EMAIL_SUBJECT': 'subject',
            'NIV_SEND_TIME': 'send_time',
            'NIV_LOG_LEVEL': 'log_level',
            'NIV_ENABLE_SCHEDULING': 'enable_scheduling'
        }

        for env_var, config_key in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                try:
                    if config_key == 'receiver_emails':
                        # Parse JSON array from environment variable
                        config[config_key] = json.loads(env_value)
                    elif config_key in ['smtp_port', 'enable_scheduling']:
                        # Parse as integer or boolean
                        if config_key == 'smtp_port':
                            config[config_key] = int(env_value)
                        elif config_key == 'enable_scheduling':
                            config[config_key] = env_value.lower() in ('true', '1', 'yes', 'on')
                    else:
                        config[config_key] = env_value

                    log_debug(logger, f"Overrode {config_key} with environment variable {env_var}")
                except (json.JSONDecodeError, ValueError) as e:
                    log_warning(logger, f"Failed to parse environment variable {env_var}: {e}")

        return config

    @staticmethod
    def validate_and_complete_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate configuration and fill in default values for optional fields.

        Args:
            config: Configuration dictionary to validate

        Returns:
            Validated and completed configuration dictionary

        Raises:
            ProjectNIVException: If validation fails
        """
        if not isinstance(config, dict):
            raise ProjectNIVException("Configuration must be a dictionary", "CONFIG_INVALID_TYPE")

        # Create a copy to avoid modifying the original
        validated_config = config.copy()

        validation_errors = []

        # Validate each field according to schema
        for field_name, field_schema in ConfigValidator.CONFIG_SCHEMA.items():
            value = validated_config.get(field_name)
            field_errors = ConfigValidator._validate_field(field_name, value, field_schema)

            if field_errors:
                validation_errors.extend(field_errors)

            # Add default value if field is missing and has a default
            if field_name not in validated_config and 'default' in field_schema:
                validated_config[field_name] = field_schema['default']
                log_debug(logger, f"Using default value for {field_name}: {field_schema['default']}")

        if validation_errors:
            error_details = "; ".join(validation_errors)
            raise ProjectNIVException(f"Configuration validation failed: {error_details}",
                                    "CONFIG_VALIDATION_ERROR", {"errors": validation_errors})

        # Cross-field validations
        ConfigValidator._validate_cross_field_rules(validated_config)

        return validated_config

    @staticmethod
    def _validate_field(field_name: str, value: Any, schema: Dict[str, Any]) -> List[str]:
        """Validate a single field against its schema."""
        errors = []

        # Check required fields
        if schema.get('required', False) and (value is None or value == ''):
            errors.append(f"Field '{field_name}' is required")
            return errors  # Don't continue validation if required field is missing

        # Skip further validation if field is not provided and not required
        if value is None or value == '':
            return errors

        # Type validation
        expected_type = schema.get('type')
        if expected_type and not isinstance(value, expected_type):
            errors.append(f"Field '{field_name}' must be of type {expected_type.__name__}")

        # String validations
        if expected_type == str and isinstance(value, str):
            # Length validations
            min_length = schema.get('min_length')
            if min_length is not None and len(value) < min_length:
                errors.append(f"Field '{field_name}' must be at least {min_length} characters")

            max_length = schema.get('max_length')
            if max_length is not None and len(value) > max_length:
                errors.append(f"Field '{field_name}' must be at most {max_length} characters")

            # Regex validation
            regex_pattern = schema.get('regex')
            if regex_pattern and not __import__('re').match(regex_pattern, value):
                errors.append(f"Field '{field_name}' format is invalid")

            # Allowed values validation
            allowed_values = schema.get('allowed_values')
            if allowed_values and value not in allowed_values:
                errors.append(f"Field '{field_name}' must be one of: {allowed_values}")

        # Integer validations
        elif expected_type == int and isinstance(value, int):
            min_val = schema.get('min')
            if min_val is not None and value < min_val:
                errors.append(f"Field '{field_name}' must be at least {min_val}")

            max_val = schema.get('max')
            if max_val is not None and value > max_val:
                errors.append(f"Field '{field_name}' must be at most {max_val}")

        # List validations
        elif expected_type == list and isinstance(value, list):
            min_items = schema.get('min_items')
            if min_items is not None and len(value) < min_items:
                errors.append(f"Field '{field_name}' must have at least {min_items} items")

            # Validate list items if specified
            item_schema = schema.get('item_schema')
            if item_schema:
                for i, item in enumerate(value):
                    item_errors = ConfigValidator._validate_field(f"{field_name}[{i}]", item, item_schema)
                    errors.extend(item_errors)

        return errors

    @staticmethod
    def _validate_cross_field_rules(config: Dict[str, Any]) -> None:
        """Validate rules that involve multiple fields."""
        # Validate email format for receiver_emails
        for email in config.get('receiver_emails', []):
            if not isinstance(email, str) or '@' not in email:
                raise ProjectNIVException(f"Invalid email format in receiver_emails: {email}",
                                        "CONFIG_INVALID_EMAIL")

        # Validate SMTP configuration combinations
        smtp_server = config.get('smtp_server')
        smtp_port = config.get('smtp_port')

        if smtp_server == 'smtp.gmail.com' and smtp_port != 587:
            log_warning(logger, "Gmail typically uses port 587 for TLS")

        if smtp_server in ['smtp.outlook.com', 'smtp.mail.yahoo.com'] and smtp_port != 587:
            log_warning(logger, f"{smtp_server} typically uses port 587 for TLS")

        # Validate time format (HH:MM)
        send_time = config.get('send_time')
        if send_time:
            try:
                hour, minute = send_time.split(':')
                hour, minute = int(hour), int(minute)
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    raise ProjectNIVException("send_time must be in HH:MM format (00:00-23:59)",
                                            "CONFIG_INVALID_TIME_FORMAT")
            except (ValueError, AttributeError):
                raise ProjectNIVException("send_time must be in HH:MM format (00:00-23:59)",
                                        "CONFIG_INVALID_TIME_FORMAT")

    @staticmethod
    def create_default_config(config_path: str = 'config.json') -> None:
        """
        Create a default configuration file with comprehensive schema.

        Args:
            config_path: Path where to create the config file
        """
        try:
            # Create default config with all schema fields
            default_config = {}
            for field_name, field_schema in ConfigValidator.CONFIG_SCHEMA.items():
                if 'default' in field_schema:
                    default_config[field_name] = field_schema['default']
                elif not field_schema.get('required', False):
                    # For non-required fields without defaults, use None
                    default_config[field_name] = None

            # Add required fields that don't have defaults (shouldn't happen in current schema)
            for field_name, field_schema in ConfigValidator.CONFIG_SCHEMA.items():
                if field_schema.get('required', False) and field_name not in default_config:
                    default_config[field_name] = ConfigValidator.DEFAULT_CONFIG.get(field_name)

            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)

            log_info(logger, f"Default config file created at {config_path}",
                    extra={"fields_count": len(default_config)})
        except Exception as e:
            error_msg = f"Error creating default config: {e}"
            log_error(logger, e, "create_default_config", {"config_path": config_path})
            raise ProjectNIVException(error_msg, "CONFIG_CREATE_ERROR")

    @staticmethod
    def update_config(config_path: str, updates: Dict[str, Any]) -> None:
        """
        Update configuration file with new values and validate.

        Args:
            config_path: Path to configuration file
            updates: Dictionary of fields to update
        """
        try:
            # Load current config
            current_config = ConfigValidator.load_config(config_path)

            # Apply updates
            current_config.update(updates)

            # Validate the updated config
            validated_config = ConfigValidator.validate_and_complete_config(current_config)

            # Write back to file
            with open(config_path, 'w') as f:
                json.dump(validated_config, f, indent=2)

            log_info(logger, f"Configuration updated successfully",
                    extra={"updated_fields": list(updates.keys()), "total_fields": len(validated_config)})
        except Exception as e:
            error_msg = f"Error updating config: {e}"
            log_error(logger, e, "update_config", {"config_path": config_path, "updates": list(updates.keys())})
            raise ProjectNIVException(error_msg, "CONFIG_UPDATE_ERROR")

    @staticmethod
    def save_config(config: Dict[str, Any], config_path: str = 'config.json') -> None:
        """
        Save configuration to file with validation.

        Args:
            config: Configuration dictionary to save
            config_path: Path where to save the config file
        """
        try:
            # Validate before saving
            validated_config = ConfigValidator.validate_and_complete_config(config)

            with open(config_path, 'w') as f:
                json.dump(validated_config, f, indent=2)

            log_info(logger, f"Configuration saved to {config_path}",
                    extra={"fields_count": len(validated_config)})
        except Exception as e:
            error_msg = f"Error saving config to {config_path}: {e}"
            log_error(logger, e, "save_config", {"config_path": config_path})
            raise ProjectNIVException(error_msg, "CONFIG_SAVE_ERROR")

    @staticmethod
    def get_config_value(config: Dict[str, Any], key: str, default: Any = None) -> Any:
        """
        Get a configuration value with optional default.

        Args:
            config: Configuration dictionary
            key: Configuration key to retrieve
            default: Default value if key is not found

        Returns:
            Configuration value or default
        """
        return config.get(key, default)

    @staticmethod
    def validate_config_path(config_path: str) -> bool:
        """
        Validate that a configuration file path is valid and accessible.

        Args:
            config_path: Path to validate

        Returns:
            True if path is valid and accessible
        """
        try:
            path = Path(config_path)
            if path.exists():
                # Check if we can read the file
                with open(config_path, 'r'):
                    pass
                return True
            else:
                # Check if parent directory exists and is writable
                parent = path.parent
                return parent.exists() and os.access(parent, os.W_OK)
        except Exception as e:
            log_debug(logger, f"Config path validation failed for {config_path}: {e}")
            return False

    @staticmethod
    def get_config_schema() -> Dict[str, Dict[str, Any]]:
        """Get the configuration schema for documentation or validation."""
        return ConfigValidator.CONFIG_SCHEMA.copy()