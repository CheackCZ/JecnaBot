import asyncio
import websockets
import json

from session import Session
from response_logic import Response_Logic

class Server:
    """
    WebSocket server pro komunikaci s uživateli.
    """

    def __init__(self, config_file):
        """
        Inicializace instance Server.

        :param config_file (str): Cesta k souboru obsahující konfiguraci serveru.
        """
        self.config = self._load_config(config_file)
        self.logic = Response_Logic(config_file)

    def _load_config(self, config_file):
        """
        Načtení konfigurace serveru z JSON souboru.
        
        :param config_file (str): Soubor obsahující konfiguraci serveru.
        
        :return (dict): Konfigurace serveru. 
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Ověření povinných klíčů
            required_keys = ["host", "port", "openai_api_key"]
            for key in required_keys:
                if key not in config:
                    raise ValueError(f"Chybí povinný klíč '{key}' v konfiguračním souboru.")
            
            # Ověření portu
            if not isinstance(config["port"], int) or not (1 <= config["port"] <= 65535):
                raise ValueError("Port v konfiguraci musí být celé číslo v rozsahu 1–65535.")
            
            return config

        except FileNotFoundError:
            raise FileNotFoundError(f"Konfigurační soubor '{config_file}' nebyl nalezen.")
        except json.JSONDecodeError:
            raise ValueError(f"Konfigurační soubor '{config_file}' není validní JSON.")

    async def handle_client(self, websocket):
        """
        Zpracování připojení konkrétního uživatele.
        
        :param websocket (websockets.WebSocketServerProtocol): Websocket připojeného uživatele.
        """
        session = Session(websocket, self.logic)
        await session.handle_session()

    async def run(self):
        """
        Spuštění WebSocket serveru a čekání na připojení uživatelů.
        """
        print(" -> Spouštím WebSocket server...")
        
        async with websockets.serve(self.handle_client, self.config["host"], self.config["port"], ping_interval=60, ping_timeout=30):
            print(f" -> Server spuštěn a naslouchá na ws://{self.config['host']}:{self.config['port']}")
            await asyncio.Future()  


if __name__ == "__main__":
    """
    Spuštění serveru 'JečnáBot'.
    """
    print(f"\n**********************************" +
           "\n*        JečnáBot Server!        *" +
           "\n**********************************\n")
    
    server = Server(config_file="config.json")
    
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("\n -> Server byl ukončen uživatelem!")