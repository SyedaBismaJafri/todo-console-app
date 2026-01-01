"""
Display subagent that uses the rich library to handle all UI rendering.
This subagent manages the console interface using rich for better formatting.
"""

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.panel import Panel
from rich.layout import Layout
from rich import print as rich_print


class DisplaySubagent:
    """
    Subagent that handles all UI rendering using the rich library.
    """
    
    def __init__(self):
        self.console = Console()
    
    def display_welcome(self):
        """Display the welcome message."""
        self.console.print(Panel("Welcome to the Todo Console Application!", title="Welcome", border_style="green"))
        self.console.print("Type 'help' or select option 7 to see available commands.\n")
    
    def display_menu(self):
        """Display the main menu and get user choice."""
        self.console.print("\n[bold blue]Todo Console Application[/]")
        self.console.print("Choose an option:")
        self.console.print("1. View Tasks")
        self.console.print("2. Add Task")
        self.console.print("3. Update Task")
        self.console.print("4. Delete Task")
        self.console.print("5. Mark Task Complete/Incomplete")
        self.console.print("6. Search Tasks")
        self.console.print("7. Help")
        self.console.print("8. Exit")
        
        choice = Prompt.ask("\n[bold cyan]Enter your choice (1-8)[/]", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
        return choice
    
    def display_tasks(self, tasks):
        """Display tasks in a formatted table."""
        if not tasks:
            self.console.print("\n[bold yellow]No tasks found. Add some tasks to get started![/]\n")
            return

        table = Table(title="Your Todo List", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=5)
        table.add_column("Status", width=10)
        table.add_column("Title", width=30)
        table.add_column("Description", width=40)
        table.add_column("Due Date", width=12)
        table.add_column("Priority", width=10)
        table.add_column("Tags", width=20)

        for task in sorted(tasks, key=lambda t: t.get("id", 0)):
            status = f"{'✓' if task.get('completed', False) else '○'} [{'green' if task.get('completed', False) else 'red'}]{'Completed' if task.get('completed', False) else 'Pending'}[/{'green' if task.get('completed', False) else 'red'}]"
            title = task.get("title", "No title")
            description = task.get("description", "")
            due_date = task.get("due_date", "No due date")
            priority = task.get("priority", "Medium")
            tags = ", ".join(task.get("tags", []))
            
            # Truncate description if too long
            if len(description) > 40:
                description = description[:37] + "..."

            table.add_row(
                str(task.get("id", "N/A")),
                status,
                title,
                description,
                due_date,
                priority,
                tags
            )

        self.console.print(table)
    
    def get_task_details(self):
        """Get task details from user input."""
        title = Prompt.ask("[bold cyan]Enter task title[/] (max 200 chars)")
        description = Prompt.ask("[bold cyan]Enter task description[/] (max 1000 chars, optional)", default="")
        
        # Get due date with validation
        while True:
            due_date = Prompt.ask("[bold cyan]Enter due date (YYYY-MM-DD, optional)[/]", default="")
            if due_date == "":
                due_date = None
                break
            # Basic validation - in a real app, you'd want more thorough validation
            if self._is_valid_date_format(due_date):
                break
            else:
                self.console.print("[red]Invalid date format. Please use YYYY-MM-DD.[/]")
        
        # Get priority
        priority = Prompt.ask("[bold cyan]Enter priority[/] (High/Medium/Low)", choices=["High", "Medium", "Low"], default="Medium")
        
        # Get tags
        tags_input = Prompt.ask("[bold cyan]Enter tags (comma-separated, optional)[/]", default="")
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else []
        
        return title, description, due_date, priority, tags
    
    def _is_valid_date_format(self, date_str):
        """Check if the date string matches YYYY-MM-DD format."""
        import re
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return bool(re.match(pattern, date_str))
    
    def get_task_id(self, action="operate on"):
        """Get a task ID from user input."""
        while True:
            try:
                task_id_input = Prompt.ask(f"[bold cyan]Enter task ID to {action}[/]")
                task_id = int(task_id_input)
                return task_id
            except ValueError:
                self.console.print("[red]Please enter a valid number.[/]")
    
    def get_search_criteria(self):
        """Get search criteria from user input."""
        self.console.print("\n[bold]Search options:[/]")
        self.console.print("1. Search by keyword in title/description")
        self.console.print("2. Search by status (completed/incomplete)")
        self.console.print("3. Search by priority")
        self.console.print("4. Search by tag")
        
        choice = Prompt.ask("Select search option", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            keyword = Prompt.ask("Enter keyword to search for")
            return {"keyword": keyword}
        elif choice == "2":
            status = Prompt.ask("Enter status", choices=["completed", "incomplete"], default="incomplete")
            return {"completed": status == "completed"}
        elif choice == "3":
            priority = Prompt.ask("Enter priority", choices=["High", "Medium", "Low"])
            return {"priority": priority}
        elif choice == "4":
            tag = Prompt.ask("Enter tag to search for")
            # For tag search, we'll need to implement custom logic
            # since tags are stored as a list
            return {"tag": tag}
    
    def get_sort_option(self):
        """Get sort option from user input."""
        self.console.print("\n[bold]Sort options:[/]")
        self.console.print("1. Sort by ID")
        self.console.print("2. Sort by Title")
        self.console.print("3. Sort by Due Date")
        self.console.print("4. Sort by Priority")
        
        choice = Prompt.ask("Select sort option", choices=["1", "2", "3", "4"])
        
        sort_options = {
            "1": "id",
            "2": "title", 
            "3": "due_date",
            "4": "priority"
        }
        
        sort_by = sort_options[choice]
        reverse = Confirm.ask("Sort in descending order?")
        
        return sort_by, reverse
    
    def show_message(self, message, style="default"):
        """Display a message with the specified style."""
        if style == "success":
            self.console.print(f"[bold green]✓ {message}[/]")
        elif style == "error":
            self.console.print(f"[bold red]✗ {message}[/]")
        elif style == "warning":
            self.console.print(f"[bold yellow]⚠ {message}[/]")
        elif style == "info":
            self.console.print(f"[bold blue]ℹ {message}[/]")
        else:
            self.console.print(message)
    
    def confirm_action(self, message):
        """Ask user to confirm an action."""
        return Confirm.ask(f"[bold yellow]{message}[/]")
    
    def show_help(self):
        """Display help information."""
        help_text = """
[b]Available Commands:[/]
  1. View Tasks      - View all tasks with their details
  2. Add Task        - Add a new task with title, description, due date, priority and tags
  3. Update Task     - Update a task's details by ID
  4. Delete Task     - Delete a task by its ID
  5. Mark Complete   - Toggle task completion status by ID
  6. Search Tasks    - Search tasks by keyword, status, priority or tag
  7. Help            - Show this help message
  8. Exit            - Exit the application

[i]All tasks are stored in memory during this session.[/]
        """
        self.console.print(Panel(help_text, title="Help", border_style="blue"))