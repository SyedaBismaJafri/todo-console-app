"""
Task Subagent
Handles task-specific operations using the search and sorting logic services.
"""

from typing import List, Dict, Any
from services.search_logic import search_data
from services.sorting_logic import sort_data
from services.validator import validate_priority
from services.time_engine import TimeSkill
from services.storage_engine import StorageSkill
from services.notification_engine import NotificationSkill
from models.task import Task
from services.task_service import TaskService


class TaskSubagent:
    """Subagent for handling task operations."""

    def __init__(self, task_service: TaskService):
        """Initialize the task subagent with a task service."""
        self.task_service = task_service
        self.time_skill = TimeSkill()
        self.storage_skill = StorageSkill()
        self.notification_skill = NotificationSkill()

        # Load tasks from storage on initialization
        self.load_tasks_from_storage()

        # Check for upcoming tasks and send notifications on startup
        self.check_upcoming_tasks_on_startup()

    def check_upcoming_tasks_on_startup(self):
        """Check for tasks due within the next hour and send notifications."""
        all_tasks = self.task_service.get_all_tasks()

        for task in all_tasks:
            if task.due_date and not task.completed:
                # Check if the task is due within the next hour using TimeSkill
                if self.time_skill.is_due_within_hours(task.due_date, 1):
                    self.notification_skill.send_alert(
                        title="Upcoming Task Reminder",
                        message=f"Task '{task.title}' is due within the next hour!"
                    )

    def load_tasks_from_storage(self):
        """Load tasks from storage on app startup."""
        data = self.storage_skill.load_data()
        if data:
            # Set the next_id based on the highest ID in the loaded data
            max_id = 0
            for task_data in data:
                task = Task(**task_data)
                self.task_service.tasks[task.id] = task
                if task.id > max_id:
                    max_id = task.id
            self.task_service.next_id = max_id + 1

    def save_tasks_to_storage(self):
        """Save all tasks to storage."""
        tasks_data = []
        for task in self.task_service.get_all_tasks():
            # Convert task to dictionary
            task_dict = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
                'created_at': task.created_at,
                'priority': task.priority,
                'tags': task.tags,
                'is_recurring': task.is_recurring,
                'frequency': task.frequency,
                'due_date': task.due_date
            }
            tasks_data.append(task_dict)

        self.storage_skill.save_data(tasks_data)

    def find_tasks(self, keyword: str, fields_to_search: List[str] = None) -> List[Task]:
        """
        Find tasks that match the keyword in specified fields.

        Args:
            keyword: String to search for
            fields_to_search: List of field names to search in (default: ['title', 'description', 'tags'])

        Returns:
            List of tasks that match the search criteria
        """
        if fields_to_search is None:
            fields_to_search = ['title', 'description', 'tags', 'due_date']

        # Convert tasks to dictionaries for searching
        tasks_as_dicts = []
        for task in self.task_service.get_all_tasks():
            task_dict = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'tags': task.tags,
                'completed': task.completed,
                'created_at': task.created_at,
                'due_date': task.due_date,
                'is_recurring': task.is_recurring,
                'frequency': task.frequency
            }
            tasks_as_dicts.append(task_dict)

        # Perform the search
        search_results = search_data(tasks_as_dicts, keyword, fields_to_search)

        # Convert back to Task objects
        found_tasks = []
        for result in search_results:
            task = Task(
                id=result['id'],
                title=result['title'],
                description=result['description'],
                priority=result['priority'],
                tags=result['tags'],
                completed=result['completed'],
                created_at=result['created_at'],
                due_date=result['due_date'],
                is_recurring=result['is_recurring'],
                frequency=result['frequency']
            )
            found_tasks.append(task)

        return found_tasks

    def get_ordered_tasks(self, sort_by: str, reverse: bool = False) -> List[Task]:
        """
        Get tasks ordered by specified field.

        Args:
            sort_by: Field to sort by ('priority' or 'date')
            reverse: Whether to sort in descending order (default: False)

        Returns:
            Sorted list of tasks
        """
        # Convert tasks to dictionaries for sorting
        tasks_as_dicts = []
        for task in self.task_service.get_all_tasks():
            task_dict = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'tags': task.tags,
                'completed': task.completed,
                'created_at': task.created_at,
                'due_date': task.due_date,
                'is_recurring': task.is_recurring,
                'frequency': task.frequency
            }
            tasks_as_dicts.append(task_dict)

        # Perform the sorting
        sorted_tasks = sort_data(tasks_as_dicts, sort_by, reverse)

        # Convert back to Task objects
        ordered_tasks = []
        for task_dict in sorted_tasks:
            task = Task(
                id=task_dict['id'],
                title=task_dict['title'],
                description=task_dict['description'],
                priority=task_dict['priority'],
                tags=task_dict['tags'],
                completed=task_dict['completed'],
                created_at=task_dict['created_at'],
                due_date=task_dict['due_date'],
                is_recurring=task_dict['is_recurring'],
                frequency=task_dict['frequency']
            )
            ordered_tasks.append(task)

        return ordered_tasks

    def validate_task_priority(self, priority: str) -> bool:
        """
        Validate that the priority input matches the allowed list.

        Args:
            priority: Priority value to validate

        Returns:
            bool: True if priority is valid, False otherwise
        """
        return validate_priority(priority)

    def get_upcoming_deadlines(self) -> List[Task]:
        """
        Get tasks with due dates within the next 24 hours.

        Returns:
            List of tasks with upcoming deadlines
        """
        upcoming_tasks = []
        for task in self.task_service.get_all_tasks():
            if task.due_date and not task.completed:
                if self.time_skill.is_reminder_due(task.due_date):
                    upcoming_tasks.append(task)
        return upcoming_tasks