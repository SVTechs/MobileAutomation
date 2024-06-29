from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_ADDED, EVENT_JOB_REMOVED
import yaml

class Task:
    def __init__(self, config_path):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_listener(self.job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_ADDED | EVENT_JOB_REMOVED)
        self.load_config(config_path)

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            for job in config['jobs']:
                self.scheduler.add_job(self.run_task, 'interval', minutes=job['interval'], id=job['id'], args=[job['task_name']])

    def run_task(self, task_name):
        print(f"Running task: {task_name}")
        # 这里添加具体的任务逻辑

    def job_listener(self, event):
        if event.exception:
            print(f"Job {event.job_id} failed with exception: {event.exception}")
        else:
            print(f"Job {event.job_id} executed successfully")

    def start(self):
        self.scheduler.start()
        print("Scheduler started")

    def stop(self):
        self.scheduler.shutdown()
        print("Scheduler stopped")

# 示例使用
if __name__ == "__main__":
    task = Task('config.yaml')
    task.start()
