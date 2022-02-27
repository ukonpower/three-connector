import threading

from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket as _WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication

sockets = []

class WebSocketApp(_WebSocket):
    def opened(self):
        print( 'open' )
        sockets.append(self)
        # send_state([self])
        # sockets.append(self)
        
    def closed(self, code, reason=None):
        print( 'close' )
        sockets.remove(self)
        
    def received_message(self, message):
        data = json.loads(message.data.decode(message.encoding))
        print( data )
        # message_queue.put(data)


class WS:
    # __sockets = []

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
            
        self.wserver.shutdown()

        for socket in sockets:
            socket.close()
            
        self.wserver = None
        
        return True
