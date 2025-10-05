import json
import os
import logging
from typing import Dict, List, Optional
from logger_config import logger

class ConfigManager:
    """Manages application configuration with validation and environment variable support."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = {}
        self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file and environment variables."""
        try:
            # Load from file
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_file}")
            else:
                logger.warning(f"Config file {self.config_file} not found, using defaults")
                self.config = self._get_default_config()
            
            # Override with environment variables
            self._load_from_env()
            
            # Validate configuration
            self.validate_config()
            
            return self.config
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.config = self._get_default_config()
            return self.config
    
    def _get_default_config(self) -> Dict:
        """Get default configuration values."""
        return {
            "sender_email": os.getenv("SENDER_EMAIL", "youremail@example.com"),
            "password": os.getenv("EMAIL_PASSWORD", "yourapppassword"),
            "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            "smtp_port": int(os.getenv("SMTP_PORT", "587")),
            "receiver_emails": os.getenv("RECEIVER_EMAILS", "recipient1@example.com,recipient2@example.com").split(","),
            "subject": os.getenv("EMAIL_SUBJECT", "Weekly Data Report"),
            "send_time": os.getenv("SEND_TIME", "08:00"),
            "data_file": os.getenv("DATA_FILE", "data/sample.csv"),
            "reports_dir": os.getenv("REPORTS_DIR", "reports"),
            "log_level": os.getenv("LOG_LEVEL", "INFO")
        }
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_mappings = {
            "SENDER_EMAIL": "sender_email",
            "EMAIL_PASSWORD": "password",
            "SMTP_SERVER": "smtp_server",
            "SMTP_PORT": "smtp_port",
            "RECEIVER_EMAILS": "receiver_emails",
            "EMAIL_SUBJECT": "subject",
            "SEND_TIME": "send_time",
            "DATA_FILE": "data_file",
            "REPORTS_DIR": "reports_dir",
            "LOG_LEVEL": "log_level"
        }
        
        for env_var, config_key in env_mappings.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                if config_key == "smtp_port":
                    value = int(value)
                elif config_key == "receiver_emails":
                    value = [email.strip() for email in value.split(",")]
                self.config[config_key] = value
                logger.info(f"Loaded {config_key} from environment variable {env_var}")
    
    def validate_config(self) -> bool:
        """Validate configuration values."""
        required_fields = [
            "sender_email", "password", "smtp_server", 
            "smtp_port", "receiver_emails", "subject"
        ]
        
        missing_fields = []
        for field in required_fields:
            if not self.config.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            logger.error(f"Missing required configuration fields: {missing_fields}")
            return False
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, self.config["sender_email"]):
            logger.error("Invalid sender email format")
            return False
        
        for email in self.config["receiver_emails"]:
            if not re.match(email_pattern, email.strip()):
                logger.error(f"Invalid receiver email format: {email}")
                return False
        
        # Validate SMTP port
        if not isinstance(self.config["smtp_port"], int) or not (1 <= self.config["smtp_port"] <= 65535):
            logger.error("Invalid SMTP port number")
            return False
        
        logger.info("Configuration validation passed")
        return True
    
    def get(self, key: str, default=None):
        """Get configuration value by key."""
        return self.config.get(key, default)
    
    def update(self, key: str, value):
        """Update configuration value."""
        self.config[key] = value
        logger.info(f"Updated configuration: {key} = {value}")
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")

# Global config instance
config = ConfigManager()