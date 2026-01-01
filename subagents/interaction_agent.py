"""
Interaction agent that uses the rich library to handle all console UI and menus.
"""
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.panel import Panel
from rich.layout import Layout
from rich import print


class InteractionAgent:
    def __init__(self):
        self.console = Console()
    
    def display_menu(self):
        """
        Display the main menu options.
        """
        self.console.print("\n[bold blue]Todo Console App[/bold blue]")
        self.console.print("1. View all tasks")
        self.console.print("2. Add a new task")
        self.console.print("3. Update a task")
        self.console.print("4. Delete a task")
        self.console.print("5. Mark task as completed")
        self.console.print("6. Sort tasks")
        self.console.print("7. Exit")
        
        choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5", "6", "7"])
        return choice
    
    def display_tasks(self, tasks):
        """
        Display tasks in a formatted table.
        
        Args:
            tasks (list): List of task dictionaries to display
        """
        if not tasks:
            self.console.print("[yellow]No tasks available.[/yellow]")
            return
        
        table = Table(title="Tasks")
        table.add_column("ID", style="dim", width=3)
        table.add_column("Title", style="bold")
        table.add_column("Due Date", style="dim")
        table.add_column("Priority", style="dim")
        table.add_column("Status", style="dim")
        
        for i, task in enumerate(tasks):
            status = "[green]✓ Completed[/green]" if task.get('completed', False) else "[red]○ Pending[/red]"
            priority = str(task.get('priority', 3))
            due_date = task.get('due_date', 'No due date')
            table.add_row(
                str(i),
                task.get('title', 'No title'),
                due_date,
                priority,
                status
            )
        
        self.console.print(table)
    
    def get_task_input(self):
        """
        Get task information from user input.
        
        Returns:
            dict: Dictionary containing task information
        """
        title = Prompt.ask("Enter task title")
        description = Prompt.ask("Enter task description (optional)", default="")
        due_date = Prompt.ask("Enter due date (YYYY-MM-DD, optional)", default="")
        if due_date == "":
            due_date = None
        
        priority_str = Prompt.ask("Enter priority (1-5, optional)", default="3")
        try:
            priority = int(priority_str)
            if priority < 1 or priority > 5:
                priority = 3  # Default to 3 if out of range
        except ValueError:
            priority = 3  # Default to 3 if not a number
        
        return {
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'completed': False
        }
    
    def get_task_id(self, prompt_text="Enter task ID"):
        """
        Get a task ID from user input.
        
        Args:
            prompt_text (str): The prompt text to display
            
        Returns:
            int: The task ID
        """
        while True:
            try:
                task_id = int(Prompt.ask(prompt_text))
                return task_id
            except ValueError:
                self.console.print("[red]Please enter a valid number.[/red]")
    
    def get_sort_option(self):
        """
        Get sorting option from user.
        
        Returns:
            tuple: (attribute to sort by, reverse order boolean)
        """
        self.console.print("\n[bold]Sort by:[/bold]")
        self.console.print("1. Title")
        self.console.print("2. Due Date")
        self.console.print("3. Priority")
        self.console.print("4. Status")
        
        choice = Prompt.ask("Select sorting option", choices=["1", "2", "3", "4"])
        
        attribute_map = {
            "1": "title",
            "2": "due_date", 
            "3": "priority",
            "4": "completed"
        }
        
        attribute = attribute_map[choice]
        reverse = Confirm.ask("Sort in descending order?")
        
        return attribute, reverse
    
    def display_message(self, message, style=""):
        """
        Display a message to the user.
        
        Args:
            message (str): The message to display
            style (str): Rich style string for formatting
        """
        if style:
            self.console.print(f"[{style}]{message}[/{style}]")
        else:
            self.console.print(message)
    
    def confirm_action(self, message):
        """
        Ask the user to confirm an action.
        
        Args:
            message (str): The confirmation message
            
        Returns:
            bool: True if user confirmed, False otherwise
        """
        return Confirm.ask(message)