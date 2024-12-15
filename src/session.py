import websockets

from utils.response_logic import Response_Logic

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
        
        await self.websocket.send(f"""\n**********************************\n*       Vítejte, JečnáBot!       *\n**********************************\n\n >> Co pro Vás mohu udělat? \n └─ Napiště 'help' pro seznam témat, 'exit' pro ukončení nebo otázku na kterou chcete odpovědět :)\n""")

        while True:
            try:
                client_message = await self.websocket.recv()
                print(f"    - Uživatel ({self.client_id}): {client_message}")

                if client_message.lower() == 'help':
                    topics = self.logic.get_topics()
                    help_message = "Témata, která mohu pomoci zodpovědět:\n"
                    
                    for topic in topics.items():
                        help_message += f"   - {topic.capitalize()},\n"
                    
                    await self.websocket.send(help_message)

                else:
                    keywords = client_message.split()
                    questions = self.logic.get_questions(keywords)
                                      
                    if questions and questions[0] != "O této oblasti nemám dostatek informací.":
                        await self.websocket.send(f"Mohu odpovědět na:\n   - " + "\n   - ".join(questions))
                    else:
                        answer = self.logic.get_answer(client_message)
                        await self.websocket.send(answer)

            except websockets.ConnectionClosed:
                print(f" > Uživatel ({self.client_id}) se odpojil.")
                break