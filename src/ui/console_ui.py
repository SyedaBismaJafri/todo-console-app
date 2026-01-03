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
        self.console.print("7. Search/Filter Tasks")
        self.console.print("8. Upcoming Deadlines")
        self.console.print("9. Exit")
    
    def display_tasks(self, tasks: List[Task]):
        """Display all tasks in a formatted way using Rich."""
        if not tasks:
            self.console.print("\n[bold yellow]No tasks found. Add some tasks to get started![/]\n")
            return

        table = Table(title="Your Todo List", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=5)
        table.add_column("Status", width=10)
        table.add_column("Title", width=25)
        table.add_column("Description", width=30)
        table.add_column("Priority", width=10)
        table.add_column("Tags", width=15)
        table.add_column("Due Date", width=12)

        for task in sorted(tasks, key=lambda t: t.id):
            status = f"{task.status_symbol} [{'green' if task.completed else 'red'}]{task.status_text}[/{'green' if task.completed else 'red'}]"
            title = task.title
            description = task.description
            priority = self._format_priority(task.priority)
            tags = ", ".join(task.tags) if task.tags else "None"
            due_date = task.due_date if task.due_date else "None"

            # Check if task is overdue or due today
            if task.due_date and not task.completed:
                try:
                    from datetime import datetime
                    due_date_obj = datetime.strptime(task.due_date, '%Y-%m-%d')
                    today = datetime.now().date()
                    if due_date_obj.date() < today:
                        # Overdue task - highlight in bold yellow
                        title = f"[bold yellow]{title}[/bold yellow]"
                        due_date = f"[bold yellow]{due_date}[/bold yellow]"
                    elif due_date_obj.date() == today:
                        # Due today - highlight in bold yellow
                        title = f"[bold yellow]{title}[/bold yellow]"
                        due_date = f"[bold yellow]{due_date}[/bold yellow]"
                except ValueError:
                    # Invalid date format
                    pass

            # Truncate description if too long
            if len(description) > 30:
                description = description[:27] + "..."

            # Truncate tags if too long
            if len(tags) > 15:
                tags = tags[:12] + "..."

            table.add_row(
                str(task.id),
                status,
                title,
                description,
                priority,
                tags,
                due_date
            )

        self.console.print(table)

    def _format_priority(self, priority: str) -> str:
        """Format priority with color coding."""
        priority_lower = priority.lower()
        if priority_lower == 'high':
            return f"[bold red]{priority}[/bold red]"
        elif priority_lower == 'medium':
            return f"[bold yellow]{priority}[/bold yellow]"
        elif priority_lower == 'low':
            return f"[bold green]{priority}[/bold green]"
        else:
            return priority
    
    def get_user_choice(self) -> str:
        """Get the user's menu choice."""
        return Prompt.ask("\n[bold cyan]Enter your choice (1-9)[/]", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    
    def get_task_details(self) -> tuple[str, str, str, List[str], bool, str, str]:
        """Get task details from user input."""
        title = Prompt.ask("[bold cyan]Enter task title[/] (max 100 chars)")
        description = Prompt.ask("[bold cyan]Enter task description[/] (max 500 chars, optional)", default="")
        priority = Prompt.ask("[bold cyan]Enter priority[/] (high/medium/low, default: medium)", default="medium")
        tags_input = Prompt.ask("[bold cyan]Enter tags[/] (comma-separated, e.g., work,home, optional)", default="")

        # Process tags
        tags = []
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',')]

        # Get recurring task details
        is_recurring_input = Prompt.ask("[bold cyan]Is this a recurring task?[/] (y/n, default: n)", default="n")
        is_recurring = is_recurring_input.lower() in ['y', 'yes']

        frequency = ""
        if is_recurring:
            frequency = Prompt.ask("[bold cyan]Enter frequency[/] (daily/weekly/monthly)", choices=["daily", "weekly", "monthly"])

        due_date = Prompt.ask("[bold cyan]Enter due date[/] (YYYY-MM-DD, optional)", default="")
        if due_date == "":
            due_date = None

        return title, description, priority, tags, is_recurring, frequency, due_date
    
    def get_task_id(self, action: str = "operate on") -> int:
        """Get a task ID from user input."""
        task_id_input = Prompt.ask(f"[bold cyan]Enter task ID to {action}[/]")
        return int(task_id_input)
    
    def get_updated_task_details(self, current_title: str, current_description: str, current_priority: str = "medium",
                                current_tags: List[str] = None, current_is_recurring: bool = False,
                                current_frequency: str = "", current_due_date: str = None) -> tuple[str, str, str, List[str], bool, str, str]:
        """Get updated task details from user, with current values as defaults."""
        if current_tags is None:
            current_tags = []

        new_title = Prompt.ask("[bold cyan]Enter new title[/] (or press Enter to keep current)", default="---KEEP_CURRENT---")
        new_description = Prompt.ask("[bold cyan]Enter new description[/] (or press Enter to keep current)", default="---KEEP_CURRENT---")
        new_priority = Prompt.ask(f"[bold cyan]Enter new priority[/] (high/medium/low, default: {current_priority})", default="---KEEP_CURRENT---")

        tags_input = Prompt.ask(f"[bold cyan]Enter new tags[/] (comma-separated, e.g., work,home, default: {', '.join(current_tags) if current_tags else 'None'})", default="---KEEP_CURRENT---")

        # Get recurring task details
        recurring_input = Prompt.ask(f"[bold cyan]Is this a recurring task?[/] (y/n, default: {'y' if current_is_recurring else 'n'})", default="---KEEP_CURRENT---")
        new_is_recurring = current_is_recurring
        if recurring_input != "---KEEP_CURRENT---":
            new_is_recurring = recurring_input.lower() in ['y', 'yes']

        new_frequency = current_frequency
        if new_is_recurring and recurring_input != "---KEEP_CURRENT---":
            new_frequency = Prompt.ask(f"[bold cyan]Enter frequency[/] (daily/weekly/monthly, default: {current_frequency})",
                                      default="---KEEP_CURRENT---")
            if new_frequency == "---KEEP_CURRENT---":
                new_frequency = current_frequency

        due_date_input = Prompt.ask(f"[bold cyan]Enter due date[/] (YYYY-MM-DD, default: {current_due_date or 'None'})", default="---KEEP_CURRENT---")
        new_due_date = current_due_date
        if due_date_input != "---KEEP_CURRENT---":
            new_due_date = due_date_input if due_date_input else None

        # Return the new values or the current ones if user chose to keep them
        title = new_title if new_title != "---KEEP_CURRENT---" else current_title
        description = new_description if new_description != "---KEEP_CURRENT---" else current_description
        priority = new_priority if new_priority != "---KEEP_CURRENT---" else current_priority

        # Process tags
        if tags_input != "---KEEP_CURRENT---":
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(',')]
            else:
                tags = []
        else:
            tags = current_tags

        return title, description, priority, tags, new_is_recurring, new_frequency, new_due_date
    
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
  1. Add Task         - Add a new task with title, description, priority, tags, and optional due date
  2. View Tasks       - View all tasks with status, priority, tags, and due dates
  3. Update Task      - Update a task's title, description, priority, tags, or due date by ID
  4. Delete Task      - Delete a task by its ID
  5. Toggle Status    - Toggle task completion status by ID
  6. Help             - Show this help message
  7. Search/Filter    - Search tasks or sort by priority/date
  8. Upcoming Deadlines - View tasks with due dates within the next 24 hours
  9. Exit             - Exit the application

[i]All tasks are stored in memory during this session.[/]
        """
        self.console.print(Panel(help_text, title="Help", border_style="blue"))
    
    def confirm_exit(self) -> bool:
        """Ask user to confirm exit."""
        return Confirm.ask("Are you sure you want to exit?")