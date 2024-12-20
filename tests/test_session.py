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

        self.mock_logic = ResponseLogic({"openai_api_key": "test_key", "ai_model": "test_model", "ai_prompt": "test_prompt"})

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


    async def test_welcome_message(self):
        """
        Tests the `_welcome_message` method to ensure the correct welcome message is sent.
        """
        mock_websocket = AsyncMock()
        mock_logger = MagicMock()
        mock_logger.get_questions.return_value = [
            "Kdy se otevírá škola?",
            "Jaká je dostupnost MHD?",
            "Kde se dá koupit jídlo?"
        ]

        session = Session(websocket=mock_websocket, logic=MagicMock())
        session.logger = mock_logger  

        expected_formatted_questions = (
            " └ 1. Kdy se otevírá škola?\n"
            " └ 2. Jaká je dostupnost MHD?\n"
            " └ 3. Kde se dá koupit jídlo?"
        )
        expected_welcome_message = (
            "\nVítejte, Ječnábot! \n\n"
            " * Dokumentace:  /README.md (https://github.com/CheackCZ/JecnaBot)\n"
            " * Podpora:      ondra.faltin@gmail.com (ondrejfaltin.cz)\n"
            "Kontaktuje podporu nebo se podívejte dokumentace pro více informací!\n"
            "\n      _       _ _          __ ____        _   "
            "\n     | |      \\_/         /_/|  _ \\      | |  "
            "\n     | | ___  ___ _ __   __ _| |_) | ___ | |_ "
            "\n _   | |/ _ \\/ __| '_ \\ / _` |  _ < / _ \\| __|"
            "\n| |__| |  __/ (__| | | | (_| | |_) | (_) | |_ "
            "\n \\____/ \\___|\\___|_| |_|\\__,_|____/ \\___/ \\__|"
            "\n\n Vítejte!\n"
            "\n >> Nejčastější otázky:\n"
            f"{expected_formatted_questions}\n"
            "\n >> Co pro Vás mohu udělat? \n"
            " └─ Napište otázku, 'exit' pro ukončení, nebo vyberte otázku pomocí čísla :)\n"
        )

        await session._welcome_message()
        mock_websocket.send.assert_awaited_once_with(expected_welcome_message)

    async def test_welcome_message_invalid(self):
        """
        Tests the `_welcome_message` method with an invalid logger configuration.
        """
        mock_websocket = AsyncMock()
        mock_logger = MagicMock()
        mock_logger.get_questions.side_effect = Exception("Logger error")

        session = Session(websocket=mock_websocket, logic=MagicMock())
        session.logger = mock_logger

        with self.assertRaises(Exception) as context:
            await session._welcome_message()
        self.assertEqual(str(context.exception), "Logger error")
        
        
    @unittest.skip("test_process_message is not implemented.")
    async def test_process_message(self):
        self.skipTest("NotImplemented - Couldn't make it work.")
        
    @unittest.skip("test_process_message_invalid is not implemented.")
    async def test_process_message_invalid(self):
        self.skipTest("NotImplemented - Couldn't make it work.")
        

if __name__ == "__main__":
    unittest.main()