import json
import requests
from typing import List
from requests.exceptions import RequestException
from PyQt5.QtCore import QObject, pyqtSignal

API_URL = "https://www.apicountries.com/countries"

class CountryFetcher(QObject):
    """Handles country data fetching from apicountries.com"""
    data_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def fetch_countries(self):
        """Fetch country names from API"""
        try:
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()
            countries = self.parse_countries(response.json())
            self.data_ready.emit(countries)
        except RequestException as e:
            self.error_occurred.emit(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            self.error_occurred.emit("Invalid API response format")
        except KeyError:
            self.error_occurred.emit("Unexpected data format in API response")
        except Exception as e:
            self.error_occurred.emit(f"Unexpected error: {str(e)}")

    def parse_countries(self, data: list) -> List[str]:
        """Parse JSON data and return sorted country names"""
        countries = []
        for country in data:
            name = country.get('name')
            if name:
                countries.append(name)
        return sorted(countries)