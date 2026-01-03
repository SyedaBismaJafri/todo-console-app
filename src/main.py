"""
Main entry point for the Todo Console App.
This file initializes the new subagents and starts the application.
"""
from services.task_service import TaskService
from services.task_subagent import TaskSubagent
from ui.display_subagent import DisplaySubagent
from ui.console_ui import ConsoleUI


def main():
    """
    Main function to run the Todo Console App.
    """
    print("Initializing Todo Console App...")

    # Initialize services and subagents
    task_service = TaskService()
    task_subagent = TaskSubagent(task_service)
    # Set the task_subagent reference in task_service for saving tasks
    task_service.set_task_subagent(task_subagent)
    display_subagent = DisplaySubagent()
    console_ui = ConsoleUI()

    print("Todo Console App initialized successfully!")
    print("Note: To run the background reminder service, run 'python -m services.background_reminder_service' in a separate terminal.")
    console_ui.display_welcome()

    while True:
        console_ui.display_menu()
        choice = console_ui.get_user_choice()

        if choice == "1":
            # Add a new task
            title, description, priority, tags, is_recurring, frequency, due_date = console_ui.get_task_details()
            task = task_service.create_task(title, description, priority, tags, is_recurring, frequency, due_date)
            if task:
                console_ui.show_message("Task added successfully!", "success")
            else:
                console_ui.show_message("Failed to add task.", "error")

        elif choice == "2":
            # View all tasks
            tasks = task_service.get_all_tasks()
            display_subagent.display_tasks(tasks)

        elif choice == "3":
            # Update a task
            if not task_service.get_all_tasks():
                console_ui.show_message("No tasks available to update.", "warning")
                continue

            display_subagent.display_tasks(task_service.get_all_tasks())
            task_id = console_ui.get_task_id("update")

            if task_service.get_task(task_id) is not None:
                current_task = task_service.get_task(task_id)
                title, description, priority, tags, is_recurring, frequency, due_date = console_ui.get_updated_task_details(
                    current_task.title,
                    current_task.description,
                    current_task.priority,
                    current_task.tags,
                    current_task.is_recurring,
                    current_task.frequency,
                    current_task.due_date
                )

                success = task_service.update_task(task_id, title, description, priority, tags, is_recurring, frequency, due_date)
                if success:
                    console_ui.show_message("Task updated successfully!", "success")
                else:
                    console_ui.show_message("Failed to update task.", "error")
            else:
                console_ui.show_message("Task not found.", "error")

        elif choice == "4":
            # Delete a task
            if not task_service.get_all_tasks():
                console_ui.show_message("No tasks available to delete.", "warning")
                continue

            display_subagent.display_tasks(task_service.get_all_tasks())
            task_id = console_ui.get_task_id("delete")

            success = task_service.delete_task(task_id)
            if success:
                console_ui.show_message("Task deleted successfully!", "success")
            else:
                console_ui.show_message("Failed to delete task.", "error")

        elif choice == "5":
            # Toggle task status
            if not task_service.get_all_tasks():
                console_ui.show_message("No tasks available.", "warning")
                continue

            display_subagent.display_tasks(task_service.get_all_tasks())
            task_id = console_ui.get_task_id("toggle completion status")

            success = task_service.toggle_task_status(task_id)
            if success:
                console_ui.show_message("Task status toggled successfully!", "success")
            else:
                console_ui.show_message("Failed to toggle task status.", "error")

        elif choice == "6":
            # Show help
            console_ui.show_help()

        elif choice == "7":
            # Search/Filter menu
            while True:
                display_subagent.display_search_filter_menu()
                search_choice = display_subagent.get_search_filter_choice()

                if search_choice == "1":
                    # Search tasks
                    keyword = display_subagent.get_search_keyword()
                    found_tasks = task_subagent.find_tasks(keyword)
                    display_subagent.display_tasks(found_tasks)

                elif search_choice == "2":
                    # Sort by priority
                    reverse = display_subagent.get_sort_order()
                    sorted_tasks = task_subagent.get_ordered_tasks('priority', reverse)
                    display_subagent.display_tasks(sorted_tasks)

                elif search_choice == "3":
                    # Sort by date
                    reverse = display_subagent.get_sort_order()
                    sorted_tasks = task_subagent.get_ordered_tasks('date', reverse)
                    display_subagent.display_tasks(sorted_tasks)

                elif search_choice == "4":
                    # Back to main menu
                    break

                else:
                    console_ui.show_message("Invalid option. Please try again.", "error")

        elif choice == "8":
            # Upcoming Deadlines
            upcoming_tasks = task_subagent.get_upcoming_deadlines()
            display_subagent.display_upcoming_deadlines(upcoming_tasks)

        elif choice == "9":
            # Exit
            if console_ui.confirm_exit():
                console_ui.show_message("Thank you for using Todo Console App!", "success")
                break

        else:
            console_ui.show_message("Invalid option. Please try again.", "error")


if __name__ == "__main__":
    main()