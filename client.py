import asyncio
import atexit
import json
import logging
import threading
from pprint import pformat
import time

import socketio
from aiohttp import web


class SocketClient:
    sio = socketio.AsyncClient()

    async def add(self):
        await self.sio.emit('add', {'response': "add camera to server"})

    async def edit(self):
        await self.sio.emit('edit', {'response': "edit camera from server"})

    async def remove(self):
        await self.sio.emit('remove', {'response': "remove camera from server"})

    # @sio.event
    # async def connect(self):
    #     logging.info("socket connected")

    def call_backs(self):
        @self.sio.event
        async def connect():
            logging.info(f"Socket connected")

        @self.sio.event
        async def my_message(data):
            print('message received with ', data)
            await self.sio.emit('my response', {'response': 'my response'})

        @self.sio.event
        async def disconnect():
            logging.info(f"Socket disconnected")

    async def run(self):
        # self.call_backs()
        await self.sio.connect("http://localhost:8001")
        await self.sio.wait()

# import asyncio
# import socketio
#
# sio = socketio.AsyncClient()
#
# @sio.event
# async def connect():
#     print('connection established')
#     await sio.emit('connect')
#
# @sio.event
# async def my_message(data):
#     print('message received with ', data)
#     await sio.emit('my response', {'response': 'my response'})
#
# @sio.event
# async def disconnect():
#     print('disconnected from server')
#
# async def main():
#     await sio.connect('http://localhost:8001')
#     await sio.wait()

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s - %(filename)s|%(funcName)s - %(levelname)s - %(message)s",
                        level=logging.DEBUG)
    client = SocketClient()
    client.call_backs()
    asyncio.run(client.run())
    # asyncio.run(main())

