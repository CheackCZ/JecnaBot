import websockets

from response_logic import Response_Logic

class Session:
    """
    Správa chatu s jedním uživatelem.
    """
    
    def __init__(self, websocket, logic):
        """
        Inicializace instance Session.
        
        :param websocket (websockets.WebSocketServerProtocol): WebSocket pro spojení s uživatelem.
        :param logic (Response_Logic): Instance logiky s odpověďmi.
        """
        self.websocket = websocket
        self.client_id = id(websocket)
        self.logic = logic

    async def handle_session(self):
        """
        Správa chatu mezi uživatelem a serverem.
        """
        print(f"\n > Uživatel ({self.client_id}) se připojil.")
        
        await self.websocket.send(f"""\n**********************************\n*       Vítejte, JečnáBot!       *\n**********************************\n\n >> Co pro Vás mohu udělat? \n └─ Napiště 'exit' pro ukončení, nebo se zeptejte na otázku, kterou chcete zodpovědět :)\n""")

        while True:
            try:
                client_message = await self.websocket.recv()
                print(f"\n    - Uživatel ({self.client_id}): {client_message}")

                if client_message.lower() == "exit":
                    await self.websocket.send(" -> Odpojuji se. Nashledanou!")
                    print(f"\n > Uživatel ({self.client_id}) se odpojil.")
                    break

                answer = self.logic.get_answer(client_message)
                await self.websocket.send(f"{answer}\n")

                print(f"    └ Odpověď bota uživateli ({self.client_id}): {answer}")

            except websockets.ConnectionClosed:
                print(f"\n > Uživatel ({self.client_id}) se odpojil.")
                break
