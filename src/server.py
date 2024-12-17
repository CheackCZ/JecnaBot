import asyncio
import websockets
import json

from session import Session
from response_logic import Response_Logic

class Server:
    """
    WebSocket server for communiocation with user.
    """

    def __init__(self, config_file):
        """
        Initializes the Server instance.

        :param config_file (str): Path to the JSON configuration file containing server settings.
        """
        self.config = self._load_config(config_file)
        self.logic = Response_Logic(config_file)
        
    def _load_config(self, config_file):
        """
        Loads and validates the server configuration from a JSON file.
        
        :param config_file (str): Configuration file.
        
        :return (dict): Server configuration. 
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Correct keys in configuration file validation
            required_keys = ["host", "port", "openai_api_key"]
            for key in required_keys:
                if key not in config:
                    raise ValueError(f"Chybí povinný klíč '{key}' v konfiguračním souboru.")
            
            # Port validation
            if not isinstance(config["port"], int) or not (1 <= config["port"] <= 65535):
                raise ValueError("Port v konfiguraci musí být celé číslo v rozsahu 1–65535.")
            
            return config

        except FileNotFoundError:
            raise FileNotFoundError(f"Konfigurační soubor '{config_file}' nebyl nalezen.")
        except json.JSONDecodeError:
            raise ValueError(f"Konfigurační soubor '{config_file}' není validní JSON.")

    async def handle_client(self, websocket):
        """
        Handles a single client connection.
        
        :param websocket (websockets.WebSocketServerProtocol): Websocket of connected user.
        """
        session = Session(websocket, self.logic)
        await session.handle_session()

    async def run(self):
        """
        Starts the WebSocket server and listens for client connections.
        """
        print(" -> Spouštím WebSocket server...")
        
        async with websockets.serve(self.handle_client, self.config["host"], self.config["port"], ping_interval=60, ping_timeout=30):
            print(f" -> Server spuštěn a naslouchá na ws://{self.config['host']}:{self.config['port']}")
            await asyncio.Future()  


if __name__ == "__main__":
    print(f"\n**********************************" +
           "\n*        JečnáBot Server!        *" +
           "\n**********************************\n")
    
    server = Server(config_file="config.json")

    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("\n -> Server byl ukončen uživatelem!")