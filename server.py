import logging

import socketio

logging.basicConfig(format="%(levelname)s - %(asctime)s :: %(message)s", level=logging.INFO)
sio = socketio.AsyncServer(async_mode='asgi', logger=True)
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    logging.info("Connected to client")


@sio.event
async def disconnect(sid):
    logging.info("Disconnected From Client")


@sio.event
async def message(sid, data):
    logging.info("Received data from client: {}".format(data))
