from datetime import datetime
from edit_config import getConfigData

class DailyTaskExecutor:
    def __init__(self):
        self.last_run_date = None

    def check_and_run_task(self, task):
        config = getConfigData()
        report_time_str = config.get("report_time", "00:30")
        report_time = datetime.strptime(report_time_str, "%H:%M").time()
        
        now = datetime.now()

        # Check if the task has already been executed today
        if self.last_run_date == now.date():
            return  # Task has already been executed today

        # Check if the current time matches the scheduled report time exactly
        if now.time() == report_time:
            task()
            self.last_run_date = now.date()  # Update last run date to today
            print(f"Task executed at {now.strftime('%Y-%m-%d %H:%M:%S')}")