"""
Storage Engine
Handles data persistence operations including saving and loading data from JSON files.
"""

import json
import os
from typing import Any, Dict, List, Optional


class StorageSkill:
    """Generic storage handling class for saving and loading data."""
    
    def __init__(self, filepath: str = "data/tasks.json"):
        """
        Initialize the storage skill with a file path.
        
        Args:
            filepath: Path to the JSON file for storage (default: data/tasks.json)
        """
        self.filepath = filepath
        # Ensure the directory exists
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def save_data(self, data: List[Dict[str, Any]]) -> bool:
        """
        Save data to a JSON file.
        
        Args:
            data: List of dictionaries to save
            
        Returns:
            True if save was successful, False otherwise
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self) -> Optional[List[Dict[str, Any]]]:
        """
        Load data from a JSON file.
        
        Returns:
            List of dictionaries if load was successful, None otherwise
        """
        try:
            if not os.path.exists(self.filepath):
                # Return empty list if file doesn't exist
                return []
            
            with open(self.filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None