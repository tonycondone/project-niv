from data_processor import generate_report
from email_utils import send_email

def main():
    report_file, summary = generate_report()
    send_email(report_file, summary)

if __name__ == "__main__":
    main()