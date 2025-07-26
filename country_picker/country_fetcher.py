import requests
import json
from typing import List
from requests.exceptions import RequestException

API_URL = "https://www.apicountries.com/countries"

def fetch_countries() -> List[str]:
    """Fetch and parse country data from API"""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return True, parse_countries(response.json())
    except RequestException as e:
        return False, f"Network error: {str(e)}"
    except json.JSONDecodeError:
        return False, "Invalid API response format"
    except KeyError:
        return False, "Unexpected data format in API response"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def parse_countries(data: list) -> List[str]:
    """Parse JSON response into sorted country names"""
    return sorted([country['name'] for country in data])