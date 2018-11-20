import asyncio
import websockets
@asyncio.coroutine
def senddata(websocket, path):
     g = "50"
     yield from websocket.send(g)

start_server = websockets.serve(senddata, 'localhost', 7777)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()