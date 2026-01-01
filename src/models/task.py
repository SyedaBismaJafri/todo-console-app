"""
Task Model
Defines the Task data structure for the todo application.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a single todo task."""
    id: int
    title: str
    description: str
    completed: bool = False
    created_at: Optional[str] = None

    def __post_init__(self):
        """Set the creation timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

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