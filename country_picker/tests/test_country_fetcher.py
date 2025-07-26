import unittest
from country_picker.country_fetcher import parse_countries

class TestJsonParsing(unittest.TestCase):
    def test_parse_countries(self):
        test_data = [
            {"name": "France", "code": "FR"},
            {"name": "Germany", "code": "DE"},
            {"name": "Switzerland", "code": "JP"}
        ]
        result = parse_countries(test_data)
        self.assertEqual(result, ["France", "Germany", "Switzerland"])
        
    def test_empty_data(self):
        self.assertEqual(parse_countries([]), [])
        
    def test_malformed_data(self):
        with self.assertRaises(KeyError):
            parse_countries([{"wrong_key": "Value"}])