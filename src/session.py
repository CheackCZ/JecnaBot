import websockets

class Session:
    
    def __init__(self, websocket):
        self.websocket = websocket
        self.client_id = id(websocket)

    async def handle_session(self):
        print(f"\n > Client ({self.client_id}) connected.")
        
        await self.websocket.send(f"""**********************************\n*      Welcome to JečnáBot!      *\n**********************************\n\n >> What can I do for you? Type 'exit' to disconnect.""")

        while True:
            try:
                # Receive a message from the client
                client_message = await self.websocket.recv()
                print(f"    - Client ({self.client_id}): {client_message}")

                if client_message.lower() == "exit":
                    await self.websocket.send("Goodbye! Disconnecting...")
                    print(f" > Client {self.client_id} disconnected.\n")
                    break

                # Respond to the client's message
                response = f"{client_message} -> How else can I help?"
                await self.websocket.send(response)

            except websockets.ConnectionClosed:
                print(f" > Client {self.client_id} connection closed.")
                break