import sys
import os
import asyncio
import json

# Add the 'src' directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from server import Server

import unittest

class TestOfServer(unittest.TestCase):
    """
    Unit test class for testing the `Server` class methods.
    """
    
    def setUp(self):
        """
        Initializes the test environment, including a `Server` instance and temporary files for invalid configurations.
        """
        self.server = Server("config.json")
        self.invalid_config_file = "invalid.config.example.json"

    def tearDown(self):
        """
        Cleans up temporary files created during tests.
        """
        if os.path.exists(self.invalid_config_file):
            os.remove(self.invalid_config_file)
        
        
    def test_init(self):
        """
        Validates proper initialization and configuration values.
        """
        self.assertEqual(self.server.config["host"], "localhost")
        self.assertEqual(self.server.config["port"], 7777)
        self.assertEqual(self.server.config["ai_prompt"], "YOUR-AI-PROMPT")
        self.assertEqual(self.server.config["ai_model"], "YOUR-AI-MODEL")
        self.assertEqual(self.server.config["openai_api_key"], "YOUR-OPENAI-API-KEY")
        
    def test_init_invalid(self):
        """
        Tests that invalid configuration inputs raise appropriate exceptions.
        """
        # Tests invalid file type (not a string)
        with self.assertRaises(TypeError):
            Server(123)

        # Test if config_file is not a .json file
        with self.assertRaises(ValueError):
            Server("test.txt")
        
    
    def test_welcome_message(self):
        """
        Verifies the server's welcome message format.
        """
        welcome_message = ( 
        r"""
Vítejte na Ječnábot serveru! 

 * Dokumentace:  /README.md (https://github.com/CheackCZ/JecnaBot)
 * Podpora:      ondra.faltin@gmail.com (ondrejfaltin.cz)
Kontaktujte podporu nebo se podívejte dokumentace pro více informací!

      _       _ _          __ ____        _     
     | |      \_/         /_/|  _ \      | |     ____                           
     | | ___  ___ _ __   __ _| |_) | ___ | |_   / ___|  ___ _ ____   _____ _ __ 
 _   | |/ _ \/ __| '_ \ / _` |  _ < / _ \| __|  \___ \ / _ \ '__\ \ / / _ \ '__|
| |__| |  __/ (__| | | | (_| | |_) | (_) | |_    ___) |  __/ |   \ V /  __/ |   
 \____/ \___|\___|_| |_|\__,_|____/ \___/ \__|  |____/ \___|_|    \_/ \___|_|   

Vítejte!

-> Naslouchám pro klávesnicové zkratky:
 └ Ctrl+R - Znovu načtení konfigurace
 └ Ctrl+C - ukončení serveru.
"""
    )
        self.assertEqual(self.server._welcome_message(), welcome_message)
        
        
    def test_load_config(self):
        """
        Ensures valid configuration files load correctly.
        """
        # Test dictionary with loaded values
        valid_json = { 
            "host": "localhost", 
            "port": 7777, 
            "ai_prompt" : "YOUR-AI-PROMPT", 
            "ai_model" : "YOUR-AI-MODEL", 
            "openai_api_key": "YOUR-OPENAI-API-KEY" }
        self.assertEqual(self.server.config, valid_json)
        
    def test_load_config_invalid(self):
        """
        Confirms that invalid configuration files raise appropriate exceptions.
        """
        # Tests invalid file name / location 
        with self.assertRaises(FileNotFoundError):
            self.server._load_config("configuration-invalid.json")
        with self.assertRaises(FileNotFoundError):
            self.server._load_config("data/config.json")
            
        # Test invalid json format
        invalid_json = "[invalid json content}"
        with open(self.invalid_config_file, "w", encoding="UTF-8") as file:
            file.write(invalid_json)

        with self.assertRaises(ValueError):
            self.server._load_config(self.invalid_config_file)
            
            
    def test_validate_config(self):
        """
        Validates that configuration keys and values are correct.
        """
        valid_config = {
            "host": "localhost",
            "port": 7777,
            "ai_prompt": "YOUR-AI-PROMPT",
            "ai_model": "YOUR-AI-MODEL",
            "openai_api_key": "YOUR-OPENAI-API-KEY"
        }
        self.assertEqual(self.server.config, valid_config)
        
    def test_validate_config_invalid(self):
        """
        Ensures invalid configurations are flagged.
        """
        # Tests missing keys
        missing_key = {
            "host": "localhost",
            "port": 7777,
            "ai_prompt": "YOUR-AI-PROMPT",
            "ai_model": "YOUR-AI-MODEL"
        }
        with self.assertRaises(ValueError):
            self.server._validate_config(missing_key)
            
        # Tests wrong (keys) data types
        wrong_values = {
            "host": 123,
            "port": "not_an_int",
            "ai_prompt": None,
            "ai_model": 123,
            "openai_api_key": None
        }
        with self.assertRaises(ValueError):
            self.server._validate_config(wrong_values)
        
    @unittest.skip("test_reload_config is not implemented.")
    async def test_reload_config(self):
        self.skipTest("NotImplementedYet.")
        
    @unittest.skip("test_reload_shortcut is not implemented.")
    async def test_reload_shortcut(self):
        self.skipTest("NotImplementedYet.")
        
    @unittest.skip("test_handle_client is not implemented.")
    async def test_handle_client(self):
        self.skipTest("NotImplementedYet.")
        
    @unittest.skip("test_run is not implemented.")
    async def test_run(self):
        self.skipTest("NotImplementedYet.")
        
if __name__ == "__main__":
    unittest.main()