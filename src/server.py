import asyncio
import websockets
import json

from session import Session
from utils.response_logic import Response_Logic

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
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

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
        
        async with websockets.serve(self.handle_client, self.config["host"], self.config["port"]):
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
        print("\n -> Server byl ručně zastaven!")