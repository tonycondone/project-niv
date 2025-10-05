import os
import sys
from data_processor import DataProcessor
from email_utils import EmailSender
from logger_config import logger
from config_manager import config

def main():
    """Main function to generate and send reports."""
    try:
        logger.info("Starting PROJECT NIV report generation")
        
        # Initialize components
        data_processor = DataProcessor()
        email_sender = EmailSender()
        
        # Test email connection first
        if not email_sender.test_connection():
            logger.error("Email connection test failed. Please check your configuration.")
            return False
        
        # Generate report
        logger.info("Generating report...")
        excel_path, summary_text, summary_stats = data_processor.generate_report()
        
        # Get chart path if available
        chart_path = None
        reports_dir = config.get('reports_dir', 'reports')
        if os.path.exists(reports_dir):
            chart_files = [f for f in os.listdir(reports_dir) if f.startswith('chart_') and f.endswith('.png')]
            if chart_files:
                chart_path = os.path.join(reports_dir, sorted(chart_files)[-1])  # Get latest chart
        
        # Prepare attachments
        attachments = [excel_path]
        if chart_path and os.path.exists(chart_path):
            attachments.append(chart_path)
        
        # Send email
        logger.info("Sending email...")
        success = email_sender.send_email(
            attachments=attachments,
            summary_text=summary_text,
            summary_stats=summary_stats,
            chart_path=chart_path
        )
        
        if success:
            logger.info("Report sent successfully!")
            print("✅ Report generated and sent successfully!")
            return True
        else:
            logger.error("Failed to send report")
            print("❌ Failed to send report. Check logs for details.")
            return False
            
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        print(f"❌ Error: {e}")
        return False

def test_configuration():
    """Test the application configuration."""
    try:
        logger.info("Testing configuration...")
        
        # Test config loading
        if not config.validate_config():
            print("❌ Configuration validation failed")
            return False
        
        # Test data file
        data_file = config.get('data_file', 'data/sample.csv')
        if not os.path.exists(data_file):
            print(f"❌ Data file not found: {data_file}")
            return False
        
        # Test email connection
        email_sender = EmailSender()
        if not email_sender.test_connection():
            print("❌ Email connection test failed")
            return False
        
        print("✅ Configuration test passed!")
        return True
        
    except Exception as e:
        logger.error(f"Configuration test failed: {e}")
        print(f"❌ Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_configuration()
    else:
        main()