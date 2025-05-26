import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(attachment_path, summary):
    # Load configuration
    config = json.load(open('config.json'))
    msg = MIMEMultipart()
    msg['From'] = config['sender_email']
    msg['To'] = ", ".join(config['receiver_emails'])
    msg['Subject'] = config['subject']

    # Email body
    body = f"Hi,\n\nPlease find attached the weekly report.\n\nSummary:\n{summary}\n\nRegards,\nPROJECT NIV"
    msg.attach(MIMEText(body, 'plain'))

    # Attach file
    with open(attachment_path, "rb") as f:
        part = MIMEApplication(f.read(), Name="report.xlsx")
        part['Content-Disposition'] = 'attachment; filename="report.xlsx"'
        msg.attach(part)

    # Send email
    server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
    server.starttls()
    server.login(config['sender_email'], config['password'])
    server.send_message(msg)
    server.quit()