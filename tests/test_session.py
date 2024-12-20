import sys
import os

import unittest
from unittest.mock import AsyncMock, MagicMock

# Add the 'src' directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from session import Session
from response_logic import ResponseLogic

class TestSession(unittest.TestCase):
    """
    Unit test class for testing the `Session` class methods.	
    """
    
    def setUp(self):
        """
        Sets up the test environment by creating mock WebSocket and logic objects and initializing a `Session` instance.
        """
        self.mock_websocket = AsyncMock()

        self.mock_logic = ResponseLogic({"openai_api_key": "test_key", "ai_model": "test_model", "ai_prompt": "test_prompt", "openai_api_key" : "key"})

        self.session = Session(websocket=self.mock_websocket, logic=self.mock_logic)


    def test_init(self):
        """
        Verifies correct initialization of the `Session` class with valid parameters.
        """
        self.assertEqual(self.session.websocket, self.mock_websocket)
        self.assertEqual(self.session.logic, self.mock_logic)
        self.assertIsInstance(self.session.client_id, int)

    def test_init_invalid(self):
        """
        Ensures exceptions are raised when the `Session` class is initialized with invalid logic.
        """
        with self.assertRaises(TypeError):
            Session(websocket=self.mock_websocket, logic=123) 

    @unittest.skip("test_handle_session is not implemented.")
    async def test_handle_session(self):
        self.skipTest("NotImplemented - Couldn't make it work.")
        
    @unittest.skip("test_handle_session_invalid is not implemented.")
    async def test_handle_session_invalid(self):
        self.skipTest("NotImplemented - Couldn't make it work.")


    @unittest.skip("test_welcome_message is not implemented.")
    async def test_welcome_message(self):
        self.skipTest("NotImplemented - Couldn't make it work.")
        
    @unittest.skip("test_welcome_message_invalid is not implemented.")
    async def test_welcome_message_invalid(self):
        self.skipTest("NotImplemented - Couldn't make it work.")
        
        
    @unittest.skip("test_process_message is not implemented.")
    async def test_process_message(self):
        self.skipTest("NotImplemented - Couldn't make it work.")
        
    @unittest.skip("test_process_message_invalid is not implemented.")
    async def test_process_message_invalid(self):
        self.skipTest("NotImplemented - Couldn't make it work.")
        

if __name__ == "__main__":
    unittest.main()