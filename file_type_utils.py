from mimetypes import guess_type

def is_file_type(filename: str, file_type: str) -> bool:
    """
    Check if the given file is of the given type.
    
    Args:
        filename (str): The name of the file to check.
        file_type (str): The type of the file to check.
    
    Returns:
        bool: True if the file is of the given type, False otherwise.
    """
    return guess_type(filename)[0] == file_type