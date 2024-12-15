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
        self.uri = f"ws://{self.config['host']}:{self.config['port']}"

    async def connect(self):
        """
        Navázání spojení se serverem a výměna zpráv.
        """
        try:
            async with websockets.connect(self.uri) as websocket:
                print(await websocket.recv())  
                
                while True:
                    try:
                        user_input = input(" > Vy: ")
                        await websocket.send(user_input)

                        if user_input.lower() == "exit":
                            print("\n -> Odpojil jste se.")
                            break

                        response = await websocket.recv()
                        print(f" └ Bot: {response}\n")
                        
                    except websockets.ConnectionClosed:
                        print(" -> Byl jste odhlášen.")
                        break
                        
        except Exception as e:
            print(f"Chyba: {e}")

if __name__ == "__main__":
    """
    Spuštění klienta.
    """
    client = Client(config_file="config.json")
    
    try:
        asyncio.run(client.connect())
    except KeyboardInterrupt:
        print("\n -> Odpojil jste se ručně!")
