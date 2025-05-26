import schedule
import time
from main import main

def run_scheduler(send_time="08:00"):
    schedule.every().monday.at(send_time).do(main)  # Sends every Monday

    print(f"[PROJECT NIV] Scheduler started. Next send at {send_time} on Monday.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()