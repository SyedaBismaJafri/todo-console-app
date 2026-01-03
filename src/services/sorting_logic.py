from datetime import datetime

def sort_data(data_list, sort_by, reverse=False):
    """
    Sort data_list by specified field with custom logic for priority and date.
    
    Args:
        data_list: List of dictionaries to sort
        sort_by: Field to sort by ('priority' or 'date')
        reverse: Whether to sort in descending order (default: False)
        
    Returns:
        Sorted list of items
    """
    if sort_by == 'priority':
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        return sorted(data_list, key=lambda x: priority_order.get(x.get('priority', '').lower(), 3), reverse=reverse)
    elif sort_by == 'date':
        def date_key(item):
            date_str = item.get('date', '')
            try:
                # Try to parse the date string to a datetime object
                return datetime.strptime(date_str, '%Y-%m-%d')
            except (ValueError, TypeError):
                # If parsing fails, return a very old date to put it at the beginning
                return datetime.min
        return sorted(data_list, key=date_key, reverse=reverse)
    else:
        # Default sorting by the field value as string
        return sorted(data_list, key=lambda x: x.get(sort_by, ''), reverse=reverse)