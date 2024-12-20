import sys
import os
import openai

from unittest.mock import patch, MagicMock

# Add the 'src' directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from response_logic import ResponseLogic

import unittest

class TestOfResponseLogic(unittest.TestCase):
    
    def setUp(self):
        self.response_logic = ResponseLogic(config_file="config.json")
        self.invalid_config_file = "invalid.config.example.json"

    def test_init(self):
        self.assertEqual(openai.api_key, self.response_logic.config["openai_api_key"])


    def test_get_answer(self):
        self.skipTest("NotImplemented.")

    def test_get_answer_invalid(self):
        self.skipTest("NotImplemented.")

if __name__ == "__main__":
    unittest.main()