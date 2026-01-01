"""
Generic sorting logic for sorting lists of dictionaries by any key.
This module contains reusable sorting functions that can be used in any application.
"""

def sort_by_key(data_list, key, reverse=False):
    """
    Sort a list of dictionaries by a specific key.
    
    Args:
        data_list (list): List of dictionaries to sort
        key (str): The key to sort by
        reverse (bool): Whether to sort in descending order (default: False)
        
    Returns:
        list: Sorted list of dictionaries
    """
    try:
        return sorted(data_list, key=lambda x: x.get(key, ''), reverse=reverse)
    except TypeError:
        # If there are mixed types that can't be compared, return original list
        return data_list


def sort_by_multiple_keys(data_list, keys, reverse=False):
    """
    Sort a list of dictionaries by multiple keys in order of priority.
    
    Args:
        data_list (list): List of dictionaries to sort
        keys (list): List of keys to sort by in priority order
        reverse (bool): Whether to sort in descending order (default: False)
        
    Returns:
        list: Sorted list of dictionaries
    """
    def sort_key(item):
        return tuple(item.get(key, '') for key in keys)
    
    try:
        return sorted(data_list, key=sort_key, reverse=reverse)
    except TypeError:
        # If there are mixed types that can't be compared, return original list
        return data_list


def sort_by_custom_function(data_list, sort_func, reverse=False):
    """
    Sort a list of dictionaries using a custom sort function.
    
    Args:
        data_list (list): List of dictionaries to sort
        sort_func (function): Function that takes a dictionary and returns a sort key
        reverse (bool): Whether to sort in descending order (default: False)
        
    Returns:
        list: Sorted list of dictionaries
    """
    try:
        return sorted(data_list, key=sort_func, reverse=reverse)
    except TypeError:
        # If there are mixed types that can't be compared, return original list
        return data_list


def sort_by_numeric_key(data_list, key, reverse=False):
    """
    Sort a list of dictionaries by a numeric key.
    
    Args:
        data_list (list): List of dictionaries to sort
        key (str): The key to sort by (should have numeric values)
        reverse (bool): Whether to sort in descending order (default: False)
        
    Returns:
        list: Sorted list of dictionaries
    """
    def safe_numeric_value(item):
        value = item.get(key, 0)
        try:
            return float(value)
        except (ValueError, TypeError):
            # If conversion fails, return 0 as default
            return 0
    
    try:
        return sorted(data_list, key=safe_numeric_value, reverse=reverse)
    except TypeError:
        # If there are mixed types that can't be compared, return original list
        return data_list


def sort_by_date_key(data_list, key, date_format='%Y-%m-%d', reverse=False):
    """
    Sort a list of dictionaries by a date key.
    
    Args:
        data_list (list): List of dictionaries to sort
        key (str): The key to sort by (should have date values)
        date_format (str): The format of the date string (default: '%Y-%m-%d')
        reverse (bool): Whether to sort in descending order (default: False)
        
    Returns:
        list: Sorted list of dictionaries
    """
    from datetime import datetime
    
    def safe_date_value(item):
        date_str = item.get(key, '')
        try:
            return datetime.strptime(date_str, date_format)
        except (ValueError, TypeError):
            # If parsing fails, return a very old date as default
            return datetime.min
    
    try:
        return sorted(data_list, key=safe_date_value, reverse=reverse)
    except TypeError:
        # If there are mixed types that can't be compared, return original list
        return data_list