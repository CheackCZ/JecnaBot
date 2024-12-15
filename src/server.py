import asyncio
import websockets

from session import Session

class Server:
    
    async def handle_client(self, websocket):
        session = Session(websocket)
        await session.handle_session()

    async def run(self):
        print(" -> Starting WebSocket server...")
        async with websockets.serve(self.handle_client, "localhost", 7777):
            print(" -> Server started and listening on ws://localhost:7777")
            await asyncio.Future()  
            
if __name__ == "__main__":
    print(f"""\n**********************************\n*        JečnáBot Server!        *\n**********************************\n""")
    
    server = Server()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("\n -> Server stopped manually!")