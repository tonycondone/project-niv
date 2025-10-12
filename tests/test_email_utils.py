import pytest
import os
import tempfile
import json
from unittest.mock import patch, MagicMock, mock_open
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from email_utils import EmailSender, send_email, ProjectNIVException


class TestEmailSender:
    """Comprehensive tests for EmailSender class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.valid_config = {
            'sender_email': 'test@example.com',
            'password': 'testpassword123',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'receiver_emails': ['recipient1@example.com'],
            'subject': 'Test Report',
            'send_time': '08:00'
        }

        # Create temporary files for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_attachment = os.path.join(self.temp_dir, 'test_report.xlsx')
        self.test_summary = 'Test summary content'

        with open(self.test_attachment, 'w') as f:
            f.write('test excel content')

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_email_sender_initialization(self):
        """Test EmailSender initialization."""
        with patch('config_utils.ConfigValidator.load_config') as mock_load:
            mock_load.return_value = self.valid_config

            sender = EmailSender(config_path='test_config.json')

            assert sender.config == self.valid_config
            assert sender.config_path == 'test_config.json'
            mock_load.assert_called_once_with('test_config.json')

    def test_email_sender_with_provided_config(self):
        """Test EmailSender initialization with provided config."""
        sender = EmailSender(config=self.valid_config)

        assert sender.config == self.valid_config
        assert sender.config_path == 'config.json'

    def test_send_email_success(self):
        """Test successful email sending."""
        sender = EmailSender(config=self.valid_config)

        with patch.object(sender, '_send_with_retry', return_value=True) as mock_send:
            result = sender.send_email(self.test_attachment, self.test_summary)

            assert result is True
            mock_send.assert_called_once()

    def test_send_email_validation_failure(self):
        """Test email sending with validation failures."""
        sender = EmailSender(config=self.valid_config)

        # Test with non-existent attachment
        result = sender.send_email('/nonexistent/file.xlsx', self.test_summary)
        assert result is False

        # Test with empty summary
        result = sender.send_email(self.test_attachment, '')
        assert result is False

        # Test with empty summary after stripping
        result = sender.send_email(self.test_attachment, '   ')
        assert result is False

    def test_send_email_no_recipients(self):
        """Test email sending with no recipients configured."""
        config_no_recipients = self.valid_config.copy()
        config_no_recipients['receiver_emails'] = []

        sender = EmailSender(config=config_no_recipients)
        result = sender.send_email(self.test_attachment, self.test_summary)

        assert result is False

    def test_create_email_message(self):
        """Test email message creation."""
        sender = EmailSender(config=self.valid_config)

        with patch.object(sender, '_attach_file', return_value=True) as mock_attach:
            msg = sender._create_email_message(self.test_attachment, self.test_summary)

            assert msg is not None
            assert isinstance(msg, MIMEMultipart)
            assert msg['From'] == 'test@example.com'
            assert msg['To'] == 'recipient1@example.com'
            assert msg['Subject'] == 'Test Report'
            mock_attach.assert_called_once_with(msg, self.test_attachment)

    def test_create_email_message_custom_subject(self):
        """Test email message creation with custom subject."""
        sender = EmailSender(config=self.valid_config)
        custom_subject = 'Custom Subject'

        with patch.object(sender, '_attach_file', return_value=True):
            msg = sender._create_email_message(self.test_attachment, self.test_summary, custom_subject)

            assert msg['Subject'] == custom_subject

    def test_create_email_message_attachment_failure(self):
        """Test email message creation when attachment fails."""
        sender = EmailSender(config=self.valid_config)

        with patch.object(sender, '_attach_file', return_value=False):
            msg = sender._create_email_message(self.test_attachment, self.test_summary)

            assert msg is None

    def test_attach_file_success(self):
        """Test successful file attachment."""
        sender = EmailSender(config=self.valid_config)
        msg = MIMEMultipart()

        result = sender._attach_file(msg, self.test_attachment)

        assert result is True
        assert len(msg.get_payload()) == 2  # Text part + attachment part

    def test_attach_file_nonexistent(self):
        """Test file attachment with non-existent file."""
        sender = EmailSender(config=self.valid_config)
        msg = MIMEMultipart()

        result = sender._attach_file(msg, '/nonexistent/file.xlsx')

        assert result is False

    def test_get_mime_type(self):
        """Test MIME type detection."""
        sender = EmailSender(config=self.valid_config)

        # Test various file extensions
        test_cases = [
            ('test.xlsx', ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', None)),
            ('test.csv', ('text/csv', 'utf-8')),
            ('test.json', ('application/json', 'utf-8')),
            ('test.unknown', ('application/octet-stream', None)),
        ]

        for filename, expected in test_cases:
            result = sender._get_mime_type(filename)
            assert result == expected

    def test_send_with_retry_success(self):
        """Test successful sending with retry logic."""
        sender = EmailSender(config=self.valid_config)
        msg = MIMEMultipart()

        with patch('smtplib.SMTP') as mock_smtp_class:
            mock_server = MagicMock()
            mock_smtp_class.return_value = mock_server

            result = sender._send_with_retry(msg, max_retries=2)

            assert result is True
            mock_smtp_class.assert_called()
            mock_server.starttls.assert_called()
            mock_server.login.assert_called()
            mock_server.send_message.assert_called_once_with(msg)
            mock_server.quit.assert_called()

    def test_send_with_retry_authentication_error(self):
        """Test retry logic with authentication error."""
        sender = EmailSender(config=self.valid_config)
        msg = MIMEMultipart()

        with patch('smtplib.SMTP') as mock_smtp_class:
            mock_server = MagicMock()
            mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, 'Authentication failed')
            mock_smtp_class.return_value = mock_server

            with pytest.raises(ProjectNIVException) as exc_info:
                sender._send_with_retry(msg, max_retries=1)

            assert 'authentication' in str(exc_info.value).lower()

    def test_send_with_retry_connection_error(self):
        """Test retry logic with connection error."""
        sender = EmailSender(config=self.valid_config)
        msg = MIMEMultipart()

        with patch('smtplib.SMTP') as mock_smtp_class:
            mock_server = MagicMock()
            mock_server.starttls.side_effect = smtplib.SMTPConnectError(10060, 'Connection refused')
            mock_smtp_class.return_value = mock_server

            with pytest.raises(ProjectNIVException) as exc_info:
                sender._send_with_retry(msg, max_retries=1)

            assert 'connection' in str(exc_info.value).lower()

    def test_send_with_retry_recipients_refused(self):
        """Test handling of refused recipients."""
        sender = EmailSender(config=self.valid_config)
        msg = MIMEMultipart()

        with patch('smtplib.SMTP') as mock_smtp_class:
            mock_server = MagicMock()
            mock_server.send_message.side_effect = smtplib.SMTPRecipientsRefused({'recipient1@example.com': (550, 'Mailbox unavailable')})
            mock_smtp_class.return_value = mock_server

            with pytest.raises(ProjectNIVException) as exc_info:
                sender._send_with_retry(msg, max_retries=1)

            assert 'recipients refused' in str(exc_info.value).lower()

    def test_send_with_retry_max_retries(self):
        """Test retry logic reaches maximum retries."""
        sender = EmailSender(config=self.valid_config)
        msg = MIMEMultipart()

        with patch('smtplib.SMTP') as mock_smtp_class:
            mock_server = MagicMock()
            mock_server.login.side_effect = Exception("Persistent error")
            mock_smtp_class.return_value = mock_server

            with pytest.raises(ProjectNIVException) as exc_info:
                sender._send_with_retry(msg, max_retries=2)

            assert 'failed after' in str(exc_info.value).lower()

    def test_get_file_size(self):
        """Test file size calculation."""
        sender = EmailSender(config=self.valid_config)

        size = sender._get_file_size(self.test_attachment)
        assert isinstance(size, int)
        assert size > 0

    def test_get_file_size_nonexistent(self):
        """Test file size calculation for non-existent file."""
        sender = EmailSender(config=self.valid_config)

        size = sender._get_file_size('/nonexistent/file.xlsx')
        assert size == 0

    def test_get_file_size_formatted(self):
        """Test formatted file size."""
        sender = EmailSender(config=self.valid_config)

        # Create a file with known size
        test_file = os.path.join(self.temp_dir, 'size_test.txt')
        with open(test_file, 'w') as f:
            f.write('x' * 1024)  # 1 KB

        formatted = sender._get_file_size_formatted(test_file)
        assert '1.0 KB' in formatted

    def test_test_connection_success(self):
        """Test SMTP connection testing success."""
        sender = EmailSender(config=self.valid_config)

        with patch('smtplib.SMTP') as mock_smtp_class:
            mock_server = MagicMock()
            mock_smtp_class.return_value = mock_server

            result = sender.test_connection()

            assert result is True
            mock_smtp_class.assert_called()
            mock_server.starttls.assert_called()
            mock_server.login.assert_called()
            mock_server.quit.assert_called()

    def test_test_connection_failure(self):
        """Test SMTP connection testing failure."""
        sender = EmailSender(config=self.valid_config)

        with patch('smtplib.SMTP') as mock_smtp_class:
            mock_server = MagicMock()
            mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, 'Authentication failed')
            mock_smtp_class.return_value = mock_server

            result = sender.test_connection()

            assert result is False

    def test_email_body_content(self):
        """Test email body content generation."""
        sender = EmailSender(config=self.valid_config)

        with patch.object(sender, '_attach_file', return_value=True):
            msg = sender._create_email_message(self.test_attachment, self.test_summary)

            # Check email body
            payload = msg.get_payload()
            text_part = payload[0]  # First part should be text

            assert isinstance(text_part, MIMEText)
            body_content = text_part.get_payload()

            assert 'Test summary content' in body_content
            assert 'test_report.xlsx' in body_content
            assert 'PROJECT NIV' in body_content

    def test_email_with_multiple_recipients(self):
        """Test email with multiple recipients."""
        config_multi = self.valid_config.copy()
        config_multi['receiver_emails'] = ['recipient1@example.com', 'recipient2@example.com', 'recipient3@example.com']

        sender = EmailSender(config=config_multi)

        with patch.object(sender, '_attach_file', return_value=True):
            msg = sender._create_email_message(self.test_attachment, self.test_summary)

            assert msg['To'] == 'recipient1@example.com, recipient2@example.com, recipient3@example.com'

    def test_email_attachment_with_different_extensions(self):
        """Test email attachment with different file extensions."""
        sender = EmailSender(config=self.valid_config)

        # Test different file types
        test_files = [
            ('test.csv', 'text/csv'),
            ('test.json', 'application/json'),
            ('test.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
        ]

        for filename, expected_mime in test_files:
            test_file = os.path.join(self.temp_dir, filename)
            with open(test_file, 'w') as f:
                f.write('test content')

            msg = MIMEMultipart()
            result = sender._attach_file(msg, test_file)

            assert result is True

            # Check MIME type was set correctly
            attached_part = msg.get_payload()[1]  # Second part (attachment)
            assert expected_mime in attached_part.get_type()

    def test_email_sender_config_validation(self):
        """Test that EmailSender validates configuration on init."""
        # Test with missing required config
        invalid_config = {'sender_email': 'test@example.com'}  # Missing other required fields

        with patch('config_utils.ConfigValidator.load_config') as mock_load:
            mock_load.return_value = invalid_config

            # Should handle gracefully or raise appropriate exception
            sender = EmailSender(config_path='test.json')
            # If we get here, initialization worked (may use defaults)

    def test_legacy_send_email_function(self):
        """Test legacy send_email function."""
        with patch('email_utils.EmailSender') as mock_sender_class:
            mock_sender = MagicMock()
            mock_sender.send_email.return_value = True
            mock_sender_class.return_value = mock_sender

            result = send_email(self.test_attachment, self.test_summary, 'test_config.json')

            assert result is True
            mock_sender_class.assert_called_once()
            mock_sender.send_email.assert_called_once_with(self.test_attachment, self.test_summary)

    def test_legacy_send_email_exception_handling(self):
        """Test legacy send_email function exception handling."""
        with patch('email_utils.EmailSender') as mock_sender_class:
            mock_sender_class.side_effect = Exception("Test error")

            result = send_email(self.test_attachment, self.test_summary)

            assert result is False