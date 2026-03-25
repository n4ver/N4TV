"""Utility functions for log processing and data manipulation."""
import json
from typing import Dict, List, Tuple


def extract_log_no(url: str) -> int:
    """Extract log number from logs.tf URL.
    
    Args:
        url: The logs.tf URL (e.g., 'https://logs.tf/1234567')
    
    Returns:
        Log ID as integer, or -1 if invalid.
    """
    try:
        parts = url.split("/")
        log_id = parts[-1].split("#")[0]
        log_id_int = int(log_id)
        
        if log_id_int <= 0:
            return -1
        return log_id_int
    except (ValueError, IndexError):
        return -1


def special_sort(items: List[List]) -> List[List]:
    """Sort items by second element (class order).
    
    Args:
        items: List of [id, class_order] pairs
    
    Returns:
        Sorted list by class order value.
    """
    return sorted(items, key=lambda x: x[1])


def load_json(filepath: str) -> Dict:
    """Load JSON file with graceful fallback.
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        Parsed JSON data, or empty dict if file not found.
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}