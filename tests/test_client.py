import sys
import os

# Add the 'src' directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from client import Client

import unittest

class TestOfClient(unittest.TestCase):
    """
    Unit test class for testing the `Client` class methods.
    """
    
    def setUp(self):
        """
        Prepares the test environment, including a `Client` instance and temporary files for invalid configurations.
        """
        self.client = Client("config.json")
        self.invalid_config_file = "invalid.config.example.json"

    def tearDown(self):
        """
        Cleans up temporary files created during tests.
        """
        if os.path.exists("invalid.config.example.json"):
            os.remove("invalid.config.example.json")     


    def test_init(self):
        """
        Validates proper initialization, configuration values, and WebSocket URI construction.
        """
        # Tests configration file key-value pairs
        self.assertEqual(self.client.config["host"], "localhost")
        self.assertEqual(self.client.config["port"], 7777)
        self.assertEqual(self.client.config["ai_prompt"], "You are an assistant that only provides accurate and factual information about SPŠE Ječná, a technical high school located in Prague. Avoid speculating or providing irrelevant information. Always respond in the same language as the user's input. If the user asks in Czech, respond only in Czech. If the user asks in English, respond only in English. Do not mix languages.")
        self.assertEqual(self.client.config["ai_model"], "ft:gpt-4o-mini-2024-07-18:personal:jecna-bot:AgYGPtrI")
        self.assertEqual(self.client.config["openai_api_key"], "API-KEY")
        
        # Tests the uri for websocket
        self.assertEqual(self.client.uri, f"ws://{self.client.config['host']}:{self.client.config['port']}")
        
    def test_init_invalid(self):
        """
        Ensures exceptions are raised for invalid configuration inputs.
        """
        # Tests invalid file type (not a string)
        with self.assertRaises(TypeError):
            Client(123)
        with self.assertRaises(TypeError):
            Client(True)

        # Tests file type (not type of .json)
        with self.assertRaises(ValueError):
            Client("test.csv")
        with self.assertRaises(ValueError):
            Client("test.txt")
            
            
    def test_load_config(self):
        """
        Confirms proper loading of valid configuration files.
        """
        # Test dictionary with loaded values
        valid_json = { "host": "localhost", "port": 7777, "ai_prompt" : "You are an assistant that only provides accurate and factual information about SPŠE Ječná, a technical high school located in Prague. Avoid speculating or providing irrelevant information. Always respond in the same language as the user\'s input. If the user asks in Czech, respond only in Czech. If the user asks in English, respond only in English. Do not mix languages.", "ai_model" : "ft:gpt-4o-mini-2024-07-18:personal:jecna-bot:AgYGPtrI", "openai_api_key": "API-KEY" }
        self.assertEqual(self.client.config, valid_json)
        
    def test_load_config_invalid(self):
        """
        Verifies appropriate exceptions for invalid or malformed configuration files.
        """
        # Tests invalid file name / location 
        with self.assertRaises(FileNotFoundError):
            self.client.load_config("configuration-invalid.json")
        with self.assertRaises(FileNotFoundError):
            self.client.load_config("data/config.json")
            
        # Test invalid json format
        invalid_json = "[invalid json content}"
        with open(self.invalid_config_file, "w", encoding="UTF-8") as file:
            file.write(invalid_json)

        with self.assertRaises(ValueError):
            self.client.load_config(self.invalid_config_file)
            
    
    @unittest.skip("test_connect is not implemented.")
    def test_connect(self):
        self.skipTest("NotImplemented.")

    @unittest.skip("test_connect_invalid is not implemented.")
    def test_connect_invalid(self):
        self.skipTest("NotImplemented.")
        
    
if __name__ == "__main__":
    unittest.main()