"""
Console UI
Handles the Rich-based console user interface for the todo application.
"""

from typing import List
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print
from models.task import Task


class ConsoleUI:
    """Class for handling console user interface using Rich."""
    
    def __init__(self):
        self.console = Console()
    
    def display_welcome(self):
        """Display the welcome message."""
        self.console.print(Panel("Welcome to the Todo Console Application!", title="Welcome", border_style="green"))
        self.console.print("Type 'help' or select option 6 to see available commands.\n")
    
    def display_menu(self):
        """Display the main menu."""
        self.console.print("\n[bold blue]Todo Console Application[/]")
        self.console.print("Choose an option:")
        self.console.print("1. Add Task")
        self.console.print("2. View Tasks")
        self.console.print("3. Update Task")
        self.console.print("4. Delete Task")
        self.console.print("5. Toggle Task Status")
        self.console.print("6. Help")
        self.console.print("7. Exit")
    
    def display_tasks(self, tasks: List[Task]):
        """Display all tasks in a formatted way using Rich."""
        if not tasks:
            self.console.print("\n[bold yellow]No tasks found. Add some tasks to get started![/]\n")
            return
        
        table = Table(title="Your Todo List", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=5)
        table.add_column("Status", width=10)
        table.add_column("Title", width=30)
        table.add_column("Description", width=50)
        
        for task in sorted(tasks, key=lambda t: t.id):
            status = f"{task.status_symbol} [{'green' if task.completed else 'red'}]{task.status_text}[/{'green' if task.completed else 'red'}]"
            title = task.title
            description = task.description
            
            # Truncate description if too long
            if len(description) > 50:
                description = description[:47] + "..."
            
            table.add_row(
                str(task.id),
                status,
                title,
                description
            )
        
        self.console.print(table)
    
    def get_user_choice(self) -> str:
        """Get the user's menu choice."""
        return Prompt.ask("\n[bold cyan]Enter your choice (1-7)[/]", choices=["1", "2", "3", "4", "5", "6", "7"])
    
    def get_task_details(self) -> tuple[str, str]:
        """Get task details from user input."""
        title = Prompt.ask("[bold cyan]Enter task title[/] (max 100 chars)")
        description = Prompt.ask("[bold cyan]Enter task description[/] (max 500 chars, optional)", default="")
        return title, description
    
    def get_task_id(self, action: str = "operate on") -> int:
        """Get a task ID from user input."""
        task_id_input = Prompt.ask(f"[bold cyan]Enter task ID to {action}[/]")
        return int(task_id_input)
    
    def get_updated_task_details(self, current_title: str, current_description: str) -> tuple[str, str]:
        """Get updated task details from user, with current values as defaults."""
        new_title = Prompt.ask("[bold cyan]Enter new title[/] (or press Enter to keep current)", default="---KEEP_CURRENT---")
        new_description = Prompt.ask("[bold cyan]Enter new description[/] (or press Enter to keep current)", default="---KEEP_CURRENT---")
        
        # Return the new values or the current ones if user chose to keep them
        title = new_title if new_title != "---KEEP_CURRENT---" else current_title
        description = new_description if new_description != "---KEEP_CURRENT---" else current_description
        
        return title, description
    
    def show_message(self, message: str, style: str = "default"):
        """Display a message with the specified style."""
        if style == "success":
            self.console.print(f"[bold green]✓ {message}[/]")
        elif style == "error":
            self.console.print(f"[bold red]✗ {message}[/]")
        elif style == "warning":
            self.console.print(f"[bold yellow]⚠ {message}[/]")
        else:
            self.console.print(message)
    
    def show_help(self):
        """Display help information."""
        help_text = """
[b]Available Commands:[/]
  1. Add Task      - Add a new task with title and description
  2. View Tasks    - View all tasks with their status indicators
  3. Update Task   - Update a task's title or description by ID
  4. Delete Task   - Delete a task by its ID
  5. Toggle Status - Toggle task completion status by ID
  6. Help          - Show this help message
  7. Exit          - Exit the application

[i]All tasks are stored in memory during this session.[/]
        """
        self.console.print(Panel(help_text, title="Help", border_style="blue"))
    
    def confirm_exit(self) -> bool:
        """Ask user to confirm exit."""
        return Confirm.ask("Are you sure you want to exit?")