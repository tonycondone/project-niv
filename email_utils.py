import smtplib
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from config_utils import ConfigValidator
from logger import logger, log_error, log_info, log_warning, log_debug, log_performance, ProjectNIVException

class EmailSender:
    """Enhanced email sender with robust error handling and logging."""

    def __init__(self, config: Optional[Dict[str, Any]] = None, config_path: str = 'config.json'):
        """
        Initialize email sender with configuration.

        Args:
            config: Optional configuration dictionary
            config_path: Path to configuration file if config not provided
        """
        self.config = config
        self.config_path = config_path
        self._smtp_connection = None

        if not self.config:
            self.config = ConfigValidator.load_config(config_path)

        log_debug(logger, "EmailSender initialized",
                 extra={"config_fields": len(self.config), "config_path": config_path})

    def send_email(self, attachment_path: str, summary: str, subject: Optional[str] = None) -> bool:
        """
        Send email with report attachment using enhanced error handling.

        Args:
            attachment_path: Path to the report file to attach
            summary: Summary text to include in email body
            subject: Optional custom subject (uses config default if not provided)

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        start_time = time.time()

        try:
            # Validate inputs
            success, validation_errors = self._validate_inputs(attachment_path, summary)
            if not success:
                for error in validation_errors:
                    log_warning(logger, error)
                return False

            # Prepare email
            msg = self._create_email_message(attachment_path, summary, subject)
            if not msg:
                return False

            # Send email with retry logic
            send_success = self._send_with_retry(msg)

            # Log performance metrics
            duration = time.time() - start_time
            log_performance(logger, "send_email", duration,
                           extra={"attachment_size": self._get_file_size(attachment_path),
                                 "recipient_count": len(self.config['receiver_emails']),
                                 "success": send_success})

            if send_success:
                log_info(logger, f"Email sent successfully to {len(self.config['receiver_emails'])} recipients",
                        extra={"duration": duration, "attachment": os.path.basename(attachment_path)})
            else:
                log_error(logger, ProjectNIVException("Failed to send email after retries"),
                         "send_email", {"attachment": attachment_path})

            return send_success

        except Exception as e:
            duration = time.time() - start_time
            log_error(logger, e, "send_email",
                     extra={"duration": duration, "attachment": attachment_path})
            return False

    def _validate_inputs(self, attachment_path: str, summary: str) -> Tuple[bool, List[str]]:
        """Validate email inputs and return (success, error_list)."""
        errors = []

        # Check attachment exists and is readable
        if not os.path.exists(attachment_path):
            errors.append(f"Attachment file not found: {attachment_path}")
        elif not os.access(attachment_path, os.R_OK):
            errors.append(f"Attachment file not readable: {attachment_path}")
        elif os.path.getsize(attachment_path) == 0:
            errors.append(f"Attachment file is empty: {attachment_path}")

        # Validate summary
        if not summary or not summary.strip():
            errors.append("Email summary cannot be empty")

        # Validate configuration
        if not self.config.get('receiver_emails'):
            errors.append("No recipient emails configured")

        return len(errors) == 0, errors

    def _create_email_message(self, attachment_path: str, summary: str, custom_subject: Optional[str] = None) -> Optional[MIMEMultipart]:
        """Create the email message with proper formatting."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['sender_email']
            msg['To'] = ", ".join(self.config['receiver_emails'])
            msg['Subject'] = custom_subject or self.config['subject']

            # Enhanced email body with timestamp and metadata
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            body = f"""Hi,

Please find attached the latest data report.

Summary:
{summary}

Generated on: {timestamp}
Report size: {self._get_file_size_formatted(attachment_path)}

Regards,
PROJECT NIV Data Platform
"""
            msg.attach(MIMEText(body, 'plain'))

            # Attach file with proper encoding
            attachment_success = self._attach_file(msg, attachment_path)
            if not attachment_success:
                return None

            log_debug(logger, "Email message created successfully",
                     extra={"subject": msg['Subject'], "attachment": os.path.basename(attachment_path)})
            return msg

        except Exception as e:
            log_error(logger, e, "_create_email_message",
                     {"attachment": attachment_path, "subject": custom_subject})
            return None

    def _attach_file(self, msg: MIMEMultipart, file_path: str) -> bool:
        """Attach file to email message with proper error handling."""
        try:
            filename = os.path.basename(file_path)

            with open(file_path, "rb") as f:
                file_data = f.read()

            # Determine MIME type based on file extension
            mime_type, encoding = self._get_mime_type(filename)

            if mime_type == 'application/octet-stream':
                # Generic binary attachment
                from email.mime.application import MIMEApplication
                part = MIMEApplication(file_data, Name=filename)
            else:
                # Specific MIME type
                part = MIMEText(file_data.decode('utf-8', errors='ignore'), _subtype=mime_type.split('/')[-1])

            part['Content-Disposition'] = f'attachment; filename="{filename}"'
            part.set_type(mime_type)

            msg.attach(part)

            log_debug(logger, f"File attached successfully: {filename} ({len(file_data)} bytes)")
            return True

        except Exception as e:
            log_error(logger, e, "_attach_file", {"file_path": file_path})
            return False

    def _get_mime_type(self, filename: str) -> Tuple[str, Optional[str]]:
        """Get MIME type for file based on extension."""
        extension = Path(filename).suffix.lower()

        mime_types = {
            '.xlsx': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', None),
            '.xls': ('application/vnd.ms-excel', None),
            '.csv': ('text/csv', 'utf-8'),
            '.json': ('application/json', 'utf-8'),
            '.txt': ('text/plain', 'utf-8'),
            '.pdf': ('application/pdf', None),
            '.png': ('image/png', None),
            '.jpg': ('image/jpeg', None),
            '.jpeg': ('image/jpeg', None),
        }

        return mime_types.get(extension, ('application/octet-stream', None))

    def _send_with_retry(self, msg: MIMEMultipart, max_retries: int = 3) -> bool:
        """Send email with retry logic for robustness."""
        for attempt in range(max_retries):
            try:
                log_debug(logger, f"Email send attempt {attempt + 1}/{max_retries}")

                # Create new SMTP connection for each attempt
                server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
                server.starttls()

                # Login and send
                server.login(self.config['sender_email'], self.config['password'])
                server.send_message(msg)
                server.quit()

                log_info(logger, f"Email sent successfully on attempt {attempt + 1}")
                return True

            except smtplib.SMTPAuthenticationError as e:
                log_error(logger, e, f"send_email_attempt_{attempt + 1}",
                         {"error_type": "authentication", "attempt": attempt + 1})
                if attempt == max_retries - 1:
                    raise ProjectNIVException("SMTP authentication failed. Check credentials.",
                                            "EMAIL_AUTH_FAILED")
                time.sleep(2 ** attempt)  # Exponential backoff

            except smtplib.SMTPConnectError as e:
                log_error(logger, e, f"send_email_attempt_{attempt + 1}",
                         {"error_type": "connection", "attempt": attempt + 1})
                if attempt == max_retries - 1:
                    raise ProjectNIVException("SMTP connection failed. Check server settings.",
                                            "EMAIL_CONNECTION_FAILED")
                time.sleep(2 ** attempt)

            except smtplib.SMTPRecipientsRefused as e:
                log_error(logger, e, f"send_email_attempt_{attempt + 1}",
                         {"error_type": "recipients_refused", "attempt": attempt + 1})
                raise ProjectNIVException("Email recipients refused by server",
                                        "EMAIL_RECIPIENTS_REFUSED")

            except Exception as e:
                log_error(logger, e, f"send_email_attempt_{attempt + 1}",
                         {"error_type": "general", "attempt": attempt + 1})
                if attempt == max_retries - 1:
                    raise ProjectNIVException(f"Email sending failed after {max_retries} attempts",
                                            "EMAIL_SEND_FAILED")
                time.sleep(2 ** attempt)

        return False

    def _get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        try:
            return os.path.getsize(file_path)
        except OSError:
            return 0

    def _get_file_size_formatted(self, file_path: str) -> str:
        """Get formatted file size."""
        size_bytes = self._get_file_size(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def test_connection(self) -> bool:
        """
        Test SMTP connection and authentication.

        Returns:
            bool: True if connection test successful
        """
        try:
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['sender_email'], self.config['password'])
            server.quit()

            log_info(logger, "SMTP connection test successful")
            return True

        except Exception as e:
            log_error(logger, e, "test_connection")
            return False

# Legacy function for backward compatibility
def send_email(attachment_path: str, summary: str, config_path: str = 'config.json') -> bool:
    """
    Send email with report attachment (legacy function).

    Args:
        attachment_path: Path to the report file to attach
        summary: Summary text to include in email body
        config_path: Path to configuration file

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        email_sender = EmailSender(config_path=config_path)
        return email_sender.send_email(attachment_path, summary)
    except Exception as e:
        log_error(logger, e, "legacy_send_email")
        return False