import websockets
import asyncio

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
        Sends a welcome message.
        """
        common_questions = self.logger.get_questions()
        formatted_questions = "\n".join([f" └ {i+1}. {q}" for i, q in enumerate(common_questions)])

        welcome_message = ( 
            "\nVítejte, Ječnábot! \n\n" +
            " * Dokumentace:  /README.md (https://github.com/CheackCZ/JecnaBot)\n" +
            " * Podpora:      ondra.faltin@gmail.com (ondrejfaltin.cz)\n" +
            "Kontaktuje podporu nebo se podívejte dokumentace pro více informací!\n" + 
                  
            "\n      _       _ _          __ ____        _   " +
            "\n     | |      \_/         /_/|  _ \      | |  " +
            "\n     | | ___  ___ _ __   __ _| |_) | ___ | |_ " +
            "\n _   | |/ _ \/ __| '_ \ / _` |  _ < / _ \| __|" +
            "\n| |__| |  __/ (__| | | | (_| | |_) | (_) | |_ " +
            "\n \____/ \___|\___|_| |_|\__,_|____/ \___/ \__|" +
          
            "\n\n Vítejte!\n" +
          
            "\n >> Nejčastější otázky:\n"
            f"{formatted_questions}\n"
          
            "\n >> Co pro Vás mohu udělat? \n"
            " └─ Napište otázku, 'exit' pro ukončení, nebo vyberte otázku pomocí čísla :)\n"
        )
        await self.websocket.send(welcome_message)
        
        
    async def _process_message(self, client_message):
        """
        Processes the client's message and responds accordingly.
        """
        common_questions = self.logger.get_questions()

        if client_message.isdigit() and 1 <= int(client_message) <= len(common_questions):
            client_message = common_questions[int(client_message) - 1]

        print(f"\n    - Uživatel ({self.client_id}): {client_message}")

        if client_message.lower() == "exit":
            await self.websocket.send(" -> Odpojuji se. Nashledanou!")
            print(f"\n > Uživatel ({self.client_id}) se odpojil.")
            return

        if client_message.lower() == "reload" and self.server:
            await self.server.reload_config()
            await self.websocket.send(" -> Konfigurace byla úspěšně aktualizována.")
            return

        answer = self.logic.get_answer(client_message)
        await self.websocket.send(f"{answer}")

        self.logger.log_record(question=client_message, answer=answer)
        asyncio.create_task(self.logger.analyze_logs_async())

        print(f"    └ Odpověď bota uživateli ({self.client_id}): {answer}")