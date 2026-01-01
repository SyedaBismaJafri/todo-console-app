"""
Main entry point for the Todo Console App.
This file initializes the new subagents and starts the application.
"""
from subagents.task_subagent import TaskSubagent
from subagents.display_subagent import DisplaySubagent


def main():
    """
    Main function to run the Todo Console App.
    """
    print("Initializing Todo Console App...")

    # Initialize subagents
    task_subagent = TaskSubagent()
    display_subagent = DisplaySubagent()

    print("Todo Console App initialized successfully!")
    display_subagent.display_welcome()

    while True:
        choice = display_subagent.display_menu()

        if choice == "1":
            # View all tasks
            tasks = task_subagent.get_all_tasks()
            display_subagent.display_tasks(tasks)

        elif choice == "2":
            # Add a new task
            title, description, due_date, priority, tags = display_subagent.get_task_details()
            task = task_subagent.create_task(title, description, due_date, priority, tags)
            if task:
                display_subagent.show_message("Task added successfully!", "success")
            else:
                display_subagent.show_message("Failed to add task.", "error")

        elif choice == "3":
            # Update a task
            if not task_subagent.get_all_tasks():
                display_subagent.show_message("No tasks available to update.", "warning")
                continue

            display_subagent.display_tasks(task_subagent.get_all_tasks())
            task_id = display_subagent.get_task_id("update")

            if task_subagent.get_task(task_id) is not None:
                display_subagent.show_message("Enter new values (press Enter to keep current value):")
                title, description, due_date, priority, tags = display_subagent.get_task_details()

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

                success = task_subagent.update_task(task_id, **updates)
                if success:
                    display_subagent.show_message("Task updated successfully!", "success")
                else:
                    display_subagent.show_message("Failed to update task.", "error")
            else:
                display_subagent.show_message("Task not found.", "error")

        elif choice == "4":
            # Delete a task
            if not task_subagent.get_all_tasks():
                display_subagent.show_message("No tasks available to delete.", "warning")
                continue

            display_subagent.display_tasks(task_subagent.get_all_tasks())
            task_id = display_subagent.get_task_id("delete")

            if display_subagent.confirm_action("Are you sure you want to delete this task?"):
                success = task_subagent.delete_task(task_id)
                if success:
                    display_subagent.show_message("Task deleted successfully!", "success")
                else:
                    display_subagent.show_message("Failed to delete task.", "error")
            else:
                display_subagent.show_message("Deletion cancelled.", "warning")

        elif choice == "5":
            # Mark task as complete/incomplete
            if not task_subagent.get_all_tasks():
                display_subagent.show_message("No tasks available.", "warning")
                continue

            display_subagent.display_tasks(task_subagent.get_all_tasks())
            task_id = display_subagent.get_task_id("toggle completion status")

            task = task_subagent.get_task(task_id)
            if task:
                if task.get("completed", False):
                    success = task_subagent.mark_incomplete(task_id)
                    status = "incomplete"
                else:
                    success = task_subagent.mark_completed(task_id)
                    status = "complete"

                if success:
                    display_subagent.show_message(f"Task marked as {status}!", "success")
                else:
                    display_subagent.show_message(f"Failed to mark task as {status}.", "error")
            else:
                display_subagent.show_message("Task not found.", "error")

        elif choice == "6":
            # Search tasks
            criteria = display_subagent.get_search_criteria()
            tasks = task_subagent.search_tasks(**criteria)
            display_subagent.display_tasks(tasks)

        elif choice == "7":
            # Show help
            display_subagent.show_help()

        elif choice == "8":
            # Exit
            display_subagent.show_message("Thank you for using Todo Console App!", "info")
            break

        else:
            display_subagent.show_message("Invalid option. Please try again.", "error")


if __name__ == "__main__":
    main()