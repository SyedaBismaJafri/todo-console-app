"""
Generic validator skill for checking empty strings, date formats, and range limits.
"""
import re
from datetime import datetime


def is_empty(value):
    """
    Check if a value is empty (None, empty string, or empty collection).
    
    Args:
        value: The value to check
        
    Returns:
        bool: True if the value is empty, False otherwise
    """
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    if isinstance(value, (list, tuple, dict)) and len(value) == 0:
        return True
    return False


def validate_date_format(date_string, format_pattern="%Y-%m-%d"):
    """
    Validate if a string matches a specific date format.
    
    Args:
        date_string (str): The date string to validate
        format_pattern (str): The expected date format (default: "%Y-%m-%d")
        
    Returns:
        bool: True if the date string matches the format, False otherwise
    """
    try:
        datetime.strptime(date_string, format_pattern)
        return True
    except ValueError:
        return False


def validate_range(value, min_val=None, max_val=None):
    """
    Validate if a numeric value is within a specified range.
    
    Args:
        value: The value to check (should be numeric)
        min_val: The minimum allowed value (optional)
        max_val: The maximum allowed value (optional)
        
    Returns:
        bool: True if the value is within range, False otherwise
    """
    try:
        num_value = float(value)
        if min_val is not None and num_value < min_val:
            return False
        if max_val is not None and num_value > max_val:
            return False
        return True
    except (ValueError, TypeError):
        return False


def validate_email_format(email):
    """
    Validate if a string matches a basic email format.
    
    Args:
        email (str): The email string to validate
        
    Returns:
        bool: True if the email matches the format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_string_length(string, min_length=None, max_length=None):
    """
    Validate if a string's length is within a specified range.
    
    Args:
        string (str): The string to validate
        min_length (int): The minimum allowed length (optional)
        max_length (int): The maximum allowed length (optional)
        
    Returns:
        bool: True if the string length is within range, False otherwise
    """
    length = len(string)
    if min_length is not None and length < min_length:
        return False
    if max_length is not None and length > max_length:
        return False
    return True