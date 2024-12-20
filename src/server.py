import asyncio
import websockets
import json
import keyboard

from session import Session
from response_logic import ResponseLogic

class Server:
    """
    WebSocket server for communication with users.
    """

    def __init__(self, config_file):
        """
        Initializes the Server instance.

        :param config_file (str): Path to the JSON configuration file containing server settings.
        """
        if type(config_file) !=  str:
            raise TypeError("Konfigurační soubor musí být dosazen a vložen jako String!")

        if not config_file.endswith(".json"):
            raise ValueError("Konfigurační soubor musí mít příponu .json!")

        self.config_file = config_file
        self.config = self._load_config(config_file)
        
        self.config_lock = asyncio.Lock()
        
        self.logic = ResponseLogic(self.config)
        
        
    def _welcome_message(self):
        """
        Returns the welcome message.
        """
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
        return welcome_message


    def _load_config(self, config_file):
        """
        Loads and validates the server configuration from a JSON file.
        
        :param config_file (str): Configuration file.
        :return (dict): Validated server configuration. 
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            self._validate_config(config)
            return config

        except FileNotFoundError:
            raise FileNotFoundError(f"Konfigurační soubor '{config_file}' nebyl nalezen.")
        
        except json.JSONDecodeError:
            raise ValueError(f"Konfigurační soubor '{config_file}' není validní JSON.")
        
    def _validate_config(self, config):
        """
        Validates the configuration.

        :param config (dict): Configuration dictionary.
        :raises ValueError: If any validation fails.
        """
        # Define validation rules
        rules = {
            "host":             lambda h: type(h) == str,
            "port":             lambda p: type(p) == int and 1 <= p <= 65535,
            "ai_prompt":        lambda a: type(a) == str,
            "ai_model":         lambda a: type(a) == str,
            "openai_api_key":   lambda o: type(o) == str
        }

        # Check for missing keys
        missing_keys = [] 
        for key in rules: 
            if key not in config:
                missing_keys.append(key)
        
        if missing_keys:
            raise ValueError(f"Chybí povinné klíče: {', '.join(missing_keys)}.")

        # Validates each key
        for key, rule in rules.items():
            if not rule(config[key]):
                raise ValueError(f"Hodnota pro '{key}' není validní.")
    
    async def reload_config(self):
        """
        Reloads the server configuration asynchronously.
        """ 
        async with self.config_lock:
            try:
                self.config = self._load_config(config_file=self.config_file)
                self.logic = ResponseLogic(self.config)
                
                print(" -> Konfigurace správně načtena!")
            except Exception as e:
                print(f" -> Error při načítání konfigurace: {e}")


    async def reload_shortcut(self):
        """
        Listens for keyboard shortcuts for admin commands.
        """
        while True:
            if keyboard.is_pressed("ctrl+r"):
                print("\n -> Znovu načítám konfiguraci ...")
                await self.reload_config()
                
            await asyncio.sleep(0.1)


    async def handle_client(self, websocket):
        """
        Handles a single client connection.
        
        :param websocket (websockets.WebSocketServerProtocol): Websocket of connected user.
        """
        async with self.config_lock:
            session = Session(websocket, self.logic)
        await session.handle_session()


    async def run(self):
        """
        Starts the WebSocket server and listens for client connections.
        """
        print(self._welcome_message())
        
        print(" -> Spouštím WebSocket server...")

        server_task = websockets.serve(self.handle_client, self.config["host"], self.config["port"], ping_interval=60, ping_timeout=30)
        print(f" -> Server spuštěn a naslouchá na ws://{self.config['host']}:{self.config['port']}")

        shortcut_task = self.reload_shortcut()

        await asyncio.gather(server_task, shortcut_task)


if __name__ == "__main__":
    server = Server(config_file="../config.json")

    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("\n -> Server byl ukončen uživatelem!")
