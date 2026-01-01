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

    def create_task(self, title: str, description: str = "") -> Task:
        """Create a new task with the given title and description."""
        # Validate inputs
        temp_task = Task(id=0, title=title, description=description)
        temp_task.validate()

        task_id = self.next_id
        self.next_id += 1

        task = Task(
            id=task_id,
            title=title,
            description=description
        )

        self.tasks[task_id] = task
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID."""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self.tasks.values())

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """Update a task's title or description."""
        task = self.tasks.get(task_id)
        if not task:
            return False

        # Prepare updated values
        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description

        # Validate the updated task
        updated_task = Task(id=task.id, title=new_title, description=new_description, completed=task.completed)
        updated_task.validate()

        # Apply the updates
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def toggle_task_status(self, task_id: int) -> bool:
        """Toggle the completion status of a task."""
        task = self.tasks.get(task_id)
        if task:
            task.completed = not task.completed
            return True
        return False

    def task_exists(self, task_id: int) -> bool:
        """Check if a task exists by its ID."""
        return task_id in self.tasks