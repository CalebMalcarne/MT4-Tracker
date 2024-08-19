from datetime import datetime
from edit_config import getConfigData

class DailyTaskExecutor:
    def __init__(self):
        self.last_run_date = None

    def check_and_run_task(self, task):
        config = getConfigData()
        report_time = config.get("report_time", "00:30")
        now = datetime.now()

        check_time = datetime.now().strftime("%H:%M")   

        if check_time == report_time and self.last_run_date != now.date():
            task()
            self.last_run_date = now.date()  # Update last run date to today
            print(f"Task executed at {now.strftime('%Y-%m-%d %H:%M:%S')}")