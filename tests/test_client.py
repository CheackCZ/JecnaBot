import sys
import os
import json

# Add the 'src' directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from client import Client

import unittest

class TestOfClient(unittest.TestCase):
    
    def setUp(self):
        self.client = Client("config.json")
        
    def tearDown(self):
        if os.path.exists("invalid.config.example.json"):
            os.remove("invalid.config.example.json")
        
    def test_init(self):
        # Tests configration file key-value pairs
        self.assertEqual(self.client.config["host"], "localhost")
        self.assertEqual(self.client.config["port"], 7777)
        self.assertEqual(self.client.config["openai_api_key"], "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")
        
        # Tests the uri for websocket
        self.assertEqual(self.client.uri, f"ws://{self.client.config['host']}:{self.client.config['port']}")
        
    def test_init_invalid(self):
        # Tests invalid file type (not a string)
        with self.assertRaises(TypeError):
            Client(123)

        # Tests file type (not type of .json)
        with self.assertRaises(Exception):
            Client("test.csv")
            
            
        # Tests invalid host name.
        self.invalid_config_file = "invalid.config.example.json"
        with open(self.invalid_config_file, "w", encoding="UTF-8") as file:
            json.dump({"host": 123}, file)
            
        with self.assertRaises(ValueError):
            Client(self.invalid_config_file)
            
            
        # Tests invalid port data type (is no an integer).
        with open(self.invalid_config_file, "w", encoding="UTF-8") as file:
            json.dump({"port": "123"}, file)
            
        with self.assertRaises(ValueError):
            Client(self.invalid_config_file)
            
        # Tests invalid port number range.
        with open(self.invalid_config_file, "w", encoding="UTF-8") as file:
            json.dump({"port": 700000}, file)
            
        with self.assertRaises(ValueError):
            Client(self.invalid_config_file)
            
        # Tests invalid port number range.
        with open(self.invalid_config_file, "w", encoding="UTF-8") as file:
            json.dump({"port": -10}, file)
            
        with self.assertRaises(ValueError):
            Client(self.invalid_config_file)
        
        
        # Test invalid openai_api_key (not a string)
        with open(self.invalid_config_file, "w", encoding="UTF-8") as file:
            json.dump({"openai_api_key" : 123}, file)
            
        with self.assertRaises(ValueError):
            Client("invalid.config.example.json")
            
        
    def test_connect(self):
        pass
        
    
if __name__ == "__main__":
    unittest.main()