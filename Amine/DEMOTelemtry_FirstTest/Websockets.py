from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import random
class SimpleEcho(WebSocket):
    b = [b'60', b'30', b'60', b'30', b'60', b'30', b'60']
    def handleMessage(self):
        # echo message back to client

        self.sendMessage('50')

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


while True:
    server = SimpleWebSocketServer('', 7777, SimpleEcho)
    server.serveforever()
    server.close()

print('hi')