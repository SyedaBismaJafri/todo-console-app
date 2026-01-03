"""
Background Reminder Service
A module that can run in the background to continuously check for upcoming tasks and send notifications.
"""

import time
from datetime import datetime
from services.task_service import TaskService
from services.task_subagent import TaskSubagent
from services.storage_engine import StorageSkill
from services.notification_engine import NotificationSkill
from services.time_engine import TimeSkill


class BackgroundReminderService:
    """Service to run in the background and check for upcoming tasks."""
    
    def __init__(self, check_interval=60):  # Check every minute
        """
        Initialize the background reminder service.
        
        Args:
            check_interval: Time in seconds between checks (default: 60 seconds)
        """
        self.check_interval = check_interval
        self.storage_skill = StorageSkill()
        self.notification_skill = NotificationSkill()
        self.time_skill = TimeSkill()
        self.running = False
        
        # Initialize task service to load tasks
        self.task_service = TaskService()
        self.task_subagent = TaskSubagent(self.task_service)
        # Set the task_subagent reference in task_service for saving tasks
        self.task_service.set_task_subagent(self.task_subagent)
    
    def check_upcoming_tasks(self):
        """Check for tasks due within the next hour and send notifications."""
        all_tasks = self.task_service.get_all_tasks()
        
        for task in all_tasks:
            if task.due_date and not task.completed:
                # Check if the task is due within the next hour using TimeSkill
                if self.time_skill.is_due_within_hours(task.due_date, 1):
                    # Check if we've already notified about this task recently
                    # to avoid spamming notifications
                    notification_sent = getattr(task, 'notification_sent', False)
                    if not notification_sent:
                        self.notification_skill.send_alert(
                            title="Upcoming Task Reminder",
                            message=f"Task '{task.title}' is due within the next hour!"
                        )
                        # Mark that notification was sent for this task
                        # In a real implementation, you might want to track this differently
                        task.notification_sent = True
    
    def start(self):
        """Start the background reminder service."""
        print("Starting background reminder service...")
        self.running = True
        
        while self.running:
            try:
                # Reload tasks from storage to get any updates from other processes
                self.task_subagent.load_tasks_from_storage()
                
                # Check for upcoming tasks
                self.check_upcoming_tasks()
                
                # Wait for the specified interval before checking again
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                print("\nStopping background reminder service...")
                self.running = False
            except Exception as e:
                print(f"Error in background reminder service: {e}")
                time.sleep(self.check_interval)  # Continue running even if there's an error
    
    def stop(self):
        """Stop the background reminder service."""
        self.running = False
        print("Background reminder service stopped.")


def run_background_service():
    """Function to run the background service."""
    service = BackgroundReminderService()
    try:
        service.start()
    except KeyboardInterrupt:
        service.stop()


if __name__ == "__main__":
    run_background_service()