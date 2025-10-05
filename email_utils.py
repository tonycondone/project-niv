import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config_utils import ConfigValidator
from logger import logger, log_error, log_info, ProjectNIVException

def send_email(attachment_path: str, summary: str, config_path: str = 'config.json') -> bool:
    """
    Send email with report attachment.

    Args:
        attachment_path: Path to the report file to attach
        summary: Summary text to include in email body
        config_path: Path to configuration file

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Load and validate configuration
        config = ConfigValidator.load_config(config_path)

        # Validate attachment exists
        if not os.path.exists(attachment_path):
            raise ProjectNIVException(f"Attachment file not found: {attachment_path}")

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = config['sender_email']
        msg['To'] = ", ".join(config['receiver_emails'])
        msg['Subject'] = config['subject']

        # Email body
        body = f"Hi,\n\nPlease find attached the weekly report.\n\nSummary:\n{summary}\n\nRegards,\nPROJECT NIV"
        msg.attach(MIMEText(body, 'plain'))

        # Attach file
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)

        # Send email
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['sender_email'], config['password'])
        server.send_message(msg)
        server.quit()

        log_info(logger, f"Email sent successfully to {len(config['receiver_emails'])} recipients")
        return True

    except Exception as e:
        log_error(logger, e, "send_email")
        return False