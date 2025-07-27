"""
Unit tests for the country data parser

This module contains tests that validate the behavior of the `parse_countries` function
from the `country_picker.fetcher` module. Tests cover various data scenarios including
valid data, empty data, and malformed data structures.
"""

import unittest
from country_picker.fetcher import parse_countries

class TestJsonParsing(unittest.TestCase):
    """Tests for parse_countries() function"""
    
    def test_parse_countries(self):
        """Tests valid country data parsing and sorting"""
        test_data = [
            {"name": "France", "code": "FR"},
            {"name": "Germany", "code": "DE"},
            {"name": "Switzerland", "code": "CH"}
        ]
        result = parse_countries(test_data)
        self.assertEqual(result, ["France", "Germany", "Switzerland"])
        
    def test_empty_data(self):
        """Tests empty input handling"""
        self.assertEqual(parse_countries([]), [])
        
    def test_malformed_data(self):
        """Tests KeyError on missing 'name' field"""
        with self.assertRaises(KeyError):
            parse_countries([{"wrong_key": "Value"}])