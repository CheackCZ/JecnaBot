import websockets
import asyncio

from log_manager import Log_Manager
from response_logic import Response_Logic

class Session:
    """
    Handles a single WebSocket session with a client.
    """

    def __init__(self, websocket, logic):
        """
        Initializes new Session instance.

        :param websocket (websockets.WebSocketServerProtocol): WebSocket connection with the client.
        :param logic (Response_Logic): An instance of Response_Logic to generate answers for user input.
        """
        self.websocket = websocket
        self.client_id = id(websocket)
        self.logic = logic
        self.logger = Log_Manager()

    async def handle_session(self):
        """
        Manages a WebSocket session with the client.
        """
        print(f"\n > Uživatel ({self.client_id}) se připojil.")

        common_questions = self.logger.get_questions()
        formatted_questions = "\n".join([f" └ {i+1}. {q}" for i, q in enumerate(common_questions)])

        welcome_message = (
            "\n**********************************\n"
            "*       Vítejte, JečnáBot!       *\n"
            "**********************************\n\n"
            " >> Nejčastější otázky:\n"
            f"{formatted_questions}\n"
            "\n >> Co pro Vás mohu udělat? \n"
            " └─ Napište číslo otázky, 'exit' pro ukončení, nebo svou otázku :)\n"
        )
        await self.websocket.send(welcome_message)

        while True:
            try:
                client_message = await self.websocket.recv()
                if client_message.isdigit() and 1 <= int(client_message) <= len(common_questions):
                    client_message = common_questions[int(client_message) - 1]

                print(f"\n    - Uživatel ({self.client_id}): {client_message}")

                if client_message.lower() == "exit":
                    await self.websocket.send(" -> Odpojuji se. Nashledanou!")
                    print(f"\n > Uživatel ({self.client_id}) se odpojil.")
                    break

                answer = self.logic.get_answer(client_message)
                await self.websocket.send(f"{answer}")

                self.logger.log_record(question=client_message, answer=answer)

                asyncio.create_task(self.logger.analyze_logs_async())

                print(f"    └ Odpověď bota uživateli ({self.client_id}): {answer}")

                common_questions = self.logger.get_questions()

            except websockets.ConnectionClosed:
                print(f"\n > Uživatel ({self.client_id}) se odpojil.")
                break