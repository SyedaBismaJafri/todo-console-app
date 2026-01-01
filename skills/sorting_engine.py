"""
Generic sorting engine skill for sorting lists based on provided attributes.
"""


def sort_list_by_attribute(data_list, attribute, reverse=False):
    """
    Sort a list of dictionaries or objects by a specific attribute.
    
    Args:
        data_list (list): List of dictionaries or objects to sort
        attribute (str): The attribute/key to sort by
        reverse (bool): Whether to sort in descending order (default: False)
        
    Returns:
        list: Sorted list based on the specified attribute
    """
    try:
        return sorted(data_list, key=lambda x: x.get(attribute) if isinstance(x, dict) else getattr(x, attribute), reverse=reverse)
    except (AttributeError, KeyError):
        # If the attribute doesn't exist, return the original list
        return data_list


def sort_list_by_multiple_attributes(data_list, attributes, reverse=False):
    """
    Sort a list of dictionaries or objects by multiple attributes in order of priority.
    
    Args:
        data_list (list): List of dictionaries or objects to sort
        attributes (list): List of attributes/keys to sort by in priority order
        reverse (bool): Whether to sort in descending order (default: False)
        
    Returns:
        list: Sorted list based on the specified attributes
    """
    def sort_key(item):
        key_values = []
        for attr in attributes:
            if isinstance(item, dict):
                key_values.append(item.get(attr))
            else:
                key_values.append(getattr(item, attr))
        return tuple(key_values)
    
    try:
        return sorted(data_list, key=sort_key, reverse=reverse)
    except (AttributeError, KeyError):
        # If the attribute doesn't exist, return the original list
        return data_list


def sort_list_by_custom_function(data_list, sort_function, reverse=False):
    """
    Sort a list using a custom sort function.
    
    Args:
        data_list (list): List to sort
        sort_function (function): Function that takes an item and returns the sort key
        reverse (bool): Whether to sort in descending order (default: False)
        
    Returns:
        list: Sorted list based on the custom function
    """
    try:
        return sorted(data_list, key=sort_function, reverse=reverse)
    except TypeError:
        # If the sort function fails, return the original list
        return data_list