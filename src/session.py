import websockets
import asyncio
import json

from log_manager import LogManager
from response_logic import ResponseLogic

class Session:
    """
    Handles a single WebSocket session with a client.
    """

    def __init__(self, websocket, logic):
        """
        Initializes new Session instance.

        :param websocket (websockets.WebSocketServerProtocol): WebSocket connection with the client.
        :param logic (ResponseLogic): An instance of ResponseLogic to generate answers for user input.
        """
        if type(logic) != ResponseLogic:
            raise TypeError("Parametr logic musí být instancí třídy ResponseLogic.")
        
        self.websocket = websocket
        self.client_id = id(websocket)
        self.logic = logic
        self.logger = LogManager()


    async def handle_session(self):
        """
        Manages a WebSocket session with the client.
        """
        print(f"\n > Uživatel ({self.client_id}) se připojil.")
        
        await self._welcome_message()
        
        while True:
            try:
                client_message = await self.websocket.recv()
                await self._process_message(client_message)

            except websockets.ConnectionClosed:
                print(f"\n > Uživatel ({self.client_id}) se odpojil.")
                break
            
            except Exception as e:
                print(f"Chyba: {e}")
                break


    async def _welcome_message(self):
        """
        Sends a welcome message and frequently asked questions separately.
        """
        common_questions = self.logger.get_questions()
        formatted_questions = [{"id": i + 1, "text": q} for i, q in enumerate(common_questions)]

        welcome_message = {
            "type": "welcome",
            "message": "Ahoj, Co pro Vás mohu udělat?",
            "questions": formatted_questions
        }

        print("Sending welcome message:", json.dumps(welcome_message))  # Debug
        await self.websocket.send(json.dumps(welcome_message))
        
        
    async def _process_message(self, client_message):
        """
        Processes the client's message and responds accordingly.
        """
        common_questions = self.logger.get_questions()

        if client_message.isdigit() and 1 <= int(client_message) <= len(common_questions):
            client_message = common_questions[int(client_message) - 1]

        print(f"\n    - Uživatel ({self.client_id}): {client_message}")

        if client_message.lower() == "exit":
            response_message = {
                "type": "info",
                "message": " -> Odpojuji se. Nashledanou!"
            }
            await self.websocket.send(json.dumps(response_message))
            print(f"\n > Uživatel ({self.client_id}) se odpojil.")
            return

        if client_message.lower() == "reload" and self.server:
            response_message = {
                "type": "info",
                "message": " -> Konfigurace byla úspěšně aktualizována."
            }
            await self.websocket.send(json.dumps(response_message))
            return

        # Process the answer
        answer = self.logic.get_answer(client_message)
        response_message = {
            "type": "response",
            "message": answer
        }

        await self.websocket.send(json.dumps(response_message))

        self.logger.log_record(question=client_message, answer=answer)
        asyncio.create_task(self.logger.analyze_logs_async())

        print(f"    └ Odpověď bota uživateli ({self.client_id}): {answer}")