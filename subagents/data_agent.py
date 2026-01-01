"""
Data agent that uses validator and sorting_engine skills to manage the life-cycle of tasks.
"""
from skills.validator import is_empty, validate_date_format, validate_range
from skills.sorting_engine import sort_list_by_attribute
from datetime import datetime


class DataAgent:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task_data):
        """
        Add a new task to the task list after validating it.
        
        Args:
            task_data (dict): Dictionary containing task information
            
        Returns:
            bool: True if task was added successfully, False otherwise
        """
        # Validate required fields
        if is_empty(task_data.get('title')):
            print("Error: Task title cannot be empty.")
            return False
        
        # Validate optional fields if present
        if 'due_date' in task_data and task_data['due_date']:
            if not validate_date_format(task_data['due_date']):
                print("Error: Invalid date format. Use YYYY-MM-DD.")
                return False
        
        if 'priority' in task_data and task_data['priority'] is not None:
            if not validate_range(task_data['priority'], 1, 5):
                print("Error: Priority must be between 1 and 5.")
                return False
        
        # Set default values if not provided
        if 'completed' not in task_data:
            task_data['completed'] = False
        if 'created_at' not in task_data:
            task_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 'priority' not in task_data:
            task_data['priority'] = 3  # Default priority
        
        # Add the task
        self.tasks.append(task_data)
        return True
    
    def update_task(self, task_id, updated_data):
        """
        Update an existing task with new data after validating it.
        
        Args:
            task_id (int): ID of the task to update
            updated_data (dict): Dictionary containing updated task information
            
        Returns:
            bool: True if task was updated successfully, False otherwise
        """
        if 0 <= task_id < len(self.tasks):
            # Validate updated fields
            if 'title' in updated_data and is_empty(updated_data['title']):
                print("Error: Task title cannot be empty.")
                return False
            
            if 'due_date' in updated_data and updated_data['due_date']:
                if not validate_date_format(updated_data['due_date']):
                    print("Error: Invalid date format. Use YYYY-MM-DD.")
                    return False
            
            if 'priority' in updated_data and updated_data['priority'] is not None:
                if not validate_range(updated_data['priority'], 1, 5):
                    print("Error: Priority must be between 1 and 5.")
                    return False
            
            # Update the task
            self.tasks[task_id].update(updated_data)
            return True
        else:
            print(f"Error: Task with ID {task_id} does not exist.")
            return False
    
    def delete_task(self, task_id):
        """
        Delete a task by its ID.
        
        Args:
            task_id (int): ID of the task to delete
            
        Returns:
            bool: True if task was deleted successfully, False otherwise
        """
        if 0 <= task_id < len(self.tasks):
            del self.tasks[task_id]
            return True
        else:
            print(f"Error: Task with ID {task_id} does not exist.")
            return False
    
    def get_task(self, task_id):
        """
        Get a specific task by its ID.
        
        Args:
            task_id (int): ID of the task to retrieve
            
        Returns:
            dict or None: The task dictionary if found, None otherwise
        """
        if 0 <= task_id < len(self.tasks):
            return self.tasks[task_id]
        else:
            return None
    
    def get_all_tasks(self):
        """
        Get all tasks.
        
        Returns:
            list: List of all task dictionaries
        """
        return self.tasks
    
    def sort_tasks(self, attribute, reverse=False):
        """
        Sort tasks by a specific attribute.
        
        Args:
            attribute (str): Attribute to sort by
            reverse (bool): Whether to sort in descending order
            
        Returns:
            list: Sorted list of tasks
        """
        return sort_list_by_attribute(self.tasks, attribute, reverse)
    
    def mark_task_completed(self, task_id):
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of the task to mark as completed
            
        Returns:
            bool: True if task was marked as completed, False otherwise
        """
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id]['completed'] = True
            return True
        else:
            print(f"Error: Task with ID {task_id} does not exist.")
            return False