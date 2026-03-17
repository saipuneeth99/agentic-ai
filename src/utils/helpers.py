"""Utility functions for the agentic system"""

import json
from typing import Any, Dict, Optional
from src.config import logger


def print_json(data: Any, indent: int = 2) -> str:
    """Pretty print JSON data
    
    Args:
        data: Data to print
        indent: JSON indentation
        
    Returns:
        JSON string
    """
    return json.dumps(data, indent=indent, default=str)


def safe_parse_json(text: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Safely parse JSON text
    
    Args:
        text: JSON text
        default: Default value if parsing fails
        
    Returns:
        Parsed JSON or default
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse JSON: {e}")
        return default or {}


def format_task_output(task_result: Dict[str, Any]) -> str:
    """Format task result for output
    
    Args:
        task_result: Task result dictionary
        
    Returns:
        Formatted string
    """
    return print_json(task_result)
