"""
Generic input validation logic for validating various data types.
This module contains reusable validation functions that can be used in any application.
"""

import re
from datetime import datetime


def validate_string(value, min_length=0, max_length=None, allowed_patterns=None):
    """
    Validate a string based on length and optional patterns.
    
    Args:
        value (str): The string to validate
        min_length (int): Minimum allowed length (default: 0)
        max_length (int): Maximum allowed length (default: None)
        allowed_patterns (list): List of regex patterns that the string must match
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    if len(value) < min_length:
        return False
    
    if max_length is not None and len(value) > max_length:
        return False
    
    if allowed_patterns:
        for pattern in allowed_patterns:
            if not re.match(pattern, value):
                return False
    
    return True


def validate_number(value, min_val=None, max_val=None, integer_only=False):
    """
    Validate a number based on range and type.
    
    Args:
        value: The value to validate
        min_val (int/float): Minimum allowed value (default: None)
        max_val (int/float): Maximum allowed value (default: None)
        integer_only (bool): Whether only integers are allowed (default: False)
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        num_value = float(value)
    except (ValueError, TypeError):
        return False
    
    if integer_only and not num_value.is_integer():
        return False
    
    if min_val is not None and num_value < min_val:
        return False
    
    if max_val is not None and num_value > max_val:
        return False
    
    return True


def validate_date(value, date_format='%Y-%m-%d'):
    """
    Validate a date string against a specific format.
    
    Args:
        value (str): The date string to validate
        date_format (str): The expected date format (default: '%Y-%m-%d')
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    try:
        datetime.strptime(value, date_format)
        return True
    except ValueError:
        return False


def validate_email(value):
    """
    Validate an email address using a basic regex pattern.
    
    Args:
        value (str): The email to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, value) is not None


def validate_url(value):
    """
    Validate a URL using a basic regex pattern.
    
    Args:
        value (str): The URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
    return re.match(pattern, value) is not None


def validate_choice(value, valid_choices):
    """
    Validate that a value is in a list of valid choices.
    
    Args:
        value: The value to validate
        valid_choices (list): List of valid choices
        
    Returns:
        bool: True if valid, False otherwise
    """
    return value in valid_choices


def validate_not_empty(value):
    """
    Validate that a value is not empty.
    
    Args:
        value: The value to validate
        
    Returns:
        bool: True if not empty, False otherwise
    """
    if value is None:
        return False
    
    if isinstance(value, str) and value.strip() == '':
        return False
    
    if isinstance(value, (list, tuple, dict)) and len(value) == 0:
        return False
    
    return True


def validate_phone_number(value, country_code='+1'):
    """
    Validate a phone number based on a country code.
    
    Args:
        value (str): The phone number to validate
        country_code (str): The country code (default: '+1' for US)
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', value)
    
    if country_code == '+1':  # US/Canada
        # US numbers should be 10 or 11 digits (with optional country code)
        if len(digits_only) == 10:
            return True
        elif len(digits_only) == 11 and digits_only[0] == '1':
            return True
        else:
            return False
    else:
        # For other countries, just check if it has at least 7 digits
        return len(digits_only) >= 7


def validate_custom_pattern(value, pattern):
    """
    Validate a value against a custom regex pattern.
    
    Args:
        value (str): The value to validate
        pattern (str): The regex pattern to match against
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    return re.match(pattern, value) is not None