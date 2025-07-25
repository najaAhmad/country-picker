import unittest
from unittest.mock import patch
from country_picker.country_fetcher import CountryFetcher
from unittest.mock import patch, MagicMock
import requests

class TestNetwork(unittest.TestCase):
    def test_parse_countries(self):
        """Test parsing of country data from apicountries.com format"""
        mock_data = [
            {"name": "Brazil", "code": "BR"},
            {"country": "Argentina", "code": "AR"},
            {"countryName": "Japan", "code": "JP"},
            {"invalid": "data"},
        ]
        fetcher = CountryFetcher()
        result = fetcher.parse_countries(mock_data)
        self.assertEqual(result, ["Argentina", "Brazil", "Japan"])

    @patch('requests.get')
    def test_api_success(self, mock_get):
        """Test successful API response"""
        mock_response = MagicMock()
        mock_response.json.return_value = [{"name": "Canada"}, {"name": "Mexico"}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        fetcher = CountryFetcher()
        fetcher.data_ready = MagicMock()
        fetcher.fetch_countries()
        
        fetcher.data_ready.emit.assert_called_with(["Canada", "Mexico"])

    @patch('requests.get')
    def test_api_failure(self, mock_get):
        """Test network failure"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")
        
        fetcher = CountryFetcher()
        fetcher.error_occurred = MagicMock()
        fetcher.fetch_countries()
        
        fetcher.error_occurred.emit.assert_called_with("Network error: Failed to connect")

if __name__ == "__main__":
    unittest.main()