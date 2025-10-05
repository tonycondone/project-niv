from data_processor import generate_report
from email_utils import send_email

def main():
    print("🚀 [PROJECT NIV] Starting automated email reporting system...")
    print("=" * 60)
    
    # Generate report
    report_file, summary = generate_report()
    
    print("=" * 60)
    
    # Send email
    send_email(report_file, summary)
    
    print("=" * 60)
    print("🏁 [PROJECT NIV] Process completed!")

if __name__ == "__main__":
    main()