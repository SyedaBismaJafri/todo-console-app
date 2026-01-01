"""
Generic search logic for searching lists of dictionaries by key/value.
This module contains reusable search functions that can be used in any application.
"""

def search_by_key_value(data_list, key, value):
    """
    Search a list of dictionaries by a specific key-value pair.
    
    Args:
        data_list (list): List of dictionaries to search
        key (str): The key to search for
        value: The value to match
        
    Returns:
        list: List of dictionaries that match the key-value pair
    """
    return [item for item in data_list if item.get(key) == value]


def search_by_multiple_criteria(data_list, criteria):
    """
    Search a list of dictionaries by multiple criteria.
    
    Args:
        data_list (list): List of dictionaries to search
        criteria (dict): Dictionary of key-value pairs to match
        
    Returns:
        list: List of dictionaries that match all criteria
    """
    results = []
    for item in data_list:
        match = True
        for key, value in criteria.items():
            if item.get(key) != value:
                match = False
                break
        if match:
            results.append(item)
    return results


def search_by_keyword(data_list, keyword, keys_to_search=None):
    """
    Search a list of dictionaries for a keyword in specified keys.
    
    Args:
        data_list (list): List of dictionaries to search
        keyword (str): The keyword to search for
        keys_to_search (list): List of keys to search in. If None, searches all keys.
        
    Returns:
        list: List of dictionaries that contain the keyword
    """
    results = []
    keyword_lower = keyword.lower()
    
    for item in data_list:
        match = False
        if keys_to_search:
            # Search only in specified keys
            for key in keys_to_search:
                if key in item and keyword_lower in str(item[key]).lower():
                    match = True
                    break
        else:
            # Search in all values
            for value in item.values():
                if keyword_lower in str(value).lower():
                    match = True
                    break
        
        if match:
            results.append(item)
    
    return results


def fuzzy_search(data_list, key, value, threshold=0.6):
    """
    Perform a fuzzy search on a specific key in the list of dictionaries.
    
    Args:
        data_list (list): List of dictionaries to search
        key (str): The key to search in
        value (str): The value to match against
        threshold (float): Similarity threshold (0-1), default 0.6
        
    Returns:
        list: List of dictionaries that match above the threshold
    """
    try:
        from difflib import SequenceMatcher
    except ImportError:
        # If difflib is not available, fall back to exact match
        return search_by_key_value(data_list, key, value)
    
    results = []
    value_lower = value.lower()
    
    for item in data_list:
        item_value = str(item.get(key, ""))
        similarity = SequenceMatcher(None, value_lower, item_value.lower()).ratio()
        
        if similarity >= threshold:
            results.append(item)
    
    return results