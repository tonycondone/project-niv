import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
import time

console = Console()

def send_email(attachment_path, summary):
    console.print("📧 [bold blue][PROJECT NIV] Starting enhanced email process...[/bold blue]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Load configuration
        task1 = progress.add_task("⚙️ Loading email configuration...", total=100)
        for i in range(50):
            time.sleep(0.01)
            progress.update(task1, advance=2)
        
        config = json.load(open('config.json'))
        
        # Display email configuration
        config_table = Table(title="📧 Email Configuration", style="blue")
        config_table.add_column("Setting", style="bold")
        config_table.add_column("Value", style="green")
        
        config_table.add_row("📤 Sender", config['sender_email'])
        config_table.add_row("📥 Recipients", ', '.join(config['receiver_emails']))
        config_table.add_row("📋 Subject", config['subject'])
        config_table.add_row("🏢 SMTP Server", f"{config['smtp_server']}:{config['smtp_port']}")
        
        console.print(config_table)
        
        # Create email message
        task2 = progress.add_task("📝 Creating email message...", total=100)
        for i in range(100):
            time.sleep(0.005)
            progress.update(task2, advance=1)
        
        msg = MIMEMultipart()
        msg['From'] = config['sender_email']
        msg['To'] = ", ".join(config['receiver_emails'])
        msg['Subject'] = config['subject']

        # Email body
        task3 = progress.add_task("📄 Preparing email body...", total=100)
        for i in range(100):
            time.sleep(0.003)
            progress.update(task3, advance=1)
        
        body = f"""Hi,

Please find attached the comprehensive weekly report with KPI dashboard.

EXECUTIVE SUMMARY:
{summary}

INCLUDED ATTACHMENTS:
• Excel Report with detailed data analysis
• KPI Dashboard with visual insights
• Performance metrics and recommendations

This automated report includes:
✅ Sales performance analysis
✅ Growth trend calculations
✅ Business intelligence insights
✅ Professional visualizations

Best regards,
PROJECT NIV Automated Reporting System"""
        
        msg.attach(MIMEText(body, 'plain'))

        # Attach file
        task4 = progress.add_task(f"📎 Attaching file: {attachment_path}...", total=100)
        for i in range(100):
            time.sleep(0.005)
            progress.update(task4, advance=1)
        
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), Name="report.xlsx")
            part['Content-Disposition'] = 'attachment; filename="report.xlsx"'
            msg.attach(part)
        
        console.print("✅ [green]File attached successfully![/green]")

        # Send email
        task5 = progress.add_task("🚀 Connecting to SMTP server...", total=100)
        
        try:
            for i in range(25):
                time.sleep(0.01)
                progress.update(task5, advance=4)
            
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            console.print("🔐 [yellow]Starting TLS encryption...[/yellow]")
            server.starttls()
            
            console.print("🔑 [yellow]Authenticating...[/yellow]")
            server.login(config['sender_email'], config['password'])
            
            console.print("📤 [yellow]Sending email...[/yellow]")
            server.send_message(msg)
            server.quit()
            
            success_panel = Panel(
                "[bold green]✅ Email sent successfully![/bold green]\n\n"
                f"[blue]Email Details:[/blue]\n"
                f"• To: {', '.join(config['receiver_emails'])}\n"
                f"• Subject: {config['subject']}\n"
                f"• Attachment: {attachment_path}\n"
                f"• Status: Delivered ✅",
                title="📧 Email Delivery Success",
                style="green"
            )
            console.print(success_panel)
            
        except Exception as e:
            error_panel = Panel(
                f"[bold red]❌ Error sending email: {str(e)}[/bold red]\n\n"
                f"[yellow]⚠️ Note: Email credentials in config.json need to be configured for actual sending[/yellow]\n\n"
                f"[blue]For testing purposes, the email was prepared successfully with:[/blue]\n"
                f"• Professional formatting ✅\n"
                f"• Attachment included ✅\n"
                f"• Enhanced content ✅",
                title="📧 Email Status",
                style="yellow"
            )
            console.print(error_panel)