import asyncio
import websockets
import json


class Client:
    """
    WebSocket client for communication with the server.
    """
    
    def __init__(self, config_file):
        """
        Initializes the Client instance.

        :param config_file (str): Path to the JSON configuration file containing server settings.
        """
        if type(config_file) != str:
            raise TypeError("Konfigurační soubor musí být poskytnut jako string!")

        if not config_file.endswith(".json"):
            raise ValueError("Konfigurační soubor musí mít příponu .json!")

        self.config = self.load_config(config_file)
        self.uri = f"ws://{self.config['host']}:{self.config['port']}"


    def load_config(self, config_file):
        """
        Loads the configuration from a JSON file.

        :param config_file (str): Path to the JSON configuration file.
        :return (dict): The loaded configuration.
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Konfigurační soubor '{config_file}' nebyl nalezen.")
        except json.JSONDecodeError:
            raise ValueError(f"Konfigurační soubor '{config_file}' není validní JSON.")


    async def connect(self):
        """
        Establishes a connection with the server and manages the message exchange.
        """
        print(" -> Připojuji se k serveru...")

        try:
            async with websockets.connect(self.uri, open_timeout=10) as websocket:
                print(await websocket.recv()) 
                
                while True:
                    user_input = input(" > Vy: ").strip()

                    if not user_input:
                        print(" -> Zadejte platnou zprávu.")
                        continue

                    await websocket.send(user_input)

                    if user_input.lower() == "exit":
                        print("\n -> Odpojil jste se použitím příkazu.")
                        break

                    response = await websocket.recv()
                    print(f" └ Bot: {response}\n")

        except websockets.ConnectionClosedError:
            print(" -> Spojení bylo uzavřeno serverem.")
        except asyncio.TimeoutError:
            print(" -> Spojení se serverem vypršelo.")
        except Exception as e:
            print(f" -> Chyba: {e}")


if __name__ == "__main__":
    client = Client(config_file="../config.json")
    
    try:
        asyncio.run(client.connect())
    except KeyboardInterrupt:
        print("\n -> Odpojil jste se ručně!")
    except Exception as e:
        print(f" -> Program skončil chybou: {e}")
