
import socketio

sio = socketio.AsyncServer()


sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

sio.on('chat message', namespace='/chat')
async def message(sid, data):
    print("message ", data)
    await sio.emit('reply', room=sid)

sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

