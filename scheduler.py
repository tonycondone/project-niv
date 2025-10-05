import schedule
import time
from main import main

def run_scheduler(send_time="08:00"):
    print("⏰ [PROJECT NIV] Starting automated scheduler...")
    print("=" * 60)
    
    schedule.every().monday.at(send_time).do(main)  # Sends every Monday

    print(f"📅 Scheduler configured to run every Monday at {send_time}")
    print(f"🔄 Next scheduled run: {schedule.next_run()}")
    print("=" * 60)
    print("⏳ Scheduler is running... (Press Ctrl+C to stop)")
    print("=" * 60)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user")
        print("👋 [PROJECT NIV] Goodbye!")

if __name__ == "__main__":
    run_scheduler()