def validate_priority(priority):
    """
    Validate that the priority input matches the allowed list.
    
    Args:
        priority: Priority value to validate
        
    Returns:
        bool: True if priority is valid, False otherwise
    """
    allowed_priorities = ['high', 'medium', 'low']
    return priority.lower() in allowed_priorities