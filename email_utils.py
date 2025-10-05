import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from datetime import datetime
from typing import List, Optional, Dict
from jinja2 import Template, Environment, FileSystemLoader
from logger_config import logger
from config_manager import config

class EmailSender:
    """Handles email composition and sending with HTML templates."""
    
    def __init__(self):
        self.config = config
        self.template_env = Environment(loader=FileSystemLoader('templates'))
        self.setup_email_config()
    
    def setup_email_config(self):
        """Setup email configuration from config manager."""
        self.sender_email = self.config.get('sender_email')
        self.password = self.config.get('password')
        self.smtp_server = self.config.get('smtp_server')
        self.smtp_port = self.config.get('smtp_port')
        self.receiver_emails = self.config.get('receiver_emails', [])
        self.subject = self.config.get('subject', 'Weekly Data Report')
    
    def create_html_email(self, summary_text: str, summary_stats: Dict = None, 
                         chart_path: Optional[str] = None) -> str:
        """Create HTML email content using Jinja2 template."""
        try:
            template = self.template_env.get_template('email_template.html')
            
            # Prepare template data
            template_data = {
                'subject': self.subject,
                'report_date': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
                'summary_text': summary_text,
                'summary_stats': summary_stats.get('summary_stats', []) if summary_stats else [],
                'chart_path': chart_path
            }
            
            html_content = template.render(**template_data)
            logger.info("HTML email template rendered successfully")
            return html_content
            
        except Exception as e:
            logger.error(f"Error creating HTML email: {e}")
            # Fallback to plain text
            return self.create_plain_text_email(summary_text)
    
    def create_plain_text_email(self, summary_text: str) -> str:
        """Create plain text email as fallback."""
        return f"""Hi,

Please find attached the weekly report.

Summary:
{summary_text}

Regards,
PROJECT NIV - Automated Reporting System

Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"""
    
    def attach_files(self, msg: MIMEMultipart, attachments: List[str]):
        """Attach multiple files to email message."""
        try:
            for attachment_path in attachments:
                if not os.path.exists(attachment_path):
                    logger.warning(f"Attachment file not found: {attachment_path}")
                    continue
                
                # Determine file type and create appropriate MIME type
                if attachment_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    # Image attachment
                    with open(attachment_path, "rb") as f:
                        img_data = f.read()
                        image = MIMEImage(img_data)
                        image.add_header('Content-Disposition', 
                                      f'attachment; filename="{os.path.basename(attachment_path)}"')
                        msg.attach(image)
                        logger.info(f"Attached image: {attachment_path}")
                
                else:
                    # Other file types (Excel, CSV, etc.)
                    with open(attachment_path, "rb") as f:
                        file_data = f.read()
                        part = MIMEApplication(file_data, Name=os.path.basename(attachment_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                        msg.attach(part)
                        logger.info(f"Attached file: {attachment_path}")
                        
        except Exception as e:
            logger.error(f"Error attaching files: {e}")
            raise
    
    def send_email(self, attachments: List[str], summary_text: str, 
                   summary_stats: Dict = None, chart_path: Optional[str] = None) -> bool:
        """Send email with attachments and HTML content."""
        try:
            # Validate configuration
            if not all([self.sender_email, self.password, self.smtp_server, self.receiver_emails]):
                raise ValueError("Missing required email configuration")
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = ", ".join(self.receiver_emails)
            msg['Subject'] = self.subject
            
            # Create email content
            html_content = self.create_html_email(summary_text, summary_stats, chart_path)
            plain_content = self.create_plain_text_email(summary_text)
            
            # Attach both plain text and HTML versions
            msg.attach(MIMEText(plain_content, 'plain'))
            msg.attach(MIMEText(html_content, 'html'))
            
            # Attach files
            if attachments:
                self.attach_files(msg, attachments)
            
            # Send email
            logger.info(f"Sending email to {len(self.receiver_emails)} recipients")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.send_message(msg)
            server.quit()
            
            logger.info("Email sent successfully")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test SMTP connection without sending email."""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.quit()
            logger.info("SMTP connection test successful")
            return True
        except Exception as e:
            logger.error(f"SMTP connection test failed: {e}")
            return False

# Backward compatibility functions
def send_email(attachment_path, summary):
    """Legacy function for backward compatibility."""
    sender = EmailSender()
    attachments = [attachment_path] if attachment_path else []
    return sender.send_email(attachments, summary)

def send_email_with_chart(attachment_path, summary, chart_path=None):
    """Enhanced function that supports chart attachments."""
    sender = EmailSender()
    attachments = [attachment_path] if attachment_path else []
    if chart_path and os.path.exists(chart_path):
        attachments.append(chart_path)
    return sender.send_email(attachments, summary, chart_path=chart_path)