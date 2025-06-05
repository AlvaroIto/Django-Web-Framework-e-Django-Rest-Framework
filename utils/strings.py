def is_positive_number(value):
    """
    Check if the given string represents a positive number.

    Args:
        string (str): The string to check.

    Returns:
        bool: True if the string is a positive number, False otherwise.
    """
    try:
        number_string = float(value)
    except ValueError:
        return False
    return number_string > 0