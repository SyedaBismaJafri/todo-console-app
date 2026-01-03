"""
Task Service
Handles the business logic for task management in the todo application.
"""

from typing import Dict, List, Optional
from models.task import Task


class TaskService:
    """Service class for managing tasks."""

    def __init__(self) -> None:
        """Initialize the task service with an empty task dictionary and starting ID."""
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1
        self.task_subagent = None  # Will be set after initialization

    def set_task_subagent(self, task_subagent):
        """Set the task_subagent reference for saving tasks and notifications."""
        self.task_subagent = task_subagent

    def create_task(self, title: str, description: str = "", priority: str = "medium", tags: List[str] = None,
                    is_recurring: bool = False, frequency: str = "", due_date: str = None) -> Task:
        """Create a new task with the given title, description, priority, tags, and optional recurring settings."""
        if tags is None:
            tags = []

        # Validate inputs
        temp_task = Task(
            id=0,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            is_recurring=is_recurring,
            frequency=frequency,
            due_date=due_date
        )
        temp_task.validate()

        task_id = self.next_id
        self.next_id += 1

        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            is_recurring=is_recurring,
            frequency=frequency,
            due_date=due_date
        )

        self.tasks[task_id] = task

        # Save tasks to storage if task_subagent is available
        if self.task_subagent:
            self.task_subagent.save_tasks_to_storage()

            # Check if the new task is due within the next hour and send notification
            if due_date:
                from services.time_engine import TimeSkill
                time_skill = TimeSkill()
                if time_skill.is_due_within_hours(due_date, 1):
                    self.task_subagent.notification_skill.send_alert(
                        title="New Task Reminder",
                        message=f"New task '{title}' is due within the next hour!"
                    )

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID."""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self.tasks.values())

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
                    priority: Optional[str] = None, tags: Optional[List[str]] = None,
                    is_recurring: Optional[bool] = None, frequency: Optional[str] = None,
                    due_date: Optional[str] = None) -> bool:
        """Update a task's title, description, priority, tags, or recurring settings."""
        task = self.tasks.get(task_id)
        if not task:
            return False

        # Prepare updated values
        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description
        new_priority = priority if priority is not None else task.priority
        new_tags = tags if tags is not None else task.tags
        new_is_recurring = is_recurring if is_recurring is not None else task.is_recurring
        new_frequency = frequency if frequency is not None else task.frequency
        new_due_date = due_date if due_date is not None else task.due_date

        # Validate the updated task
        updated_task = Task(
            id=task.id,
            title=new_title,
            description=new_description,
            completed=task.completed,
            priority=new_priority,
            tags=new_tags,
            is_recurring=new_is_recurring,
            frequency=new_frequency,
            due_date=new_due_date
        )
        updated_task.validate()

        # Apply the updates
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if is_recurring is not None:
            task.is_recurring = is_recurring
        if frequency is not None:
            task.frequency = frequency
        if due_date is not None:
            task.due_date = due_date

        # Save tasks to storage if task_subagent is available
        if self.task_subagent:
            self.task_subagent.save_tasks_to_storage()

            # Check if the updated task is due within the next hour and send notification
            if new_due_date:
                from services.time_engine import TimeSkill
                time_skill = TimeSkill()
                if time_skill.is_due_within_hours(new_due_date, 1):
                    self.task_subagent.notification_skill.send_alert(
                        title="Updated Task Reminder",
                        message=f"Task '{task.title}' is due within the next hour!"
                    )

        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        if task_id in self.tasks:
            del self.tasks[task_id]

            # Save tasks to storage if task_subagent is available
            if self.task_subagent:
                self.task_subagent.save_tasks_to_storage()

            return True
        return False

    def toggle_task_status(self, task_id: int) -> bool:
        """Toggle the completion status of a task. If a recurring task is marked complete, create a new instance."""
        task = self.tasks.get(task_id)
        if task:
            # If the task is recurring and we're marking it as complete
            if task.is_recurring and not task.completed:
                # Mark the current task as complete
                task.completed = True

                # Create a new instance of the task with the next occurrence date
                from services.time_engine import TimeSkill
                next_date = TimeSkill.calculate_next_date(task.due_date or task.created_at.split('T')[0], task.frequency)

                if next_date:
                    new_task = Task(
                        id=self.next_id,
                        title=task.title,
                        description=task.description,
                        priority=task.priority,
                        tags=task.tags,
                        is_recurring=task.is_recurring,
                        frequency=task.frequency,
                        due_date=next_date
                    )
                    new_task.validate()

                    self.tasks[self.next_id] = new_task
                    self.next_id += 1

                # Save tasks to storage if task_subagent is available
                if self.task_subagent:
                    self.task_subagent.save_tasks_to_storage()

                    # Check if the new recurring task is due within the next hour and send notification
                    if next_date:
                        from services.time_engine import TimeSkill
                        time_skill = TimeSkill()
                        if time_skill.is_due_within_hours(next_date, 1):
                            self.task_subagent.notification_skill.send_alert(
                                title="Recurring Task Reminder",
                                message=f"Recurring task '{task.title}' is due within the next hour!"
                            )

                return True
            else:
                # For non-recurring tasks or marking incomplete
                task.completed = not task.completed

                # Save tasks to storage if task_subagent is available
                if self.task_subagent:
                    self.task_subagent.save_tasks_to_storage()

                return True
        return False

    def task_exists(self, task_id: int) -> bool:
        """Check if a task exists by its ID."""
        return task_id in self.tasks