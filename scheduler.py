import time
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

def scheduled_task():
    subprocess.run(["python", "update_rankings.py"])

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'cron', day_of_week='sun', hour=20, minute=0)
scheduler.start()

print("Scheduler started. Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(60)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler stopped.")
