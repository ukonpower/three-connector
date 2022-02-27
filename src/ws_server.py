import threading
import json

from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket as _WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication

sockets = []

class WebSocketApp(_WebSocket):

    global sockets
    
    def opened(self):
        sockets.append(self)
        
    def closed(self, code, reason=None):
        sockets.remove(self)
        
    def received_message(self, message):
        data = json.loads(message.data.decode(message.encoding))

class WS:

    global sockets

    def __init__(self):
        self.wserver = None
    
    def start_server(self, host, port):
        
        if self.wserver:
            return False
        
        self.wserver = make_server(host, port,
            server_class=WSGIServer,
            handler_class=WebSocketWSGIRequestHandler,
            app=WebSocketWSGIApplication(handler_cls=WebSocketApp)
        )
        self.wserver.initialize_websockets_manager()
        
        self.wserver_thread = threading.Thread(target=self.wserver.serve_forever)
        self.wserver_thread.daemon = True
        self.wserver_thread.start()

        return True

    def stop_server(self):
        if not self.wserver:
            return False

        # clear sockets
        for socket in sockets:
            socket.close()
                
        sockets.clear()

        # shutdown server
        self.wserver.shutdown()
        self.wserver_thread.join()
        self.wserver = None
        
        return True
    
    def broadcast(self, message):
        for socket in sockets:
            socket.send(message)

