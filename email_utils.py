import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(attachment_path, summary):
    print("📧 [PROJECT NIV] Starting email process...")
    
    # Load configuration
    print("⚙️ Loading email configuration...")
    config = json.load(open('config.json'))
    print(f"📤 Sender: {config['sender_email']}")
    print(f"📥 Recipients: {', '.join(config['receiver_emails'])}")
    print(f"📋 Subject: {config['subject']}")
    
    # Create email message
    print("📝 Creating email message...")
    msg = MIMEMultipart()
    msg['From'] = config['sender_email']
    msg['To'] = ", ".join(config['receiver_emails'])
    msg['Subject'] = config['subject']

    # Email body
    print("📄 Preparing email body...")
    body = f"Hi,\n\nPlease find attached the weekly report.\n\nSummary:\n{summary}\n\nRegards,\nPROJECT NIV"
    msg.attach(MIMEText(body, 'plain'))

    # Attach file
    print(f"📎 Attaching file: {attachment_path}")
    with open(attachment_path, "rb") as f:
        part = MIMEApplication(f.read(), Name="report.xlsx")
        part['Content-Disposition'] = 'attachment; filename="report.xlsx"'
        msg.attach(part)
    print("✅ File attached successfully!")

    # Send email
    print("🚀 Connecting to SMTP server...")
    try:
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        print("🔐 Starting TLS encryption...")
        server.starttls()
        print("🔑 Authenticating...")
        server.login(config['sender_email'], config['password'])
        print("📤 Sending email...")
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
        print("🎉 PROJECT NIV email process completed!")
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        print("⚠️ Note: Email credentials in config.json need to be configured for actual sending")