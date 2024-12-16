import asyncio
import websockets
import json

class Client:
    """
    WebSocket klient pro komunikaci se serverem.
    """
    
    def __init__(self, config_file):
        """
        Inicializace instance Client.
        
        :param config_file (str): Cesta k JSON souboru obsahujícímu konfiguraci.        
        """
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        # Validace portu
        if not isinstance(self.config["port"], int) or not (1 <= self.config["port"] <= 65535):
            raise ValueError("Port v konfiguraci musí být celé číslo v rozsahu 1–65535.")

        self.uri = f"ws://{self.config['host']}:{self.config['port']}"
    
    async def connect(self):
        """
        Navázání spojení se serverem a výměna zpráv.
        """
        try:
            async with websockets.connect(self.uri, open_timeout=10) as websocket:
                print(await websocket.recv())  
                
                while True:
                    try:
                        user_input = input(" > Vy: ")
                        await websocket.send(user_input)

                        if user_input.lower() == "exit":
                            print("\n -> Odpojil jste se použitím příkazu.")
                            break

                        response = await websocket.recv()
                        print(f" └ Bot: {response}\n")
                        
                    except asyncio.TimeoutError:
                        print(" -> Spojení se serverem vypršelo.")
                    except websockets.ConnectionClosed:
                        print(" -> Spojení bylo uzavřeno serverem.")
                        
        except Exception as e:
            print(f"Chyba: {e}")

if __name__ == "__main__":
    """
    Spuštění klienta.
    """
    client = Client(config_file="../config.json")
    
    try:
        asyncio.run(client.connect())
    except KeyboardInterrupt:
        print("\n -> Odpojil jste se ručně!")
