import asyncio
import atexit
import json
import logging
import threading
from pprint import pformat
import time

import socketio
from aiohttp import web


class SocketServer:
    sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")

    def aiohttp_server(self):
        app = web.Application()
        self.sio.attach(app)
        runner = web.AppRunner(app)
        return runner

    def run(self, runner):
        self.call_backs()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, "0.0.0.0", 8001)
        loop.run_until_complete(site.start())
        loop.run_forever()

    def call_backs(self):
        @self.sio.event
        async def connect(sid, environ):
            logging.info(f"Socket from {str(sid)} is connected.")

        @self.sio.event
        async def disconnect(sid):
            logging.info(f"Socket from {str(sid)} is disconnected")

        @self.sio.on("add")
        async def add(sid, data):
            if data:
                logging.info(f'Received data: {pformat(data, indent=4)} from client.')

        @self.sio.on("edit")
        async def edit(sid, data):
            if data:
                logging.info(f'Edited data: {pformat(data, indent=4)}')

        @self.sio.on('remove')
        async def remove(sid, data):
            if data:
                logging.info(f"Removed data: {pformat(data, indent=4)}")


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s - %(filename)s|%(funcName)s - %(levelname)s - %(message)s",
                        level=logging.DEBUG)
    server = SocketServer()
    server.run(server.aiohttp_server())
