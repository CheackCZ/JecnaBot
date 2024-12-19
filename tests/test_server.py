import sys
import os
import json

# Add the 'src' directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from server import Server

import unittest

class TestOfServer(unittest.TestCase):
    
    def setUp(self):
        self.server = Server("config.json")
        
        
    def test_init(self):
        # Tests configration file key-value pairs
        self.assertEqual(self.server.config["host"], "localhost")
        self.assertEqual(self.server.config["port"], 7777)
        self.assertEqual(self.server.config["openai_api_key"], "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")
        
    def test_init_invalid(self):
        # Tests invalid file type (not a string)
        with self.assertRaises(TypeError):
            Server(123)

         # Test if config_file is not a .json file
        with self.assertRaises(Exception):
            Server("test.txt")
        
        
    def test_load_config(self):
        pass
        
if __name__ == "__main__":
    unittest.main()