from websocket_server import WebsocketServer


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all(b'70')


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
# def message_received(client, server, message):
# 	if len(message) > 200:
# 		message = message[:200]+'..'
# 	print("Client(%d) said: %s" % (client['id'], message))

i = 0

PORT = 7777
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)


server.run_forever()
