"""
CLI Commands
Handles the command-line interface commands for the todo application.
"""

from typing import Optional
from services.task_service import TaskService
from ui.console_ui import ConsoleUI


class CLICommands:
    """Class for handling CLI commands."""

    def __init__(self, task_service: TaskService, ui: ConsoleUI) -> None:
        """Initialize the CLI commands handler."""
        self.task_service = task_service
        self.ui = ui

    def add_task(self) -> None:
        """Handle adding a new task."""
        try:
            title, description = self.ui.get_task_details()
            task = self.task_service.create_task(title, description)
            self.ui.show_message(f"Task added successfully with ID: {task.id}", "success")
        except ValueError as e:
            self.ui.show_message(f"Error: {e}", "error")
        except KeyboardInterrupt:
            self.ui.show_message("Task addition cancelled.", "warning")

    def view_tasks(self) -> None:
        """Handle viewing all tasks."""
        tasks = self.task_service.get_all_tasks()
        self.ui.display_tasks(tasks)

    def update_task(self) -> None:
        """Handle updating a task."""
        try:
            task_id = self.ui.get_task_id("update")

            task = self.task_service.get_task(task_id)
            if not task:
                self.ui.show_message(f"No task found with ID {task_id}.", "error")
                return

            # Show current values
            self.ui.console.print(f"[bold]Current title: {task.title}[/]")
            self.ui.console.print(f"[bold]Current description: {task.description}[/]")

            new_title, new_description = self.ui.get_updated_task_details(task.title, task.description)

            # Only update if there are changes
            title_to_update = new_title if new_title != task.title else None
            description_to_update = new_description if new_description != task.description else None

            if title_to_update is None and description_to_update is None:
                self.ui.show_message("No changes made.", "warning")
                return

            success = self.task_service.update_task(task_id, title_to_update, description_to_update)
            if success:
                self.ui.show_message("Task updated successfully.", "success")
            else:
                self.ui.show_message("Failed to update task.", "error")

        except ValueError as e:
            self.ui.show_message(f"Error: {e}", "error")
        except KeyboardInterrupt:
            self.ui.show_message("Task update cancelled.", "warning")

    def delete_task(self) -> None:
        """Handle deleting a task."""
        try:
            task_id = self.ui.get_task_id("delete")

            if not self.task_service.task_exists(task_id):
                self.ui.show_message(f"No task found with ID {task_id}.", "error")
                return

            success = self.task_service.delete_task(task_id)
            if success:
                self.ui.show_message(f"Task with ID {task_id} deleted successfully.", "success")
            else:
                self.ui.show_message(f"No task found with ID {task_id}.", "error")

        except ValueError as e:
            self.ui.show_message(f"Error: {e}", "error")
        except KeyboardInterrupt:
            self.ui.show_message("Task deletion cancelled.", "warning")

    def toggle_task_status(self) -> None:
        """Handle toggling task completion status."""
        try:
            task_id = self.ui.get_task_id("toggle")

            if not self.task_service.task_exists(task_id):
                self.ui.show_message(f"No task found with ID {task_id}.", "error")
                return

            success = self.task_service.toggle_task_status(task_id)
            if success:
                task = self.task_service.get_task(task_id)
                status = "completed" if task.completed else "incomplete"
                self.ui.show_message(f"Task with ID {task_id} marked as {status}.", "success")
            else:
                self.ui.show_message(f"No task found with ID {task_id}.", "error")

        except ValueError as e:
            self.ui.show_message(f"Error: {e}", "error")
        except KeyboardInterrupt:
            self.ui.show_message("Task toggle cancelled.", "warning")

    def show_help(self) -> None:
        """Display help information."""
        self.ui.show_help()