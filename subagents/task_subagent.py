"""
Task subagent that uses skills to manage task data.
This subagent handles all task-related operations using the generic skills.
"""

from skills.search_logic import search_by_key_value, search_by_multiple_criteria, search_by_keyword
from skills.sorting_logic import sort_by_key, sort_by_numeric_key, sort_by_date_key
from skills.input_validator import validate_string, validate_date, validate_number, validate_not_empty
from datetime import datetime


class TaskSubagent:
    """
    Subagent that manages task data using generic skills.
    """
    
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    
    def create_task(self, title, description="", due_date=None, priority="Medium", tags=None):
        """
        Create a new task with validation.
        
        Args:
            title (str): Task title
            description (str): Task description
            due_date (str): Due date in YYYY-MM-DD format
            priority (str): Priority level (High, Medium, Low)
            tags (list): List of tags for the task
            
        Returns:
            dict: Created task or None if validation fails
        """
        # Validate inputs
        if not validate_not_empty(title):
            print("Error: Title cannot be empty")
            return None
        
        if not validate_string(title, min_length=1, max_length=200):
            print("Error: Title must be between 1 and 200 characters")
            return None
        
        if description and not validate_string(description, max_length=1000):
            print("Error: Description exceeds 1000 characters")
            return None
        
        if due_date and not validate_date(due_date):
            print("Error: Invalid date format. Use YYYY-MM-DD")
            return None
        
        valid_priorities = ["High", "Medium", "Low"]
        if priority not in valid_priorities:
            print(f"Error: Priority must be one of {valid_priorities}")
            return None
        
        if tags is None:
            tags = []
        
        # Create the task
        task = {
            "id": self.next_id,
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "tags": tags,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def get_task(self, task_id):
        """
        Get a task by its ID.
        
        Args:
            task_id (int): The ID of the task to retrieve
            
        Returns:
            dict: The task or None if not found
        """
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def get_all_tasks(self):
        """
        Get all tasks.
        
        Returns:
            list: List of all tasks
        """
        return self.tasks
    
    def update_task(self, task_id, **updates):
        """
        Update a task with the provided fields.
        
        Args:
            task_id (int): The ID of the task to update
            **updates: Fields to update
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        # Validate updates if they exist
        if "title" in updates:
            if not validate_not_empty(updates["title"]):
                print("Error: Title cannot be empty")
                return False
            if not validate_string(updates["title"], min_length=1, max_length=200):
                print("Error: Title must be between 1 and 200 characters")
                return False
            task["title"] = updates["title"]
        
        if "description" in updates:
            if updates["description"] and not validate_string(updates["description"], max_length=1000):
                print("Error: Description exceeds 1000 characters")
                return False
            task["description"] = updates["description"]
        
        if "due_date" in updates:
            if updates["due_date"] and not validate_date(updates["due_date"]):
                print("Error: Invalid date format. Use YYYY-MM-DD")
                return False
            task["due_date"] = updates["due_date"]
        
        if "priority" in updates:
            valid_priorities = ["High", "Medium", "Low"]
            if updates["priority"] not in valid_priorities:
                print(f"Error: Priority must be one of {valid_priorities}")
                return False
            task["priority"] = updates["priority"]
        
        if "tags" in updates:
            task["tags"] = updates["tags"]
        
        if "completed" in updates:
            task["completed"] = updates["completed"]
        
        return True
    
    def delete_task(self, task_id):
        """
        Delete a task by its ID.
        
        Args:
            task_id (int): The ID of the task to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                del self.tasks[i]
                return True
        return False
    
    def search_tasks(self, **criteria):
        """
        Search tasks by various criteria.
        
        Args:
            **criteria: Search criteria
            
        Returns:
            list: List of matching tasks
        """
        if "keyword" in criteria:
            keyword = criteria.pop("keyword")
            # Search in title and description by default
            return search_by_keyword(self.tasks, keyword, ["title", "description"])
        elif len(criteria) > 0:
            return search_by_multiple_criteria(self.tasks, criteria)
        else:
            return self.tasks
    
    def sort_tasks(self, sort_by, reverse=False):
        """
        Sort tasks by a specific field.
        
        Args:
            sort_by (str): Field to sort by
            reverse (bool): Whether to sort in descending order
            
        Returns:
            list: Sorted list of tasks
        """
        if sort_by == "priority":
            # Define priority order for sorting
            priority_order = {"High": 3, "Medium": 2, "Low": 1}
            def priority_key(task):
                return priority_order.get(task.get("priority", "Medium"), 0)
            return sorted(self.tasks, key=priority_key, reverse=reverse)
        elif sort_by == "due_date":
            return sort_by_date_key(self.tasks, "due_date", reverse=reverse)
        elif sort_by == "id":
            return sort_by_numeric_key(self.tasks, "id", reverse=reverse)
        else:
            # Default to sorting by title
            return sort_by_key(self.tasks, sort_by, reverse)
    
    def mark_completed(self, task_id):
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The ID of the task to mark as completed
            
        Returns:
            bool: True if marked successfully, False otherwise
        """
        task = self.get_task(task_id)
        if task:
            task["completed"] = True
            return True
        return False
    
    def mark_incomplete(self, task_id):
        """
        Mark a task as incomplete.
        
        Args:
            task_id (int): The ID of the task to mark as incomplete
            
        Returns:
            bool: True if marked successfully, False otherwise
        """
        task = self.get_task(task_id)
        if task:
            task["completed"] = False
            return True
        return False