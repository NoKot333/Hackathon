import asyncio
import websockets

class ChatServer:
    def __init__(self):
        self.chat_history = []
        self.websocket_clients = set()

    async def handle_client(self, websocket, path):
        await self.send_chat_history(websocket)
        async for message in websocket:
            self.chat_history.append(message)
            await self.broadcast_message(message)

    async def send_chat_history(self, websocket):
        if self.chat_history:
            history_message = "CHAT_HISTORY:" + ";".join(self.chat_history)
            await websocket.send(history_message)

    async def broadcast_message(self, message):
        for ws in self.websocket_clients:
            await ws.send(message)

    async def server(self, websocket, path):
        await self.handle_client(websocket, path)

if __name__ == "__main__":
    chat_server = ChatServer()
    start_server = websockets.serve(chat_server.server, "localhost", 5003)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()