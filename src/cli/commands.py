"""
CLI Commands
Handles the command-line interface commands for the todo application.
"""

from typing import Optional
from subagents.task_subagent import TaskSubagent
from subagents.display_subagent import DisplaySubagent


class CLICommands:
    """Class for handling CLI commands."""

    def __init__(self, task_subagent: TaskSubagent, display_subagent: DisplaySubagent) -> None:
        """Initialize the CLI commands handler."""
        self.task_subagent = task_subagent
        self.display_subagent = display_subagent

    def add_task(self) -> None:
        """Handle adding a new task."""
        try:
            title, description, due_date, priority, tags = self.display_subagent.get_task_details()
            task = self.task_subagent.create_task(title, description, due_date, priority, tags)
            if task:
                self.display_subagent.show_message("Task added successfully!", "success")
            else:
                self.display_subagent.show_message("Failed to add task.", "error")
        except ValueError as e:
            self.display_subagent.show_message(f"Error: {e}", "error")
        except KeyboardInterrupt:
            self.display_subagent.show_message("Task addition cancelled.", "warning")

    def view_tasks(self) -> None:
        """Handle viewing all tasks."""
        tasks = self.task_subagent.get_all_tasks()
        self.display_subagent.display_tasks(tasks)

    def update_task(self) -> None:
        """Handle updating a task."""
        try:
            if not self.task_subagent.get_all_tasks():
                self.display_subagent.show_message("No tasks available to update.", "warning")
                return

            self.display_subagent.display_tasks(self.task_subagent.get_all_tasks())
            task_id = self.display_subagent.get_task_id("update")

            if self.task_subagent.get_task(task_id) is not None:
                self.display_subagent.show_message("Enter new values (press Enter to keep current value):")
                title, description, due_date, priority, tags = self.display_subagent.get_task_details()

                updates = {}
                if title:
                    updates["title"] = title
                if description:
                    updates["description"] = description
                if due_date:
                    updates["due_date"] = due_date
                if priority:
                    updates["priority"] = priority
                if tags:
                    updates["tags"] = tags

                success = self.task_subagent.update_task(task_id, **updates)
                if success:
                    self.display_subagent.show_message("Task updated successfully!", "success")
                else:
                    self.display_subagent.show_message("Failed to update task.", "error")
            else:
                self.display_subagent.show_message("Task not found.", "error")
        except ValueError as e:
            self.display_subagent.show_message(f"Error: {e}", "error")
        except KeyboardInterrupt:
            self.display_subagent.show_message("Task update cancelled.", "warning")

    def delete_task(self) -> None:
        """Handle deleting a task."""
        try:
            if not self.task_subagent.get_all_tasks():
                self.display_subagent.show_message("No tasks available to delete.", "warning")
                return

            self.display_subagent.display_tasks(self.task_subagent.get_all_tasks())
            task_id = self.display_subagent.get_task_id("delete")

            if self.display_subagent.confirm_action("Are you sure you want to delete this task?"):
                success = self.task_subagent.delete_task(task_id)
                if success:
                    self.display_subagent.show_message("Task deleted successfully!", "success")
                else:
                    self.display_subagent.show_message("Failed to delete task.", "error")
            else:
                self.display_subagent.show_message("Deletion cancelled.", "warning")
        except ValueError as e:
            self.display_subagent.show_message(f"Error: {e}", "error")
        except KeyboardInterrupt:
            self.display_subagent.show_message("Task deletion cancelled.", "warning")

    def toggle_task_status(self) -> None:
        """Handle toggling task completion status."""
        try:
            if not self.task_subagent.get_all_tasks():
                self.display_subagent.show_message("No tasks available.", "warning")
                return

            self.display_subagent.display_tasks(self.task_subagent.get_all_tasks())
            task_id = self.display_subagent.get_task_id("toggle completion status")

            task = self.task_subagent.get_task(task_id)
            if task:
                if task.get("completed", False):
                    success = self.task_subagent.mark_incomplete(task_id)
                    status = "incomplete"
                else:
                    success = self.task_subagent.mark_completed(task_id)
                    status = "complete"

                if success:
                    self.display_subagent.show_message(f"Task marked as {status}!", "success")
                else:
                    self.display_subagent.show_message(f"Failed to mark task as {status}.", "error")
            else:
                self.display_subagent.show_message("Task not found.", "error")
        except ValueError as e:
            self.display_subagent.show_message(f"Error: {e}", "error")
        except KeyboardInterrupt:
            self.display_subagent.show_message("Task toggle cancelled.", "warning")

    def search_tasks(self) -> None:
        """Handle searching tasks."""
        try:
            criteria = self.display_subagent.get_search_criteria()
            tasks = self.task_subagent.search_tasks(**criteria)
            self.display_subagent.display_tasks(tasks)
        except ValueError as e:
            self.display_subagent.show_message(f"Error: {e}", "error")
        except KeyboardInterrupt:
            self.display_subagent.show_message("Task search cancelled.", "warning")

    def show_help(self) -> None:
        """Display help information."""
        self.display_subagent.show_help()