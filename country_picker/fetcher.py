"""
Module for fetching country data with enhanced error reporting
Returns success status, message, and data in a structured tuple
"""

import requests
import json
from typing import List, Tuple
from requests.exceptions import RequestException

API_URL = "https://www.apicountries.com/countries"

def fetch_countries() -> Tuple[bool, str, List[str]]:
    """
    Fetches country data from API and returns structured result
    
    Returns:
        Tuple containing:
        - bool: Success status (True/False)
        - str: Status message
        - List[str]: Sorted country names (empty list on failure)
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return True, "Fetch Success", parse_countries(response.json())
    except RequestException as e:
        return False, f"Network error: {str(e)}", []
    except json.JSONDecodeError:
        return False, "Invalid API response format", []
    except KeyError:
        return False, "Unexpected data format in API response", []
    except Exception as e:
        return False, f"Unexpected error: {str(e)}", []

def parse_countries(data: list) -> List[str]:
    """
    Parses JSON response into sorted country names
    
    Args:
        data: JSON response parsed as list of dictionaries
        
    Returns:
        Alphabetically sorted list of country names
    """
    return sorted(country['name'] for country in data)