import json
import os
from typing import Dict, List, Optional
from logger import logger, ProjectNIVException

class ConfigValidator:
    """Validates and manages configuration settings."""

    REQUIRED_FIELDS = {
        'sender_email': str,
        'password': str,
        'smtp_server': str,
        'smtp_port': int,
        'receiver_emails': list,
        'subject': str,
        'send_time': str
    }

    DEFAULT_CONFIG = {
        'sender_email': 'youremail@example.com',
        'password': 'yourapppassword',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'receiver_emails': ['recipient1@example.com'],
        'subject': 'Weekly Data Report',
        'send_time': '08:00'
    }

    @staticmethod
    def load_config(config_path: str = 'config.json') -> Dict:
        """
        Load and validate configuration from JSON file.

        Args:
            config_path: Path to configuration file

        Returns:
            Validated configuration dictionary

        Raises:
            ProjectNIVException: If configuration is invalid or missing
        """
        try:
            if not os.path.exists(config_path):
                logger.warning(f"Config file {config_path} not found. Creating default config.")
                ConfigValidator.create_default_config(config_path)
                return ConfigValidator.DEFAULT_CONFIG.copy()

            with open(config_path, 'r') as f:
                config = json.load(f)

            ConfigValidator.validate_config(config)
            logger.info("Configuration loaded and validated successfully")
            return config

        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in config file: {e}"
            logger.error(error_msg)
            raise ProjectNIVException(error_msg)
        except Exception as e:
            error_msg = f"Error loading config: {e}"
            logger.error(error_msg)
            raise ProjectNIVException(error_msg)

    @staticmethod
    def validate_config(config: Dict) -> None:
        """
        Validate configuration dictionary.

        Args:
            config: Configuration dictionary to validate

        Raises:
            ProjectNIVException: If validation fails
        """
        if not isinstance(config, dict):
            raise ProjectNIVException("Configuration must be a dictionary")

        missing_fields = []
        invalid_fields = []

        for field, expected_type in ConfigValidator.REQUIRED_FIELDS.items():
            if field not in config:
                missing_fields.append(field)
            elif not isinstance(config[field], expected_type):
                invalid_fields.append(f"{field} (expected {expected_type.__name__})")

        if missing_fields:
            raise ProjectNIVException(f"Missing required fields: {', '.join(missing_fields)}")

        if invalid_fields:
            raise ProjectNIVException(f"Invalid field types: {', '.join(invalid_fields)}")

        # Additional validations
        if config['smtp_port'] <= 0 or config['smtp_port'] > 65535:
            raise ProjectNIVException("SMTP port must be between 1 and 65535")

        if not config['receiver_emails']:
            raise ProjectNIVException("At least one receiver email must be specified")

        for email in config['receiver_emails']:
            if not isinstance(email, str) or '@' not in email:
                raise ProjectNIVException(f"Invalid email format: {email}")

        # Validate time format (HH:MM)
        try:
            hour, minute = config['send_time'].split(':')
            hour, minute = int(hour), int(minute)
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
        except (ValueError, AttributeError):
            raise ProjectNIVException("send_time must be in HH:MM format (00:00-23:59)")

    @staticmethod
    def create_default_config(config_path: str = 'config.json') -> None:
        """
        Create a default configuration file.

        Args:
            config_path: Path where to create the config file
        """
        try:
            with open(config_path, 'w') as f:
                json.dump(ConfigValidator.DEFAULT_CONFIG, f, indent=4)
            logger.info(f"Default config file created at {config_path}")
        except Exception as e:
            error_msg = f"Error creating default config: {e}"
            logger.error(error_msg)
            raise ProjectNIVException(error_msg)

    @staticmethod
    def update_config(config_path: str, updates: Dict) -> None:
        """
        Update configuration file with new values.

        Args:
            config_path: Path to configuration file
            updates: Dictionary of fields to update
        """
        try:
            config = ConfigValidator.load_config(config_path)
            config.update(updates)

            ConfigValidator.validate_config(config)

            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)

            logger.info(f"Configuration updated: {list(updates.keys())}")
        except Exception as e:
            error_msg = f"Error updating config: {e}"
            logger.error(error_msg)
            raise ProjectNIVException(error_msg)