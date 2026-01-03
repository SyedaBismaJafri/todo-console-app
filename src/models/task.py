"""
Task Model
Defines the Task data structure for the todo application.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Task:
    """Represents a single todo task."""
    id: int
    title: str
    description: str
    completed: bool = False
    created_at: Optional[str] = None
    priority: str = "medium"  # Default priority
    tags: List[str] = None   # List of tags
    is_recurring: bool = False  # Whether the task repeats
    frequency: str = ""  # How often the task repeats (daily, weekly, monthly)
    due_date: Optional[str] = None  # When the task is due

    def __post_init__(self):
        """Set the creation timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

        if self.tags is None:
            self.tags = []

    @property
    def status_text(self) -> str:
        """Return a text representation of the task's completion status."""
        return "COMPLETED" if self.completed else "PENDING"

    @property
    def status_symbol(self) -> str:
        """Return a symbol representation of the task's completion status."""
        return "✓" if self.completed else "○"

    def validate(self) -> None:
        """Validate the task attributes."""
        if not self.title.strip():
            raise ValueError("Task title cannot be empty")

        if len(self.title.strip()) > 100:
            raise ValueError("Task title cannot exceed 100 characters")

        if len(self.description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")

        # Validate priority
        allowed_priorities = ['high', 'medium', 'low']
        if self.priority.lower() not in allowed_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(allowed_priorities)}")

        # Validate tags
        allowed_tags = ['work', 'home']
        invalid_tags = [tag for tag in self.tags if tag.lower() not in allowed_tags]
        if invalid_tags:
            raise ValueError(f"Tags must be one of: {', '.join(allowed_tags)}. Invalid tags: {', '.join(invalid_tags)}")

        # Validate frequency if task is recurring
        if self.is_recurring:
            allowed_frequencies = ['daily', 'weekly', 'monthly']
            if self.frequency.lower() not in allowed_frequencies:
                raise ValueError(f"Frequency must be one of: {', '.join(allowed_frequencies)}")