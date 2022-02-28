import threading
import json
import inspect

import websockets
import asyncio

clients = set()

class WS:

    global clients

    def __init__(self):
        self.server = None
        self.server_stop = None
        self.server_thread = None
    
    async def handler(self,websocket):
        try:
            clients.add(websocket)
        finally:
            clients.remove(websocket)

    async def ws_server(self, host, port):
        loop = asyncio.get_running_loop()
        self.server_stop = loop.create_future()
        
        async with websockets.serve(self.handler, host, port):
            result = await self.server_stop
            print(result)
            print('finiiiiiish')
        

    def run_server(self, host, port):
        asyncio.run(self.ws_server(host,port))

    def start_server(self, host, port):
        if self.server:
            return False
            
        self.server_thread = threading.Thread(target=self.run_server, args=(host,port))
        self.server_thread.setDaemon(True)
        self.server_thread.start()
            
    def stop_server(self):
        
        # if not self.server:
        #     return False

        # shutdown server
        if self.server_stop:
            self.server_stop.set_result(True)

        self.server = None
        self.wserver_thread = None

        # clear clients
        # clients.clear()
        
        return True
    
    def broadcast(self, message):
        if not self.server:
            return

        for client in clients:
            client.send(message)
