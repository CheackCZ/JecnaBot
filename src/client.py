import asyncio
import websockets

class Client:
    def __init__(self, uri="ws://localhost:7777"):
        self.uri = uri

    async def connect(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                await self.handle_chat(websocket)
        except Exception as e:
            print(f"Error: {e}")

    async def handle_chat(self, websocket):
        # Receive and display the welcome message from the server
        welcome_message = await websocket.recv()
        print(f"\n{welcome_message}")

        while True:
            # Ask the client to input a message or exit
            user_input = input(" > You: ")

            # Send the user's message to the server
            await websocket.send(user_input)

            # Exit the loop if the user types 'exit'
            if user_input.lower() == "exit":
                print("\n -> You have disconnected.")
                break

            # Receive and display the server's response
            server_response = await websocket.recv()
            print(f" └─ Bot: {server_response}\n")

if __name__ == "__main__":
    client = Client()
    
    try:
        asyncio.run(client.connect())
    except KeyboardInterrupt:
        print("\n -> You have disconnected manually!")