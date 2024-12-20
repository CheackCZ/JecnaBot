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
        self.invalid_config_file = "invalid.config.example.json"

    def tearDown(self):
        if os.path.exists(self.invalid_config_file):
            os.remove(self.invalid_config_file)
        
        
    def test_init(self):
        # Tests configration file key-value pairs
        self.assertEqual(self.server.config["host"], "localhost")
        self.assertEqual(self.server.config["port"], 7777)
        self.assertEqual(self.server.config["ai_prompt"], "You are an assistant that only provides accurate and factual information about SPŠE Ječná, a technical high school located in Prague. Avoid speculating or providing irrelevant information. Always respond in the same language as the user's input. If the user asks in Czech, respond only in Czech. If the user asks in English, respond only in English. Do not mix languages.")
        self.assertEqual(self.server.config["ai_model"], "ft:gpt-4o-mini-2024-07-18:personal:jecna-bot:AgYGPtrI")
        self.assertEqual(self.server.config["openai_api_key"], "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")
        
    def test_init_invalid(self):
        # Tests invalid file type (not a string)
        with self.assertRaises(TypeError):
            Server(123)

        # Test if config_file is not a .json file
        with self.assertRaises(ValueError):
            Server("test.txt")
        
    
    def test_welcome_message(self):
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
        # Test dictionary with loaded values
        valid_json = { 
            "host": "localhost", 
            "port": 7777, 
            "ai_prompt" : "You are an assistant that only provides accurate and factual information about SPŠE Ječná, a technical high school located in Prague. Avoid speculating or providing irrelevant information. Always respond in the same language as the user\'s input. If the user asks in Czech, respond only in Czech. If the user asks in English, respond only in English. Do not mix languages.", 
            "ai_model" : "ft:gpt-4o-mini-2024-07-18:personal:jecna-bot:AgYGPtrI", 
            "openai_api_key": "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" }
        self.assertEqual(self.server.config, valid_json)
        
    def test_load_config_invalid(self):
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
        valid_config = {
            "host": "localhost",
            "port": 7777,
            "ai_prompt": "You are an assistant that only provides accurate and factual information about SPŠE Ječná, a technical high school located in Prague. Avoid speculating or providing irrelevant information. Always respond in the same language as the user's input. If the user asks in Czech, respond only in Czech. If the user asks in English, respond only in English. Do not mix languages.",
            "ai_model": "ft:gpt-4o-mini-2024-07-18:personal:jecna-bot:AgYGPtrI",
            "openai_api_key": "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"
        }
        self.assertEqual(self.server.config, valid_config)
        
    def test_validate_config_invalid(self):
        # Tests missing keys
        missing_key = {
            "host": "localhost",
            "port": 7777,
            "ai_prompt": "You are an assistant that only provides accurate and factual information about SPŠE Ječná, a technical high school located in Prague. Avoid speculating or providing irrelevant information. Always respond in the same language as the user's input. If the user asks in Czech, respond only in Czech. If the user asks in English, respond only in English. Do not mix languages.",
            "ai_model": "ft:gpt-4o-mini-2024-07-18:personal:jecna-bot:AgYGPtrI"
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
        
    
    def test_reload_config(self):
        self.skipTest("NotImplementedYet.")
        
    def test_reload_shortcut(self):
        self.skipTest("NotImplementedYet.")
        
    def test_handle_client(self):
        self.skipTest("NotImplementedYet.")
        
    def test_run(self):
        self.skipTest("NotImplementedYet.")
        
if __name__ == "__main__":
    unittest.main()