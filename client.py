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

    async def add_camera(self, cam: dict):
        await self.sio.emit('add_camera', cam)

    async def edit_camera(self, cam: dict):
        await self.sio.emit('edit_camera', cam)

    async def remove_camera(self, cam: dict):
        await self.sio.emit('remove_camera', cam)

    # @sio.event
    # async def connect(self):
    #     logging.info("socket connected")

    def call_backs(self):
        @self.sio.event
        async def connect():
            logging.info(f"Socket connected")

        @self.sio.event
        async def response(data):
            print('message received with ', data)

        @self.sio.event
        async def disconnect():
            logging.info(f"Socket disconnected")

        @self.sio.on('execute')
        async def execute():
            logging.info("Executing the process . . .")
            await self.execute()

        @self.sio.on('show_logs')
        async def show_logs(logs):
            logging.info(pformat(logs))

    async def execute(self):
        await self.sio.emit('execute')

    async def terminate(self):
        await self.sio.emit('terminate')

    async def run(self):
        # self.call_backs()
        await self.sio.connect("http://localhost:8000")
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
    with open('cameras.json', 'r') as f:
        cam_samples = json.load(f)

    import threading
    client = SocketClient()
    client.call_backs()
    threading.Thread(target=asyncio.run, args=[(client.run())]).start()
    # asyncio.run(main())

