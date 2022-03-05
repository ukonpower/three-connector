import threading
import json
import inspect
import asyncio

import websockets

class WS:


    def __init__(self):
        self.server = None
        self.server_stop = None
        self.server_thread = None
        self.sockets = set()
        self.on_connect = None
    
    async def clientEvents(self, websocket ):
        async for message in websocket:
            print( message )
    
    async def handler(self,websocket):
        self.sockets.add(websocket)

        if self.on_connect:
            await self.on_connect(websocket)
        
        try:
            await self.clientEvents(websocket)
        finally:
            self.sockets.remove(websocket)

    async def ws_server(self, host, port):

        self.serverLoop = asyncio.get_running_loop()
        self.serverStop = self.serverLoop.create_future()

        async with websockets.serve(self.handler, host, port) as server :
            self.server = server
            await self.serverStop
        

    def run_server(self, host, port):
        asyncio.run(self.ws_server(host,port))

    def start_server(self, host, port):
        if self.server:
            return False
            
        self.server_thread = threading.Thread(target=self.run_server, args=(host,port))
        self.server_thread.setDaemon(True)
        self.server_thread.start()
            
    def stop_server(self):
        
        if not self.server:
            return False

        # shutdown server
        if self.serverLoop and self.serverStop:
            self.serverLoop.call_soon_threadsafe(self.serverStop.set_result, 1)

        self.server = None
        self.wserver_thread = None
        self.serverLoop = None
        self.server_stop = None

        return True
    
    async def send(self, websocket, type, data):
        if( not self.server ):
            return

        messageStr = json.dumps({
            "type": type,
            "data": data
        })

        await websocket.send(messageStr)

    
    def broadcast(self, type, data):
        if not self.server:
            return

        messageStr = json.dumps({
            "type": type,
            "data": data
        })

        websockets.broadcast(self.sockets, messageStr)
