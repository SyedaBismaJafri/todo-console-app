"""
Application Manager
Central orchestrator for the todo console application components.
"""

from typing import Optional
from subagents.task_subagent import TaskSubagent
from subagents.display_subagent import DisplaySubagent


class ApplicationManager:
    """Manages the overall application lifecycle and component orchestration."""

    def __init__(self):
        self.task_subagent = TaskSubagent()
        self.display_subagent = DisplaySubagent()
        self.is_running = False

    def start(self):
        """Start the application."""
        self.is_running = True
        self.display_subagent.display_welcome()

        while self.is_running:
            try:
                choice = self.display_subagent.display_menu()

                if choice == "1":
                    self.view_tasks()
                elif choice == "2":
                    self.add_task()
                elif choice == "3":
                    self.update_task()
                elif choice == "4":
                    self.delete_task()
                elif choice == "5":
                    self.toggle_task_status()
                elif choice == "6":
                    self.search_tasks()
                elif choice == "7":
                    self.show_help()
                elif choice == "8":
                    if self.display_subagent.confirm_action("Are you sure you want to exit?"):
                        self.display_subagent.show_message("Goodbye!", "info")
                        self.is_running = False
                else:
                    self.display_subagent.show_message("Invalid choice. Please select a number between 1-8.", "error")

            except KeyboardInterrupt:
                self.display_subagent.show_message("\nGoodbye!", "info")
                self.is_running = False
            except Exception as e:
                self.display_subagent.show_message(f"An error occurred: {e}", "error")

    def add_task(self):
        """Add a new task."""
        try:
            title, description, due_date, priority, tags = self.display_subagent.get_task_details()
            task = self.task_subagent.create_task(title, description, due_date, priority, tags)
            if task:
                self.display_subagent.show_message("Task added successfully!", "success")
            else:
                self.display_subagent.show_message("Failed to add task.", "error")
        except KeyboardInterrupt:
            self.display_subagent.show_message("Task addition cancelled.", "warning")

    def view_tasks(self):
        """View all tasks."""
        tasks = self.task_subagent.get_all_tasks()
        self.display_subagent.display_tasks(tasks)

    def update_task(self):
        """Update a task."""
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

    def delete_task(self):
        """Delete a task."""
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

    def toggle_task_status(self):
        """Toggle task completion status."""
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

    def search_tasks(self):
        """Search tasks."""
        try:
            criteria = self.display_subagent.get_search_criteria()
            tasks = self.task_subagent.search_tasks(**criteria)
            self.display_subagent.display_tasks(tasks)
        except ValueError as e:
            self.display_subagent.show_message(f"Error: {e}", "error")
        except KeyboardInterrupt:
            self.display_subagent.show_message("Task search cancelled.", "warning")

    def show_help(self):
        """Display help information."""
        self.display_subagent.show_help()

    def stop(self):
        """Stop the application."""
        self.is_running = False

    def get_status(self):
        """Get the current application status."""
        return {
            "is_running": self.is_running,
            "task_count": len(self.task_subagent.get_all_tasks()),
        }


def main():
    """Main entry point for the application via the manager."""
    app_manager = ApplicationManager()
    app_manager.start()


if __name__ == "__main__":
    main()