"""
Display Subagent
Handles the Rich-based console user interface for the todo application with priority and tags support.
"""

from datetime import datetime
from typing import List
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print
from models.task import Task


class DisplaySubagent:
    """Subagent for handling display operations using Rich."""

    def __init__(self):
        self.console = Console()

    def display_tasks(self, tasks: List[Task]):
        """Display all tasks in a formatted way using Rich with priority and tags columns."""
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

    def display_upcoming_deadlines(self, tasks: List[Task]):
        """Display tasks with upcoming deadlines."""
        if not tasks:
            self.console.print("\n[bold yellow]No upcoming deadlines.[/]\n")
            return

        table = Table(title="Upcoming Deadlines (Next 24 Hours)", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=5)
        table.add_column("Title", width=30)
        table.add_column("Description", width=35)
        table.add_column("Due Date", width=12)

        for task in sorted(tasks, key=lambda t: t.id):
            title = task.title
            description = task.description
            due_date = task.due_date if task.due_date else "None"

            # Truncate description if too long
            if len(description) > 35:
                description = description[:32] + "..."

            table.add_row(
                str(task.id),
                title,
                description,
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

    def display_search_filter_menu(self):
        """Display the Search/Filter menu."""
        self.console.print("\n[bold blue]Search/Filter Options[/]")
        self.console.print("1. Search Tasks")
        self.console.print("2. Sort by Priority")
        self.console.print("3. Sort by Date")
        self.console.print("4. Back to Main Menu")

    def get_search_filter_choice(self) -> str:
        """Get the user's search/filter choice."""
        return Prompt.ask("\n[bold cyan]Enter your choice (1-4)[/]", choices=["1", "2", "3", "4"])

    def get_search_keyword(self) -> str:
        """Get the search keyword from user input."""
        return Prompt.ask("[bold cyan]Enter search keyword[/]")

    def get_sort_order(self) -> bool:
        """Get the sort order from user input (True for descending, False for ascending)."""
        order = Prompt.ask("[bold cyan]Sort order?[/] (1 for descending, 2 for ascending)", choices=["1", "2"])
        return order == "1"