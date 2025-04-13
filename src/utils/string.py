import logging
from typing import Optional

logger = logging.getLogger(__name__)

def extract_json_array(json_str: str) -> str:
    """
    Extracts a JSON array from a string containing JSON.
    
    Args:
        json_str: String containing JSON
        
    Returns:
        str: Extracted JSON array
        
    Raises:
        ValueError: If the string is empty or does not contain a JSON array
        TypeError: If the input argument is not a string
    """
    if not isinstance(json_str, str):
        logger.error(f"Expected string, got {type(json_str)}")
        raise TypeError("Input argument must be a string")
        
    if not json_str:
        logger.error("Received empty string")
        raise ValueError("String cannot be empty")
        
    start_idx = json_str.find('[')
    end_idx = json_str.rfind(']')
    
    if start_idx == -1 or end_idx == -1:
        logger.error("Failed to find JSON array in string")
        raise ValueError("Failed to find JSON array in string")
        
    if start_idx >= end_idx:
        logger.error("Invalid start and end indices for JSON array")
        raise ValueError("Invalid start and end indices for JSON array")
        
    result = json_str[start_idx:end_idx + 1]
    logger.debug(f"Successfully extracted JSON array of length {len(result)} characters")
    return result 