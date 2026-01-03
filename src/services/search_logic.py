def search_data(data_list, keyword, fields_to_search):
    """
    Search through data_list for items that match the keyword in specified fields.
    
    Args:
        data_list: List of dictionaries to search through
        keyword: String to search for
        fields_to_search: List of field names to search in
        
    Returns:
        List of items that match the search criteria
    """
    if not keyword:
        return data_list
    
    keyword_lower = keyword.lower()
    results = []
    
    for item in data_list:
        for field in fields_to_search:
            if field in item:
                value = item[field]
                # Handle both single values and lists (like tags)
                if isinstance(value, list):
                    if any(keyword_lower in str(item_value).lower() for item_value in value):
                        results.append(item)
                        break
                elif keyword_lower in str(value).lower():
                    results.append(item)
                    break
    
    return results