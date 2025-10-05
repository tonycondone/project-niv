import schedule
import time
import os
import threading
from datetime import datetime, timedelta
from typing import Optional, Callable
from logger_config import logger
from config_manager import config
from data_processor import DataProcessor
from email_utils import EmailSender

class ReportScheduler:
    """Enhanced scheduler with error handling, retry logic, and flexible scheduling."""
    
    def __init__(self):
        self.config = config
        self.data_processor = DataProcessor()
        self.email_sender = EmailSender()
        self.is_running = False
        self.retry_count = 0
        self.max_retries = 3
        self.retry_delay = 300  # 5 minutes
    
    def send_report_job(self):
        """Main job function that generates and sends reports."""
        try:
            logger.info("Starting scheduled report generation")
            
            # Generate report
            excel_path, summary_text, summary_stats = self.data_processor.generate_report()
            
            # Get chart path if available
            chart_path = None
            reports_dir = self.config.get('reports_dir', 'reports')
            chart_files = [f for f in os.listdir(reports_dir) if f.startswith('chart_') and f.endswith('.png')]
            if chart_files:
                chart_path = os.path.join(reports_dir, sorted(chart_files)[-1])  # Get latest chart
            
            # Prepare attachments
            attachments = [excel_path]
            if chart_path:
                attachments.append(chart_path)
            
            # Send email
            success = self.email_sender.send_email(
                attachments=attachments,
                summary_text=summary_text,
                summary_stats=summary_stats,
                chart_path=chart_path
            )
            
            if success:
                logger.info("Scheduled report sent successfully")
                self.retry_count = 0  # Reset retry count on success
            else:
                logger.error("Failed to send scheduled report")
                self._handle_send_failure()
                
        except Exception as e:
            logger.error(f"Error in scheduled report job: {e}")
            self._handle_send_failure()
    
    def _handle_send_failure(self):
        """Handle email sending failures with retry logic."""
        self.retry_count += 1
        
        if self.retry_count <= self.max_retries:
            logger.warning(f"Retrying email send in {self.retry_delay} seconds (attempt {self.retry_count}/{self.max_retries})")
            # Schedule retry
            schedule.every(self.retry_delay).seconds.do(self.send_report_job)
        else:
            logger.error(f"Max retries ({self.max_retries}) exceeded. Giving up on this report.")
            self.retry_count = 0
    
    def setup_schedule(self, schedule_type: str = "weekly", send_time: str = "08:00", 
                      day_of_week: str = "monday"):
        """Setup scheduling based on configuration."""
        try:
            # Clear existing schedules
            schedule.clear()
            
            # Get schedule settings from config
            schedule_type = self.config.get('schedule_type', schedule_type)
            send_time = self.config.get('send_time', send_time)
            day_of_week = self.config.get('day_of_week', day_of_week).lower()
            
            # Setup schedule based on type
            if schedule_type.lower() == "daily":
                schedule.every().day.at(send_time).do(self.send_report_job)
                logger.info(f"Daily schedule set for {send_time}")
                
            elif schedule_type.lower() == "weekly":
                day_mapping = {
                    'monday': schedule.every().monday,
                    'tuesday': schedule.every().tuesday,
                    'wednesday': schedule.every().wednesday,
                    'thursday': schedule.every().thursday,
                    'friday': schedule.every().friday,
                    'saturday': schedule.every().saturday,
                    'sunday': schedule.every().sunday
                }
                
                if day_of_week in day_mapping:
                    day_mapping[day_of_week].at(send_time).do(self.send_report_job)
                    logger.info(f"Weekly schedule set for {day_of_week} at {send_time}")
                else:
                    logger.error(f"Invalid day of week: {day_of_week}")
                    return False
                    
            elif schedule_type.lower() == "monthly":
                # Monthly on the 1st at specified time
                schedule.every().month.do(self.send_report_job)
                logger.info(f"Monthly schedule set for 1st at {send_time}")
                
            else:
                logger.error(f"Invalid schedule type: {schedule_type}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting up schedule: {e}")
            return False
    
    def test_email_connection(self) -> bool:
        """Test email configuration before starting scheduler."""
        try:
            logger.info("Testing email configuration...")
            return self.email_sender.test_connection()
        except Exception as e:
            logger.error(f"Email connection test failed: {e}")
            return False
    
    def run_scheduler(self, schedule_type: str = "weekly", send_time: str = "08:00", 
                     day_of_week: str = "monday"):
        """Run the scheduler with specified parameters."""
        try:
            # Test email connection first
            if not self.test_email_connection():
                logger.error("Email configuration test failed. Please check your settings.")
                return False
            
            # Setup schedule
            if not self.setup_schedule(schedule_type, send_time, day_of_week):
                logger.error("Failed to setup schedule")
                return False
            
            self.is_running = True
            logger.info(f"PROJECT NIV Scheduler started successfully")
            logger.info(f"Schedule: {schedule_type} at {send_time}")
            if schedule_type.lower() == "weekly":
                logger.info(f"Day: {day_of_week}")
            
            # Show next run time
            next_run = schedule.next_run()
            if next_run:
                logger.info(f"Next report scheduled for: {next_run}")
            
            # Main scheduler loop
            while self.is_running:
                try:
                    schedule.run_pending()
                    time.sleep(60)  # Check every minute
                except KeyboardInterrupt:
                    logger.info("Scheduler stopped by user")
                    break
                except Exception as e:
                    logger.error(f"Error in scheduler loop: {e}")
                    time.sleep(60)  # Continue running despite errors
            
            return True
            
        except Exception as e:
            logger.error(f"Error running scheduler: {e}")
            return False
    
    def stop_scheduler(self):
        """Stop the scheduler gracefully."""
        self.is_running = False
        schedule.clear()
        logger.info("Scheduler stopped")

def run_scheduler(send_time="08:00"):
    """Legacy function for backward compatibility."""
    scheduler = ReportScheduler()
    return scheduler.run_scheduler(send_time=send_time)

if __name__ == "__main__":
    scheduler = ReportScheduler()
    try:
        scheduler.run_scheduler()
    except KeyboardInterrupt:
        logger.info("Scheduler interrupted by user")
        scheduler.stop_scheduler()