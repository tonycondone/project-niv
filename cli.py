#!/usr/bin/env python3
"""
PROJECT NIV - Command Line Interface
Enhanced CLI tool for managing automated email reports.
"""

import argparse
import sys
import os
from datetime import datetime
from logger_config import logger
from config_manager import config
from data_processor import DataProcessor
from email_utils import EmailSender
from scheduler import ReportScheduler

def setup_parser():
    """Setup command line argument parser."""
    parser = argparse.ArgumentParser(
        description="PROJECT NIV - Automated Email Reporting Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py send                    # Send report immediately
  python cli.py test                    # Test configuration
  python cli.py schedule --daily 09:00  # Schedule daily reports at 9 AM
  python cli.py schedule --weekly monday 08:00  # Schedule weekly reports
  python cli.py config --set sender_email user@example.com  # Update config
  python cli.py status                  # Show current status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Send command
    send_parser = subparsers.add_parser('send', help='Send report immediately')
    send_parser.add_argument('--data-file', help='Path to data file')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test configuration and email connection')
    
    # Schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Start scheduled reporting')
    schedule_group = schedule_parser.add_mutually_exclusive_group(required=True)
    schedule_group.add_argument('--daily', metavar='TIME', help='Schedule daily reports (e.g., 08:00)')
    schedule_group.add_argument('--weekly', nargs=2, metavar=('DAY', 'TIME'), 
                               help='Schedule weekly reports (e.g., monday 08:00)')
    schedule_group.add_argument('--monthly', metavar='TIME', help='Schedule monthly reports (e.g., 08:00)')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_subparsers = config_parser.add_subparsers(dest='config_action')
    
    config_show_parser = config_subparsers.add_parser('show', help='Show current configuration')
    config_set_parser = config_subparsers.add_parser('set', help='Set configuration value')
    config_set_parser.add_argument('key', help='Configuration key')
    config_set_parser.add_argument('value', help='Configuration value')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show application status')
    
    # Logs command
    logs_parser = subparsers.add_parser('logs', help='View recent logs')
    logs_parser.add_argument('--lines', type=int, default=50, help='Number of log lines to show')
    
    return parser

def send_report(data_file=None):
    """Send report immediately."""
    try:
        logger.info("Starting immediate report generation")
        
        # Initialize components
        data_processor = DataProcessor()
        email_sender = EmailSender()
        
        # Test email connection
        if not email_sender.test_connection():
            print("❌ Email connection test failed. Please check your configuration.")
            return False
        
        # Generate report
        print("📊 Generating report...")
        excel_path, summary_text, summary_stats = data_processor.generate_report(data_file)
        
        # Get chart path
        chart_path = None
        reports_dir = config.get('reports_dir', 'reports')
        if os.path.exists(reports_dir):
            chart_files = [f for f in os.listdir(reports_dir) if f.startswith('chart_') and f.endswith('.png')]
            if chart_files:
                chart_path = os.path.join(reports_dir, sorted(chart_files)[-1])
        
        # Prepare attachments
        attachments = [excel_path]
        if chart_path and os.path.exists(chart_path):
            attachments.append(chart_path)
        
        # Send email
        print("📧 Sending email...")
        success = email_sender.send_email(
            attachments=attachments,
            summary_text=summary_text,
            summary_stats=summary_stats,
            chart_path=chart_path
        )
        
        if success:
            print("✅ Report sent successfully!")
            print(f"📁 Excel report: {excel_path}")
            if chart_path:
                print(f"📊 Chart: {chart_path}")
            return True
        else:
            print("❌ Failed to send report. Check logs for details.")
            return False
            
    except Exception as e:
        logger.error(f"Error sending report: {e}")
        print(f"❌ Error: {e}")
        return False

def test_configuration():
    """Test configuration and email connection."""
    try:
        print("🔧 Testing configuration...")
        
        # Test config validation
        if not config.validate_config():
            print("❌ Configuration validation failed")
            return False
        print("✅ Configuration validation passed")
        
        # Test data file
        data_file = config.get('data_file', 'data/sample.csv')
        if not os.path.exists(data_file):
            print(f"❌ Data file not found: {data_file}")
            return False
        print(f"✅ Data file found: {data_file}")
        
        # Test email connection
        email_sender = EmailSender()
        if not email_sender.test_connection():
            print("❌ Email connection test failed")
            return False
        print("✅ Email connection test passed")
        
        # Test data processing
        try:
            data_processor = DataProcessor()
            df = data_processor.load_data(data_file)
            if data_processor.validate_data(df):
                print("✅ Data validation passed")
            else:
                print("❌ Data validation failed")
                return False
        except Exception as e:
            print(f"❌ Data processing test failed: {e}")
            return False
        
        print("\n🎉 All tests passed! Configuration is ready.")
        return True
        
    except Exception as e:
        logger.error(f"Configuration test failed: {e}")
        print(f"❌ Configuration test failed: {e}")
        return False

def start_scheduler(schedule_type, time_or_day, time=None):
    """Start the scheduler with specified parameters."""
    try:
        scheduler = ReportScheduler()
        
        if schedule_type == "daily":
            print(f"📅 Starting daily scheduler at {time_or_day}")
            return scheduler.run_scheduler("daily", time_or_day)
        elif schedule_type == "weekly":
            day, time = time_or_day, time
            print(f"📅 Starting weekly scheduler: {day} at {time}")
            return scheduler.run_scheduler("weekly", time, day)
        elif schedule_type == "monthly":
            print(f"📅 Starting monthly scheduler at {time_or_day}")
            return scheduler.run_scheduler("monthly", time_or_day)
        else:
            print(f"❌ Invalid schedule type: {schedule_type}")
            return False
            
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")
        print(f"❌ Error starting scheduler: {e}")
        return False

def show_config():
    """Show current configuration."""
    try:
        print("📋 Current Configuration:")
        print("=" * 50)
        
        config_items = [
            ("Sender Email", config.get('sender_email')),
            ("SMTP Server", config.get('smtp_server')),
            ("SMTP Port", config.get('smtp_port')),
            ("Receiver Emails", ", ".join(config.get('receiver_emails', []))),
            ("Subject", config.get('subject')),
            ("Data File", config.get('data_file')),
            ("Reports Directory", config.get('reports_dir')),
            ("Send Time", config.get('send_time')),
            ("Schedule Type", config.get('schedule_type', 'weekly')),
            ("Day of Week", config.get('day_of_week', 'monday'))
        ]
        
        for key, value in config_items:
            if key == "Receiver Emails" and value:
                print(f"{key:20}: {value}")
            elif key == "Sender Email" and value:
                # Mask password for security
                masked_value = value[:3] + "*" * (len(value) - 6) + value[-3:] if len(value) > 6 else "***"
                print(f"{key:20}: {masked_value}")
            else:
                print(f"{key:20}: {value}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error showing configuration: {e}")
        print(f"❌ Error: {e}")
        return False

def set_config(key, value):
    """Set configuration value."""
    try:
        # Convert value to appropriate type
        if key in ['smtp_port']:
            value = int(value)
        elif key in ['receiver_emails']:
            value = [email.strip() for email in value.split(',')]
        
        config.update(key, value)
        config.save_config()
        print(f"✅ Configuration updated: {key} = {value}")
        return True
        
    except Exception as e:
        logger.error(f"Error setting configuration: {e}")
        print(f"❌ Error: {e}")
        return False

def show_status():
    """Show application status."""
    try:
        print("📊 PROJECT NIV Status")
        print("=" * 50)
        
        # Check data file
        data_file = config.get('data_file', 'data/sample.csv')
        if os.path.exists(data_file):
            file_size = os.path.getsize(data_file)
            print(f"📁 Data file: {data_file} ({file_size} bytes)")
        else:
            print(f"❌ Data file: {data_file} (not found)")
        
        # Check reports directory
        reports_dir = config.get('reports_dir', 'reports')
        if os.path.exists(reports_dir):
            report_files = [f for f in os.listdir(reports_dir) if f.endswith(('.xlsx', '.png'))]
            print(f"📊 Reports directory: {reports_dir} ({len(report_files)} files)")
        else:
            print(f"❌ Reports directory: {reports_dir} (not found)")
        
        # Check logs directory
        if os.path.exists('logs'):
            log_files = [f for f in os.listdir('logs') if f.endswith('.log')]
            print(f"📝 Logs directory: logs/ ({len(log_files)} files)")
        else:
            print("❌ Logs directory: logs/ (not found)")
        
        # Test email connection
        try:
            email_sender = EmailSender()
            if email_sender.test_connection():
                print("✅ Email connection: OK")
            else:
                print("❌ Email connection: Failed")
        except Exception as e:
            print(f"❌ Email connection: Error - {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error showing status: {e}")
        print(f"❌ Error: {e}")
        return False

def show_logs(lines=50):
    """Show recent logs."""
    try:
        log_file = 'logs/project_niv.log'
        if not os.path.exists(log_file):
            print("❌ Log file not found")
            return False
        
        print(f"📝 Recent logs (last {lines} lines):")
        print("=" * 50)
        
        with open(log_file, 'r') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
            for line in recent_lines:
                print(line.rstrip())
        
        return True
        
    except Exception as e:
        logger.error(f"Error showing logs: {e}")
        print(f"❌ Error: {e}")
        return False

def main():
    """Main CLI function."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'send':
            send_report(args.data_file)
        elif args.command == 'test':
            test_configuration()
        elif args.command == 'schedule':
            if args.daily:
                start_scheduler("daily", args.daily)
            elif args.weekly:
                start_scheduler("weekly", args.weekly[0], args.weekly[1])
            elif args.monthly:
                start_scheduler("monthly", args.monthly)
        elif args.command == 'config':
            if args.config_action == 'show':
                show_config()
            elif args.config_action == 'set':
                set_config(args.key, args.value)
        elif args.command == 'status':
            show_status()
        elif args.command == 'logs':
            show_logs(args.lines)
        else:
            print(f"❌ Unknown command: {args.command}")
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"CLI error: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()