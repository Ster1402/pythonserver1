import json

# # create a Socket.IO server
# sio = socketio.Server()

# print(dir(socketio.Server))

data =  {
    "name": "Server",
    "salle": "15BS1",
    "liste_presence": [
      {"name":"Overlord","niveau":3,"axe":"GLO",},
      {"name":"SterDevs","niveau":3,"axe":"GLO",},
    ]
}

# @sio.event
# def connect(sid, environ, auth):
#     print('connect ', sid)
from aiohttp import web
import socketio

## creates a new Async Socket IO Server
sio = socketio.AsyncServer()
## Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
## instance
sio.attach(app)

## we can define aiohttp endpoints just as we normally
## would with no change
async def index(request):
    with open('data.json') as f:
        return web.Response(text=f.read(), content_type='text/json')

## If we wanted to create a new websocket endpoint,
## use this decorator, passing in the name of the
## event we wish to listen out for
@sio.on('message')
async def print_message(sid, message):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print(message)

    await sio.emit("message", json.dumps(data))

    
## We bind our aiohttp endpoint to our app
## router
app.router.add_get('/', index)

## We kick off our server
if __name__ == '__main__':
    web.run_app(app)