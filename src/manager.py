"""
Application Manager
Central orchestrator for the todo console application components.
"""

from typing import Optional
from services.task_service import TaskService
from ui.console_ui import ConsoleUI
from cli.commands import CLICommands


class ApplicationManager:
    """Manages the overall application lifecycle and component orchestration."""
    
    def __init__(self):
        self.task_service = TaskService()
        self.ui = ConsoleUI()
        self.cli_commands = CLICommands(self.task_service, self.ui)
        self.is_running = False
    
    def start(self):
        """Start the application."""
        self.is_running = True
        self.ui.display_welcome()
        
        while self.is_running:
            try:
                self.ui.display_menu()
                choice = self.ui.get_user_choice()
                
                if choice == "1":
                    self.cli_commands.add_task()
                elif choice == "2":
                    self.cli_commands.view_tasks()
                elif choice == "3":
                    self.cli_commands.update_task()
                elif choice == "4":
                    self.cli_commands.delete_task()
                elif choice == "5":
                    self.cli_commands.toggle_task_status()
                elif choice == "6":
                    self.cli_commands.show_help()
                elif choice == "7":
                    if self.ui.confirm_exit():
                        self.ui.show_message("Goodbye!", "success")
                        self.is_running = False
                else:
                    self.ui.show_message("Invalid choice. Please select a number between 1-7.", "error")
                    
            except KeyboardInterrupt:
                self.ui.show_message("\nGoodbye!", "success")
                self.is_running = False
            except Exception as e:
                self.ui.show_message(f"An error occurred: {e}", "error")
    
    def stop(self):
        """Stop the application."""
        self.is_running = False
    
    def get_status(self):
        """Get the current application status."""
        return {
            "is_running": self.is_running,
            "task_count": len(self.task_service.get_all_tasks()),
            "next_task_id": self.task_service.next_id
        }


def main():
    """Main entry point for the application via the manager."""
    app_manager = ApplicationManager()
    app_manager.start()


if __name__ == "__main__":
    main()