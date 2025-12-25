"""
Step 2: Raw JSON Storage
Saves and loads raw API responses to/from filesystem
"""

import json
import os
from datetime import datetime
from typing import Dict


def save_raw_response(
    data: Dict,
    output_dir: str = "data/raw",
    prefix: str = "raw"
) -> str:
    """
    Save raw JSON response to a timestamped file.
    
    Args:
        data: Dictionary containing API response data
        output_dir: Directory to save the file (default: 'data/raw')
        prefix: Filename prefix (default: 'raw')
    
    Returns:
        Path to the saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    
    counter = 1
    while True:
        filename = f"{prefix}_{date_str}_{counter:02d}.json"
        file_path = os.path.join(output_dir, filename)
        if not os.path.exists(file_path):
            break
        counter += 1
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return file_path
    except IOError as e:
        raise Exception(f"Error saving raw response to {file_path}: {str(e)}")


def load_raw_response(file_path: str) -> Dict:
    """
    Load raw JSON response from file.
    
    Args:
        file_path: Path to the JSON file
    
    Returns:
        Dictionary containing the loaded data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except IOError as e:
        raise Exception(f"Error loading raw response from {file_path}: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON from {file_path}: {str(e)}")

